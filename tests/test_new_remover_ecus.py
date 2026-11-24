import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.ecu_analyzer import identify_ecu, preview_dtcs

def test_new_ecus():
    test_cases = [
        ("Delphi CRD2 / CRD3", b"\x00" * 1000 + b"CRD2.10" + b"\x00" * 2000000, "mercedes_crd2.bin"),
        ("Delphi DCM6.2", b"\x00" * 1000 + b"DCM6.2" + b"\x00" * 2000000, "peugeot_dcm62.bin"),
        ("Bosch EDC17C69", b"\x00" * 1000 + b"EDC17C69" + b"\x00" * 2000000, "jeep_edc17c69.bin"),
        ("Continental Simos 18", b"\x00" * 1000 + b"SIMOS 18" + b"\x00" * 2000000, "golf7_simos18.bin"),
        ("Continental PCR 2.1", b"\x00" * 1000 + b"PCR2.1" + b"\x00" * 2000000, "vag_pcr21.bin"),
        ("Siemens PPD 1.x", b"\x00" * 1000 + b"PPD1.2" + b"\x00" * 2000000, "passat_ppd1.bin"),
        ("Siemens SID803A", b"\x00" * 1000 + b"SID803A" + b"\x00" * 2000000, "peugeot_sid803.bin"),
        ("Bosch MD1CP002", b"\x00" * 1000 + b"MD1CP002" + b"\x00" * 2000000, "audi_md1.bin"),
        ("Marelli 8F2 / 8F3", b"\x00" * 1000 + b"8F3" + b"\x00" * 2000000, "fiat_8f3.bin"),
    ]

    print("Running integration tests on new ECU algorithms from remover/...")
    for label, dummy_bin, fname in test_cases:
        res = identify_ecu(dummy_bin, fname)
        print(f"  [OK] {label:22s} -> Identified: {res['ecu_type']:30s} | Brand: {res['brand']:15s} | Solutions: {len(res['supported_solutions'])}")
        assert len(res['supported_solutions']) > 0

        # Test preview_dtcs
        dtc_preview = preview_dtcs(dummy_bin, ['DPF / FAP', 'EGR'], ['P2002', 'P0401'])
        assert len(dtc_preview) > 0
        print(f"       DTC Preview count: {len(dtc_preview)} codes simulated.")

    print("\nALL NEW REMOVER ECU INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_new_ecus()
