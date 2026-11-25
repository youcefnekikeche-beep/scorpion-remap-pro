import urllib.request
import urllib.parse
import json
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("whatsapp_service")

def clean_phone_number(phone: str) -> str:
    """Normalize phone number to international format without + or spaces (e.g. 213555123456)"""
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("0") and len(digits) == 10:
        # Algerian local format: 0555123456 -> 213555123456
        digits = "213" + digits[1:]
    elif digits.startswith("00"):
        digits = digits[2:]
    return digits

def send_real_whatsapp_otp(phone: str, code: str, client_name: str, config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Sends a real WhatsApp OTP verification message using the configured gateway API.
    Supported providers:
      1. ultramsg: https://api.ultramsg.com
      2. green_api: https://api.green-api.com
      3. twilio: Twilio WhatsApp REST API
      4. meta: Meta Cloud API
    """
    clean_phone = clean_phone_number(phone)
    if not clean_phone:
        return False, "Numéro de téléphone invalide."

    provider = config.get("provider", "ultramsg").lower()
    instance_id = config.get("instance_id", "").strip()
    api_token = config.get("api_token", "").strip()

    message = (
        f"🦂 *SCORPION REMAP PRO*\n\n"
        f"Bonjour *{client_name}*,\n"
        f"Votre code de confirmation WhatsApp est :\n\n"
        f"🔑 *{code}*\n\n"
        f"Entrez ce code sur le site pour activer votre compte et débloquer vos 10 Crédits offerts.\n"
        f"Ne partagez ce code avec personne."
    )

    if not api_token or not instance_id:
        logger.warning("WhatsApp API Gateway not configured yet. Set instance_id and api_token in admin settings.")
        return False, "Passerelle WhatsApp non configurée. Veuillez renseigner l'Instance ID et Token dans le panneau d'administration."

    try:
        if provider == "ultramsg":
            url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
            payload = {
                "token": api_token,
                "to": clean_phone,
                "body": message
            }
            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                if res_data.get("sent") == "true" or "id" in res_data:
                    return True, "Message WhatsApp envoyé avec succès !"
                else:
                    return False, f"Erreur UltraMsg: {res_data.get('message', res_data)}"

        elif provider == "green_api":
            url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{api_token}"
            payload = {
                "chatId": f"{clean_phone}@c.us",
                "message": message
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                if "idMessage" in res_data:
                    return True, "Message WhatsApp envoyé avec succès via Green-API !"
                else:
                    return False, f"Erreur Green-API: {res_data}"

        else:
            return False, f"Fournisseur WhatsApp '{provider}' non supporté."

    except Exception as e:
        logger.error(f"WhatsApp send error: {e}")
        return False, f"Erreur d'envoi WhatsApp: {str(e)}"
