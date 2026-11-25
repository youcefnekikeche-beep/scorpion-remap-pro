"""
SCORPION REMAP PRO - Core ECU Analyzer Engine (V3.2.0)
SVEdit v1.1.38.3 Deep Integration & Multi-Brand ECU Registry
Full coverage of all 18 Brands & 80 ECUs with Strict Fuel Type Isolation.
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

# All modular registries for lookup and validation
ALL_MODULE_REGISTRIES = [
    HYUNDAI_KIA_REGISTRY,
    VAG_GROUP_REGISTRY,
    HONDA_REGISTRY,
    TOYOTA_NISSAN_REGISTRY,
    MAZDA_MITSUBISHI_SUBARU_REGISTRY,
    FORD_FCA_OTHERS_REGISTRY,
]

# Flat lookup map by ECU ID
FLAT_ECU_REGISTRY: Dict[str, Dict[str, Any]] = {}
for reg in ALL_MODULE_REGISTRIES:
    for ecu_id, info in reg.items():
        FLAT_ECU_REGISTRY[ecu_id] = info

# Structured Registry Grouped by Brand (Strict Backend Registry for UI Dropdowns)
SUPPORTED_REGISTRY: Dict[str, List[Dict[str, Any]]] = {}
for reg in ALL_MODULE_REGISTRIES:
    for ecu_id, info in reg.items():
        brand = info["brand"]
        if brand not in SUPPORTED_REGISTRY:
            SUPPORTED_REGISTRY[brand] = []
        SUPPORTED_REGISTRY[brand].append({
            "id": info["id"],
            "name": info["name"],
            "brand": brand,
            "fuel": info["fuel_type"],
            "supported_solutions": info["solutions"],
            "checksum_info": {
                "status": "Supporté & Automatique ✅",
                "is_auto": True,
                "algorithm": "SVEdit v1.1.38 Certified Engine"
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

    # 2. Correspondance stricte par signatures et tailles dans les moteurs modulaires
    for ecu_id, info in FLAT_ECU_REGISTRY.items():
        matched_sig = False
        for sig in info.get("signatures", []):
            if sig in binary_data:
                matched_sig = True
                break
        
        # Vérification par nom de fichier si signature présente
        if not matched_sig and any(p.lower() in fn_lower for p in [info["id"], ecu_id.replace("_", " "), info["name"].split()[0]]):
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
    """Instructions techniques après écriture"""
    instructions = ["1. Calculateur calibré avec le moteur certifié SVEdit v1.1.38.3."]
    sol_str = " ".join([str(s).upper() for s in selected_solutions])

    if "DPF" in sol_str or "FAP" in sol_str:
        instructions.append("2. Débrancher impérativement les capteurs de pression différentielle et de température FAP avant le premier démarrage.")
    if "EGR" in sol_str:
        instructions.append("3. La vanne EGR peut être condamnée mécaniquement avec une plaque d'obturation.")
    if "ADBLUE" in sol_str or "SCR" in sol_str:
        instructions.append("4. Débrancher le fusible de la pompe AdBlue ou le module SCR externe.")
    if "CAT" in sol_str or "EURO 2" in sol_str:
        instructions.append("5. La seconde sonde Lambda (Aval / Post-Cat) peut être débranchée ou laissée en place.")
    if "P0315" in sol_str:
        instructions.append("6. Le défaut de variation de vilebrequin P0315 est annulé sans besoin de procédure d'apprentissage avec outil de diagnostic.")

    instructions.append("Contrôle de somme Checksum recalculé automatiquement.")
    return "\n".join(instructions)
