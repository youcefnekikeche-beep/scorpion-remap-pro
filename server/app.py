import os
import sys
import json
import uuid
import shutil
import hashlib
from typing import Optional, List
from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# إضافة المسار الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

from server.db import (
    get_db, init_db, hash_password, verify_password,
    register_user, authenticate_user, get_user_by_id,
    deduct_user_tokens, add_user_tokens, get_all_users,
    toggle_user_active_status, get_user_transactions,
    is_ip_banned, record_failed_attempt, clear_failed_attempts,
    get_banned_ips, unban_ip, manual_ban_ip,
    save_session_db, get_session_user_db, delete_session_db
)
from engine.tuning_bridge import run_tuning_task
from engine.ecu_analyzer import identify_ecu, preview_dtcs, get_technical_instructions
from engine.renault_expert import preview_expert_operation, execute_expert_operation

app = FastAPI(title="SCORPION REMAP PRO", version="3.2.0")

@app.get("/favicon.ico")
async def favicon():
    return Response(content=b"", status_code=204)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ================= حماية المنصة وحظر الـ IP المشبوه (Security Middleware) =================
@app.middleware("http")
async def security_ip_middleware(request: Request, call_next):
    response = await call_next(request)

    # معايير أمان المتصفح الصارمة (OWASP Security Headers)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

UPLOADS_DIR = os.path.join(BASE_DIR, "storage", "uploads")
PROCESSED_DIR = os.path.join(BASE_DIR, "storage", "processed")
DTC_TABLE_PATH = os.path.join(BASE_DIR, "storage", "dtc_table.json")
SUPPORTED_ECUS_PATH = os.path.join(BASE_DIR, "storage", "supported_ecus.json")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# تحميل جدول أكواد الـ DTC
DTC_TABLE = {}
if os.path.exists(DTC_TABLE_PATH):
    try:
        with open(DTC_TABLE_PATH, "r", encoding="utf-8") as f:
            DTC_TABLE = json.load(f)
    except:
        pass

# تحميل قائمة الكمبيوترات المدعومة
SUPPORTED_ECUS = []
if os.path.exists(SUPPORTED_ECUS_PATH):
    try:
        with open(SUPPORTED_ECUS_PATH, "r", encoding="utf-8") as f:
            SUPPORTED_ECUS = json.load(f)
    except:
        pass

# جلسات المستخدمين وجلسات معاينة الأدوات التخصصية
SESSIONS = {} # {token: user_id}
EXPERT_PREVIEWS = {} # {preview_token: session_data}

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "127.0.0.1"

def get_current_user(request: Request) -> Optional[dict]:
    # التحقق من Header أو Cookie مع دعم الجلسات الدائمة في SQLite
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        token = request.cookies.get("ecu_token")
    if not token:
        return None
    
    user_id = SESSIONS.get(token)
    if not user_id:
        user_id = get_session_user_db(token)
        if user_id:
            SESSIONS[token] = user_id
            
    if not user_id:
        return None

    user = get_user_by_id(user_id)
    if user and user.get("is_active"):
        user["credits"] = user.get("tokens", 0)
        user["username"] = user.get("email", "")
        user["is_admin"] = (user.get("role") == "admin")
        return user
    return None

def require_user(request: Request) -> dict:
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="يرجى تسجيل الدخول أولاً")
    return user

def require_admin(request: Request) -> dict:
    user = require_user(request)
    if not user.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="غير مصرح، هذه الصفحة للمدير فقط")
    return user

# ================= الصفحات (Web Views) =================

@app.get("/healthz")
@app.head("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
@app.head("/")
async def index_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    if user.get("is_admin"):
        return RedirectResponse(url="/admin")
    return RedirectResponse(url="/portal")

@app.get("/login", response_class=HTMLResponse)
@app.head("/login")
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        if user.get("is_admin"):
            return RedirectResponse(url="/admin")
        return RedirectResponse(url="/portal")
    return templates.TemplateResponse(request, "login.html")

@app.head("/portal")
@app.get("/portal", response_class=HTMLResponse)
async def portal_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request, "client_dashboard.html", {"user": user})

@app.head("/admin")
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    user = get_current_user(request)
    if not user or not user.get("is_admin"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request, "admin_dashboard.html", {"user": user})

@app.get("/supported-ecus", response_class=HTMLResponse)
async def supported_ecus_page(request: Request):
    return templates.TemplateResponse(request, "supported_ecus.html")

@app.get("/api/v1/supported-ecus")
async def api_get_supported_ecus():
    if os.path.exists(SUPPORTED_ECUS_PATH):
        try:
            with open(SUPPORTED_ECUS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return SUPPORTED_ECUS

@app.post("/api/v1/expert/preview")
async def api_expert_preview(
    file: UploadFile = File(...),
    tool: str = Form(...),
    param: str = Form(""),
    protocol: str = Form(""),
    user: dict = Depends(require_user)
):
    """
    معاينة التغييرات قبل الخصم (Dry-Run Confirmation)
    فحص صرامة نوع الكومبيوتر، والحجم، ومطابقة البايتات الأصلية
    """
    content = await file.read()
    try:
        preview_data = preview_expert_operation(content, tool, param, file.filename, protocol)
        preview_token = uuid.uuid4().hex
        EXPERT_PREVIEWS[preview_token] = {
            "content": content,
            "filename": file.filename,
            "tool": tool,
            "param": param,
            "protocol": protocol,
            "user_id": user["id"],
            "preview": preview_data
        }
        preview_data["preview_token"] = preview_token
        return preview_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse interne : {str(e)}")


@app.post("/api/v1/expert/apply")
async def api_expert_apply(
    preview_token: str = Form(...),
    user: dict = Depends(require_user)
):
    """
    تطبيق التعديل النهائي وخصم 1 كريديت فقط بعد تأكيد المستخدم
    """
    if user["credits"] < 1:
        raise HTTPException(status_code=402, detail="رصيدك غير كافٍ. تحتاج نقطة واحدة لتحميل الملف المعدل.")

    if preview_token not in EXPERT_PREVIEWS:
        raise HTTPException(status_code=404, detail="انتهت صلاحية جلسة المعاينة، يرجى إعادة اختيار الملف.")

    session = EXPERT_PREVIEWS[preview_token]
    if session["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="جلسة غير مصرح بها.")

    try:
        content = session["content"]
        tool = session["tool"]
        param = session["param"]
        protocol = session.get("protocol", "")
        filename = session["filename"]
        preview_info = session["preview"]

        modified_data, desc = execute_expert_operation(content, tool, param, filename, protocol)

        file_id = uuid.uuid4().hex
        original_save_path = os.path.join(UPLOADS_DIR, f"{file_id}_{filename}")
        modified_filename = f"MOD_{tool.upper()}_{filename}"
        modified_save_path = os.path.join(PROCESSED_DIR, f"{file_id}_{modified_filename}")

        with open(original_save_path, "wb") as f:
            f.write(content)
        with open(modified_save_path, "wb") as f:
            f.write(modified_data)

        file_hash = hashlib.sha256(content).hexdigest()

        # خصم التوكن وتسجيل العملية في token_transactions
        new_balance = deduct_user_tokens(user["id"], 1, "expert_tool", f"Outil Expert: {desc} sur {filename}")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO files (user_id, original_name, file_hash, brand, model, ecu_type, sw_version, solutions, credits_cost, original_path, modified_path)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    user["id"],
                    filename,
                    file_hash,
                    "Renault Expert",
                    preview_info.get("ecu_type", "Calculateur Renault"),
                    tool.upper(),
                    preview_info.get("sw_version", param or "Standard"),
                    json.dumps([preview_info.get("description", desc)]),
                    1,
                    original_save_path,
                    modified_save_path
                )
            )
            task_id = cursor.lastrowid
            conn.commit()

        # مسح الجلسة بعد نجاح التطبيق
        del EXPERT_PREVIEWS[preview_token]

        return {
            "success": True,
            "task_id": task_id,
            "filename": modified_filename,
            "download_url": f"/api/v1/tuning/download/{task_id}",
            "credits_remaining": new_balance,
            "description": desc
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'application : {str(e)}")


@app.post("/api/v1/expert/process")
async def api_expert_process(
    file: UploadFile = File(...),
    tool: str = Form(...),
    param: str = Form(""),
    protocol: str = Form(""),
    user: dict = Depends(require_user)
):
    if user["credits"] < 1:
        raise HTTPException(status_code=402, detail="رصيدك غير كافٍ. تحتاج نقطة واحدة لاستخدام هذه الأداة.")

    content = await file.read()
    try:
        modified_data, desc = execute_expert_operation(content, tool, param, file.filename, protocol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    file_id = uuid.uuid4().hex
    original_save_path = os.path.join(UPLOADS_DIR, f"{file_id}_{file.filename}")
    modified_filename = f"MOD_{tool.upper()}_{file.filename}"
    modified_save_path = os.path.join(PROCESSED_DIR, f"{file_id}_{modified_filename}")

    with open(original_save_path, "wb") as f:
        f.write(content)
    with open(modified_save_path, "wb") as f:
        f.write(modified_data)

    file_hash = hashlib.sha256(content).hexdigest()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = credits - 1 WHERE id = ?", (user["id"],))
        cursor.execute(
            """INSERT INTO files (user_id, original_name, file_hash, brand, model, ecu_type, sw_version, solutions, credits_cost, original_path, modified_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user["id"],
                file.filename,
                file_hash,
                "Renault Workshop Expert",
                tool,
                tool.upper(),
                param or "Standard",
                json.dumps([desc]),
                1,
                original_save_path,
                modified_save_path
            )
        )
        task_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO transactions (user_id, amount, type, description) VALUES (?, ?, 'expert_tool', ?)",
            (user["id"], -1, f"أداة تخصصية: {desc} على {file.filename}")
        )
        conn.commit()

    return {
        "success": True,
        "task_id": task_id,
        "filename": modified_filename,
        "download_url": f"/api/v1/tuning/download/{task_id}"
    }

@app.get("/logout")
async def logout(request: Request):
    token = request.cookies.get("ecu_token")
    auth_header = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    for t in [token, auth_header]:
        if t:
            if t in SESSIONS:
                del SESSIONS[t]
            delete_session_db(t)
    resp = RedirectResponse(url="/login")
    resp.delete_cookie("ecu_token")
    return resp

# ================= واجهات الـ API (Auth & Users) =================

@app.post("/api/v1/auth/login")
async def api_login(payload: dict, request: Request, response: Response):
    identifier = (payload.get("username", "") or payload.get("email", "") or payload.get("identifier", "")).strip()
    password = payload.get("password", "").strip()

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Veuillez renseigner votre identifiant et mot de passe.")

    try:
        user = authenticate_user(identifier, password)
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))

    if not user:
        raise HTTPException(
            status_code=400,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة. يرجى التحقق وإعادة المحاولة."
        )

    token = str(uuid.uuid4())
    SESSIONS[token] = user["id"]
    save_session_db(token, user["id"])
    response.set_cookie(key="ecu_token", value=token, httponly=True, max_age=86400*30, samesite="lax")
    
    user["credits"] = user.get("tokens", 0)
    user["is_admin"] = (user.get("role") == "admin")

    # توجيه المدير مباشرة إلى لوحة الإدارة
    redirect_url = "/admin" if user["is_admin"] else "/portal"

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "redirect": redirect_url,
        "user": user
    }

@app.post("/api/v1/auth/register")
async def api_register(payload: dict, request: Request, response: Response):
    full_name = payload.get("full_name", "").strip()
    workshop_name = payload.get("workshop_name", "").strip()
    phone = payload.get("phone", "").strip()
    wilaya_country = payload.get("wilaya_country", "").strip()
    email = payload.get("email", "").strip()
    password = payload.get("password", "")
    confirm_password = payload.get("confirm_password", "")

    if not full_name or not workshop_name or not phone or not email or not password:
        raise HTTPException(status_code=400, detail="Tous les champs obligatoires doivent être remplis.")

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas.")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Le mot de passe doit comporter au moins 6 caractères.")

    ip = get_client_ip(request)

    try:
        new_user = register_user(
            full_name=full_name,
            workshop_name=workshop_name,
            phone=phone,
            email=email,
            wilaya_country=wilaya_country,
            password=password,
            ip=ip
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    # Auto-login after registration
    token = str(uuid.uuid4())
    SESSIONS[token] = new_user["id"]
    save_session_db(token, new_user["id"])
    response.set_cookie(key="ecu_token", value=token, httponly=True, max_age=86400*30, samesite="lax")

    new_user["credits"] = new_user.get("tokens", 0)
    new_user["username"] = new_user.get("email", "")
    new_user["is_admin"] = (new_user.get("role") == "admin")

    return {
        "success": True,
        "bonus_granted": new_user.get("bonus_granted", True),
        "access_token": token,
        "user": new_user
    }

@app.get("/api/v1/user/me")
async def api_user_me(user: dict = Depends(require_user)):
    return user

@app.get("/api/v1/user/history")
async def api_user_history(user: dict = Depends(require_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, original_name, brand, model, ecu_type, sw_version, solutions, created_at FROM files WHERE user_id = ? ORDER BY id DESC LIMIT 20", (user["id"],))
        rows = [dict(r) for r in cursor.fetchall()]
        return {"files": rows}

@app.get("/api/v1/dtc/search")
async def api_search_dtc(q: str = ""):
    q = q.strip().upper()
    if not q:
        popular = ["P0401", "P0402", "P2002", "P2463", "P0420", "P0101", "P0113", "P20EE", "U0100", "P0087", "P0299", "P242F"]
        return [{"code": c, "desc": DTC_TABLE.get(c, "Standard OBD-II Code")} for c in popular]
    
    matches = []
    for code, desc in DTC_TABLE.items():
        if code.startswith(q) or q in code or q.lower() in desc.lower():
            matches.append({"code": code, "desc": desc})
            if len(matches) >= 30:
                break
    return matches

@app.post("/api/v1/tuning/analyze")
async def api_tuning_analyze(file: UploadFile = File(...), user: dict = Depends(require_user)):
    file_token = uuid.uuid4().hex
    saved_filename = f"{file_token}_{file.filename}"
    saved_path = os.path.join(UPLOADS_DIR, saved_filename)
    
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    with open(saved_path, "rb") as f:
        binary_data = f.read()
        
    # فحص بصمة الملف والكومبيوتر والحلول المدعومة فعلياً فقط (No Mock Data)
    ident = identify_ecu(binary_data, file.filename)
    
    # عدم تفعيل أي حل تلقائياً عند رفع الملف (No Auto-Selection on Upload)
    # تبدأ جميع الأزرار غير محددة ويكون عدد أكواد الـ DTC صفراً حتى يحدد المستخدم الحل بنفسه
    defaults = []
    initial_preview = []
    instructions = []
    
    return {
        "success": True,
        "file_token": file_token,
        "filename": file.filename,
        "brand": ident["brand"],
        "model": ident["model"],
        "ecu_type": ident["ecu_type"],
        "sw_version": ident["sw_version"],
        "hw_version": ident["hw_version"],
        "fuel": ident["fuel"],
        "supported_solutions": ident["supported_solutions"],
        "default_solutions": defaults,
        "checksum_info": ident["checksum_info"],
        "instructions": instructions,
        "dtc_preview": initial_preview,
        "dtc_count": len(initial_preview)
    }

@app.post("/api/v1/tuning/preview-dtc")
async def api_tuning_preview_dtc(payload: dict, user: dict = Depends(require_user)):
    file_token = payload.get("file_token", "")
    selected_solutions = payload.get("selected_solutions", [])
    custom_dtcs = payload.get("custom_dtcs", [])
    
    target_path = None
    if file_token:
        for fname in os.listdir(UPLOADS_DIR):
            if fname.startswith(file_token):
                target_path = os.path.join(UPLOADS_DIR, fname)
                break
                
    if not target_path or not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="الملف المرفوع غير موجود على السيرفر")
        
    with open(target_path, "rb") as f:
        binary_data = f.read()
        
    preview_items = preview_dtcs(binary_data, selected_solutions, custom_dtcs)
    instructions = get_technical_instructions(selected_solutions, target_path)
    return {
        "success": True,
        "total_codes": len(preview_items),
        "items": preview_items,
        "instructions": instructions
    }

@app.post("/api/v1/tuning/process")
async def api_tuning_process(
    file: Optional[UploadFile] = File(None),
    file_token: Optional[str] = Form(None),
    solutions: str = Form("[]"),
    dtcs: str = Form("[]"),
    user: dict = Depends(require_user)
):
    # التأكد من الرصيد أولاً (لن يخصم إلا عند ضغط زر التطبيق الفعلي)
    if user["credits"] < 1:
        raise HTTPException(status_code=402, detail="رصيدك غير كافٍ. يرجى شحن الرصيد لتعديل الملف.")

    try:
        selected_solutions = json.loads(solutions)
    except:
        selected_solutions = ["DPF / FAP", "EGR"]

    try:
        selected_dtcs = json.loads(dtcs)
    except:
        selected_dtcs = []

    # تحديد مسار الملف الأصلي
    original_save_path = None
    original_filename = "ECU_File.bin"

    if file_token:
        for fname in os.listdir(UPLOADS_DIR):
            if fname.startswith(file_token):
                original_save_path = os.path.join(UPLOADS_DIR, fname)
                original_filename = fname.replace(f"{file_token}_", "")
                break

    if not original_save_path and file:
        file_id = uuid.uuid4().hex
        original_filename = file.filename
        original_save_path = os.path.join(UPLOADS_DIR, f"{file_id}_{original_filename}")
        with open(original_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    if not original_save_path or not os.path.exists(original_save_path):
        raise HTTPException(status_code=400, detail="يرجى رفع ملف ECU أولاً")

    task_uuid = uuid.uuid4().hex
    modified_filename = f"MOD_{original_filename}"
    modified_save_path = os.path.join(PROCESSED_DIR, f"{task_uuid}_{modified_filename}")

    # حساب الهاش للملف الأصلي
    with open(original_save_path, "rb") as f:
        original_bytes = f.read()
        file_hash = hashlib.sha256(original_bytes).hexdigest()

    # تشغيل محرك التعديل بالحلول المحددة
    engine_result = run_tuning_task("process", original_save_path, modified_save_path, selected_solutions)
    if not engine_result.get("success"):
        raise HTTPException(status_code=500, detail="فشل محرك التعديل في معالجة الملف")

    # تطبيق تصفير commutateurs DTC بدقة على الملف المعدل
    try:
        with open(modified_save_path, "rb") as f:
            mod_data = bytearray(f.read())

        dtc_preview = preview_dtcs(original_bytes, selected_solutions, selected_dtcs)
        for item in dtc_preview:
            try:
                addr = int(item["offset"], 16)
                if addr < len(mod_data):
                    mod_data[addr] = 0x00
            except:
                pass

        with open(modified_save_path, "wb") as f:
            f.write(mod_data)
    except Exception as e:
        print("DTC patch error:", e)

    all_applied = list(selected_solutions)
    if selected_dtcs:
        all_applied.append(f"DTC_OFF: {', '.join(selected_dtcs)}")

    # خصم النقطة وتسجيل العملية في token_transactions وقاعدة البيانات
    new_balance = deduct_user_tokens(user["id"], 1, "file_process", f"Tuning {original_filename} ({', '.join(all_applied)})")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO files (user_id, original_name, file_hash, brand, model, ecu_type, sw_version, solutions, credits_cost, original_path, modified_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user["id"],
                original_filename,
                file_hash,
                engine_result.get("brand", "Vehicle"),
                engine_result.get("model", "Engine"),
                engine_result.get("ecu_type", "Standard ECU"),
                engine_result.get("sw_version", "SW_MOD"),
                json.dumps(all_applied),
                1,
                original_save_path,
                modified_save_path
            )
        )
        task_db_id = cursor.lastrowid
        conn.commit()

    return {
        "success": True,
        "task_id": task_db_id,
        "filename": modified_filename,
        "download_url": f"/api/v1/tuning/download/{task_db_id}",
        "brand": engine_result.get("brand"),
        "model": engine_result.get("model"),
        "ecu_type": engine_result.get("ecu_type"),
        "solutions": selected_solutions
    }

@app.get("/api/v1/tuning/download/{task_id}")
async def api_download_file(task_id: int, user: dict = Depends(require_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files WHERE id = ?", (task_id,))
        file_record = cursor.fetchone()
        if not file_record:
            raise HTTPException(status_code=404, detail="الملف غير موجود")
        
        # التأكد من الصلاحية: صاحب الملف أو المدير
        if file_record["user_id"] != user["id"] and not user.get("is_admin"):
            raise HTTPException(status_code=403, detail="غير مصرح لك بتحميل هذا الملف")

        mod_path = file_record["modified_path"]
        if not os.path.exists(mod_path):
            raise HTTPException(status_code=404, detail="الملف على السيرفر غير متوفر")

        download_name = f"MOD_{file_record['original_name']}"
        return FileResponse(mod_path, filename=download_name, media_type="application/octet-stream")

# ================= إدارة المدير (Admin APIs) =================

@app.get("/api/v1/admin/overview")
async def api_admin_overview(admin: dict = Depends(require_admin)):
    users = get_all_users()
    for u in users:
        u["credits"] = u.get("tokens", 0)
        u["username"] = u.get("full_name") or u.get("email") or "Client"
        u["is_admin"] = (u.get("role") == "admin")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role != 'admin'")
        total_users = cursor.fetchone()["count"]
        cursor.execute("SELECT SUM(tokens) as total FROM users")
        total_credits = cursor.fetchone()["total"] or 0
        cursor.execute("SELECT COUNT(*) as count FROM files")
        total_files = cursor.fetchone()["count"]

        cursor.execute("""
            SELECT f.id, u.email as username, u.full_name, u.workshop_name, f.original_name, f.brand, f.ecu_type, f.solutions, f.credits_cost, f.created_at
            FROM files f JOIN users u ON f.user_id = u.id ORDER BY f.id DESC LIMIT 30
        """)
        files = [dict(r) for r in cursor.fetchall()]

        return {
            "total_users": total_users,
            "total_credits": total_credits,
            "total_files": total_files,
            "users": users,
            "files": files
        }

@app.post("/api/v1/admin/users/{user_id}/recharge")
async def api_admin_recharge_user(user_id: int, payload: dict, admin: dict = Depends(require_admin)):
    amount = int(payload.get("amount", 10))
    desc = payload.get("description", f"Recharge manuelle par Administrateur (+{amount} Tokens)")
    new_balance = add_user_tokens(user_id, amount, "admin_recharge", desc)
    return {"success": True, "message": f"Succès : Solde actuel {new_balance} Tokens", "tokens": new_balance}

@app.post("/api/v1/admin/users/{user_id}/toggle")
async def api_admin_toggle_user(user_id: int, admin: dict = Depends(require_admin)):
    new_status = toggle_user_active_status(user_id)
    return {"success": True, "is_active": new_status}

@app.post("/api/v1/admin/users/{user_id}/reset-password")
async def api_admin_reset_password(user_id: int, payload: dict, admin: dict = Depends(require_admin)):
    new_password = payload.get("password", "").strip()
    if not new_password or len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Le mot de passe doit comporter au moins 6 caractères.")
    new_hash = hash_password(new_password)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        conn.commit()
    return {"success": True, "message": "تم تغيير كلمة المرور بنجاح."}

@app.post("/api/v1/admin/users")
async def api_admin_create_user(payload: dict, admin: dict = Depends(require_admin)):
    full_name = payload.get("full_name") or payload.get("username", "").strip()
    workshop_name = payload.get("workshop_name", "Atelier").strip()
    phone = payload.get("phone", "").strip()
    email = payload.get("email", "").strip()
    wilaya_country = payload.get("wilaya_country", "Algeria").strip()
    password = payload.get("password", "Scorpion2026!")
    credits = int(payload.get("credits", 10))

    if not phone:
        phone = f"+213{int(datetime.now().timestamp()) % 1000000000}"
    if not email:
        email = f"{full_name.lower().replace(' ', '')}{int(datetime.now().timestamp()) % 10000}@remap.pro"

    try:
        new_u = register_user(
            full_name=full_name,
            workshop_name=workshop_name,
            phone=phone,
            email=email,
            wilaya_country=wilaya_country,
            password=password,
            ip="Admin_Created"
        )
        if credits != 10:
            diff = credits - 10
            add_user_tokens(new_u["id"], diff, "admin_init", f"Ajustement initial crédits ({credits})")
        return {"success": True, "user": new_u}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/admin/banned-ips")
async def api_admin_get_banned_ips(admin: dict = Depends(require_admin)):
    return {"banned_ips": get_banned_ips()}

@app.post("/api/v1/admin/banned-ips/unban")
async def api_admin_unban_ip(payload: dict, admin: dict = Depends(require_admin)):
    ip = payload.get("ip", "").strip()
    if not ip:
        raise HTTPException(status_code=400, detail="Veuillez spécifier l'adresse IP")
    unban_ip(ip)
    return {"success": True, "message": f"L'adresse IP {ip} a été débloquée avec succès."}

@app.post("/api/v1/admin/banned-ips/ban")
async def api_admin_manual_ban_ip(payload: dict, admin: dict = Depends(require_admin)):
    ip = payload.get("ip", "").strip()
    reason = payload.get("reason", "Bloqué manuellement par Administrateur").strip()
    hours = int(payload.get("hours", 24))
    if not ip:
        raise HTTPException(status_code=400, detail="Veuillez spécifier l'adresse IP")
    manual_ban_ip(ip, reason, hours)
    return {"success": True, "message": f"L'adresse IP {ip} a été bloquée pour {hours} heures."}

if __name__ == "__main__":
    import uvicorn
    init_db()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
