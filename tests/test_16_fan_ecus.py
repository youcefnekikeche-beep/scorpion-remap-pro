import sys
import os
import struct

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.renault_expert import (
    FAN_ECU_DATABASE,
    preview_expert_operation,
    execute_expert_operation
)

def run_tests():
    print("Testing all 16 ECU families for Renault Fan Temp Mod...")
    all_passed = True

    for ecu_key, cfg in FAN_ECU_DATABASE.items():
        # Determine file size to test
        size = 1048576 # 1MB standard
        if ecu_key == "EMS3132":
            size = 262144
        elif ecu_key in ("EDC16CP33", "EDC17C42", "EMS3120"):
            size = 2097152

        dummy = bytearray(b"\x00" * size)

        # Inject standard signature or static offset with stock temperature e.g. 98°C
        stock_temp = 98
        stock_raw = cfg["formula_write"](stock_temp)
        fmt = cfg["type"]
        val_size = cfg["size"]

        if fmt == "8bit":
            packed = struct.pack("B", stock_raw % 256)
        elif fmt == "16bit_le":
            packed = struct.pack("<H", stock_raw)
        elif fmt == "16bit_be":
            packed = struct.pack(">H", stock_raw)

        # Put at static offset or signature
        injected = False
        if cfg.get("static_offsets"):
            off = cfg["static_offsets"][0]
            if off + len(packed) <= len(dummy):
                dummy[off:off+len(packed)] = packed
                injected = True
        
        if not injected and cfg.get("signatures"):
            sig, offset = cfg["signatures"][0]
            pos = 1000
            dummy[pos:pos+len(sig)] = sig
            dummy[pos+offset:pos+offset+len(packed)] = packed
            injected = True

        if not injected:
            # Fallback for V42 pattern
            dummy[163976:163978] = packed

        # Test preview with protocol override
        try:
            prev = preview_expert_operation(bytes(dummy), "renault_fan_temp", "90", f"test_{ecu_key}.bin", ecu_key)
            assert prev["bytes_modified"] > 0
            # Test execute
            mod_data, desc = execute_expert_operation(bytes(dummy), "renault_fan_temp", "90", f"test_{ecu_key}.bin", ecu_key)
            assert len(mod_data) == len(dummy)
            print(f"  [OK] Protocol {ecu_key:10s} -> Stock: {prev.get('current_temp')}°C -> Target: 90°C -> Mod: {prev['bytes_modified']} bytes | {desc}")
        except Exception as e:
            print(f"  [FAIL] Protocol {ecu_key}: {e}")
            all_passed = False

    if all_passed:
        print("\nALL 16 PROTOCOLS PASSED VALIDATION WITH FLYING COLORS!")
    else:
        print("\nSOME PROTOCOLS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
