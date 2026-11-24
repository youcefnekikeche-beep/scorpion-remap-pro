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

        # إنشاء حساب المدير الافتراضي (Default Admin Account)
        admin_email = "admin@scorpion-remap.pro"
        cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO users (full_name, workshop_name, phone, email, wilaya_country, password_hash, tokens, role, ip_address, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "Administrateur SCORPION",
                "SCORPION REMAP HQ",
                "+213000000000",
                admin_email,
                "Algeria",
                hash_password("AdminScorpion2026!"),
                9999,
                "admin",
                "127.0.0.1",
                1
            ))
            admin_id = cursor.lastrowid
            cursor.execute("""
            INSERT INTO token_transactions (user_id, amount, type, description)
            VALUES (?, ?, ?, ?)
            """, (admin_id, 9999, "admin_init", "Initialisation compte administrateur"))

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

        cursor.execute("""
        INSERT INTO users (full_name, workshop_name, phone, email, wilaya_country, password_hash, tokens, role, ip_address, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            workshop_name,
            phone,
            email,
            wilaya_country,
            hash_password(password),
            initial_tokens,
            "user",
            ip,
            1
        ))
        new_user_id = cursor.lastrowid

        if bonus_granted:
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
            "role": "user",
            "bonus_granted": bonus_granted
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

        if user["is_active"] != 1:
            raise PermissionError("Ce compte est suspendu ou désactivé par l'administrateur.")

        return dict(user)

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None

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
        SELECT id, full_name, workshop_name, phone, email, wilaya_country, tokens, role, ip_address, is_active, created_at
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
    """فحص ما إذا كان عنوان الـ IP محظوراً حالياً"""
    if not ip or ip in ("127.0.0.1", "localhost"):
        return False, None

    now = datetime.utcnow()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT banned_until, reason FROM banned_ips 
        WHERE ip_address = ? AND is_active = 1
        """, (ip,))
        row = cursor.fetchone()
        if row:
            try:
                until = datetime.fromisoformat(row["banned_until"])
                if now < until:
                    remaining_mins = int((until - now).total_seconds() / 60) + 1
                    return True, f"Adresse IP temporairement bloquée pour sécurité ({row['reason']}). Réessayez dans {remaining_mins} minute(s)."
                else:
                    # انتهت فترة الحظر
                    cursor.execute("UPDATE banned_ips SET is_active = 0 WHERE ip_address = ?", (ip,))
                    conn.commit()
            except Exception:
                pass
    return False, None

def record_failed_attempt(ip: str, max_attempts: int = 5, ban_minutes: int = 30) -> Tuple[int, bool]:
    """تسجيل محاولة دخول فاشلة، وحظر الـ IP تلقائياً عند تجاوز الحد الأقصى"""
    if not ip or ip in ("127.0.0.1", "localhost"):
        return 1, False

    now = datetime.utcnow()
    if ip not in _IP_ATTEMPTS:
        _IP_ATTEMPTS[ip] = {"count": 1, "first_attempt": now}
    else:
        # مسح العداد إذا مر أكثر من 15 دقيقة على أول محاولة فاشلة
        if (now - _IP_ATTEMPTS[ip]["first_attempt"]).total_seconds() > 900:
            _IP_ATTEMPTS[ip] = {"count": 1, "first_attempt": now}
        else:
            _IP_ATTEMPTS[ip]["count"] += 1

    attempts = _IP_ATTEMPTS[ip]["count"]
    if attempts >= max_attempts:
        banned_until = (now + timedelta(minutes=ban_minutes)).isoformat()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO banned_ips (ip_address, attempts, reason, banned_until, is_active)
            VALUES (?, ?, 'Multiples tentatives de connexion échouées (Protection Anti-Brute-Force)', ?, 1)
            ON CONFLICT(ip_address) DO UPDATE SET 
                attempts = attempts + 1,
                banned_until = excluded.banned_until,
                is_active = 1
            """, (ip, attempts, banned_until))
            conn.commit()
        # تصفير الذاكرة
        del _IP_ATTEMPTS[ip]
        return attempts, True

    return attempts, False

def clear_failed_attempts(ip: str):
    """مسح محاولات الـ IP عند تسجيل الدخول الناجح"""
    if ip in _IP_ATTEMPTS:
        del _IP_ATTEMPTS[ip]

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
