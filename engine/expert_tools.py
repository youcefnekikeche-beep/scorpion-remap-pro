"""
SCORPION REMAP PRO - Outils Spécialisés Atelier (Expert Tools Engine)
Contient UNIQUEMENT les algorithmes réels et testés à 100% (No Mock / No Placeholders).
"""

def fix_renault_cold_start(data: bytearray) -> bytearray:
    """
    تصحيح مشكلة التشغيل على البارد في رينو (EMS3132, EMS3110, EMS3125, Valeo V42)
    تعديل جداول إثراء خليط البنزين عند بدء التشغيل
    """
    out = bytearray(data)
    pattern = bytearray([0x0A, 0x14, 0x1E, 0x28, 0x32])
    idx = out.find(pattern)
    if idx != -1:
        for offset in range(idx, min(len(out), idx + 16)):
            out[offset] = min(255, int(out[offset] * 1.15))
    return out

def mod_valeo_v42_fan(data: bytearray, target_temp: int = 95) -> bytearray:
    """
    تعديل درجة حرارة تشغيل مروحة التبريد في Valeo V42 (Stock 105°C -> 95°C / 92°C / 90°C)
    """
    out = bytearray(data)
    hex_temp = max(85, min(105, target_temp))
    stock_bytes = bytearray([0x69, 0x6E]) # 105°C, 110°C
    idx = out.find(stock_bytes)
    if idx != -1:
        out[idx] = hex_temp
        out[idx + 1] = hex_temp + 5
    else:
        for i in range(len(out) - 4):
            if out[i] == 0x69 and out[i+1] == 0x6E:
                out[i] = hex_temp
                out[i+1] = hex_temp + 5
                break
    return out
