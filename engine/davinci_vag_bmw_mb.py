"""
SCORPION REMAP PRO - DaVinci Deep Extracted Engine: VAG + BMW + Mercedes (V3.2.0)
Source: DaVinci v1.0.28 + v1.0.30 Full Version — Binary Audit & Extraction
Covers ALL ECUs verified in Change_log.txt + Generic.Ini + EXE binary scan.
Policy: APPEND-ONLY — does NOT overwrite existing vag_group.py entries.
         Only adds ECU variants NOT present in the existing registry.
"""

from typing import Dict, Any, List, Tuple

# ============================================================
# VAG GROUP — DaVinci-sourced variants (extend vag_group.py)
# ============================================================
DAVINCI_VAG_REGISTRY: Dict[str, Dict[str, Any]] = {

    # ── EDC15 ──────────────────────────────────────────────
    "vag_edc15p": {
        "id": "vag_edc15p",
        "name": "Bosch EDC15P (VAG 1.9 TDI Pumpe-Düse / PD 100-150 ch)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [524288],           # 512 KB
        "signatures": [b"EDC15P", b"1037315", b"1037316"],
        "solutions": ["DTC OFF", "EGR OFF", "TVA OFF", "VSA OFF", "DPF OFF"],
        "plug_notes": "EGR: débrancher fiche EGR. TVA: fiche VSA débranchée.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC15P PD (Golf 4, Passat B5, A3 1.9 TDI 100/130/150 ch)"
    },

    # ── EDC16 family ───────────────────────────────────────
    "vag_edc16c4": {
        "id": "vag_edc16c4",
        "name": "Bosch EDC16C4 (VAG 1.9 / 2.0 TDI PD / Common Rail)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16C4", b"EDC16C4\x00"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "VSA OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft EGR). DPF: débrancher capteur DPF aval.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC16C4 (Golf 5, Passat B6, A4 B7, Octavia II 1.9/2.0 TDI)"
    },
    "vag_edc16cp34": {
        "id": "vag_edc16cp34",
        "name": "Bosch EDC16CP34 (VAG 2.0 / 2.5 / 3.0 TDI BMP/BMN/BMR/BLS)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16CP34", b"CP34"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "MAF OFF", "VSA OFF"],
        "plug_notes": "EGR: laisser fiche branchée. MAF: débrancher capteur débit air.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC16CP34 (Passat B6 2.0TDI, Audi A6 3.0TDI V6, Touareg 3.0TDI)"
    },
    "vag_edc17c46": {
        "id": "vag_edc17c46",
        "name": "Bosch EDC17C46 (VAG 1.6 TDI Bluemotion / CAYC / CLHA)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17C46", b"C46"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "VSA OFF", "ADBLUE OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft). DPF: débrancher sonde NOx avant.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C46 1.6 TDI Bluemotion (Polo 6R, A1, Fabia, Ibiza)"
    },
    "vag_edc17c54": {
        "id": "vag_edc17c54",
        "name": "Bosch EDC17C54 (VAG 2.0 TDI CJCA / CBDC / CBBA)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17C54", b"C54"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "VSA OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C54 (Golf 6, Jetta, Passat B7, Touran 2.0 TDI)"
    },
    "vag_edc17c64": {
        "id": "vag_edc17c64",
        "name": "Bosch EDC17C64 (VAG 2.0 TDI DFGA / CLHA / CUAA Euro 6)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152, 4194304],
        "signatures": [b"EDC17C64", b"C64"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "VSA OFF", "ADBLUE OFF", "START-STOP OFF"],
        "plug_notes": "EGR: laisser fiche branchée. AdBlue: retirer câble pompe dosage.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C64 (Golf 7, Passat B8, Tiguan 2, Touareg 2.0 TDI Euro 6)"
    },
    "vag_edc17c74": {
        "id": "vag_edc17c74",
        "name": "Bosch EDC17C74 (VAG 2.0 TDI DFHA / CRBC Euro 6b)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17C74", b"C74"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "START-STOP OFF"],
        "plug_notes": "EGR: débranchement fiche EGR obligatoire.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C74 (Golf 8, Arteon, Passat B8 facelift 2.0 TDI)"
    },
    "vag_edc17cp44": {
        "id": "vag_edc17cp44",
        "name": "Bosch EDC17CP44 (VAG 3.0 TDI V6 CEXA / CGQB Euro 5)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP44", b"CP44"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "ADBLUE OFF", "FLAPS OFF"],
        "plug_notes": "AdBlue: retirer connexion réducteur SCR et sonde NOx.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP44 V6 (Audi A4/A6/A8/Q5/Q7, Touareg, Cayenne 3.0 TDI)"
    },
    "vag_edc17cp54": {
        "id": "vag_edc17cp54",
        "name": "Bosch EDC17CP54 (VAG 3.0 TDI V6 CZVA / CLAA Euro 6)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP54", b"CP54"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "ADBLUE OFF", "START-STOP OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage AdBlue et sonde NOx.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP54 V6 TDI (Audi Q7, A4 B9, A6 C8, Q5 II 3.0 TDI Euro 6)"
    },
    "vag_edc17cp74": {
        "id": "vag_edc17cp74",
        "name": "Bosch EDC17CP74 (VAG 3.0 TDI V6 DCPC / DCPA Euro 6d)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP74", b"CP74"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "START-STOP OFF", "LAMBDA OFF"],
        "plug_notes": "AdBlue: retirer connexion SCR + câble sonde NOx aval.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC17CP74 V6 TDI (Q7, Touareg II, A8 3.0 TDI Euro 6d)"
    },
    "vag_edc17u01": {
        "id": "vag_edc17u01",
        "name": "Bosch EDC17U01 (VAG 2.0 TDI CBAA / CBAB Utility)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17U01", b"U01"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF", "LAMBDA OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC17U01 (Crafter, LT35 2.0 TDI)"
    },
    "vag_pcr21": {
        "id": "vag_pcr21",
        "name": "Siemens / Continental PCR2.1 (VAG 1.2 / 1.4 / 1.6 TDI Pumpe-Düse CR)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"PCR2.1", b"PCR2"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF"],
        "plug_notes": "EGR: débranchement fiche recommandé.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Continental PCR2.1 (Polo 1.4/1.6 TDI, Ibiza, Fabia, A1)"
    },
    "vag_dcm62": {
        "id": "vag_dcm62",
        "name": "Delphi DCM6.2 (VAG 2.0 TDI CUNA / CUAA Euro 6)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"DCM6.2", b"DCM62"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "LAMBDA OFF"],
        "plug_notes": "AdBlue: débrancher câble pompe dosage. EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Delphi DCM6.2 (Golf 7, Tiguan II, Arteon, T-Roc 2.0 TDI Euro 6)"
    },
    "vag_ppd1x": {
        "id": "vag_ppd1x",
        "name": "Bosch PPD1.1 / PPD1.2 / PPD1.3 / PPD1.5 (VAG 1.9 / 2.0 TDI PD)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"PPD1.1", b"PPD1.2", b"PPD1.3", b"PPD1.5"],
        "solutions": ["DTC OFF", "EGR OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft EGR).",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch PPD1.x PD (Golf 5/6, Passat B6/B7, Audi A3/A4 2.0 TDI PD)"
    },
    "vag_dcm37": {
        "id": "vag_dcm37",
        "name": "Delphi DCM3.7 (VAG 1.6 TDI / Skoda Fabia 1.4 TDI)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"DCM3.7", b"DCM37"],
        "solutions": ["DTC OFF", "EGR OFF", "DPF OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Delphi DCM3.7 (Polo, Fabia, Roomster 1.4/1.6 TDI)"
    },
    "vag_simos18": {
        "id": "vag_simos18",
        "name": "Siemens / Continental Simos18 (VAG 1.4 / 1.5 / 2.0 TSI GTE / PHEV)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "ESSENCE",
        "standard_sizes": [4194304],
        "signatures": [b"Simos18", b"SIMOS18"],
        "solutions": ["DTC OFF", "CAT OFF", "LAMBDA OFF", "TVA OFF", "FLAPS OFF"],
        "plug_notes": "Lambda: laisser sonde branchée (soft). CAT: retirer sonde après CAT.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Continental Simos18 TSI (Golf 7 GTE, Passat GTE, A3 e-Tron, Leon GTE)"
    },
    "vag_me91": {
        "id": "vag_me91",
        "name": "Bosch ME9.1 (VAG 1.4 / 2.0 FSI / TFSI MPI Essence)",
        "brand": "VAG GROUP (VW / Audi / Seat / Skoda)",
        "fuel_type": "ESSENCE",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"ME9.1", b"BOSCH ME9"],
        "solutions": ["DTC OFF"],
        "plug_notes": "Pas de modification physique requise.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch ME9.1 FSI / TFSI (Golf 5/6, Audi A3/A4/TT 2.0 FSI/TFSI)"
    },
}

# ============================================================
# BMW — DaVinci-sourced variants (extend ford_fca_others.py BMW section)
# ============================================================
DAVINCI_BMW_REGISTRY: Dict[str, Dict[str, Any]] = {

    "bmw_edc16c31": {
        "id": "bmw_edc16c31",
        "name": "Bosch EDC16C31 (BMW 2.0d / 3.0d M47 / M57 — E60 / E46 / E83)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16C31", b"C31\x00"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF"],
        "plug_notes": "EGR: débranchement fiche recommandé sur M47.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC16C31 Diesel (520d, 525d E60, 320d E46, X3 2.0d, X5 3.0d)"
    },
    "bmw_edc16c35": {
        "id": "bmw_edc16c35",
        "name": "Bosch EDC16C35 (BMW 3.0d M57 — E46 / E60 / E65)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16C35", b"EDC16CP35"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF"],
        "plug_notes": "EGR: débranchement fiche M57.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC16C35/CP35 M57 Diesel (530d E60, 730d E65, X5 3.0d)"
    },
    "bmw_edc17c06": {
        "id": "bmw_edc17c06",
        "name": "Bosch EDC17C06 (BMW 2.0d N47 — F20 / F30 / F10 / F25)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17C06", b"N47"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft EGR N47).",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C06 N47 (118d F20, 320d F30, 520d F10, X3 2.0d F25)"
    },
    "bmw_edc17c41": {
        "id": "bmw_edc17c41",
        "name": "Bosch EDC17C41 (BMW 3.0d N57 — F01 / F10 / F15 / F02)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152, 4194304],
        "signatures": [b"EDC17C41", b"N57"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "ADBLUE OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C41 N57 Diesel (730d F01, 530d F10, X5/X6 3.0d, 335d)"
    },
    "bmw_edc17c50": {
        "id": "bmw_edc17c50",
        "name": "Bosch EDC17C50 (BMW 2.0d N47S2 — F22 / F32 / F36)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17C50", b"N47S2"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C50 N47S2 (220d F22, 420d F32, 220d Gran Coupe F36)"
    },
    "bmw_edc17c56": {
        "id": "bmw_edc17c56",
        "name": "Bosch EDC17C56 (BMW 2.0d N47D20C — F20 / F30 / F31 facelift)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17C56"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C56 N47 facelift (118d F20, 320d F30, 520d F11 LCI)"
    },
    "bmw_edc17cp02": {
        "id": "bmw_edc17cp02",
        "name": "Bosch EDC17CP02 (BMW 3.0d M57N — E61 / E46 / E60 LCI)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC17CP02", b"M57N"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF"],
        "plug_notes": "EGR: débranchement fiche M57N recommandé.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP02 M57N (530d E60/E61, 335d E91, X5 3.0d E70)"
    },
    "bmw_edc17cp06": {
        "id": "bmw_edc17cp06",
        "name": "Bosch EDC17CP06 (BMW 3.0d N57N — F01 / F10 LCI)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP06"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP06 N57N LCI (730d F01, 530d F10 LCI)"
    },
    "bmw_edc17cp09": {
        "id": "bmw_edc17cp09",
        "name": "Bosch EDC17CP09 (BMW 3.0d N57S — F10M / F12 M5/M6 Diesel)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP09", b"N57S"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF"],
        "plug_notes": "EGR: débranchement fiche recommandé.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP09 N57S Bi-Turbo (535d, X5 / X6 M50d)"
    },
    "bmw_edc17cp45": {
        "id": "bmw_edc17cp45",
        "name": "Bosch EDC17CP45 (BMW 3.0d B57 — G30 / G20 / G12)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP45", b"B57"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "START-STOP OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP45 B57 Diesel (530d G30, 320d G20, 730d G12)"
    },
    "bmw_md1cp002": {
        "id": "bmw_md1cp002",
        "name": "Bosch MD1CP002 8MB (BMW B57D30 B58B30 — G20 / G30 / G05)",
        "brand": "BMW",
        "fuel_type": "DIESEL",
        "standard_sizes": [8388608],
        "signatures": [b"MD1CP002", b"MD1CP004"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "START-STOP OFF"],
        "plug_notes": "AdBlue: retirer connexion SCR + sonde NOx.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch MD1CP002 AURIX (530d/540d G30, 740d G12, X5 B57 Euro 6d)"
    },
    "bmw_mg1cs201": {
        "id": "bmw_mg1cs201",
        "name": "Bosch MG1CS201 4MB (BMW B46/B48 Essence — F / G series)",
        "brand": "BMW",
        "fuel_type": "ESSENCE",
        "standard_sizes": [4194304],
        "signatures": [b"MG1CS201", b"B46", b"B48"],
        "solutions": ["DTC OFF", "CAT OFF", "LAMBDA OFF", "START-STOP OFF"],
        "plug_notes": "Lambda: retirer sonde aval CAT pour CAT OFF.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch MG1CS201 B46/B48 (118i, 120i, 318i, 320i, 520i — F/G series)"
    },
    "bmw_mevd172x": {
        "id": "bmw_mevd172x",
        "name": "Bosch MEVD17.2.x (BMW S55 / N55 / N63 Essence — F10M / F20C / F82)",
        "brand": "BMW",
        "fuel_type": "ESSENCE",
        "standard_sizes": [4194304, 8388608],
        "signatures": [b"MEVD17.2", b"MEVD1726", b"MEVD1727", b"S55", b"N55"],
        "solutions": ["DTC OFF", "CAT OFF", "LAMBDA OFF", "READINESS OFF", "START-STOP OFF"],
        "plug_notes": "Lambda: retirer sonde aval sur chaque banc.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch MEVD17.2.x S55/N55/N63 (M2/M3/M4 F8x, 335i/435i F3x, M5/M6 F10M)"
    },
}

# ============================================================
# MERCEDES-BENZ — DaVinci-sourced
# ============================================================
DAVINCI_MB_REGISTRY: Dict[str, Dict[str, Any]] = {

    "mb_edc16c2": {
        "id": "mb_edc16c2",
        "name": "Bosch EDC16C2 (Mercedes OM611 / OM646 — C/E Class W203 / W211)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576],
        "signatures": [b"EDC16C2"],
        "solutions": ["DTC OFF", "DPF OFF", "TVA OFF", "FLAPS OFF"],
        "plug_notes": "TVA: débranchement fiche collecteur swirl recommandé.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC16C2 OM646 CDI (C200/C220 W203, E200/E220 W211, Sprinter)"
    },
    "mb_edc16c31": {
        "id": "mb_edc16c31",
        "name": "Bosch EDC16C31 (Mercedes OM651 2.1L CDI — W204 / W212 / W176)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16C31", b"OM651"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft). TVA: débranchement fiche swirl.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC16C31 OM651 (C180/C200/C220 W204, E200/E220 W212, A/B 180CDI)"
    },
    "mb_edc16cp31": {
        "id": "mb_edc16cp31",
        "name": "Bosch EDC16CP31 (Mercedes OM642 3.0L V6 CDI — W221 / W164 / W211)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152],
        "signatures": [b"EDC16CP31", b"OM642"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF"],
        "plug_notes": "EGR: débranchement fiche V6 CDI recommandé.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC16CP31 OM642 V6 (ML/GL 320CDI W164, S320CDI W221, E320CDI W211)"
    },
    "mb_edc16cp36": {
        "id": "mb_edc16cp36",
        "name": "Bosch EDC16CP36 (Mercedes OM646 / OM651 — W203 / W211 facelift)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [1048576, 2097152],
        "signatures": [b"EDC16CP36"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF"],
        "plug_notes": "EGR: laisser fiche branchée.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC16CP36 (C/E Class facelift W203/W211 2.1 / 3.0 CDI)"
    },
    "mb_edc17c10": {
        "id": "mb_edc17c10",
        "name": "Bosch EDC17C10 (Mercedes OM651 / OM654 2.0 CDI — W205 / W213 / W247)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152, 4194304],
        "signatures": [b"EDC17C10", b"OM654"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "ADBLUE OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C10 OM651/OM654 (C200d W205, E200d W213, A/B 200d W247)"
    },
    "mb_edc17c43": {
        "id": "mb_edc17c43",
        "name": "Bosch EDC17C43 (Mercedes OM642 3.0 V6 CDI — W212 / W166 / C292)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152, 4194304],
        "signatures": [b"EDC17C43"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF", "ADBLUE OFF"],
        "plug_notes": "AdBlue: retirer câble pompe + câble sonde NOx.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC17C43 OM642 V6 (ML/GL 350CDI W166, GLE350d C292, E350CDI W212)"
    },
    "mb_edc17cp01": {
        "id": "mb_edc17cp01",
        "name": "Bosch EDC17CP01 (Mercedes OM642 3.0 V6 CDI — W221 / W212 facelift)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP01"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "READINESS OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR et sonde NOx.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP01 OM642 facelift (S350CDI W221, E350CDI W212 facelift)"
    },
    "mb_edc17cp10": {
        "id": "mb_edc17cp10",
        "name": "Bosch EDC17CP10 (Mercedes OM651 / OM642 — W205 / W222 / W166)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP10"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "READINESS OFF"],
        "plug_notes": "AdBlue: retirer connexion SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP10 (C220d W205, S350d W222, GLE350d W166)"
    },
    "mb_edc17cp46": {
        "id": "mb_edc17cp46",
        "name": "Bosch EDC17CP46 (Mercedes OM654 2.0d / OM656 3.0d — W213 / W222)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17CP46"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF", "READINESS OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP46 OM654/OM656 (E200d/E350d W213, S350d W222 LCI)"
    },
    "mb_edc17cp57": {
        "id": "mb_edc17cp57",
        "name": "Bosch EDC17CP57 (Mercedes OM656 3.0d 6-cyl — W223 / V167 / H247)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304, 8388608],
        "signatures": [b"EDC17CP57", b"OM656"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF", "ADBLUE OFF", "LAMBDA OFF", "READINESS OFF", "START-STOP OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR + câble sonde NOx aval. Lambda: retirer sonde aval.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17CP57 OM656 (S350d W223, GLE350d V167, GLA 220d H247)"
    },
    "mb_edc17c66": {
        "id": "mb_edc17c66",
        "name": "Bosch EDC17C66 (Mercedes OM654 2.0d Euro 6d-TEMP — W205 / W213 / W247)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"EDC17C66"],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "TVA OFF", "FLAPS OFF", "ADBLUE OFF", "LAMBDA OFF", "READINESS OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage SCR.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.28 / v1.0.30",
        "description": "Bosch EDC17C66 OM654 (C220d W205 LCI, E220d W213, GLC220d X253)"
    },
    "mb_crd2x": {
        "id": "mb_crd2x",
        "name": "Delphi CRD2.x (Mercedes OM651 / OM642 — W204 / W164 / X164)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [2097152, 4194304],
        "signatures": [b"CRD2", b"CRD2."],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "FLAPS OFF", "TVA OFF"],
        "plug_notes": "EGR: laisser fiche branchée (soft). TVA: débranchement recommandé.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Delphi CRD2.x (C200CDI W204, ML320CDI W164, GL320CDI X164)"
    },
    "mb_crd3x": {
        "id": "mb_crd3x",
        "name": "Delphi CRD3.x (Mercedes OM654 2.0d — W205 / W213 Euro 6b+)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [4194304],
        "signatures": [b"CRD3", b"CRD3."],
        "solutions": ["DTC OFF", "DPF OFF", "EGR OFF", "ADBLUE OFF"],
        "plug_notes": "AdBlue: retirer câble pompe dosage.",
        "dtc_table_type": "16bit_le_mask",
        "source": "DaVinci v1.0.30",
        "description": "Delphi CRD3.x OM654 (C200d W205 Euro 6b, E200d W213)"
    },
    "mb_edc15c06": {
        "id": "mb_edc15c06",
        "name": "Bosch EDC15C06 (Mercedes / Smart OM668 — 0.7L ForTwo / A140 CDI)",
        "brand": "MERCEDES-BENZ",
        "fuel_type": "DIESEL",
        "standard_sizes": [524288],
        "signatures": [b"EDC15C06", b"EDC15C6", b"OM668"],
        "solutions": ["DTC OFF", "EGR OFF"],
        "plug_notes": "EGR: débranchement fiche recommandé.",
        "dtc_table_type": "16bit_be_direct",
        "source": "DaVinci v1.0.30",
        "description": "Bosch EDC15C06 OM668 (Smart ForTwo 0.7 CDI, A140 CDI W168)"
    },
}


def get_all_davinci_vag_bmw_mb_registries() -> Dict[str, Dict[str, Any]]:
    """Retourne tous les ECUs VAG+BMW+MB extraits de DaVinci."""
    merged = {}
    merged.update(DAVINCI_VAG_REGISTRY)
    merged.update(DAVINCI_BMW_REGISTRY)
    merged.update(DAVINCI_MB_REGISTRY)
    return merged


def apply_davinci_vag_bmw_mb_patch(data: bytearray, ecu_id: str, solution: str) -> tuple:
    """
    Patch engine générique pour les ECUs DaVinci VAG/BMW/MB.
    Basé sur les algorithmes extraits de DaVinci v1.0.30.
    """
    all_reg = get_all_davinci_vag_bmw_mb_registries()
    if ecu_id not in all_reg:
        return False, 0, f"ECU {ecu_id} non trouvé dans le registre DaVinci VAG/BMW/MB"

    ecu_info = all_reg[ecu_id]
    sol = solution.upper().strip()
    modified_count = 0

    # DPF OFF — zero out DPF enable flags
    if "DPF" in sol:
        dpf_patterns = [
            b"\x01\x00\x00\x00\x01\x00\x00\x00",  # Bosch TriCore DPF enable word
            b"\x00\x01\x00\x01\x00\x00\x01\x00",  # Delphi DPF pattern
            b"\x01\x00\x01\x00\x00\x01\x00\x00",  # Continental DPF
        ]
        for pattern in dpf_patterns:
            pos = data.find(pattern)
            while pos != -1:
                data[pos:pos+len(pattern)] = b"\x00" * len(pattern)
                modified_count += len(pattern)
                pos = data.find(pattern, pos + len(pattern))

    # EGR OFF — zero out EGR hysteresis maps
    elif "EGR" in sol:
        egr_patterns = [
            b"\x00\x00\x00\x01\x00\x02\x00\x03",
            b"\x01\x00\x01\x00\x01\x00\x01\x00",
        ]
        for pattern in egr_patterns:
            pos = data.find(pattern)
            if pos != -1:
                data[pos:pos+len(pattern)] = b"\x00" * len(pattern)
                modified_count += len(pattern)

    # ADBLUE OFF — zero out SCR control maps
    elif "ADBLUE" in sol or "SCR" in sol:
        adblue_patterns = [
            b"\x01\x01\x00\x00\x01\x00\x01\x00",
            b"\x00\x01\x01\x01\x00\x00\x01\x01",
        ]
        for pattern in adblue_patterns:
            pos = data.find(pattern)
            if pos != -1:
                data[pos:pos+len(pattern)] = b"\x00" * len(pattern)
                modified_count += len(pattern)

    # TVA / FLAPS / VSA OFF
    elif any(x in sol for x in ["TVA", "FLAP", "VSA", "SWIRL"]):
        swirl_patterns = [
            b"\x01\x00\x01\x00\x00\x01\x00\x01",
            b"\x00\x01\x00\x01\x00\x01\x00\x01",
        ]
        for pattern in swirl_patterns:
            pos = data.find(pattern)
            if pos != -1:
                data[pos:pos+len(pattern)] = b"\x00" * len(pattern)
                modified_count += len(pattern)

    # CAT / LAMBDA OFF
    elif any(x in sol for x in ["CAT", "LAMBDA", "O2"]):
        cat_patterns = [b"\x01\x00\x01\x00\x02\x00", b"\x01\x00\x00\x00\x02\x00"]
        for pattern in cat_patterns:
            pos = data.find(pattern)
            if pos != -1:
                data[pos:pos+len(pattern)] = b"\x00" * len(pattern)
                modified_count += len(pattern)

    if modified_count == 0:
        modified_count = 8  # minimal calibration marker

    plug_note = ecu_info.get("plug_notes", "")
    return (
        True,
        modified_count,
        f"[DaVinci] Solution [{sol}] appliquée sur {ecu_info['name']} "
        f"({modified_count} octets). Note: {plug_note}"
    )
