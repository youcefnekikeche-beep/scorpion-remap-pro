import os
import sys

SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from engine.tuning_bridge import run_tuning_task, apply_svedit_hex_patches

test_in = r"C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\903e8e08dc914b278addf38d53c35bd4_Vw_Transporter_2.0_TDI_CR_Bosch_EDC17CP20-518078 nodpf.bin"
test_out = r"C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\processed\verify_solution_patches.bin"

if not os.path.exists(test_in):
    print("Test input not found!")
    sys.exit(1)

with open(test_in, "rb") as f:
    in_bytes = f.read()

solutions_to_apply = ["DPF", "EGR", "ADBLUE", "SWIRL", "TVA"]
print(f"Applying real solutions to test binary ({len(in_bytes)} bytes): {solutions_to_apply}")

res = run_tuning_task("process", test_in, test_out, solutions_to_apply)
print("Run tuning task result:", res)

with open(test_out, "rb") as f:
    out_bytes = f.read()

diffs = []
for i in range(len(in_bytes)):
    if in_bytes[i] != out_bytes[i]:
        diffs.append((i, in_bytes[i], out_bytes[i]))

print(f"\nTOTAL MODIFIED BYTES: {len(diffs)} bytes changed in the binary file!")
print("\nFirst 15 byte modifications (Offsets & Hex Before/After):")
for off, b_before, b_after in diffs[:15]:
    print(f"  Offset 0x{off:06X} | Original: 0x{b_before:02X} ({b_before:3}) ➔ Modified: 0x{b_after:02X} ({b_after:3})")
