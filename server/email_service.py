import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, Tuple

logger = logging.getLogger("email_service")

def send_verification_email(to_email: str, code: str, client_name: str, config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Sends a real, professional HTML verification email with the 6-digit OTP code.
    Uses standard SMTP (Gmail, Brevo, Sendgrid, Zoho, cPanel, etc.).
    """
    to_email = to_email.strip().lower()
    if not to_email or "@" not in to_email:
        return False, "Adresse email invalide."

    smtp_host = config.get("smtp_host", "").strip() or os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(config.get("smtp_port", 0) or os.environ.get("SMTP_PORT", 587))
    smtp_user = config.get("smtp_user", "").strip() or os.environ.get("SMTP_USER", "")
    smtp_password = config.get("smtp_password", "").strip() or os.environ.get("SMTP_PASSWORD", "")
    from_email = config.get("smtp_from_email", "").strip() or os.environ.get("SMTP_FROM_EMAIL", smtp_user or "noreply@scorpion-remap.pro")
    from_name = config.get("smtp_from_name", "").strip() or "SCORPION REMAP PRO"

    # Always log the verification code for server auditing & admin reference
    print(f"[EMAIL OTP] Code for {to_email} ({client_name}): {code}")

    if not smtp_user or not smtp_password:
        logger.warning(f"SMTP not configured. Generated code {code} for {to_email}")
        return False, "Le serveur SMTP n'est pas encore configuré dans le panneau d'administration."

    subject = f"🔑 Code de confirmation : {code} — SCORPION REMAP PRO"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #050811;
                color: #e2e8f0;
                margin: 0;
                padding: 30px 10px;
            }}
            .card {{
                max-width: 560px;
                margin: 0 auto;
                background: linear-gradient(145deg, #0f172a 0%, #1e111a 100%);
                border: 1px solid rgba(225, 29, 72, 0.4);
                border-radius: 18px;
                padding: 36px 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.8);
                text-align: center;
            }}
            .logo {{
                font-size: 38px;
                margin-bottom: 8px;
            }}
            h1 {{
                font-size: 22px;
                color: #ffffff;
                margin: 0 0 16px 0;
                font-weight: 800;
                letter-spacing: 0.5px;
            }}
            p {{
                font-size: 14px;
                color: #94a3b8;
                line-height: 1.6;
                margin: 10px 0;
            }}
            .otp-box {{
                margin: 28px auto;
                padding: 16px 28px;
                background: #020617;
                border: 2px dashed #e11d48;
                border-radius: 14px;
                display: inline-block;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: 900;
                color: #38bdf8;
                letter-spacing: 8px;
                font-family: 'Courier New', Courier, monospace;
            }}
            .bonus-badge {{
                display: inline-block;
                background: rgba(16, 185, 129, 0.15);
                color: #34d399;
                border: 1px solid #10b981;
                font-size: 13px;
                font-weight: 700;
                padding: 6px 14px;
                border-radius: 20px;
                margin-top: 15px;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #1e293b;
                font-size: 12px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="logo">🦂</div>
            <h1>SCORPION REMAP PRO</h1>
            <p>Bonjour <strong>{client_name}</strong>,</p>
            <p>Merci pour votre inscription. Voici votre code secret de vérification d'adresse email :</p>
            
            <div class="otp-box">
                <div class="otp-code">{code}</div>
            </div>

            <div>
                <span class="bonus-badge">🎁 +10 Crédits offerts à l'activation</span>
            </div>

            <p style="margin-top: 22px; font-size: 13px;">
                Saisissez ce code dans la fenêtre d'activation pour accéder immédiatement à votre espace atelier et à vos solutions ECU.
            </p>

            <div class="footer">
                Ce code est personnel et confidentiel. Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email.<br>
                &copy; 2026 SCORPION REMAP PRO — Tous droits réservés.
            </div>
        </div>
    </body>
    </html>
    """

    text_content = (
        f"SCORPION REMAP PRO\n\n"
        f"Bonjour {client_name},\n"
        f"Votre code de confirmation email est : {code}\n\n"
        f"Entrez ce code sur le site pour activer votre compte et débloquer vos 10 Crédits offerts.\n\n"
        f"Ne partagez ce code avec personne."
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=12) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())

        logger.info(f"Verification email successfully sent to {to_email}")
        return True, "Email de confirmation envoyé avec succès !"

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Auth error: {e}")
        return False, f"Erreur d'authentification SMTP : vérifiez l'utilisateur et le mot de passe d'application. ({e})"
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False, f"Erreur d'envoi de l'email : {str(e)}"
