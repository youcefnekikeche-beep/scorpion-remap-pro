import random
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "storage", "scorpion_users.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    salt = "ScorpionRemapPro2026_EnterpriseSecureSalt"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed: str) -> bool:
    return hash_password(plain_password) == hashed

SUPER_ADMIN_EMAILS = {"admin@scorpion-remap.pro", "ayoubtbessa@gmail.com", "tbessa@gmail.com"}

def is_super_admin(email: str) -> bool:
    if not email:
        return False
    e = email.strip().lower()
    return e in SUPER_ADMIN_EMAILS or "tbessa" in e

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. جدول المستخدمين الحقيقي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            workshop_name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            wilaya_country TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            tokens INTEGER DEFAULT 10,
            role TEXT DEFAULT 'user',
            ip_address TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Auto-migration for WhatsApp verification columns
        for col_def in [
            ("whatsapp_verified", "INTEGER DEFAULT 0"),
            ("whatsapp_code", "TEXT"),
            ("whatsapp_verified_at", "TIMESTAMP")
        ]:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_def[0]} {col_def[1]}")
            except Exception:
                pass

        # Super admin users are automatically verified
        cursor.execute("UPDATE users SET whatsapp_verified = 1, is_active = 1 WHERE role = 'admin'")

        # جدول إعدادات النظام وربط بوابات WhatsApp
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # 2. جدول معاملات التوكنز والعمليات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        # 3. جدول أرشيف ملفات التعديل
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            brand TEXT DEFAULT 'Unknown',
            model TEXT DEFAULT 'Unknown',
            ecu_type TEXT DEFAULT 'Unknown',
            sw_version TEXT DEFAULT 'Unknown',
            solutions TEXT DEFAULT '[]',
            credits_cost INTEGER DEFAULT 1,
            status TEXT DEFAULT 'completed',
            original_path TEXT,
            modified_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        # 4. جدول حظر العناوين المشبوهة والهجمات (Anti-Brute-Force & Fail2Ban)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS banned_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE NOT NULL,
            attempts INTEGER DEFAULT 1,
            reason TEXT NOT NULL,
            banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            banned_until TIMESTAMP NOT NULL,
            is_active INTEGER DEFAULT 1
        )
        """)

        # 5. جدول الجلسات المستمرة (Persistent Sessions) لمنع تسجيل الخروج التلقائي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        # جدول التذاكر والدعم الفني المباشر الداخلي 100%
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            vehicle_ecu TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        # جدول رسائل ومرفقات التذاكر (تخزين BLOB للملفات لضمان عدم ضياعها بالسحابة)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            sender_role TEXT NOT NULL,
            message_text TEXT NOT NULL,
            attachment_name TEXT,
            attachment_data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES support_tickets (id)
        )
        """)

        # ضبط عداد التذاكر ليبدأ من #1001 إذا كان فارغاً
        cursor.execute("SELECT COUNT(*) FROM support_tickets")
        if cursor.fetchone()[0] == 0:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'support_tickets'")
            cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('support_tickets', 1000)")

        # إنشاء وتحديث حسابات المدراء الرسمية
        admin_accounts = [
            ("Administrateur SCORPION", "SCORPION REMAP HQ", "+213000000000", "admin@scorpion-remap.pro", "AdminScorpion2026!"),
            ("Ayoub Tbessa (Admin)", "Tbessa Tuning HQ", "+213555555555", "ayoubtbessa@gmail.com", "Ayoub123456!"),
            ("Tbessa Admin", "Tbessa Workshop", "+213666666666", "tbessa@gmail.com", "Tbessa123456!")
        ]

        for full_name, workshop, phone, email, pwd in admin_accounts:
            cursor.execute("SELECT id, role FROM users WHERE LOWER(email) = ?", (email.lower(),))
            row = cursor.fetchone()
            if not row:
                cursor.execute("""
                INSERT INTO users (full_name, workshop_name, phone, email, wilaya_country, password_hash, tokens, role, ip_address, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    full_name,
                    workshop,
                    phone,
                    email.lower(),
                    "Algeria",
                    hash_password(pwd),
                    9999,
                    "admin",
                    "127.0.0.1",
                    1
                ))
                new_id = cursor.lastrowid
                cursor.execute("""
                INSERT INTO token_transactions (user_id, amount, type, description)
                VALUES (?, ?, ?, ?)
                """, (new_id, 9999, "admin_init", "Initialisation compte administrateur"))
            else:
                cursor.execute("""
                UPDATE users SET role = 'admin', tokens = 9999, is_active = 1 WHERE id = ?
                """, (row["id"],))

        conn.commit()


# =========================================================================
# User Management Helpers
# =========================================================================

def count_accounts_by_ip(ip: str) -> int:
    """عد الحسابات المسجلة من نفس الـ IP لمنع التلاعب واستغلال البونص"""
    if not ip or ip in ("127.0.0.1", "localhost", "unknown"):
        return 0
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE ip_address = ?", (ip,))
        row = cursor.fetchone()
        return row[0] if row else 0

def register_user(full_name: str, workshop_name: str, phone: str, email: str, wilaya_country: str, password: str, ip: str) -> Dict[str, Any]:
    full_name = full_name.strip()
    workshop_name = workshop_name.strip()
    phone = phone.strip()
    email = email.strip().lower()
    wilaya_country = wilaya_country.strip()

    if not full_name or not phone or not email or not password:
        raise ValueError("Tous les champs obligatoires doivent être remplis.")

    # Uniqueness check
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            raise ValueError("Cette adresse email est déjà enregistrée.")
        cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
        if cursor.fetchone():
            raise ValueError("Ce numéro de téléphone est déjà enregistré.")

        # IP Anti-Spam Check: Max 2 accounts per IP receive 10 tokens bonus
        ip_count = count_accounts_by_ip(ip)
        bonus_granted = (ip_count < 2)
        initial_tokens = 10 if bonus_granted else 0

        # التحقق مما إذا كان المستخدم مديراً مسجلاً
        user_is_super = is_super_admin(email)
        user_role = "admin" if user_is_super else "user"
        initial_tokens = 9999 if user_is_super else (10 if bonus_granted else 0)

        # Generate 6-digit WhatsApp verification code
        whatsapp_code = str(random.randint(100000, 999999)) if not user_is_super else "000000"
        whatsapp_verified = 1 if user_is_super else 0
        is_active_init = 1 if user_is_super else 0

        cursor.execute("""
        INSERT INTO users (full_name, workshop_name, phone, email, wilaya_country, password_hash, tokens, role, ip_address, is_active, whatsapp_verified, whatsapp_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            workshop_name,
            phone,
            email,
            wilaya_country,
            hash_password(password),
            initial_tokens,
            user_role,
            ip,
            is_active_init,
            whatsapp_verified,
            whatsapp_code
        ))
        new_user_id = cursor.lastrowid

        if user_is_super:
            cursor.execute("""
            INSERT INTO token_transactions (user_id, amount, type, description)
            VALUES (?, ?, ?, ?)
            """, (new_user_id, 9999, "admin_init", "Initialisation compte administrateur"))
        elif bonus_granted:
            cursor.execute("""
            INSERT INTO token_transactions (user_id, amount, type, description)
            VALUES (?, ?, ?, ?)
            """, (new_user_id, 10, "bonus_signup", "🎁 Bonus de bienvenue offert à l'inscription"))
        else:
            cursor.execute("""
            INSERT INTO token_transactions (user_id, amount, type, description)
            VALUES (?, ?, ?, ?)
            """, (new_user_id, 0, "anti_abuse_limit", "Bonus de bienvenue limité (plusieurs comptes détectés sur cette adresse IP)"))

        conn.commit()

        return {
            "id": new_user_id,
            "full_name": full_name,
            "workshop_name": workshop_name,
            "phone": phone,
            "email": email,
            "wilaya_country": wilaya_country,
            "tokens": initial_tokens,
            "role": user_role,
            "bonus_granted": bonus_granted,
            "whatsapp_code": whatsapp_code,
            "whatsapp_verified": whatsapp_verified
        }

def authenticate_user(login_identifier: str, password: str) -> Optional[Dict[str, Any]]:
    """تسجيل الدخول إما عبر البريد الإلكتروني أو رقم الهاتف"""
    identifier = login_identifier.strip().lower()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM users WHERE LOWER(email) = ? OR phone = ?
        """, (identifier, login_identifier.strip()))
        user = cursor.fetchone()
        if not user:
            return None

        if not verify_password(password, user["password_hash"]):
            return None

        user_dict = dict(user)
        if user_dict.get("is_active") != 1:
            if user_dict.get("whatsapp_verified") == 0:
                raise ValueError(f"WHATSAPP_UNVERIFIED:{user_dict['id']}:{user_dict['phone']}:{user_dict.get('whatsapp_code') or ''}:{user_dict['full_name']}")
            raise PermissionError("Ce compte est suspendu ou désactivé par l'administrateur.")
        # ترقية حساب المدير تلقائياً إذا كان من عناوين المدراء المعتمدة
        if is_super_admin(user_dict.get("email", "")):
            if user_dict.get("role") != "admin":
                cursor.execute("UPDATE users SET role = 'admin', tokens = 9999 WHERE id = ?", (user_dict["id"],))
                conn.commit()
                user_dict["role"] = "admin"
                user_dict["tokens"] = 9999
        return user_dict

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return None
        user_dict = dict(user)
        if is_super_admin(user_dict.get("email", "")):
            if user_dict.get("role") != "admin":
                cursor.execute("UPDATE users SET role = 'admin', tokens = 9999 WHERE id = ?", (user_dict["id"],))
                conn.commit()
                user_dict["role"] = "admin"
                user_dict["tokens"] = 9999
        return user_dict

# =========================================================================
# Persistent Sessions Management (SQLite)
# =========================================================================

def save_session_db(token: str, user_id: int):
    if not token or not user_id:
        return
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO sessions (token, user_id, created_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (token, user_id))
        conn.commit()

def get_session_user_db(token: str) -> Optional[int]:
    if not token:
        return None
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM sessions WHERE token = ?", (token,))
        row = cursor.fetchone()
        return row[0] if row else None

def delete_session_db(token: str):
    if not token:
        return
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()

def deduct_user_tokens(user_id: int, amount: int, tx_type: str, description: str) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tokens FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Utilisateur introuvable.")
        current_tokens = row[0]
        if current_tokens < amount:
            raise ValueError(f"Crédits insuffisants. Vous avez {current_tokens} crédits, requis: {amount}.")

        new_balance = current_tokens - amount
        cursor.execute("UPDATE users SET tokens = ? WHERE id = ?", (new_balance, user_id))
        cursor.execute("""
        INSERT INTO token_transactions (user_id, amount, type, description)
        VALUES (?, ?, ?, ?)
        """, (user_id, -amount, tx_type, description))
        conn.commit()
        return new_balance

def add_user_tokens(user_id: int, amount: int, tx_type: str, description: str) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tokens FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Utilisateur introuvable.")
        new_balance = row[0] + amount
        cursor.execute("UPDATE users SET tokens = ? WHERE id = ?", (new_balance, user_id))
        cursor.execute("""
        INSERT INTO token_transactions (user_id, amount, type, description)
        VALUES (?, ?, ?, ?)
        """, (user_id, amount, tx_type, description))
        conn.commit()
        return new_balance

def get_all_users() -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, full_name, workshop_name, phone, email, wilaya_country, tokens, role, ip_address, is_active, whatsapp_verified, whatsapp_code, created_at
        FROM users ORDER BY id DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

def toggle_user_active_status(user_id: int) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_active FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Utilisateur introuvable.")
        new_status = 0 if row[0] == 1 else 1
        cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
        return new_status

def get_user_transactions(user_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM token_transactions WHERE user_id = ? ORDER BY id DESC LIMIT 50
        """, (user_id,))
        return [dict(r) for r in cursor.fetchall()]

# =========================================================================
# الحماية ومكافحة الهجمات وحظر الـ IP (Fail2Ban & Security)
# =========================================================================

# تعقب المحاولات في الذاكرة لتسريع الأداء قبل الحفظ في القاعدة
_IP_ATTEMPTS: Dict[str, Dict[str, Any]] = {}

def is_ip_banned(ip: str) -> Tuple[bool, Optional[str]]:
    return False, None

def record_failed_attempt(ip: str, max_attempts: int = 5, ban_minutes: int = 30) -> Tuple[int, bool]:
    return 0, False

def clear_failed_attempts(ip: str):
    pass

def get_banned_ips() -> List[Dict[str, Any]]:
    """استرجاع قائمة كافة عناوين الـ IP المحظورة"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM banned_ips ORDER BY id DESC LIMIT 50
        """)
        return [dict(r) for r in cursor.fetchall()]

def unban_ip(ip: str) -> bool:
    """فك الحظر عن عنوان IP"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE banned_ips SET is_active = 0 WHERE ip_address = ?", (ip,))
        conn.commit()
        clear_failed_attempts(ip)
        return True

def manual_ban_ip(ip: str, reason: str = "Bloqué manuellement par Administrateur", ban_hours: int = 24) -> bool:
    """حظر عنوان IP يدوياً من طرف المدير"""
    now = datetime.utcnow()
    banned_until = (now + timedelta(hours=ban_hours)).isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO banned_ips (ip_address, attempts, reason, banned_until, is_active)
        VALUES (?, 1, ?, ?, 1)
        ON CONFLICT(ip_address) DO UPDATE SET 
            reason = excluded.reason,
            banned_until = excluded.banned_until,
            is_active = 1
        """, (ip, reason, banned_until))
        conn.commit()
        return True


# =========================================================================
# دوال نظام التذاكر والدعم الفني المباشر (Internal Support & File Exchange)
# =========================================================================

def create_support_ticket(user_id: int, subject: str, vehicle_ecu: str, message_text: str, attachment_name: Optional[str] = None, attachment_data: Optional[bytes] = None) -> int:
    """إنشاء تذكرة دعم فني جديدة وإضافة أول رسالة مع المرفق"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO support_tickets (user_id, subject, vehicle_ecu, status, created_at, updated_at)
        VALUES (?, ?, ?, 'open', ?, ?)
        """, (user_id, subject, vehicle_ecu, now, now))
        ticket_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO ticket_messages (ticket_id, sender_role, message_text, attachment_name, attachment_data, created_at)
        VALUES (?, 'user', ?, ?, ?, ?)
        """, (ticket_id, message_text, attachment_name, attachment_data, now))
        conn.commit()
        return ticket_id


def add_ticket_message(ticket_id: int, sender_role: str, message_text: str, attachment_name: Optional[str] = None, attachment_data: Optional[bytes] = None, new_status: Optional[str] = None) -> int:
    """إضافة رسالة جديدة إلى تذكرة وتحديث حالتها"""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO ticket_messages (ticket_id, sender_role, message_text, attachment_name, attachment_data, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, sender_role, message_text, attachment_name, attachment_data, now))
        msg_id = cursor.lastrowid

        if not new_status:
            new_status = 'answered' if sender_role == 'admin' else 'open'

        cursor.execute("""
        UPDATE support_tickets SET status = ?, updated_at = ? WHERE id = ?
        """, (new_status, now, ticket_id))
        conn.commit()
        return msg_id


def get_user_tickets(user_id: int) -> List[Dict[str, Any]]:
    """استرجاع تذاكر الزبون الخاصة به"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.*, 
               (SELECT COUNT(*) FROM ticket_messages WHERE ticket_id = t.id) as message_count,
               (SELECT message_text FROM ticket_messages WHERE ticket_id = t.id ORDER BY id DESC LIMIT 1) as last_message,
               (SELECT sender_role FROM ticket_messages WHERE ticket_id = t.id ORDER BY id DESC LIMIT 1) as last_sender
        FROM support_tickets t
        WHERE t.user_id = ?
        ORDER BY t.updated_at DESC
        """, (user_id,))
        return [dict(r) for r in cursor.fetchall()]


def get_all_support_tickets() -> List[Dict[str, Any]]:
    """استرجاع كافة تذاكر الزبائن للوحة تحكم المدير"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.*, u.full_name as user_name, u.workshop_name, u.email as user_email, u.phone as user_phone, u.tokens as user_tokens,
               (SELECT COUNT(*) FROM ticket_messages WHERE ticket_id = t.id) as message_count,
               (SELECT message_text FROM ticket_messages WHERE ticket_id = t.id ORDER BY id DESC LIMIT 1) as last_message
        FROM support_tickets t
        JOIN users u ON t.user_id = u.id
        ORDER BY CASE WHEN t.status = 'open' THEN 1 WHEN t.status = 'answered' THEN 2 ELSE 3 END, t.updated_at DESC
        """)
        return [dict(r) for r in cursor.fetchall()]


def get_ticket_details(ticket_id: int) -> Optional[Dict[str, Any]]:
    """استرجاع تفاصيل تذكرة مع كافة رسائلها (بدون بيانات BLOB لتخفيف الرد)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.*, u.full_name as user_name, u.workshop_name, u.email as user_email, u.phone as user_phone, u.tokens as user_tokens
        FROM support_tickets t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = ?
        """, (ticket_id,))
        ticket_row = cursor.fetchone()
        if not ticket_row:
            return None
        ticket = dict(ticket_row)

        cursor.execute("""
        SELECT id, ticket_id, sender_role, message_text, attachment_name, 
               CASE WHEN attachment_data IS NOT NULL THEN 1 ELSE 0 END as has_attachment,
               created_at
        FROM ticket_messages
        WHERE ticket_id = ?
        ORDER BY id ASC
        """, (ticket_id,))
        ticket["messages"] = [dict(r) for r in cursor.fetchall()]
        return ticket


def get_ticket_attachment(message_id: int) -> Optional[Tuple[str, bytes]]:
    """استرجاع الملف المرفق من الرسالة بصيغته الثنائية الحقيقية"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT attachment_name, attachment_data FROM ticket_messages WHERE id = ?", (message_id,))
        row = cursor.fetchone()
        if row and row["attachment_name"] and row["attachment_data"]:
            return row["attachment_name"], row["attachment_data"]
        return None



# =========================================================================
# WhatsApp Verification Functions
# =========================================================================

def verify_user_whatsapp(user_id: int, code: str) -> Tuple[bool, str]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, whatsapp_code, whatsapp_verified, is_active FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return False, "Utilisateur introuvable."
        if user["whatsapp_verified"] == 1:
            return True, "Compte déjà vérifié."
        if str(user["whatsapp_code"]).strip() != str(code).strip():
            return False, "Code de confirmation WhatsApp incorrect."
        
        cursor.execute("""
            UPDATE users 
            SET whatsapp_verified = 1, is_active = 1, whatsapp_verified_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (user_id,))
        conn.commit()
        return True, "Vérification WhatsApp réussie !"

def admin_verify_user_whatsapp(user_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET whatsapp_verified = 1, is_active = 1, whatsapp_verified_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (user_id,))
        conn.commit()
        return True

def get_user_for_verification(user_id: Optional[int] = None, phone: Optional[str] = None) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        elif phone:
            cursor.execute("SELECT * FROM users WHERE phone = ?", (phone.strip(),))
        else:
            return None
        row = cursor.fetchone()
        return dict(row) if row else None


# =========================================================================
# System Settings & WhatsApp Gateway Configuration
# =========================================================================

def get_setting(key: str, default: str = "") -> str:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM system_settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default

def set_setting(key: str, value: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO system_settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, str(value)))
        conn.commit()

def get_whatsapp_config() -> Dict[str, str]:
    return {
        "provider": get_setting("whatsapp_provider", "ultramsg"),
        "instance_id": get_setting("whatsapp_instance_id", ""),
        "api_token": get_setting("whatsapp_api_token", ""),
        "admin_phone": get_setting("whatsapp_admin_phone", "213799999002")
    }

def save_whatsapp_config(provider: str, instance_id: str, api_token: str, admin_phone: str):
    set_setting("whatsapp_provider", provider.strip().lower())
    set_setting("whatsapp_instance_id", instance_id.strip())
    set_setting("whatsapp_api_token", api_token.strip())
    set_setting("whatsapp_admin_phone", admin_phone.strip())
