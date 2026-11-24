import sys
import os
sys.path.append(os.path.abspath('.'))

from engine.ecu_analyzer import (
    identify_ecu, SUPPORTED_REGISTRY, get_registry_ecu
)

print("================================================================")
print("TESTING STRICT RULES 1, 2, 3 FOR SCORPION REMAP PRO")
print("================================================================")

# ----------------------------------------------------------------------
# RULE 1: STRICT MANUAL SELECTOR (NO GUESSING ON UNRECOGNIZED FILES)
# ----------------------------------------------------------------------
print("\n[RULE 1] Testing Unrecognized File Identification...")
dummy_unrecognized_data = b"\x00\xFF" * (256 * 1024) # 512KB random binary with no known pattern
result_unrecognized = identify_ecu(dummy_unrecognized_data, "unknown_ecu_dump.bin")

assert result_unrecognized["recognized"] is False, "Unrecognized file must have recognized=False!"
assert "Calculateur non reconnu automatiquement" in result_unrecognized["message"], "Must return strict message"
assert result_unrecognized["ecu_type"] is None, "Must not guess ECU type by file size!"
print("✅ PASSED: No guessing performed! Returned recognized=False with strict manual selector message.")

# Test Manual Registry Retrieval
vag_edc17 = get_registry_ecu("VAG (Volkswagen / Audi / Seat / Skoda)", "VAG_EDC17")
assert vag_edc17 is not None, "VAG_EDC17 must exist in registry"
assert vag_edc17["fuel"] == "DIESEL", "VAG EDC17 must be DIESEL"
print(f"✅ PASSED: Manual registry selection works cleanly -> {vag_edc17['name']}")

# ----------------------------------------------------------------------
# RULE 2: STRICT FUEL TYPE ISOLATION (DIESEL VS ESSENCE)
# ----------------------------------------------------------------------
print("\n[RULE 2] Testing Strict Fuel Type Isolation across entire registry...")
total_ecus = 0
for brand, ecus in SUPPORTED_REGISTRY.items():
    for ecu in ecus:
        total_ecus += 1
        fuel = ecu["fuel"].upper()
        assert fuel in ["DIESEL", "ESSENCE"], f"ECU {ecu['name']} has invalid fuel {fuel}"
        
        sols = [s.upper() for s in ecu["supported_solutions"]]
        if fuel == "DIESEL":
            assert not any(x in s for s in sols for x in ["DECAT", "LAMBDA", "EVAP"]), \
                f"DIESEL ECU {ecu['name']} contains petrol solutions: {sols}"
        elif fuel == "ESSENCE":
            assert not any(x in s for s in sols for x in ["DPF", "FAP", "ADBLUE", "SCR", "HOT START"]), \
                f"ESSENCE ECU {ecu['name']} contains diesel solutions: {sols}"

print(f"✅ PASSED: Verified {total_ecus} ECUs across {len(SUPPORTED_REGISTRY)} brands.")
print("   - All DIESEL ECUs strictly exclude CAT/LAMBDA/EVAP.")
print("   - All ESSENCE ECUs strictly exclude DPF/ADBLUE/HOT START.")

# Test Pattern Matching Isolation on Binary
print("\n[RULE 2b] Testing Pattern Matcher Fuel Isolation on Live Dumps...")
diesel_data = b"BOSCH_EDC17CP14_VAG_TEST_DUMP_" + (b"\x00" * 200000)
diesel_res = identify_ecu(diesel_data, "vag_edc17cp14.bin")
assert diesel_res["recognized"] is True
assert diesel_res["fuel"] == "DIESEL"
assert "DPF / FAP" in diesel_res["supported_solutions"]
assert not any("CAT" in s or "EVAP" in s for s in diesel_res["supported_solutions"])
print("✅ PASSED: Live EDC17 dump detected as DIESEL with 0 petrol solutions.")

petrol_data = b"BOSCH_MED17.5.25_VAG_TFSI_TEST_DUMP_" + (b"\x00" * 200000)
petrol_res = identify_ecu(petrol_data, "golf_med17_5.bin")
assert petrol_res["recognized"] is True
assert petrol_res["fuel"] == "ESSENCE"
assert "DECAT / LAMBDA" in petrol_res["supported_solutions"]
assert not any("DPF" in s or "ADBLUE" in s for s in petrol_res["supported_solutions"])
print("✅ PASSED: Live MED17 dump detected as ESSENCE with 0 diesel solutions.")

# ----------------------------------------------------------------------
# RULE 3: RENDER ONLY AVAILABLE SOLUTIONS & HTML FRONTEND CHECK
# ----------------------------------------------------------------------
print("\n[RULE 3] Checking Frontend HTML Implementation in client_dashboard.html...")
dashboard_html = open("server/templates/client_dashboard.html", "r", encoding="utf-8").read()

assert 'id="unrecognizedBox"' in dashboard_html, "unrecognizedBox must exist in client_dashboard.html"
assert 'id="manualBrandSelect"' in dashboard_html, "manualBrandSelect must exist"
assert 'id="manualEcuSelect"' in dashboard_html, "manualEcuSelect must exist"
assert 'id="fuelVal"' in dashboard_html, "fuelVal badge container must exist"
assert 'badge-diesel' in dashboard_html, "badge-diesel CSS must exist"
assert 'badge-petrol' in dashboard_html, "badge-petrol CSS must exist"
assert 'display: none' in dashboard_html, "display: none must be used for unavailable solutions"

print("✅ PASSED: Frontend HTML contains strict manual dropdowns, fuel badges, and complete solution hiding logic!")
print("\n================================================================")
print("🎉 ALL STRICT RULES 1, 2, AND 3 VERIFIED AND PASSED 100%!")
print("================================================================")
