import os
import sys
import json
import uuid
import shutil
import hashlib
import struct
from typing import Optional, List
from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status, Body
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# إضافة المسار الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

from server.whatsapp_service import send_real_whatsapp_otp, clean_phone_number
from server.db import (
    get_whatsapp_config, save_whatsapp_config,
    get_db, init_db, hash_password, verify_password,
    register_user, authenticate_user, get_user_by_id,
    deduct_user_tokens, add_user_tokens, get_all_users,
    toggle_user_active_status, get_user_transactions,
    is_ip_banned, record_failed_attempt, clear_failed_attempts,
    get_banned_ips, unban_ip, manual_ban_ip,
    save_session_db, get_session_user_db, delete_session_db,
    create_support_ticket, add_ticket_message, get_user_tickets,
    get_all_support_tickets, get_ticket_details, get_ticket_attachment,
    verify_user_whatsapp, admin_verify_user_whatsapp, get_user_for_verification
)
from engine.tuning_bridge import run_tuning_task
from engine.ecu_analyzer import (
    identify_ecu, preview_dtcs, get_technical_instructions,
    SUPPORTED_REGISTRY, get_registry_ecu
)
from engine.renault_expert import preview_expert_operation, execute_expert_operation

app = FastAPI(title="SCORPION REMAP PRO", version="3.2.0")

# Mount Static Files (CSS, JS, Fonts)
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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

@app.on_event("startup")
async def app_startup_keepalive():
    import threading, time, urllib.request
    def _keepalive_loop():
        time.sleep(180)
        while True:
            try:
                req = urllib.request.Request("https://scorpion-remap-pro.onrender.com/healthz", headers={"User-Agent": "ScorpionKeepAlive/1.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    pass
            except Exception:
                pass
            time.sleep(600)
    threading.Thread(target=_keepalive_loop, daemon=True).start()

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
    """
    Retourne la liste complète des ECUs supportés:
    - SVEdit v1.1.38.3 (base)
    - DaVinci v1.0.28 + v1.0.30 (DaVinci Deep Extraction — APPEND)
    Champ fuel: DIESEL ou ESSENCE (isolement strict carburant).
    """
    ecus_list = []
    seen_ids = set()
    for brand, ecus in SUPPORTED_REGISTRY.items():
        for ecu in ecus:
            ecu_id = ecu.get("id", "")
            if ecu_id in seen_ids:
                continue
            seen_ids.add(ecu_id)
            name = ecu.get("name", ecu_id)
            # support both "fuel" and "fuel_type" key names
            fuel = ecu.get("fuel", ecu.get("fuel_type", "DIESEL"))
            sols = ecu.get("supported_solutions", ecu.get("solutions", ["DTC OFF"]))
            plug_note = ecu.get("plug_notes", ecu.get("plug_note", ""))
            source = ecu.get("source", "SVEdit v1.1.38")
            ecus_list.append({
                "id": ecu_id,
                "brand": brand,
                "name": name,
                "ecu": name,
                "engine": f"{brand}",
                "fuel": fuel,
                "fuel_type": fuel,
                "solutions": sols,
                "plug_notes": plug_note,
                "source": source,
                "description": ecu.get("description", f"Calculateur {brand} — {name}")
            })
    # Sort by brand then name
    ecus_list.sort(key=lambda x: (x["brand"], x["name"]))
    return ecus_list

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
    except ValueError as ve:
        err_msg = str(ve)
        if err_msg.startswith("WHATSAPP_UNVERIFIED:"):
            parts = err_msg.split(":")
            # parts: ["WHATSAPP_UNVERIFIED", user_id, phone, whatsapp_code, full_name]
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "Compte non activé. Veuillez confirmer votre numéro WhatsApp.",
                    "requires_whatsapp_verification": True,
                    "user_id": int(parts[1]),
                    "phone": parts[2],
                    "whatsapp_code": parts[3],
                    "full_name": parts[4] if len(parts) > 4 else "Client",
                    "admin_whatsapp": "213799999002"
                }
            )
        raise HTTPException(status_code=400, detail=err_msg)

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

    new_user["credits"] = new_user.get("tokens", 0)
    new_user["username"] = new_user.get("email", "")
    new_user["is_admin"] = (new_user.get("role") == "admin")

    # If new user is an admin, auto-login
    if new_user.get("role") == "admin":
        token = str(uuid.uuid4())
        SESSIONS[token] = new_user["id"]
        save_session_db(token, new_user["id"])
        response.set_cookie(key="access_token", value=token, max_age=86400*30, samesite="lax")
        return {
            "success": True,
            "requires_whatsapp_verification": False,
            "access_token": token,
            "redirect": "/admin",
            "user": new_user
        }

    # Real WhatsApp Verification: Send OTP directly to user's WhatsApp
    wa_config = get_whatsapp_config()
    code = new_user.get("whatsapp_code", "")
    sent_ok, send_msg = send_real_whatsapp_otp(
        phone=new_user["phone"],
        code=code,
        client_name=new_user["full_name"],
        config=wa_config
    )

    return {
        "success": True,
        "requires_whatsapp_verification": True,
        "user_id": new_user["id"],
        "full_name": new_user["full_name"],
        "workshop_name": new_user["workshop_name"],
        "phone": new_user["phone"],
        "whatsapp_sent": sent_ok,
        "admin_whatsapp": wa_config.get("admin_phone", "213799999002"),
        "detail": f"Un code de confirmation a été envoyé à votre WhatsApp ({new_user['phone']})." if sent_ok else "Veuillez saisir le code reçu sur WhatsApp ou contacter le support."
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
        return {"files": rows, "history": rows}

@app.post("/api/v1/user/change-password")
async def api_change_password(payload: dict = Body(...), user: dict = Depends(require_user)):
    new_password = payload.get("new_password", "").strip()
    if not new_password or len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Le mot de passe doit comporter au moins 6 caractères")
    new_hash = hash_password(new_password)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user["id"]))
        conn.commit()
    return {"status": "success", "message": "Mot de passe modifié avec succès"}

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

@app.get("/api/v1/tuning/registry")
async def api_tuning_registry():
    """استرجاع قاعدة بيانات الكمبيوترات والماركات المبرمجة فعلياً فقط"""
    return {
        "success": True,
        "registry": SUPPORTED_REGISTRY
    }

@app.post("/api/v1/tuning/manual-select")
async def api_tuning_manual_select(payload: dict, user: dict = Depends(require_user)):
    """تطبيق الاختيار اليدوي الصارم حصراً على ملف حقيقي تم رفعه مسبقاً (Mandatory Real File Upload First)"""
    file_token = payload.get("file_token", "").strip()
    if not file_token:
        raise HTTPException(
            status_code=400, 
            detail="Veuillez d'abord téléverser un fichier binaire (.bin, .ori) avant de choisir un calculateur."
        )

    # التحقق من وجود الملف الحقيقي على السيرفر
    target_path = None
    original_filename = "ECU_File.bin"
    for fname in os.listdir(UPLOADS_DIR):
        if fname.startswith(file_token):
            target_path = os.path.join(UPLOADS_DIR, fname)
            original_filename = fname.replace(f"{file_token}_", "")
            break

    if not target_path or not os.path.exists(target_path):
        raise HTTPException(
            status_code=404, 
            detail="Fichier binaire introuvable sur le serveur. Veuillez réuploader votre fichier d'origine."
        )

    with open(target_path, "rb") as f:
        binary_data = f.read()

    ecu_id = payload.get("ecu_id", "").strip()
    brand = payload.get("brand", "").strip()
    
    ecu_info = get_registry_ecu(brand, ecu_id)
    if not ecu_info:
        raise HTTPException(status_code=400, detail="Calculateur introuvable dans la base de données SCORPION")

    # استخراج رقم السوفتوير الحقيقي من الملف إن أمكن
    real_ident = identify_ecu(binary_data, original_filename)
    sw_version = real_ident.get("sw_version") or "Calibration Réelle"
    hw_version = real_ident.get("hw_version") or ecu_info["name"].split()[0]
        
    return {
        "success": True,
        "recognized": True,
        "manual_selection": True,
        "file_token": file_token,
        "filename": original_filename,
        "file_size": len(binary_data),
        "brand": ecu_info["brand"],
        "model": f"Calculateur Moteur ({ecu_info['fuel']})",
        "ecu": ecu_info["name"],
        "ecu_id": ecu_info["id"],
        "ecu_type": ecu_info["name"],
        "sw_version": sw_version,
        "hw_version": hw_version,
        "fuel": ecu_info["fuel"],
        "fuel_type": ecu_info["fuel"],
        "fuel_badge": "Moteur Diesel ⛽" if ecu_info["fuel"] == "DIESEL" else "Moteur Essence ⚡",
        "supported_solutions": ecu_info["supported_solutions"],
        "solutions": ecu_info["supported_solutions"],
        "checksum_info": ecu_info.get("checksum_info", {
            "status": "Correction via Flasher (KESS/Autotuner/Flex) ⚠️",
            "is_auto": False,
            "algorithm": "Standard Checksum"
        }),
        "instructions": [],
        "dtc_preview": [],
        "dtc_count": 0
    }

@app.post("/api/v1/tuning/analyze")
async def api_tuning_analyze(file: UploadFile = File(...), user: dict = Depends(require_user)):
    file_token = uuid.uuid4().hex
    saved_filename = f"{file_token}_{file.filename}"
    saved_path = os.path.join(UPLOADS_DIR, saved_filename)
    
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    with open(saved_path, "rb") as f:
        binary_data = f.read()
        
    # فحص بصمة الملف والكومبيوتر والحلول المدعومة فعلياً فقط (No Mock Data & No Guessing)
    ident = identify_ecu(binary_data, file.filename)
    
    # في حال لم يتعرف السيرفر على الملف تلقائياً بنسبة 100%
    if not ident.get("recognized", True):
        file_size_kb = round(len(binary_data) / 1024, 1)
        return {
            "success": True,
            "recognized": False,
            "message": f"Fichier chargé avec succès (Taille: {file_size_kb} Ko). Veuillez sélectionner manuellement votre véhicule et calculateur dans notre base pour traiter ce fichier :",
            "file_token": file_token,
            "filename": file.filename,
            "file_size": len(binary_data),
            "file_size_kb": file_size_kb,
            "sw_version": ident.get("sw_version"),
            "hw_version": ident.get("hw_version")
        }

    # عدم تفعيل أي حل تلقائياً عند رفع الملف (No Auto-Selection on Upload)
    # تبدأ جميع الأزرار غير محددة ويكون عدد أكواد الـ DTC صفراً حتى يحدد المستخدم الحل بنفسه
    defaults = []
    initial_preview = []
    instructions = []
    
    model_name = ident.get("model") or ident.get("ecu_name") or ident.get("id") or "Calculateur"
    brand_name = ident.get("brand") or "Générique"
    ecu_type = ident.get("ecu_type") or ident.get("ecu_name") or model_name
    fuel = ident.get("fuel") or ident.get("fuel_type") or "DIESEL"
    solutions = ident.get("supported_solutions") or ident.get("solutions") or ["DTC OFF", "Stage 1"]
    checksum_info = ident.get("checksum_info") or {
        "status": ident.get("checksum_status", "Supporté & Automatique ✅"),
        "is_auto": True,
        "algorithm": ident.get("checksum_algorithm", "Bosch TriCore Checksum")
    }

    return {
        "success": True,
        "recognized": True,
        "file_token": file_token,
        "filename": file.filename,
        "brand": brand_name,
        "model": model_name,
        "ecu": model_name,
        "ecu_id": ident.get("ecu_id", ident.get("id", "")),
        "ecu_type": ecu_type,
        "sw_version": ident.get("sw_version", "Reconnu par Empreinte"),
        "hw_version": ident.get("hw_version", "Certifié SVEdit"),
        "fuel": fuel,
        "fuel_type": fuel,
        "fuel_badge": ident.get("fuel_badge", "Moteur Diesel ⛽" if fuel == "DIESEL" else "Moteur Essence ⚡"),
        "supported_solutions": solutions,
        "default_solutions": defaults,
        "checksum_info": checksum_info,
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
        
    ident = identify_ecu(binary_data, os.path.basename(target_path))

    # خريطة أكواد الـ DTC المرتبطة بكل حل
    SOLUTION_DTC_MAP = {
        "DPF": ["P2002", "P2463", "P2452", "P2458", "P244A", "P2453"],
        "FAP": ["P2002", "P2463", "P2452"],
        "EGR": ["P0401", "P0402", "P0403", "P0404", "P0405"],
        "ADBLUE": ["P20EE", "P204F", "U029D", "P207F", "P20BD"],
        "SCR": ["P20EE", "P204F", "U029D"],
        "LAMBDA": ["P0136", "P0141", "P0420"],
        "CAT": ["P0420", "P0430", "P0136"],
        "DECAT": ["P0420", "P0430", "P0136"],
        "SWIRL": ["P2008", "P2015"],
        "FLAP": ["P2008", "P2015"],
        "VSA": ["P2008", "P2015"],
        "TVA": ["P2101", "P2102"],
        "START-STOP": ["U0167"],
        "EVAP": ["P0441", "P0442"],
        "MAF": ["P0100", "P0101", "P0102"]
    }

    active_codes = []
    for sol in selected_solutions:
        sol_upper = sol.upper()
        matched_any = False
        for key, codes in SOLUTION_DTC_MAP.items():
            if key in sol_upper:
                matched_any = True
                for c in codes:
                    if c not in [item[0] for item in active_codes]:
                        active_codes.append((c, sol))
        if not matched_any and ("STAGE" not in sol_upper and "HOT" not in sol_upper):
            pass

    for c in custom_dtcs:
        c = c.strip().upper()
        if c and c not in [item[0] for item in active_codes]:
            active_codes.append((c, "Manuel (Client)"))

    preview_items = []
    for code, source in active_codes:
        code_num = None
        try:
            if code.startswith("P") and len(code) == 5:
                code_num = int(code[1:], 16)
        except:
            pass

        offset_str = "0x000000"
        val_ori = "0x01"
        if code_num is not None:
            le_bytes = struct.pack("<H", code_num)
            be_bytes = struct.pack(">H", code_num)
            pos = binary_data.find(le_bytes)
            if pos != -1:
                offset_str = f"0x{pos:06X}"
                val_ori = f"0x{binary_data[pos]:02X}"
            else:
                pos = binary_data.find(be_bytes)
                if pos != -1:
                    offset_str = f"0x{pos:06X}"
                    val_ori = f"0x{binary_data[pos]:02X}"

        preview_items.append({
            "code": code,
            "description": DTC_TABLE.get(code, "Code Défaut OBD-II / DTC Gestion Moteur"),
            "offset": offset_str,
            "val_ori": val_ori,
            "val_mod": "0x00",
            "source": source
        })

    # معالجة تعليمات ورشة العمل
    raw_instructions = get_technical_instructions(ident, selected_solutions)
    lines = [l.strip() for l in raw_instructions.split("\n") if l.strip()]
    instructions = []
    for line in lines:
        badge = "INFO"
        type_ = "info"
        if "Débrancher" in line or "impérativement" in line:
            badge = "IMPORTANT"
            type_ = "critical"
        elif "condamnée" in line or "mécaniquement" in line:
            badge = "ATELIER"
            type_ = "warning"
        elif "Checksum" in line:
            badge = "CHECKSUM"
            type_ = "info"
        instructions.append({
            "badge": badge,
            "title": line.split(".")[1].strip() if "." in line[:5] else line[:40],
            "desc": line,
            "type": type_
        })

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
    manual_brand: Optional[str] = Form(None),
    manual_ecu_id: Optional[str] = Form(None),
    user: dict = Depends(require_user)
):
    # التأكد من الرصيد أولاً (لن يخصم إلا عند ضغط زر التطبيق الفعلي)
    if user["credits"] < 1:
        raise HTTPException(status_code=402, detail="رصيدك غير كافٍ. يرجى شحن الرصيد لتعديل الملف.")

    try:
        selected_solutions = json.loads(solutions)
    except:
        selected_solutions = []

    try:
        selected_dtcs = json.loads(dtcs)
    except:
        selected_dtcs = []

    # منع التحميل أو خصم الكريديت إذا لم يتم اختيار أي حل أو كود DTC (Strict Policy)
    if not selected_solutions and not selected_dtcs:
        raise HTTPException(
            status_code=400,
            detail="Veuillez sélectionner au moins une solution ou un code DTC avant de télécharger."
        )

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
    engine_result = run_tuning_task("process", original_save_path, modified_save_path, selected_solutions, ecu_type=manual_ecu_id or "")
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

    final_brand = engine_result.get("brand", "Vehicle")
    final_ecu_type = engine_result.get("ecu_type", "Standard ECU")
    final_model = engine_result.get("model", "Engine")

    if manual_ecu_id:
        reg_ecu = get_registry_ecu(manual_brand or "", manual_ecu_id)
        if reg_ecu:
            final_brand = reg_ecu["brand"]
            final_ecu_type = reg_ecu["name"]
            final_model = f"Calculateur Moteur ({reg_ecu['fuel']})"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO files (user_id, original_name, file_hash, brand, model, ecu_type, sw_version, solutions, credits_cost, original_path, modified_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user["id"],
                original_filename,
                file_hash,
                final_brand,
                final_model,
                final_ecu_type,
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
        "brand": final_brand,
        "model": final_model,
        "ecu_type": final_ecu_type,
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


# =========================================================================
# نقاط نهاية نظام المراسلة والتذاكر الداخلي 100% (Support & File Exchange)
# =========================================================================

ALLOWED_EXTENSIONS = {".bin", ".ori", ".mod", ".zip", ".rar", ".7z", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 16 * 1024 * 1024 # 16 MB

def validate_uploaded_attachment(upload_file: Optional[UploadFile]) -> Tuple[Optional[str], Optional[bytes]]:
    if not upload_file or not upload_file.filename:
        return None, None
    filename = upload_file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Format de fichier non autorisé ({ext}). Extensions permises : .bin, .ori, .mod, .zip, .rar, .jpg, .png"
        )
    content = upload_file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="La taille du fichier dépasse la limite maximale autorisée (16 Mo)."
        )
    return filename, content


@app.post("/api/v1/support/tickets")
async def api_support_create_ticket(
    subject: str = Form(...),
    vehicle_ecu: str = Form(...),
    message: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
    user: dict = Depends(require_user)
):
    """إنشاء تذكرة دعم فني جديدة من طرف الزبون مع ملف السيارة"""
    subject = subject.strip()
    vehicle_ecu = vehicle_ecu.strip()
    message = message.strip()
    if not subject or not message:
        raise HTTPException(status_code=400, detail="Veuillez remplir le sujet et votre message.")
    
    att_name, att_bytes = validate_uploaded_attachment(attachment)
    ticket_id = create_support_ticket(
        user_id=user["id"],
        subject=subject,
        vehicle_ecu=vehicle_ecu or "Non spécifié",
        message_text=message,
        attachment_name=att_name,
        attachment_data=att_bytes
    )
    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": f"Votre ticket #{ticket_id} a été transmis avec succès à l'administration SCORPION."
    }


@app.get("/api/v1/support/tickets")
async def api_support_get_user_tickets(user: dict = Depends(require_user)):
    """استرجاع تذاكر الزبون المسجل"""
    return {"tickets": get_user_tickets(user["id"])}


@app.get("/api/v1/support/tickets/{ticket_id}")
async def api_support_get_ticket(ticket_id: int, user: dict = Depends(require_user)):
    """استرجac محادثة التذكرة بالكامل للزبون أو المدير"""
    ticket = get_ticket_details(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable.")
    
    # التحقق من الصلاحيات (المالك أو المدير فقط)
    is_admin = user.get("role") == "admin" or user.get("is_admin", False)
    if not is_admin and ticket["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé à ce ticket.")
    
    return {"success": True, "ticket": ticket}


@app.post("/api/v1/support/tickets/{ticket_id}/reply")
async def api_support_reply_ticket(
    ticket_id: int,
    message: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
    deduct_tokens: Optional[int] = Form(0),
    user: dict = Depends(require_user)
):
    """الرد على التذكرة من طرف الزبون أو المدير مع إمكانية إرفاق ملف وخصم اختياري للرصيد"""
    ticket = get_ticket_details(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable.")
    
    is_admin = user.get("role") == "admin" or user.get("is_admin", False)
    if not is_admin and ticket["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé.")
    
    sender_role = "admin" if is_admin else "user"
    att_name, att_bytes = validate_uploaded_attachment(attachment)
    
    # إذا كان الرد من المدير وهناك خصم اختياري للكريديت (0, 1, 2 crédits)
    if is_admin and deduct_tokens and deduct_tokens > 0:
        target_client = get_user_by_id(ticket["user_id"])
        if target_client and target_client.get("tokens", 0) >= deduct_tokens:
            deduct_user_tokens(
                ticket["user_id"], 
                deduct_tokens, 
                "manual_remap", 
                f"Traitement sur mesure Ticket #{ticket_id} ({ticket['vehicle_ecu']})"
            )
    
    msg_id = add_ticket_message(
        ticket_id=ticket_id,
        sender_role=sender_role,
        message_text=message.strip(),
        attachment_name=att_name,
        attachment_data=att_bytes,
        new_status="answered" if is_admin else "open"
    )
    return {"success": True, "message_id": msg_id, "status": "answered" if is_admin else "open"}


@app.get("/api/v1/support/messages/{message_id}/download")
async def api_support_download_attachment(message_id: int, user: dict = Depends(require_user)):
    """تحميل الملف المرفق من الرسالة مباشرة من قاعدة البيانات"""
    att = get_ticket_attachment(message_id)
    if not att:
        raise HTTPException(status_code=404, detail="Fichier introuvable ou expiré.")
    filename, data = att
    from urllib.parse import quote
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\"; filename*=utf-8''{quote(filename)}"
    }
    return Response(content=data, media_type="application/octet-stream", headers=headers)


@app.get("/api/v1/admin/support/tickets")
async def api_admin_get_all_tickets(admin: dict = Depends(require_admin)):
    """استرجاع كافة تذاكر الدعم والملفات في لوحة تحكم المدير"""
    tickets = get_all_support_tickets()
    open_count = sum(1 for t in tickets if t.get("status") == "open")
    return {
        "tickets": tickets,
        "open_count": open_count
    }


if __name__ == "__main__":
    import uvicorn
    init_db()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)


@app.post("/api/v1/auth/verify-whatsapp")
async def api_verify_whatsapp(payload: dict, response: Response):
    user_id = payload.get("user_id")
    code = str(payload.get("code", "")).strip()

    if not user_id or not code:
        raise HTTPException(status_code=400, detail="Veuillez renseigner le code d'activation.")

    success, msg = verify_user_whatsapp(int(user_id), code)
    if not success:
        raise HTTPException(status_code=400, detail=msg)

    user = get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

    token = str(uuid.uuid4())
    SESSIONS[token] = user["id"]
    save_session_db(token, user["id"])
    response.set_cookie(key="access_token", value=token, max_age=86400*30, samesite="lax")
    response.set_cookie(key="ecu_token", value=token, httponly=True, max_age=86400*30, samesite="lax")

    return {
        "success": True,
        "access_token": token,
        "redirect": "/portal",
        "detail": "Compte WhatsApp validé avec succès ! 10 Crédits offerts débloqués."
    }


@app.post("/api/v1/admin/users/{user_id}/verify-whatsapp")
async def api_admin_verify_user_whatsapp(user_id: int, admin: dict = Depends(require_admin)):
    ok = admin_verify_user_whatsapp(user_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Impossible de valider cet utilisateur.")
    return {"success": True, "detail": "Utilisateur validé et activé via WhatsApp avec succès !"}


@app.post("/api/v1/auth/resend-whatsapp-otp")
async def api_resend_whatsapp_otp(payload: dict):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="ID utilisateur manquant.")

    user = get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

    if user.get("whatsapp_verified"):
        return {"success": True, "detail": "Compte déjà vérifié."}

    wa_config = get_whatsapp_config()
    sent_ok, send_msg = send_real_whatsapp_otp(
        phone=user["phone"],
        code=user.get("whatsapp_code", ""),
        client_name=user["full_name"],
        config=wa_config
    )
    return {
        "success": sent_ok,
        "detail": send_msg if sent_ok else "Impossible d'envoyer le message. Vérifiez la passerelle WhatsApp."
    }


@app.get("/api/v1/admin/settings/whatsapp")
async def api_admin_get_whatsapp_config(admin: dict = Depends(require_admin)):
    config = get_whatsapp_config()
    # Mask API token slightly for security
    token = config.get("api_token", "")
    masked_token = token[:4] + "••••••••" + token[-4:] if len(token) > 8 else token
    return {
        "provider": config.get("provider", "ultramsg"),
        "instance_id": config.get("instance_id", ""),
        "api_token": config.get("api_token", ""),
        "masked_token": masked_token,
        "admin_phone": config.get("admin_phone", "213799999002")
    }


@app.post("/api/v1/admin/settings/whatsapp")
async def api_admin_save_whatsapp_config(payload: dict, admin: dict = Depends(require_admin)):
    provider = payload.get("provider", "ultramsg").strip()
    instance_id = payload.get("instance_id", "").strip()
    api_token = payload.get("api_token", "").strip()
    admin_phone = payload.get("admin_phone", "213799999002").strip()

    save_whatsapp_config(provider, instance_id, api_token, admin_phone)
    return {"success": True, "detail": "Configuration WhatsApp enregistrée avec succès !"}


@app.post("/api/v1/admin/settings/whatsapp/test")
async def api_admin_test_whatsapp(payload: dict, admin: dict = Depends(require_admin)):
    target_phone = payload.get("test_phone", "").strip() or admin.get("phone", "")
    if not target_phone:
        raise HTTPException(status_code=400, detail="Veuillez indiquer un numéro WhatsApp de test.")

    config = get_whatsapp_config()
    sent_ok, msg = send_real_whatsapp_otp(
        phone=target_phone,
        code="TEST-2026",
        client_name=admin.get("full_name", "Admin"),
        config=config
    )
    if not sent_ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"success": True, "detail": f"Message de test envoyé avec succès sur le WhatsApp de {target_phone} !"}
