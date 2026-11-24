import os
import sys
import time
import re
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable
CLOUDFLARED_EXE = os.path.join(PROJECT_DIR, "cloudflared.exe")

UVICORN_LOG = os.path.join(PROJECT_DIR, "uvicorn.log")
CLOUDFLARED_LOG = os.path.join(PROJECT_DIR, "cloudflared.log")
DESKTOP_URL_FILE = r"C:\Users\ZY Laptop\Desktop\رابط_السيرفر_اونلاين.txt"

print("=" * 60)
print("🚀 إطلاق سيرفر SCORPION REMAP PRO V3.2.0 (أونلاين)...")
print("=" * 60)

server_env = os.environ.copy()
server_env["PYTHONPATH"] = PROJECT_DIR

# تنظيف اللوغات
with open(UVICORN_LOG, "w", encoding="utf-8") as f:
    f.write("")

# 1. تشغيل خادم Uvicorn / FastAPI
server_cmd = [
    PYTHON_EXE, "-m", "uvicorn", "server.app:app",
    "--host", "0.0.0.0",
    "--port", "8000"
]

print(">>> تشغيل الـ Backend على المنفذ 8000...")
uvicorn_file = open(UVICORN_LOG, "a", encoding="utf-8")
server_process = subprocess.Popen(
    server_cmd,
    cwd=PROJECT_DIR,
    env=server_env,
    stdout=uvicorn_file,
    stderr=subprocess.STDOUT
)

time.sleep(2)

def update_desktop_file(public_url):
    try:
        with open(DESKTOP_URL_FILE, "w", encoding="utf-8") as f:
            f.write(f"====================================================\n"
                    f" 🦂 رابط منصة SCORPION REMAP PRO V3.2.0 (أونلاين)\n"
                    f"====================================================\n\n"
                    f"🌐 الرابط المباشر للمنصة (يعمل من أي جهاز في العالم):\n"
                    f"{public_url}\n\n"
                    f"🎁 تسجيل حساب جديد (Créer un compte):\n"
                    f"- يحصل كل مستخدم جديد فوراً على 10 توكنز (Crédits) مجاناً لتجربة كافة الحلول.\n"
                    f"- إمكانية الدخول بالبريد الإلكتروني أو رقم الهاتف / WhatsApp.\n\n"
                    f"🛡️ حساب المدير العام (Admin Account):\n"
                    f"البريد الإلكتروني: admin@scorpion-remap.pro\n"
                    f"كلمة المرور:       AdminScorpion2026!\n"
                    f"الرصيد:            9,999 توكنز\n\n"
                    f"⚡ واجهة تعديل حرارة المروحة (EVO Fan Modifier):\n"
                    f"- مدمجة بـ 16 بروتوكول لرينو وداسيا: DCM1.2, EDC16CP33, EDC17C42, EMS3110, EMS3120, EMS3130, EMS3132, EMS3155, EMS3160, S3000, SID305, SID306, SID307, SIM32, V40, V42\n"
                    f"====================================================\n")
        print(f">>> تم تحديث الملف على سطح المكتب: {public_url}")
    except Exception as e:
        print(f"Error updating desktop file: {e}")

def start_tunnel():
    with open(CLOUDFLARED_LOG, "w", encoding="utf-8") as f:
        f.write("")
    cf_file = open(CLOUDFLARED_LOG, "a", encoding="utf-8")
    tunnel_cmd = [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:8000"]
    proc = subprocess.Popen(tunnel_cmd, stdout=cf_file, stderr=subprocess.STDOUT)
    
    url = None
    start_t = time.time()
    while time.time() - start_t < 25:
        time.sleep(1)
        if os.path.exists(CLOUDFLARED_LOG):
            try:
                with open(CLOUDFLARED_LOG, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    matches = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', content)
                    if matches:
                        url = matches[0]
                        break
            except:
                pass
    return proc, url

print(">>> فتح نفق Cloudflare Tunnel...")
tunnel_process, public_url = start_tunnel()

if public_url:
    update_desktop_file(public_url)
    print("\n" + "=" * 60)
    print(f"🎉 المنصة أونلاين الآن: {public_url}")
    print("=" * 60)
else:
    print("⚠️ جاري المحاولة...")

# حلقة مراقبة ذكية لإعادة الاتصال التلقائي في حال انقطاع النفق
last_check_time = time.time()
try:
    while True:
        time.sleep(5)
        # التأكد من عمل السيرفر الداخلي
        if server_process.poll() is not None:
            print("Restarting server backend...")
            server_process = subprocess.Popen(server_cmd, cwd=PROJECT_DIR, env=server_env, stdout=uvicorn_file, stderr=subprocess.STDOUT)

        # فحص حالة نفق Cloudflare
        tunnel_dead = (tunnel_process.poll() is not None)
        tunnel_unauthorized = False
        if os.path.exists(CLOUDFLARED_LOG):
            try:
                with open(CLOUDFLARED_LOG, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()[-2000:]
                    if "Unauthorized: Tunnel not found" in content or "i/o timeout" in content and "ERR" in content:
                        tunnel_unauthorized = True
            except:
                pass

        if tunnel_dead or tunnel_unauthorized:
            print("⚠️ تم اكتشاف انقطاع أو انتهاء صلاحية النفق، جاري إعادة إنشاء رابط جديد فوراً...")
            try:
                tunnel_process.terminate()
                time.sleep(1)
                tunnel_process.kill()
            except:
                pass
            tunnel_process, new_url = start_tunnel()
            if new_url:
                public_url = new_url
                update_desktop_file(new_url)
                print(f"✅ تم تجديد الرابط بنجاح: {new_url}")

except KeyboardInterrupt:
    print("\nإيقاف السيرفر...")
    server_process.terminate()
    tunnel_process.terminate()
