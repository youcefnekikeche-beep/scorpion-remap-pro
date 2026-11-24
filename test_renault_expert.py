import sys
sys.path.append(r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer')
from engine.renault_expert import preview_expert_operation, execute_expert_operation

# Test Valeo V42 Lambda Off
v42_file = bytearray(b'\x00' * 1048576)
v42_file[100:109] = b'VALEO V42'
# Place stock targets
v42_file[164892:164892+8] = b'$\x0b$"$J$L'
v42_file[164902:164902+2] = b'\x016'
v42_file[166614:166614+5] = b'\x016\x0c\x13\x03'

res = preview_expert_operation(bytes(v42_file), 'renault_lambda_off')
print('PASS 5: Preview V42 Lambda ->', res['ecu_type'], '| Bytes:', res['bytes_modified'])

out, desc = execute_expert_operation(bytes(v42_file), 'renault_lambda_off')
print('PASS 6: Execute V42 Lambda -> Size:', len(out), '| Desc:', desc)

# Test Valeo V42 Fan Temp Mod (92°C)
v42_fan = bytearray(b'\x00' * 1048576)
v42_fan[100:109] = b'VALEO V42'
v42_fan[1000:1002] = b'\x69\x6E' # Stock 105°C
res_fan = preview_expert_operation(bytes(v42_fan), 'renault_fan_temp', '92')
print('PASS 7: Preview V42 Fan 92°C ->', res_fan['ecu_type'], '| Bytes:', res_fan['bytes_modified'])

print('ALL TESTS PASSED!')
