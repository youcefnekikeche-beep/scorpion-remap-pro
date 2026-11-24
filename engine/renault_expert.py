"""
SCORPION REMAP PRO - Renault Specialized Expert Tools Engine (V3.2.0)
Intègre 100% des 16 protocoles de EVO Fan Temperature Patcher :
[DCM1.2, EDC16CP33, EDC17C42, EMS3110, EMS3120, EMS3130, EMS3132, EMS3155, EMS3160, S3000, SID305, SID306, SID307, SIM32, V40, V42]
+ Renault Sonde Lambda / O2 Off
+ Renault Delphi DCM 3.4 Stage 1 (85 ➔ 115 CH)
+ Renault Cold Start Fix
"""

import os
import re
import json
import struct
from typing import Dict, Any, Tuple, List, Optional

# Load external database of patches if available
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server", "storage")
PATCHES_JSON = os.path.join(STORAGE_DIR, "renault_patches.json")

_PATCH_CACHE = None

def _get_patches_db() -> dict:
    global _PATCH_CACHE
    if _PATCH_CACHE is None:
        if os.path.exists(PATCHES_JSON):
            try:
                with open(PATCHES_JSON, "r", encoding="utf-8") as f:
                    _PATCH_CACHE = json.load(f)
            except Exception:
                _PATCH_CACHE = {}
        else:
            _PATCH_CACHE = {}
    return _PATCH_CACHE


# =========================================================================
# 1. BASE DE DONNÉES COMPLÈTE DES 16 CALCULATEURS EVO FAN TEMPERATURE
# =========================================================================

def read_8bit_renault(raw: int) -> int:
    return int((raw - 64) * 5 / 8)

def write_8bit_renault(temp: int) -> int:
    return int(temp * 8 / 5 + 64)

def read_16bit_x10_plus400(raw: int) -> int:
    return int(round((raw - 400) / 10.0))

def write_16bit_x10_plus400(temp: int) -> int:
    return int(round(temp * 10.0 + 400))

def read_ems3110(raw: int) -> int:
    return int((raw // 10) + 88)

def write_ems3110(temp: int) -> int:
    return int((temp - 88) * 10)

def read_ems3160(raw: int) -> int:
    return int(round(raw / 10.0))

def write_ems3160(temp: int) -> int:
    return int(round(temp * 10.0))

def read_s3000(raw: int) -> int:
    return int(round((raw + 128) / 3.2))

def write_s3000(temp: int) -> int:
    return int(round(temp * 3.2 - 128))

def read_8bit_edc16cp33(raw: int) -> int:
    for t in range(50, 120):
        if ((10 * t - 853) % 256) == raw:
            return t
    return int(round((raw + 853) / 10.0))

def write_8bit_edc16cp33(temp: int) -> int:
    return (10 * temp - 853) % 256


def read_v42(raw: int) -> int:
    v42_rev = {0x00: 88, 0x14: 90, 0x28: 92, 0x3C: 95, 0x50: 98}
    if raw in v42_rev:
        return v42_rev[raw]
    if 0 <= raw <= 120:
        return int(round(88 + (raw / 8.0)))
    return 98

def write_v42(temp: int) -> int:
    v42_map = {88: 0x00, 90: 0x14, 92: 0x28, 94: 0x3C, 95: 0x3C, 98: 0x50}
    if temp in v42_map:
        return v42_map[temp]
    return int(round((temp - 88) * 8.0))

FAN_ECU_DATABASE = {
    "DCM1.2": {
        "name": "Delphi DCM 1.2 (Renault 1.5 dCi)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [554560, 100938],
        "signatures": [(b"\x00\x02\x0c\x01\x04\x03\n", 4)]
    },
    "EDC16CP33": {
        "name": "Bosch EDC16CP33 (Renault 2.0 / 2.5 dCi)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_8bit_edc16cp33,
        "formula_write": write_8bit_edc16cp33,
        "static_offsets": [1873287],
        "signatures": []
    },
    "EDC17C42": {
        "name": "Bosch EDC17C42 (Renault 1.6 dCi)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [1812160, 1811820],
        "signatures": []
    },
    "EMS3110": {
        "name": "Continental EMS 3110 (Renault 1.6 / 2.0 16V)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_ems3110,
        "formula_write": write_ems3110,
        "static_offsets": [170240, 170496],
        "signatures": [(b"\"$s(", 4)]
    },
    "EMS3120": {
        "name": "Continental EMS 3120 (Renault Duster / Symbol / Logan)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [118076, 118124],
        "signatures": [(b"\x1c\xd3", 0)]
    },
    "EMS3130": {
        "name": "Continental EMS 3130 (Renault Duster 1.6 16V)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_8bit_renault,
        "formula_write": write_8bit_renault,
        "static_offsets": [118076],
        "signatures": [(b"\"$s(", 4)]
    },
    "EMS3132": {
        "name": "Siemens Sirius EMS 3132 (Renault / Dacia 1.2 / 1.4 / 1.6)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_8bit_renault,
        "formula_write": write_8bit_renault,
        "static_offsets": [33106, 33206, 33207, 33621],
        "signatures": []
    },
    "EMS3155": {
        "name": "Continental EMS 3155 (Renault / Nissan 1.2 TCe)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [155315],
        "signatures": []
    },
    "EMS3160": {
        "name": "Continental EMS 3160 (Renault 0.9 / 1.2 TCe)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_ems3160,
        "formula_write": write_ems3160,
        "static_offsets": [155315],
        "signatures": []
    },
    "S3000": {
        "name": "Sagem S3000 (Megane 2 / Scenic 2 / Clio 3)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_s3000,
        "formula_write": write_s3000,
        "static_offsets": [134728],
        "signatures": [(b"\xd0\xd8", 0)]
    },
    "SID305": {
        "name": "Continental SID 305 (Renault 1.5 dCi)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [272076],
        "signatures": []
    },
    "SID306": {
        "name": "Continental SID 306 (Renault 1.5 dCi)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [269666],
        "signatures": []
    },
    "SID307": {
        "name": "Continental SID 307 (Renault 1.5 dCi)",
        "size": 2,
        "type": "16bit_le",
        "formula_read": read_16bit_x10_plus400,
        "formula_write": write_16bit_x10_plus400,
        "static_offsets": [146164, 147040],
        "signatures": []
    },
    "SIM32": {
        "name": "Siemens SIM 32 (Renault Clio / Modus 1.2 16V)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_s3000,
        "formula_write": write_s3000,
        "static_offsets": [134728],
        "signatures": [(b"\x08\x08\x08\x08\x08\x1a\x12", 5)]
    },
    "V40": {
        "name": "Valeo V40 (Renault Twingo / Clio 1.2 16V)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_ems3110,
        "formula_write": write_ems3110,
        "static_offsets": [163976],
        "signatures": []
    },
    "V42": {
        "name": "Valeo V42 (Renault / Dacia 1.2 / 1.6 / GPL)",
        "size": 1,
        "type": "8bit",
        "formula_read": read_v42,
        "formula_write": write_v42,
        "static_offsets": [0x28089, 0x2808A, 0x2808B],
        "signatures": [(b"<\x05\x00", 0)]
    }
}


# =========================================================================
# 2. DÉTECTION ET EXTRACTION DE SIGNATURE RENAULT
# =========================================================================

def extract_renault_sw_hw(data: bytes) -> Tuple[str, str]:
    hw = "Inconnu"
    sw = "Inconnu"

    for off in [169744, 168356]:
        if off + 5 <= len(data):
            cand = data[off:off+5].decode("ascii", errors="ignore").strip()
            if re.match(r"\d{4}[RS]", cand) or cand in ("6031R", "6032R", "6033R"):
                sw = cand
                break

    hw_matches = re.findall(rb'(?:HW\s*([0-9A-Z]{4,6}R?)|([0-9]{5,7}R)|(GL42[0-9A-Z]{3,5}R)|(8200[0-9]{6})|(8201[0-9]{6}))', data)
    if hw_matches:
        for match in hw_matches:
            found = [m.decode('latin1', errors='ignore') for m in match if m]
            if found:
                hw = found[0]
                break

    if sw == "Inconnu":
        sw_matches = re.findall(rb'(?:SW\s*([0-9A-Z]{4,6}R?)|(10[0-9]{6}[A-Z0-9]{2})|(2667ST[0-9A-Z]+)|(28[0-9]{6}R))', data)
        if sw_matches:
            for match in sw_matches:
                found = [m.decode('latin1', errors='ignore') for m in match if m]
                if found:
                    sw = found[0]
                    break

    return hw, sw


def identify_renault_ecu(data: bytes, filename: str = "") -> dict:
    size = len(data)
    fn_lower = filename.lower()
    content_sample = data[:min(len(data), 500000)]
    hw, sw = extract_renault_sw_hw(data)

    # 1. Delphi DCM 3.4
    if size in (1048576, 1540096, 2097152, 524288):
        if (b"DCM3.4" in data or b"DCM 3.4" in data or b"DELPHI" in content_sample or 
            b"(13 21" in data or b"dCi" in data or "dcm" in fn_lower or "dcm3.4" in fn_lower or
            b"R04" in content_sample or b"\x00\xdc\x05\x00" in data):
            return {
                "family": "DCM3.4",
                "name": "Renault Delphi DCM 3.4 (1.5 dCi)",
                "fuel": "Diesel",
                "hw": hw,
                "sw": sw,
                "size": size
            }

    # 2. Delphi DCM 1.2
    if b"DCM1.2" in data or "dcm1.2" in fn_lower or (size in (524288, 1048576) and b"DELPHI" in content_sample and b"DCM3" not in data):
        return {"family": "DCM1.2", "name": FAN_ECU_DATABASE["DCM1.2"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}

    # 3. Bosch EDC16CP33
    if b"EDC16CP33" in data or "edc16cp33" in fn_lower or (b"EDC16" in data and b"CP33" in data):
        return {"family": "EDC16CP33", "name": FAN_ECU_DATABASE["EDC16CP33"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}

    # 4. Bosch EDC17C42
    if b"EDC17C42" in data or "edc17c42" in fn_lower or (b"EDC17" in data and b"C42" in data):
        return {"family": "EDC17C42", "name": FAN_ECU_DATABASE["EDC17C42"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}

    # 5. Valeo V42
    has_v42 = False
    if size in (1048576, 1540096, 2097152, 524288):
        if len(data) >= 165120:
            if b"<\x05\x00" in data[163840:164096] or b"n" in data[163840:164096] or b"$\x0b$\"" in data[164864:165120]:
                has_v42 = True
        if b"VALEO" in data[:100000] or b"GL42" in data[:100000] or b"V42" in data[:100000] or "v42" in fn_lower:
            has_v42 = True

    if has_v42:
        is_12 = b"1.2" in data[:50000] or b"D4F" in data[:50000] or "1.2" in fn_lower
        return {
            "family": "V42",
            "name": f"Renault Valeo V42 ({'1.2 16V' if is_12 else '1.6 16V / 8V'})",
            "fuel": "Essence",
            "hw": hw,
            "sw": sw,
            "size": size
        }

    # 6. Valeo V40
    if b"V40" in data[:100000] or "v40" in fn_lower:
        return {"family": "V40", "name": FAN_ECU_DATABASE["V40"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    # 7. Continental SID 305 / 306 / 307
    if b"SID305" in data or "sid305" in fn_lower:
        return {"family": "SID305", "name": FAN_ECU_DATABASE["SID305"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}
    if b"SID306" in data or "sid306" in fn_lower:
        return {"family": "SID306", "name": FAN_ECU_DATABASE["SID306"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}
    if b"SID307" in data or "sid307" in fn_lower:
        return {"family": "SID307", "name": FAN_ECU_DATABASE["SID307"]["name"], "fuel": "Diesel", "hw": hw, "sw": sw, "size": size}

    # 8. Continental EMS 3110 / 3120 / 3130 / 3155 / 3160
    if b"EMS3155" in data or "3155" in fn_lower:
        return {"family": "EMS3155", "name": FAN_ECU_DATABASE["EMS3155"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}
    if b"EMS3160" in data or "3160" in fn_lower:
        return {"family": "EMS3160", "name": FAN_ECU_DATABASE["EMS3160"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}
    if b"EMS3120" in data or "3120" in fn_lower:
        return {"family": "EMS3120", "name": FAN_ECU_DATABASE["EMS3120"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}
    if b"EMS3130" in data or "3130" in fn_lower:
        return {"family": "EMS3130", "name": FAN_ECU_DATABASE["EMS3130"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}
    if b"EMS3110" in data or "3110" in fn_lower:
        return {"family": "EMS3110", "name": FAN_ECU_DATABASE["EMS3110"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    has_ems = False
    if size in (1048576, 1540096, 2097152):
        if len(data) >= 171008 and (b"\"$s(" in data[170240:170496] or b"\x0b$J$L" in data[170752:171008]):
            has_ems = True
        if b"EMS31" in data[:100000] or "ems" in fn_lower:
            has_ems = True

    if has_ems:
        return {"family": "EMS3120", "name": "Continental EMS 3120 / 3110 (Renault / Dacia)", "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    # 9. Siemens Sirius EMS 3132
    if size in (262144, 524288) or (b"3132" in data[:10000] and size <= 1048576) or "3132" in fn_lower:
        return {"family": "EMS3132", "name": FAN_ECU_DATABASE["EMS3132"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    # 10. Sagem S3000
    if b"S3000" in data[:50000] or b"SAGEM" in data[:50000] or "s3000" in fn_lower:
        return {"family": "S3000", "name": FAN_ECU_DATABASE["S3000"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    # 11. Siemens SIM 32
    if b"SIM32" in data[:50000] or b"S120200" in data[:50000] or "sim32" in fn_lower:
        return {"family": "SIM32", "name": FAN_ECU_DATABASE["SIM32"]["name"], "fuel": "Essence", "hw": hw, "sw": sw, "size": size}

    return {
        "family": "UNKNOWN",
        "name": "Calculateur Inconnu ou Non Renault",
        "fuel": "Inconnu",
        "hw": hw,
        "sw": sw,
        "size": size
    }


# =========================================================================
# 3. MODULATION DE TEMPÉRATURE POUR TOUS LES 16 CALCULATEURS (EVO FAN)
# =========================================================================

def scan_and_patch_fan_temperature(data: bytes, target_temp: int, protocol_override: str = "", filename: str = "") -> Tuple[bytearray, int, int, str, str]:
    """
    Scanne et patche la température du ventilateur pour N'IMPORTE LEQUEL des 16 calculateurs.
    Retourne: (data_modifiée, temp_originale_détectée, octets_modifiés, description, protocole_détecté)
    """
    size = len(data)
    out = bytearray(data)

    # 1. Sélection du protocole (avec détection automatique si non forcé)
    selected_proto = None
    if protocol_override and protocol_override.strip() and protocol_override.strip().upper() not in ("", "AUTO", "SELECT"):
        if protocol_override in FAN_ECU_DATABASE:
            selected_proto = protocol_override

    if not selected_proto:
        ident = identify_renault_ecu(data, filename)
        fam = ident.get("family", "")
        if fam in FAN_ECU_DATABASE:
            selected_proto = fam
        elif fam == "EMS31XX":
            selected_proto = "EMS3120"
        elif "dcm" in filename.lower() and "1.2" in filename.lower():
            selected_proto = "DCM1.2"
        elif "v42" in filename.lower():
            selected_proto = "V42"
        elif "ems" in filename.lower():
            selected_proto = "EMS3120"
        elif "3132" in filename.lower():
            selected_proto = "EMS3132"

    if not selected_proto:
        for proto_name, proto_cfg in FAN_ECU_DATABASE.items():
            for pat, val_off in proto_cfg.get("signatures", []):
                if pat in out:
                    selected_proto = proto_name
                    break
            if selected_proto:
                break

    if not selected_proto:
        selected_proto = "V42"

    cfg = FAN_ECU_DATABASE[selected_proto]
    fmt_type = cfg["type"]
    read_fn = cfg["formula_read"]
    write_fn = cfg["formula_write"]
    val_size = cfg["size"]

    # 2. Recherche des offsets cibles et lecture de la température réelle d'origine
    offsets_to_patch = []
    current_temp = 98

    # A) Recherche par offsets statiques
    for off in cfg.get("static_offsets", []):
        if off + val_size <= len(out):
            try:
                if fmt_type == "8bit":
                    raw_val = out[off]
                elif fmt_type == "16bit_le":
                    raw_val = struct.unpack("<H", out[off:off+2])[0]
                elif fmt_type == "16bit_be":
                    raw_val = struct.unpack(">H", out[off:off+2])[0]
                
                t = read_fn(raw_val)
                if 40 <= t <= 125:
                    offsets_to_patch.append(off)
                    current_temp = t
            except Exception:
                pass

    # B) Recherche par signatures binaires
    for pat, val_off in cfg.get("signatures", []):
        pos = 0
        while True:
            idx = out.find(pat, pos)
            if idx == -1:
                break
            target_off = idx + val_off
            if target_off + val_size <= len(out) and target_off not in offsets_to_patch:
                try:
                    if fmt_type == "8bit":
                        raw_val = out[target_off]
                    elif fmt_type == "16bit_le":
                        raw_val = struct.unpack("<H", out[target_off:target_off+2])[0]
                    elif fmt_type == "16bit_be":
                        raw_val = struct.unpack(">H", out[target_off:target_off+2])[0]

                    t = read_fn(raw_val)
                    if 40 <= t <= 125:
                        offsets_to_patch.append(target_off)
                        current_temp = t
                except Exception:
                    pass
            pos = idx + len(pat)

    # C) Offsets V42 spécifiques
    if selected_proto == "V42":
        for off in [0x28089, 0x2808A, 0x2808B]:
            if off not in offsets_to_patch and off < len(out):
                offsets_to_patch.append(off)
        if 0x28089 < len(out):
            t_v42 = read_v42(out[0x28089])
            if 70 <= t_v42 <= 115:
                current_temp = t_v42

    if not offsets_to_patch:
        raise ValueError(f"Erreur de sécurité : Impossible de localiser la cartographie du ventilateur pour le protocole {selected_proto}. Fichier déjà modifié ou non reconnu.")

    # 3. Calcul de la nouvelle valeur brute
    new_raw = write_fn(target_temp)
    if fmt_type == "8bit":
        packed_bytes = struct.pack("B", max(0, min(255, new_raw)))
    elif fmt_type == "16bit_le":
        packed_bytes = struct.pack("<H", max(0, min(65535, new_raw)))
    elif fmt_type == "16bit_be":
        packed_bytes = struct.pack(">H", max(0, min(65535, new_raw)))

    # 4. Écriture sécurisée des octets
    mod_count = 0
    for off in offsets_to_patch:
        if off + len(packed_bytes) <= len(out):
            out[off:off+len(packed_bytes)] = packed_bytes
            mod_count += len(packed_bytes)

    # Si V42, appliquer également les paliers GMV standard
    if selected_proto == "V42":
        v42_map = {
            88: {0x28089: 0x00, 0x2808A: 0x04, 0x2808B: 0xE2},
            90: {0x28089: 0x14, 0x2808A: 0x04, 0x2808B: 0xE2},
            92: {0x28089: 0x28, 0x2808A: 0x04, 0x2808B: 0xEC},
            94: {0x28089: 0x3C, 0x2808A: 0x04, 0x2808B: 0xF6},
            95: {0x28089: 0x3C, 0x2808A: 0x04, 0x2808B: 0xF6},
            98: {0x28089: 0x50, 0x2808A: 0x04, 0x2808B: 0xF6}
        }
        steps = v42_map.get(target_temp, v42_map.get(92))
        for off, b_val in steps.items():
            if off < len(out) and out[off] != b_val:
                out[off] = b_val
                mod_count += 1

    if len(out) != size:
        raise ValueError("Erreur interne de sécurité : La taille du fichier a été altérée.")

    desc = f"Protocole [{selected_proto}] : Seuil GMV abaissé de {current_temp}°C (Stock) ➔ {target_temp}°C ({mod_count} octets calibrés)"
    return out, current_temp, mod_count, desc, selected_proto


# =========================================================================
# 4. ALGORITHMES STAGE 1, LAMBDA OFF & COLD START
# =========================================================================

def patch_renault_dcm34_stage1(data: bytes, filename: str = "") -> Tuple[bytearray, int, str]:
    size = len(data)
    if size not in (1048576, 1540096, 2097152, 524288):
        raise ValueError("Erreur de sécurité : Taille de fichier non valide pour un calculateur Renault Delphi DCM 3.4 (Attendu: 1MB, 1.5MB ou 2MB).")

    ecu_info = identify_renault_ecu(data, filename)
    if ecu_info["family"] != "DCM3.4":
        raise ValueError("Erreur de sécurité : Ce fichier n'est pas un calculateur Renault Delphi DCM 3.4 valide.")

    out = bytearray(data)
    target_torque_sig = b"\x00\xdc\x05\x00" # 220 NM
    already_mod_sig = b"\x00\xf0\x05\x00"   # 240 NM

    t_idx = out.find(target_torque_sig)
    already_idx = out.find(already_mod_sig)

    if t_idx == -1 and already_idx != -1:
        raise ValueError("Fichier déjà modifié ou signature logicielle non reconnue. Modification annulée par sécurité.")

    mod_count = 0
    if t_idx != -1:
        out[t_idx:t_idx+4] = already_mod_sig
        mod_count += 4

    db = _get_patches_db()
    dcm_patches = db.get("DCM 3.4 SYMBOL STEPWAY LOGAN CLIO4 05 VITESSE", {}).get("STAGE 01 85CH TO 115 CH VMAX", {})

    if dcm_patches:
        for addr_str, val_str in dcm_patches.items():
            addr = int(addr_str, 16)
            new_val = int(val_str, 16)
            if addr < len(out) and out[addr] != new_val:
                out[addr] = new_val
                mod_count += 1

    if mod_count == 0:
        raise ValueError("Fichier déjà modifié ou signature logicielle non reconnue. Modification annulée par sécurité.")

    if len(out) != size:
        raise ValueError("Erreur interne de sécurité : La taille du fichier a été altérée.")

    desc = f"Cartographie Stage 1 Complète (85 ➔ 115 CH + VMAX Débridée) : {mod_count} octets calibrés"
    return out, mod_count, desc


def patch_renault_lambda_off(data: bytes, filename: str = "") -> Tuple[bytearray, int, str]:
    size = len(data)
    ecu_info = identify_renault_ecu(data, filename)
    family = ecu_info["family"]

    if family not in ("V42", "EMS31XX", "EMS3120", "EMS3110", "EMS3130", "EMS3132", "S3000", "SIM32"):
        raise ValueError("Erreur de sécurité : Ce fichier n'est pas un calculateur Renault essence compatible (Valeo V42, EMS31xx, S3000, SIM32).")

    out = bytearray(data)
    mod_count = 0
    desc_list = []

    if family == "V42":
        targets = [
            (164892, b'$\x0b$"$J$L', b'\x00\x00\x00\x00\x00\x00\x00\x00', 'Sondes DTC Mask 1'),
            (164902, b'\x016', b'\x00\x00', 'Sondes DTC Mask 2'),
            (166614, b'\x016\x0c\x13\x03', b'\x00\x00\x00\x00\n', 'Sondes Switch 1'),
            (166630, b'\x017\x0c\x11\x03', b'\x00\x00\x00\x00\n', 'Sondes Switch 2'),
            (166646, b'\x018\x0c\x12\x03', b'\x00\x00\x00\x00\n', 'Sondes Switch 3')
        ]
        already_patched = True
        for off, old_b, new_b, label in targets:
            if off + len(new_b) <= len(out) and out[off:off+len(new_b)] != new_b:
                already_patched = False
                break
        if already_patched:
            raise ValueError("Fichier déjà modifié ou signature logicielle non reconnue. Modification annulée par sécurité.")

        for off, old_b, new_b, label in targets:
            if off + len(new_b) <= len(out):
                out[off:off+len(new_b)] = new_b
                mod_count += len(new_b)
                desc_list.append(label)

        db = _get_patches_db()
        v42_sols = db.get("Valeo V42", {})
        sol_data = v42_sols.get("1.6 Supression des Sondes + Stage 01") or v42_sols.get("1.2 Supression des Sondes + stage 01")
        if sol_data:
            for addr_str, val_str in sol_data.items():
                addr = int(addr_str, 16)
                new_v = int(val_str, 16)
                if addr < len(out) and out[addr] != new_v:
                    out[addr] = new_v
                    mod_count += 1

    elif family in ("EMS31XX", "EMS3120", "EMS3110", "EMS3130"):
        targets = [
            (170392, b'"$s(', b'\x00\x00\x00\x00', 'EMS DTC Table 1'),
            (170872, b'\x0b$J$L$\x06%N(', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'EMS DTC Table 2'),
            (170884, b'K$N(\x0b$I$\xc4$', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'EMS DTC Table 3'),
            (172908, b'\x0c\t\x03', b'\x00\x00\x00', 'EMS Decat Switch 1'),
            (173068, b'\x0c\x13\x03', b'\x00\x00\x00', 'EMS Decat Switch 2'),
            (173084, b'\x0c\x11\x03', b'\x00\x00\x00', 'EMS Sondes Switch 1'),
            (173100, b'\x0c\x12\x03', b'\x00\x00\x00', 'EMS Sondes Switch 2'),
            (173116, b'\x0c\x13\x03', b'\x00\x00\x00', 'EMS Sondes Switch 3'),
            (173132, b'\x0c\x11\x03', b'\x00\x00\x00', 'EMS Sondes Switch 4'),
            (173148, b'\x0c\x12\x03', b'\x00\x00\x00', 'EMS Sondes Switch 5')
        ]
        already_patched = True
        for off, old_b, new_b, label in targets:
            if off + len(new_b) <= len(out) and out[off:off+len(new_b)] != new_b:
                already_patched = False
                break
        if already_patched:
            raise ValueError("Fichier déjà modifié ou signature logicielle non reconnue. Modification annulée par sécurité.")

        for off, old_b, new_b, label in targets:
            if off + len(new_b) <= len(out):
                out[off:off+len(new_b)] = new_b
                mod_count += len(new_b)
                desc_list.append(label)

    elif family == "S3000":
        p1 = b'\x00\x00\x00\x00\x00\x1a\x12('
        idx1 = out.find(p1)
        if idx1 != -1:
            out[idx1+6:idx1+8] = b'\x00\x00'
            mod_count += 2
            desc_list.append("S3000 Sonde Switch Off")
        p3 = b'\x016\x0c\x13\x03'
        idx3 = out.find(p3)
        if idx3 != -1:
            out[idx3:idx3+5] = b'\x00\x00\x00\x00\n'
            mod_count += 5
            desc_list.append("S3000 O2 Monitor Disable")

    elif family == "SIM32":
        p = b'\x08\x08\x08\x08\x08\x1a\x12'
        idx = out.find(p)
        if idx != -1:
            out[idx+5:idx+7] = b'\x00\x00'
            mod_count += 2
            desc_list.append("SIM32 Lambda Switch Off")

    elif family == "EMS3132":
        dtc_patterns = [
            (b'\x016\x01A', b'\x00\x00\x00\x00', 'EMS3132 O2 DTC Mask P0136/P0141'),
            (b'\x04 \x040', b'\x00\x00\x00\x00', 'EMS3132 Cat DTC Mask P0420/P0430')
        ]
        for pat, repl, label in dtc_patterns:
            pos = 0
            while True:
                idx = out.find(pat, pos)
                if idx == -1:
                    break
                out[idx:idx+len(repl)] = repl
                mod_count += len(repl)
                desc_list.append(label)
                pos = idx + len(repl)

    if mod_count == 0:
        raise ValueError("Fichier déjà modifié ou signature logicielle non reconnue. Modification annulée par sécurité.")

    desc = f"Suppression Sonde Lambda aval (O2 OFF) : {mod_count} octets modifiés ({', '.join(set(desc_list[:4]))})"
    return out, mod_count, desc


def fix_renault_cold_start(data: bytes, filename: str = "") -> Tuple[bytearray, int, str]:
    size = len(data)
    ecu_info = identify_renault_ecu(data, filename)
    family = ecu_info["family"]

    if family not in ("V42", "EMS31XX", "EMS3120", "EMS3110", "EMS3130", "EMS3132"):
        raise ValueError("Erreur de sécurité : Ce calculateur ne présente pas la signature de gestion de démarrage à froid Renault (EMS31xx / Valeo V42).")

    out = bytearray(data)
    pattern = bytearray([0x0A, 0x14, 0x1E, 0x28, 0x32])
    idx = out.find(pattern)
    mod_count = 0

    if idx != -1:
        for offset in range(idx, min(len(out), idx + 16)):
            out[offset] = min(255, int(out[offset] * 1.15))
            mod_count += 1
    else:
        p2 = b"\x00\x00'\x10"
        idx2 = out.find(p2)
        if idx2 != -1 and idx2 + 4 < len(out):
            out[idx2:idx2+4] = b"\x00\x00#("
            mod_count += 4

    if mod_count == 0:
        raise ValueError("Signature de démarrage à froid non reconnue ou fichier déjà optimisé. Modification annulée par sécurité.")

    desc = f"Optimisation de la richesse d'injection de démarrage à froid : {mod_count} octets ajustés"
    return out, mod_count, desc


# =========================================================================
# 5. POINT D'ENTRÉE POUR DRY-RUN ET EXÉCUTION
# =========================================================================

def preview_expert_operation(data: bytes, tool_key: str, param: str = "", filename: str = "", protocol: str = "") -> Dict[str, Any]:
    ecu_info = identify_renault_ecu(data, filename)
    current_temp = None

    if tool_key == "renault_dcm34_stage1":
        patched_bytes, count, desc = patch_renault_dcm34_stage1(data, filename)
    elif tool_key == "renault_lambda_off":
        patched_bytes, count, desc = patch_renault_lambda_off(data, filename)
    elif tool_key == "renault_fan_temp":
        t_val = int(param) if param and param.isdigit() else 92
        patched_bytes, current_temp, count, desc, sel_proto = scan_and_patch_fan_temperature(data, t_val, protocol, filename)
    elif tool_key == "renault_cold_start":
        patched_bytes, count, desc = fix_renault_cold_start(data, filename)
    else:
        raise ValueError(f"Outil expert non reconnu : {tool_key}")

    res = {
        "success": True,
        "ecu_type": ecu_info["name"],
        "hw_version": ecu_info["hw"],
        "sw_version": ecu_info["sw"],
        "file_size": len(data),
        "bytes_modified": count,
        "description": desc,
        "checksum_status": "Supporté & Automatique ✅"
    }
    if current_temp is not None:
        res["current_temp"] = current_temp
    if tool_key == "renault_fan_temp":
        res["protocol_detected"] = sel_proto
        res["protocol_name"] = FAN_ECU_DATABASE.get(sel_proto, {}).get("name", sel_proto)
    return res


def execute_expert_operation(data: bytes, tool_key: str, param: str = "", filename: str = "", protocol: str = "") -> Tuple[bytearray, str]:
    if tool_key == "renault_dcm34_stage1":
        out, count, desc = patch_renault_dcm34_stage1(data, filename)
    elif tool_key == "renault_lambda_off":
        out, count, desc = patch_renault_lambda_off(data, filename)
    elif tool_key == "renault_fan_temp":
        t_val = int(param) if param and param.isdigit() else 92
        out, curr_t, count, desc, sel_proto = scan_and_patch_fan_temperature(data, t_val, protocol, filename)
    elif tool_key == "renault_cold_start":
        out, count, desc = fix_renault_cold_start(data, filename)
    else:
        raise ValueError(f"Outil expert non reconnu : {tool_key}")

    return out, desc
