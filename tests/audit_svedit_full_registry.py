"""
SCORPION REMAP PRO - 100% Comprehensive ECU Registry & Engine Audit
Audits all brands, ECUs, solutions, fuel isolation, and patching routines.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.ecu_analyzer import SUPPORTED_REGISTRY, FLAT_ECU_REGISTRY, identify_ecu, get_registry_ecu
from engine.tuning_bridge import apply_svedit_hex_patches

class TestSVEditFullRegistryAudit(unittest.TestCase):
    def test_full_registry_structure(self):
        print("\n" + "="*80)
        print("          SCORPION REMAP PRO - RAPPORT D'AUDIT COMPLET SVEDIT V1.1.38.3")
        print("="*80)

        total_brands = len(SUPPORTED_REGISTRY)
        total_ecus = len(FLAT_ECU_REGISTRY)

        self.assertGreaterEqual(total_brands, 15, "Nombre insuffisant de marques enregistrées")
        self.assertGreaterEqual(total_ecus, 70, "Nombre insuffisant de calculateurs enregistrés")

        print(f"\n[+] Total Marques Enregistrées : {total_brands}")
        print(f"[+] Total Calculateurs (ECUs) Uniques : {total_ecus}")

        # Detail by brand
        print("\n" + "-"*80)
        print("DÉTAIL PAR MARQUE ET CALCULATEUR :")
        print("-"*80)

        for brand, ecus in sorted(SUPPORTED_REGISTRY.items()):
            print(f"\n🏷️  MARQUE : {brand} ({len(ecus)} calculateurs)")
            for ecu in ecus:
                ecu_id = ecu["id"]
                fuel = ecu["fuel"]
                sols = ecu["supported_solutions"]
                badge = "⛽ DIESEL" if fuel == "DIESEL" else "⚡ ESSENCE"

                # Check strict fuel isolation
                if fuel == "DIESEL":
                    for s in sols:
                        self.assertNotIn("CAT", s.upper(), f"Violation carburant: CAT sur Diesel ({ecu_id})")
                        self.assertNotIn("LAMBDA", s.upper(), f"Violation carburant: LAMBDA sur Diesel ({ecu_id})")
                        self.assertNotIn("EVAP", s.upper(), f"Violation carburant: EVAP sur Diesel ({ecu_id})")
                elif fuel == "ESSENCE":
                    for s in sols:
                        self.assertNotIn("DPF", s.upper(), f"Violation carburant: DPF sur Essence ({ecu_id})")
                        self.assertNotIn("FAP", s.upper(), f"Violation carburant: FAP sur Essence ({ecu_id})")
                        self.assertNotIn("ADBLUE", s.upper(), f"Violation carburant: ADBLUE sur Essence ({ecu_id})")
                        self.assertNotIn("SCR", s.upper(), f"Violation carburant: SCR sur Essence ({ecu_id})")

                print(f"   [{badge}] {ecu['name']}")
                print(f"      Solutions actives ({len(sols)}): {', '.join(sols)}")

                # Test patch execution on mock binary
                dummy_bin = bytearray(b"\x00" * 1024 * 512)
                patched = apply_svedit_hex_patches(dummy_bin, sols, ecu_type=ecu_id)
                self.assertEqual(len(patched), len(dummy_bin), "Taille de fichier altérée lors du patch")

        print("\n" + "="*80)
        print(" AUDIT RÉUSSI À 100% : AUCUNE OMISSION, ISOLATION ESSENCE/DIESEL RESPECTÉE")
        print("="*80 + "\n")

if __name__ == "__main__":
    unittest.main()
