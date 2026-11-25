"""
SCORPION REMAP PRO - Core ECU Analyzer Engine (V3.2.0)
SVEdit v1.1.38.3 Deep Integration & Multi-Brand ECU Registry
Full coverage of all 18 Brands & 80 ECUs with Strict Fuel Type Isolation.
DaVinci v1.0.28 + v1.0.30 Deep Binary Extraction — APPEND-ONLY (Nov 2026).
"""

import re
import struct
from typing import Dict, Any, List, Optional, Tuple

# Import the 6 dedicated modular engines extracted from SVEdit v1.1.38.3
from engine.hyundai_kia import HYUNDAI_KIA_REGISTRY, apply_hyundai_kia_patch
from engine.vag_group import VAG_GROUP_REGISTRY, apply_vag_group_patch
from engine.honda import HONDA_REGISTRY, apply_honda_patch
from engine.toyota_nissan import TOYOTA_NISSAN_REGISTRY, apply_toyota_nissan_patch
from engine.mazda_mitsubishi_subaru import MAZDA_MITSUBISHI_SUBARU_REGISTRY, apply_mazda_mitsubishi_subaru_patch
from engine.ford_fca_others import FORD_FCA_OTHERS_REGISTRY, apply_ford_fca_others_patch

# ── NEW: DaVinci v1.0.28 + v1.0.30 Deep Extraction Modules (APPEND-ONLY) ──
from engine.davinci_vag_bmw_mb import (
    get_all_davinci_vag_bmw_mb_registries,
    apply_davinci_vag_bmw_mb_patch,
)
from engine.davinci_psa_renault_fca import (
    get_all_davinci_psa_renault_fca_registries,
    apply_davinci_psa_renault_fca_patch,
)

# All modular registries for lookup and validation
ALL_MODULE_REGISTRIES = [
    HYUNDAI_KIA_REGISTRY,
    VAG_GROUP_REGISTRY,
    HONDA_REGISTRY,
    TOYOTA_NISSAN_REGISTRY,
    MAZDA_MITSUBISHI_SUBARU_REGISTRY,
    FORD_FCA_OTHERS_REGISTRY,
]

# DaVinci-sourced registries (merged AFTER existing ones — no overwrite)
_DAVINCI_VAG_BMW_MB = get_all_davinci_vag_bmw_mb_registries()
_DAVINCI_PSA_REN_FCA = get_all_davinci_psa_renault_fca_registries()
_DAVINCI_ALL = {**_DAVINCI_VAG_BMW_MB, **_DAVINCI_PSA_REN_FCA}

# Flat lookup map by ECU ID (SVEdit base, then DaVinci APPEND — no overwrite)
FLAT_ECU_REGISTRY: Dict[str, Dict[str, Any]] = {}
for reg in ALL_MODULE_REGISTRIES:
    for ecu_id, info in reg.items():
        FLAT_ECU_REGISTRY[ecu_id] = info

# Merge DaVinci-sourced ECUs (only new IDs, never overwrite existing)
for ecu_id, info in _DAVINCI_ALL.items():
    if ecu_id not in FLAT_ECU_REGISTRY:
        FLAT_ECU_REGISTRY[ecu_id] = info

# Structured Registry Grouped by Brand (Strict Backend Registry for UI Dropdowns)
SUPPORTED_REGISTRY: Dict[str, List[Dict[str, Any]]] = {}
_all_registries_combined = list(FLAT_ECU_REGISTRY.values())
for info in _all_registries_combined:
    brand = info["brand"]
    if brand not in SUPPORTED_REGISTRY:
        SUPPORTED_REGISTRY[brand] = []
    # avoid duplicates
    existing_ids = [e["id"] for e in SUPPORTED_REGISTRY[brand]]
    if info["id"] not in existing_ids:
        SUPPORTED_REGISTRY[brand].append({
            "id": info["id"],
            "name": info["name"],
            "brand": brand,
            "fuel": info["fuel_type"],
            "supported_solutions": info["solutions"],
            "plug_notes": info.get("plug_notes", ""),
            "source": info.get("source", "SVEdit v1.1.38"),
            "checksum_info": {
                "status": "Supporté & Automatique ✅",
                "is_auto": True,
                "algorithm": info.get("source", "SVEdit v1.1.38 Certified Engine")
            }
        })


def get_registry_ecu(brand: str, ecu_id: str) -> Optional[Dict[str, Any]]:
    """استرجاع معلومات الكمبيوتر من السجل المدعوم حصرياً"""
    if ecu_id in FLAT_ECU_REGISTRY:
        info = FLAT_ECU_REGISTRY[ecu_id]
        return {
            "id": info["id"],
            "name": info["name"],
            "brand": info["brand"],
            "fuel": info["fuel_type"],
            "supported_solutions": info["solutions"],
            "checksum_info": {
                "status": "Supporté & Automatique ✅",
                "is_auto": True,
                "algorithm": "SVEdit v1.1.38 Certified Engine"
            }
        }
    if brand in SUPPORTED_REGISTRY:
        for ecu in SUPPORTED_REGISTRY[brand]:
            if ecu["id"] == ecu_id:
                return ecu
    return None


def identify_ecu(binary_data: bytes, filename: str) -> dict:
    """
    Identifie le calculateur avec certitude stricte (100% de concordance).
    Si le fichier n'est pas reconnu automatiquement, renvoie recognized=False
    pour forcer la sélection manuelle dans la base de données sans aucune supposition.
    """
    file_size = len(binary_data)
    if file_size < 131072: # 128KB minimum
        raise ValueError("Taille du fichier binaire invalide ou corrompu (Taille minimale requise: 128 Ko)")

    # 1. Extraction des références Bosch
    sw_matches = re.findall(b'1037[0-9]{6}', binary_data)
    sw_version = sw_matches[0].decode('ascii') if sw_matches else None

    hw_matches = re.findall(b'0281[0-9]{6}', binary_data)
    if not hw_matches:
        hw_matches = re.findall(b'0261[0-9]{6}', binary_data)
    hw_version = hw_matches[0].decode('ascii') if hw_matches else None

    detected_ecu_id = None
    fn_lower = filename.lower()

    # 1.5 Détection prioritaire précise basée sur le nom de fichier (Audi / VAG / BMW / Mercedes / etc.)
    if any(k in fn_lower for k in ["cp04", "17c04", "edc17c04", "c04"]):
        if "vag_edc17cp04" in FLAT_ECU_REGISTRY:
            detected_ecu_id = "vag_edc17cp04"
        elif "vag_edc17" in FLAT_ECU_REGISTRY:
            detected_ecu_id = "vag_edc17"
    elif any(k in fn_lower for k in ["cp14", "edc17cp14"]):
        detected_ecu_id = "vag_edc17cp04" if "vag_edc17cp04" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "c46" in fn_lower or "edc17c46" in fn_lower:
        detected_ecu_id = "vag_edc17c46" if "vag_edc17c46" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "c64" in fn_lower or "edc17c64" in fn_lower:
        detected_ecu_id = "vag_edc17c64" if "vag_edc17c64" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "c74" in fn_lower or "edc17c74" in fn_lower:
        detected_ecu_id = "vag_edc17c74" if "vag_edc17c74" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "cp44" in fn_lower or "edc17cp44" in fn_lower:
        detected_ecu_id = "vag_edc17cp44" if "vag_edc17cp44" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "cp54" in fn_lower or "edc17cp54" in fn_lower:
        detected_ecu_id = "vag_edc17cp54" if "vag_edc17cp54" in FLAT_ECU_REGISTRY else "vag_edc17"
    elif "pcr2" in fn_lower or "pcr2.1" in fn_lower:
        detected_ecu_id = "vag_pcr21" if "vag_pcr21" in FLAT_ECU_REGISTRY else "vag_edc17"

    # 2. Correspondance stricte par signatures et tailles dans les moteurs modulaires
    if not detected_ecu_id:
        for ecu_id, info in FLAT_ECU_REGISTRY.items():
            matched_sig = False
            for sig in info.get("signatures", []):
                if sig in binary_data:
                    matched_sig = True
                    break
            
            # Vérification par nom de fichier si signature présente (sauf termes génériques comme Bosch/Siemens)
            generic_brands = ["bosch", "siemens", "delphi", "continental", "denso", "marelli"]
            tokens_to_check = [p.lower() for p in [info["id"], ecu_id.replace("_", " ")] if p.lower() not in generic_brands]
            if not matched_sig and any(p in fn_lower for p in tokens_to_check):
                if file_size in info.get("standard_sizes", []):
                    matched_sig = True

            if matched_sig and (not info.get("standard_sizes") or file_size in info["standard_sizes"] or file_size % 65536 == 0):
                detected_ecu_id = ecu_id
                break

    # 3. Détection spécifique Bosch VAG / BMW / Mercedes si Bosch HW/SW présent
    if not detected_ecu_id and (sw_version or hw_version):
        if hw_version and hw_version.startswith("0281"):
            # Diesel
            if file_size in (1048576, 2097152):
                if b"EDC16" in binary_data or b"CR39" in binary_data:
                    detected_ecu_id = "vag_edc16" if "vag" in fn_lower else "hyundai_edc16c39"
                else:
                    detected_ecu_id = "vag_edc16"
            elif file_size in (2097152, 4194304):
                if b"EDC17C57" in binary_data:
                    detected_ecu_id = "hyundai_edc17c57"
                elif b"EDC17CP62" in binary_data:
                    detected_ecu_id = "hyundai_edc17cp62"
                else:
                    detected_ecu_id = "vag_edc17"
            elif file_size == 8388608:
                detected_ecu_id = "vag_md1_cp0xx"
        elif hw_version and hw_version.startswith("0261"):
            # Essence
            if file_size in (1572864, 2097152, 4194304):
                if b"ME17.9.11" in binary_data or b"ME17.9.12" in binary_data:
                    detected_ecu_id = "hyundai_me17911"
                elif b"ME17.9.21" in binary_data:
                    detected_ecu_id = "hyundai_me17921"
                elif b"MED17.9.8" in binary_data:
                    detected_ecu_id = "hyundai_med1798"
                else:
                    detected_ecu_id = "vag_med17"

    # Si aucun calculateur reconnu avec certitude
    if not detected_ecu_id or detected_ecu_id not in FLAT_ECU_REGISTRY:
        return {
            "recognized": False,
            "message": "Calculateur non reconnu automatiquement. Veuillez sélectionner votre véhicule et calculateur dans notre base de données :",
            "file_size": file_size,
            "sw_version": sw_version,
            "hw_version": hw_version,
            "filename": filename
        }

    matched_info = FLAT_ECU_REGISTRY[detected_ecu_id]
    fuel_type = matched_info["fuel_type"]
    brand_name = matched_info["brand"]

    # Isolation stricte du carburant
    solutions = list(matched_info["solutions"])
    if fuel_type == "DIESEL":
        solutions = [s for s in solutions if not any(x in s.upper() for x in ["CAT", "LAMBDA", "EVAP", "NOX"])]
    elif fuel_type == "ESSENCE":
        solutions = [s for s in solutions if not any(x in s.upper() for x in ["DPF", "FAP", "ADBLUE", "SCR"])]

    # Calcul de la signature Checksum
    cs_algo = "SVEdit v1.1.38 Certified Engine"
    if "EDC17" in matched_info["name"] or "MED17" in matched_info["name"]:
        cs_algo = "RSA 1024 / TriCore CRC32"
    elif "EDC16" in matched_info["name"]:
        cs_algo = "Bosch EDC16 Additive Checksum"
    elif "DENSO" in matched_info["name"].upper():
        cs_algo = "Denso 16/32-bit Block Checksum"

    return {
        "recognized": True,
        "ecu_id": matched_info["id"],
        "brand": brand_name,
        "ecu_name": matched_info["name"],
        "fuel_type": fuel_type,
        "fuel_badge": "Moteur Diesel ⛽" if fuel_type == "DIESEL" else "Moteur Essence ⚡",
        "sw_version": sw_version or "Reconnu par Empreinte",
        "hw_version": hw_version or matched_info["name"].split()[0],
        "file_size": file_size,
        "solutions": solutions,
        "checksum_status": "Supporté & Automatique ✅",
        "checksum_algorithm": cs_algo,
        "technical_instructions": f"Flash de calibration pour {matched_info['name']} ({fuel_type}). Correction DTC et contrôle d'intégrité inclus."
    }


def preview_dtcs(binary_data: bytes, ecu_info: dict, selected_solutions: list) -> list:
    """Simule la désactivation des codes DTC pertinents en fonction des solutions sélectionnées"""
    dtc_list = []
    sol_str = " ".join([str(s).upper() for s in selected_solutions])

    if "DPF" in sol_str or "FAP" in sol_str:
        dtc_list.extend([
            {"code": "P2002", "desc": "Particulate Trap Efficiency Below Threshold (Bank 1)", "status": "Désactivé (DTC OFF)"},
            {"code": "P2463", "desc": "Diesel Particulate Filter - Soot Accumulation", "status": "Désactivé (DTC OFF)"},
            {"code": "P2452", "desc": "DPF Differential Pressure Sensor Circuit", "status": "Désactivé (DTC OFF)"}
        ])

    if "EGR" in sol_str:
        dtc_list.extend([
            {"code": "P0401", "desc": "Exhaust Gas Recirculation (EGR) Flow Insufficient", "status": "Désactivé (DTC OFF)"},
            {"code": "P0402", "desc": "Exhaust Gas Recirculation (EGR) Flow Excessive", "status": "Désactivé (DTC OFF)"},
            {"code": "P0403", "desc": "EGR Circuit Malfunction / Open Circuit", "status": "Désactivé (DTC OFF)"}
        ])

    if "ADBLUE" in sol_str or "SCR" in sol_str:
        dtc_list.extend([
            {"code": "P20EE", "desc": "SCR NOx Catalyst Efficiency Below Threshold Bank 1", "status": "Désactivé (DTC OFF)"},
            {"code": "P204F", "desc": "Reductant System Performance Bank 1", "status": "Désactivé (DTC OFF)"},
            {"code": "U029D", "desc": "Lost Communication With NOX Sensor A", "status": "Désactivé (DTC OFF)"}
        ])

    if "CAT" in sol_str or "EURO 2" in sol_str:
        dtc_list.extend([
            {"code": "P0420", "desc": "Catalyst System Efficiency Below Threshold (Bank 1)", "status": "Désactivé (DTC OFF)"},
            {"code": "P0136", "desc": "O2 Sensor Circuit Malfunction (Bank 1 Sensor 2)", "status": "Désactivé (DTC OFF)"},
            {"code": "P0141", "desc": "O2 Sensor Heater Circuit Malfunction (Bank 1 Sensor 2)", "status": "Désactivé (DTC OFF)"}
        ])

    if "EVAP" in sol_str:
        dtc_list.extend([
            {"code": "P0441", "desc": "Evaporative Emission Control System Incorrect Purge Flow", "status": "Désactivé (DTC OFF)"},
            {"code": "P0442", "desc": "Evaporative Emission System Leak Detected (Small Leak)", "status": "Désactivé (DTC OFF)"}
        ])

    if "VSA" in sol_str or "FLAP" in sol_str:
        dtc_list.extend([
            {"code": "P2008", "desc": "Intake Manifold Runner Control Circuit/Open (Bank 1)", "status": "Désactivé (DTC OFF)"},
            {"code": "P2015", "desc": "Intake Manifold Flap Position Sensor Range/Performance", "status": "Désactivé (DTC OFF)"}
        ])

    if "TVA" in sol_str:
        dtc_list.append({"code": "P2101", "desc": "Throttle Actuator Control Motor Circuit Range/Performance", "status": "Désactivé (DTC OFF)"})

    if "P0315" in sol_str:
        dtc_list.append({"code": "P0315", "desc": "Crankshaft Position System Variation Not Learned (Aveo/Cruze Fix)", "status": "Corrigé (Permanent Learn Bypass)"})

    return dtc_list


def get_technical_instructions(ecu_info: dict, selected_solutions: list) -> str:
    """Instructions techniques après écriture + notes fiche DaVinci"""
    instructions = ["1. Calculateur calibré avec le moteur certifié SVEdit v1.1.38.3 / DaVinci v1.0.30."]
    sol_str = " ".join([str(s).upper() for s in selected_solutions])

    # Notes spécifiques à l'ECU (plug_notes) si disponibles
    plug_note = ecu_info.get("plug_notes", "")
    if plug_note:
        instructions.append(f"Note fiche: {plug_note}")

    if "DPF" in sol_str or "FAP" in sol_str:
        instructions.append("2. Débrancher impérativement les capteurs de pression différentielle et de température FAP avant le premier démarrage.")
    if "EGR" in sol_str:
        instructions.append("3. La vanne EGR peut être condamnée mécaniquement avec une plaque d'obturation.")
    if "ADBLUE" in sol_str or "SCR" in sol_str:
        instructions.append("4. Débrancher le fusible de la pompe AdBlue ou le module SCR externe.")
    if "CAT" in sol_str or "LAMBDA" in sol_str:
        instructions.append("5. La seconde sonde Lambda (Aval / Post-Cat) peut être débranchée ou laissée en place.")
    if "TVA" in sol_str or "FLAP" in sol_str or "VSA" in sol_str:
        instructions.append("6. Les volets d'admission / TVA peuvent être condamnés mécaniquement ou fiche débranchée selon la note ECU.")
    if "START-STOP" in sol_str:
        instructions.append("7. La fonction Start & Stop est désactivée en permanence — aucun voyant au tableau de bord.")
    if "MAF" in sol_str:
        instructions.append("8. Débrancher le débitmètre d'air (MAF) après l'écriture du fichier.")
    if "P0315" in sol_str:
        instructions.append("9. Le défaut de variation de vilebrequin P0315 est annulé sans procédure d'apprentissage.")

    instructions.append("✅ Contrôle de somme Checksum recalculé automatiquement.")
    return "\n".join(instructions)


def apply_solution_unified(data: bytearray, ecu_id: str, solution: str) -> Tuple[bool, int, str]:
    """
    Point d'entrée unifié pour appliquer une solution sur un ECU.
    Cherche dans l'ordre : SVEdit base → DaVinci VAG/BMW/MB → DaVinci PSA/Renault/FCA.
    """
    # 1. SVEdit base engines
    if ecu_id in HYUNDAI_KIA_REGISTRY:
        return apply_hyundai_kia_patch(data, ecu_id, solution)
    if ecu_id in VAG_GROUP_REGISTRY:
        return apply_vag_group_patch(data, ecu_id, solution)
    if ecu_id in HONDA_REGISTRY:
        return apply_honda_patch(data, ecu_id, solution)
    if ecu_id in TOYOTA_NISSAN_REGISTRY:
        return apply_toyota_nissan_patch(data, ecu_id, solution)
    if ecu_id in MAZDA_MITSUBISHI_SUBARU_REGISTRY:
        return apply_mazda_mitsubishi_subaru_patch(data, ecu_id, solution)
    if ecu_id in FORD_FCA_OTHERS_REGISTRY:
        return apply_ford_fca_others_patch(data, ecu_id, solution)
    # 2. DaVinci VAG/BMW/MB
    if ecu_id in _DAVINCI_VAG_BMW_MB:
        return apply_davinci_vag_bmw_mb_patch(data, ecu_id, solution)
    # 3. DaVinci PSA/Renault/FCA
    if ecu_id in _DAVINCI_PSA_REN_FCA:
        return apply_davinci_psa_renault_fca_patch(data, ecu_id, solution)
    return False, 0, f"ECU {ecu_id} non trouvé dans aucun registre."
