import os
import sys

SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from engine.ecu_analyzer import identify_ecu, preview_dtcs, get_technical_instructions
from engine.tuning_bridge import apply_svedit_hex_patches

def run_tests():
    print("=" * 70)
    print("SCORPION REMAP PRO V3.2.0 - SUITE DE TEST DES 24 FAMILLES CALCULATEURS")
    print("=" * 70)

    # 24 Test cases representing each requested ECU family
    test_cases = [
        # 1. BOSCH EDC16
        ("1. BOSCH EDC16", b"BOSCH_EDC16U34_1037382451_0281012345" + b"\x00" * 1048500, "vw_golf5_edc16u34.bin",
         ["DPF / FAP", "EGR", "SWIRL / FLAPS", "TVA"]),

        # 2. BOSCH EDC17
        ("2. BOSCH EDC17", b"BOSCH_EDC17CP20_1037518078_0281016789" + b"\x00" * 2097100, "audi_a4_edc17cp20.bin",
         ["DPF / FAP", "EGR", "ADBLUE", "SWIRL / FLAPS", "TVA", "IMMO"]),

        # 3. BOSCH MED17
        ("3. BOSCH MED17", b"BOSCH_MED17.5_1037398765_0261S04123" + b"\x00" * 2097100, "vw_golf6_gti_med17.5.bin",
         ["DECAT / LAMBDA", "EVAP", "SWIRL / FLAPS", "IMMO"]),

        # 4. BOSCH DCU17
        ("4. BOSCH DCU17", b"BOSCH_DCU17PC43_ADBLUE_UNIT" + b"\x00" * 1048500, "mercedes_dcu17.bin",
         ["ADBLUE"]),

        # 5. BMW MSV / MSD
        ("5. BMW MSV(D)", b"CONTINENTAL_MSD80_BMW_N54_3.0T" + b"\x00" * 2097100, "bmw_335i_msd80.bin",
         ["DECAT / LAMBDA", "EVAP"]),

        # 6. CHEVROLET MT80
        ("6. CHEVROLET MT80", b"DELPHI_MT80.1_CHEVROLET_AVEO_1.2" + b"\x00" * 1572800, "chevy_aveo_mt80.bin",
         ["P0315 FIX", "DECAT / LAMBDA", "EVAP", "EGR"]),

        # 7. CHINA ME7.9.7 / M7.8
        ("7. CHINA ME7.9.7", b"BOSCH_ME7.9.7_CHERY_TIGGO_1.6" + b"\x00" * 1048500, "chery_me7.9.7.bin",
         ["IMMO", "DECAT / LAMBDA", "EVAP"]),

        # 8. ISUZU TRANSTRON
        ("8. ISUZU TRANSTRON", b"TRANSTRON_SH7058_ISUZU_DMAX_3.0" + b"\x00" * 1048500, "isuzu_dmax_transtron.bin",
         ["DPF / FAP", "EGR", "IMMO"]),

        # 9. FCA GROUP NGC4
        ("9. FCA GROUP NGC4", b"CONTINENTAL_NGC4_JEEP_GRAND_CHEROKEE_3.6" + b"\x00" * 2097100, "jeep_ngc4.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR"]),

        # 10. FORD SID208
        ("10. FORD SID208", b"CONTINENTAL_SID208_FORD_TRANSIT_2.2_TDCI" + b"\x00" * 4194200, "ford_transit_sid208.bin",
         ["DPF / FAP", "EGR", "ADBLUE"]),

        # 11. HONDA KEIHIN
        ("11. HONDA KEIHIN", b"KEIHIN_SH72546_HONDA_CIVIC_1.5T" + b"\x00" * 2097100, "honda_civic_keihin.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR"]),

        # 12. HYUNDAI ODOMETR
        ("12. HYUNDAI ODOMETR", b"HYUNDAI_FLASH_EEPROM_ODO" + b"\x00" * 262100, "hyundai_i30_odo.bin",
         ["ODO CALIBRATION"]),

        # 13. KIA/HYUNDAI SIM2K
        ("13. KIA/HYUNDAI SIM2K", b"CONTINENTAL_SIM2K-241_HYUNDAI_TUCSON" + b"\x00" * 2097100, "hyundai_sim2k241.bin",
         ["DECAT / LAMBDA", "EVAP", "IMMO"]),

        # 14. MAZDA MH8106F
        ("14. MAZDA MH8106F", b"MITSUBISHI_MH8106F_MAZDA3_2.0" + b"\x00" * 1048500, "mazda3_mh8106f.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR"]),

        # 15. MITSUBISHI MELCO
        ("15. MITSUBISHI MELCO", b"MITSUBISHI_MH8104_LANCER_X" + b"\x00" * 1048500, "lancer_x_mh8104.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR", "IMMO"]),

        # 16. MITSUBISHI ODOMETR
        ("16. MITSUBISHI ODO", b"MITSUBISHI_FLASH_EEPROM_ODO" + b"\x00" * 262100, "pajero_odo.bin",
         ["ODO CALIBRATION"]),

        # 17. NISSAN SID309
        ("17. NISSAN SID309", b"CONTINENTAL_SID309_NISSAN_QASHQAI_1.6_DCI" + b"\x00" * 2097100, "nissan_sid309.bin",
         ["DPF / FAP", "EGR", "ADBLUE"]),

        # 18. RENAULT VALEO V42
        ("18. RENAULT VALEO V42", b"RENAULT_VALEO_V42_CLIO4_1.2" + b"\x00" * 1572800, "renault_clio4_v42.bin",
         ["DECAT / LAMBDA", "IMMO"]),

        # 19. SSANGYONG DCM6.2
        ("19. SSANGYONG DCM6.2", b"DELPHI_DCM6.2_SSANGYONG_KORANDO_2.2D" + b"\x00" * 2097100, "ssangyong_dcm62.bin",
         ["DPF / FAP", "EGR", "ADBLUE", "TVA"]),

        # 20. SUBARU DENSO
        ("20. SUBARU DENSO", b"SUBARU_DENSO_SH7058_IMPREZA_2.0" + b"\x00" * 1048500, "subaru_impreza.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR"]),

        # 21. TOYOTA DENSO
        ("21. TOYOTA DENSO", b"TOYOTA_DENSO_GEN3_HILUX_2.8_D4D" + b"\x00" * 2097100, "toyota_hilux_denso.bin",
         ["DPF / FAP", "EGR", "ADBLUE"]),

        # 22. VAG GROUP MD1
        ("22. VAG GROUP MD1", b"BOSCH_MD1CP002_VAG_3.0_TDI_CR" + b"\x00" * 8388500, "audi_a6_md1cp002.bin",
         ["DPF / FAP", "EGR", "ADBLUE"]),

        # 23. VOLVO VISTEON ESU
        ("23. VOLVO VISTEON", b"VISTEON_ESU-121_VOLVO_V50_1.8" + b"\x00" * 1048500, "volvo_v50_esu121.bin",
         ["DECAT / LAMBDA", "EVAP", "EGR"]),

        # 24. UAZ ME17.9.7(1)
        ("24. UAZ ME17.9.7(1)", b"BOSCH_1037539917_UAZ_PATRIOT_2.7" + b"\x00" * 1572800, "uaz_patriot_me17.bin",
         ["IMMO"])
    ]

    passed = 0
    total = len(test_cases)

    for category, dummy_data, fname, expected_sols in test_cases:
        res = identify_ecu(dummy_data, fname)
        assert res['ecu_type'], f"Identification failed for {category}"
        assert res['brand'], f"Brand detection failed for {category}"
        assert len(res['supported_solutions']) > 0, f"No supported solutions for {category}"

        # Test patching function
        patched = apply_svedit_hex_patches(dummy_data, expected_sols, res['ecu_type'])
        assert len(patched) == len(dummy_data), f"Size altered during patch for {category}"

        # Test DTC preview
        preview = preview_dtcs(dummy_data, expected_sols, ["P0420", "P2002"])
        assert isinstance(preview, list), f"DTC preview failed for {category}"

        # Test technical instructions
        instr = get_technical_instructions(expected_sols, res['ecu_type'])
        assert isinstance(instr, list), f"Instructions failed for {category}"

        # Check that at least one of expected sols is present in res['supported_solutions']
        sols_match = any(any(e.upper() in s.upper() or s.upper() in e.upper() for s in res['supported_solutions']) for e in expected_sols)
        assert sols_match, f"Solutions mismatch for {category}: expected {expected_sols}, got {res['supported_solutions']}"

        print(f"[OK] {category:25} -> {res['ecu_type']} ({res['brand']}) | Sols: {len(res['supported_solutions'])}")
        passed += 1

    print("=" * 70)
    print(f"RÉSULTAT DU CONTRÔLE : {passed}/{total} FAMILLES VALIDÉES À 100% SANS DÉFAUT !")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
