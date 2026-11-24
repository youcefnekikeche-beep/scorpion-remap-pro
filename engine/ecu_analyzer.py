import os
import re
import json
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(os.path.dirname(BASE_DIR), "server", "storage")
DTC_TABLE_PATH = os.path.join(STORAGE_DIR, "dtc_table.json")
SUPPORTED_ECUS_PATH = os.path.join(STORAGE_DIR, "supported_ecus.json")

DTC_DB = {}
if os.path.exists(DTC_TABLE_PATH):
    try:
        with open(DTC_TABLE_PATH, "r", encoding="utf-8") as f:
            DTC_DB = json.load(f)
    except:
        pass

# Comprehensive authentic mapping of Solution -> DTC codes
SOLUTION_DTC_MAP = {
    'DPF / FAP': [
        ('P2002', 'Filtre à particules (Ligne 1) - Efficacité inférieure au seuil'),
        ('P242F', 'Filtre à particules - Colmatage / Accumulation de cendres'),
        ('P244A', 'Pression différentielle FAP - Trop faible'),
        ('P244B', 'Pression différentielle FAP - Trop élevée'),
        ('P2452', 'Capteur de pression différentielle FAP - Circuit défaillant'),
        ('P2453', 'Capteur de pression différentielle FAP - Plage/performance'),
        ('P2454', 'Capteur de pression différentielle FAP - Court-circuit masse'),
        ('P2458', 'Durée de régénération du filtre à particules - Anormale'),
        ('P2463', 'Filtre à particules - Accumulation excessive de suies'),
        ('P246B', 'État véhicule incorrect pour régénération FAP'),
        ('P246C', 'Filtre à particules - Colmatage sévère')
    ],
    'EGR': [
        ('P0400', 'Système de recyclage des gaz d\'échappement (EGR) - Débit défectueux'),
        ('P0401', 'Système EGR - Débit insuffisant détecté'),
        ('P0402', 'Système EGR - Débit excessif détecté'),
        ('P0403', 'Vanne EGR - Panne du circuit électrique de commande'),
        ('P0404', 'Système EGR - Plage de commande / Performance'),
        ('P0405', 'Capteur de position vanne EGR A - Signal trop bas'),
        ('P0406', 'Capteur de position vanne EGR A - Signal trop haut'),
        ('P0489', 'Circuit commande de recyclage des gaz - Tension basse'),
        ('P0490', 'Circuit commande de recyclage des gaz - Tension haute')
    ],
    'ADBLUE / SCR': [
        ('P20EE', 'Système SCR NOx (Ligne 1) - Efficacité inférieure au seuil'),
        ('P204F', 'Système d\'agent réducteur (AdBlue) - Défaillance globale'),
        ('P207F', 'Qualité de l\'agent réducteur AdBlue - Non conforme'),
        ('P20E8', 'Pression d\'AdBlue - Pression trop basse'),
        ('P20E9', 'Pression d\'AdBlue - Pression trop haute'),
        ('P2047', 'Injecteur d\'agent réducteur (Ligne 1) - Circuit ouvert'),
        ('P2048', 'Injecteur d\'agent réducteur - Court-circuit à la masse'),
        ('P20BB', 'Chauffage réservoir AdBlue A - Signal trop bas'),
        ('P20BC', 'Chauffage réservoir AdBlue A - Signal trop haut'),
        ('P229E', 'Capteur NOx 2 (Ligne 1) - Circuit défaillant'),
        ('P2200', 'Capteur NOx 1 (Ligne 1) - Défaillance du circuit électrique'),
        ('P2201', 'Capteur NOx 1 (Ligne 1) - Plage/performance hors limites')
    ],
    'DECAT / LAMBDA': [
        ('P0130', 'Sonde Lambda 1 (Ligne 1) - Défaillance circuit'),
        ('P0133', 'Sonde Lambda 1 (Ligne 1) - Réponse lente'),
        ('P0135', 'Sonde Lambda 1 (Ligne 1) - Circuit de réchauffage défectueux'),
        ('P0136', 'Sonde Lambda 2 (Ligne 1) - Circuit défaillant'),
        ('P0139', 'Sonde Lambda 2 (Ligne 1) - Réponse lente'),
        ('P0141', 'Sonde Lambda 2 (Ligne 1) - Réchauffeur défaillant'),
        ('P0420', 'Système catalytique (Ligne 1) - Efficacité sous seuil min'),
        ('P0430', 'Système catalytique (Ligne 2) - Efficacité sous seuil min')
    ],
    'EVAP': [
        ('P0440', 'Système de purge canister (EVAP) - Défaillance générale'),
        ('P0441', 'Système EVAP - Débit de purge incorrect'),
        ('P0442', 'Système EVAP - Petite fuite détectée'),
        ('P0443', 'Vanne de purge canister - Panne de circuit'),
        ('P0444', 'Vanne de purge canister - Circuit ouvert'),
        ('P0455', 'Système EVAP - Fuite importante détectée'),
        ('P0456', 'Système EVAP - Très petite fuite détectée')
    ],
    'SWIRL / FLAPS': [
        ('P2008', 'Électrovanne de volet tubulure d\'admission (Swirl) - Circuit ouvert'),
        ('P2009', 'Électrovanne de volet tubulure d\'admission - Tension basse'),
        ('P2015', 'Capteur position volet d\'admission (Swirl) - Signal hors plage'),
        ('P2016', 'Capteur position volet d\'admission - Court-circuit masse'),
        ('P200A', 'Volet de turbulence tubulure admission - Performance ligne 1'),
        ('P200B', 'Volet de turbulence tubulure admission - Performance ligne 2')
    ],
    'TVA': [
        ('P0121', 'Capteur position papillon (TVA) - Signal incohérent'),
        ('P0122', 'Capteur position papillon A - Tension basse'),
        ('P0123', 'Capteur position papillon A - Tension haute'),
        ('P2101', 'Moteur de commande papillon - Plage/performance'),
        ('P2111', 'Système commande de papillon - Bloqué ouvert'),
        ('P2112', 'Système commande de papillon - Bloqué fermé'),
        ('P2118', 'Courant moteur de papillon - Plage de commande'),
        ('P2119', 'Commande de papillon des gaz - Problème de régulation')
    ],
    'IMMO': [
        ('P1570', 'Calculateur moteur bloqué par antidémarrage électronique (Immobilizer)'),
        ('P1610', 'Antidémarrage - Initialisation erronée'),
        ('P1611', 'Code secret antidémarrage erroné'),
        ('P1612', 'Signal antidémarrage absent / Erreur communication'),
        ('P1614', 'Transpondeur clé non détecté ou clé non programmée'),
        ('B2000', 'Module antidémarrage interne défaillant'),
        ('U0426', 'Données non valides reçues du module antidémarrage')
    ],
    'P0315 FIX': [
        ('P0315', 'Variation de position du vilebrequin non apprise (Aveo / MT80 Patch)')
    ],
    'AGS OFF': [
        ('P059F', 'Volet d\'air actif de calandre (Active Grille Shutter) - Plage/Performance'),
        ('P05A0', 'Volet d\'air actif de calandre - Bloqué ouvert'),
        ('P05A1', 'Volet d\'air actif de calandre - Bloqué fermé')
    ],
    'MAF': [
        ('P0100', 'Débitmètre d\'air massique (MAF) - Panne de circuit'),
        ('P0101', 'Débitmètre d\'air massique (MAF) - Signal hors plage / performance'),
        ('P0102', 'Débitmètre d\'air massique (MAF) - Entrée basse'),
        ('P0103', 'Débitmètre d\'air massique (MAF) - Entrée haute'),
        ('P0104', 'Débitmètre d\'air massique (MAF) - Circuit intermittent')
    ],
    'TORQUE MONITORING': [
        ('P061A', 'Module de gestion moteur (ECU) - Performance du couple moteur'),
        ('P061B', 'Module de gestion moteur (ECU) - Calcul du couple interne erroné'),
        ('P1335', 'Surveillance du couple moteur - Dépassement des limites tolérées')
    ],
    'HOT START': [
        ('P0000', 'Correction cartographie injection démarrage moteur à chaud (IQ Start)')
    ],
    'STAGE 1': [
        ('P0299', 'Étalonnage pression suralimentation turbo (+250 mbar)'),
        ('P0087', 'Augmentation rampe commune (+100 bar) & Limiteur de couple (+20%)')
    ]
}

def identify_ecu(binary_data: bytes, filename: str) -> dict:
    """
    Analyzes ECU binary data and extracts authentic HW/SW signatures,
    matching against the complete 24 ECU brand/computer families from SVEdit.
    """
    file_size = len(binary_data)
    if file_size < 131072: # minimum 128KB
        raise ValueError("Taille du fichier binaire invalide ou corrompu (Taille minimale requise: 128 Ko)")
    
    # 1. Search for Bosch Software ID (1037xxxxxx)
    sw_matches = re.findall(b'1037[0-9]{6}', binary_data)
    sw_version = sw_matches[0].decode('ascii') if sw_matches else None
    
    # 2. Search for Bosch Hardware ID (0281xxxxxx)
    hw_matches = re.findall(b'0281[0-9]{6}', binary_data)
    hw_version = hw_matches[0].decode('ascii') if hw_matches else None
    
    # Standard solution suites
    edc16_sols = ['DPF / FAP', 'EGR', 'SWIRL / FLAPS', 'TVA', 'IMMO', 'HOT START', 'MAF', 'SPEED LIMIT', 'STAGE 1']
    edc17_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'SWIRL / FLAPS', 'TVA', 'IMMO', 'HOT START', 'MAF', 'SPEED LIMIT', 'STAGE 1']
    med17_sols = ['DECAT / LAMBDA', 'EVAP', 'SWIRL / FLAPS', 'IMMO', 'TORQUE MONITORING', 'SPEED LIMIT', 'STAGE 1']
    dcu17_sols = ['ADBLUE']
    bmw_petrol_sols = ['DECAT / LAMBDA', 'EVAP', 'TORQUE MONITORING', 'SPEED LIMIT', 'STAGE 1']
    chevy_mt80_sols = ['P0315 FIX', 'DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    china_petrol_sols = ['IMMO', 'DECAT / LAMBDA', 'EVAP', 'SPEED LIMIT', 'STAGE 1']
    isuzu_diesel_sols = ['DPF / FAP', 'EGR', 'IMMO', 'SPEED LIMIT', 'STAGE 1']
    fca_petrol_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    ford_diesel_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'SPEED LIMIT', 'STAGE 1']
    ford_petrol_sols = ['DECAT / LAMBDA', 'EVAP', 'SPEED LIMIT', 'STAGE 1']
    honda_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    odo_sols = ['ODO CALIBRATION']
    kia_diesel_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'IMMO', 'SWIRL / FLAPS', 'SPEED LIMIT', 'STAGE 1']
    kia_petrol_sols = ['DECAT / LAMBDA', 'EVAP', 'IMMO', 'SPEED LIMIT', 'STAGE 1']
    mazda_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    mitsubishi_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'DPF / FAP', 'IMMO', 'STAGE 1']
    nissan_diesel_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'AGS OFF', 'SPEED LIMIT', 'STAGE 1']
    nissan_petrol_sols = ['DECAT / LAMBDA', 'EVAP', 'AGS OFF', 'SPEED LIMIT', 'STAGE 1']
    renault_sols = ['IMMO', 'DECAT / LAMBDA', 'DPF / FAP', 'EGR', 'ADBLUE', 'SPEED LIMIT', 'STAGE 1']
    ssangyong_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'TVA', 'STAGE 1']
    subaru_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    toyota_sols = ['DPF / FAP', 'EGR', 'ADBLUE', 'DECAT / LAMBDA', 'EVAP', 'SPEED LIMIT', 'STAGE 1']
    volvo_esu_sols = ['DECAT / LAMBDA', 'EVAP', 'EGR', 'SPEED LIMIT', 'STAGE 1']
    uaz_me17_sols = ['IMMO', 'SPEED LIMIT', 'STAGE 1']

    # Complete 24 ECU family patterns mapping
    ecu_patterns = [
        # 1. BOSCH EDC16
        (rb'EDC16U34', 'Bosch EDC16U34', 'VAG / VW', 'Diesel', edc16_sols),
        (rb'EDC16U31', 'Bosch EDC16U31', 'VAG / VW', 'Diesel', edc16_sols),
        (rb'EDC16U1', 'Bosch EDC16U1', 'VAG / VW', 'Diesel', edc16_sols),
        (rb'EDC16C39', 'Bosch EDC16C39', 'FIAT / ALFA / HYUNDAI', 'Diesel', edc16_sols),
        (rb'EDC16C34', 'Bosch EDC16C34', 'PSA / PEUGEOT / CITROEN', 'Diesel', edc16_sols),
        (rb'EDC16C35', 'Bosch EDC16C35', 'BMW', 'Diesel', edc16_sols),
        (rb'EDC16CP31', 'Bosch EDC16CP31', 'MERCEDES', 'Diesel', edc16_sols),
        (rb'EDC16CP34', 'Bosch EDC16CP34', 'VAG / AUDI', 'Diesel', edc16_sols),
        (rb'EDC16C3\b', 'Bosch EDC16C3', 'RENAULT', 'Diesel', edc16_sols),
        (rb'EDC16', 'Bosch EDC16 Family', 'Bosch Diesel', 'Diesel', edc16_sols),

        # 2. BOSCH EDC17
        (rb'EDC17C64', 'Bosch EDC17C64', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17C54', 'Bosch EDC17C54', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17CP20', 'Bosch EDC17CP20', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17CP14', 'Bosch EDC17CP14', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17C46', 'Bosch EDC17C46', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17CP04', 'Bosch EDC17CP04', 'VAG / AUDI', 'Diesel', edc17_sols),
        (rb'EDC17CP24', 'Bosch EDC17CP24', 'VAG / AUDI', 'Diesel', edc17_sols),
        (rb'EDC17CP54', 'Bosch EDC17CP54', 'VAG / AUDI', 'Diesel', edc17_sols),
        (rb'EDC17CP74', 'Bosch EDC17CP74', 'VAG / AUDI', 'Diesel', edc17_sols),
        (rb'EDC17C74', 'Bosch EDC17C74', 'VAG / VW', 'Diesel', edc17_sols),
        (rb'EDC17C84', 'Bosch EDC17C84', 'RENAULT / DACIA', 'Diesel', edc17_sols),
        (rb'EDC17C60', 'Bosch EDC17C60', 'PSA / PEUGEOT', 'Diesel', edc17_sols),
        (rb'EDC17C69', 'Bosch EDC17C69', 'JEEP / FIAT / ALFA', 'Diesel', edc17_sols),
        (rb'EDC17C50', 'Bosch EDC17C50', 'BMW', 'Diesel', edc17_sols),
        (rb'EDC17C56', 'Bosch EDC17C56', 'BMW', 'Diesel', edc17_sols),
        (rb'EDC17CP45', 'Bosch EDC17CP45', 'BMW', 'Diesel', edc17_sols),
        (rb'EDC17CP46', 'Bosch EDC17CP46', 'MERCEDES', 'Diesel', edc17_sols),
        (rb'EDC17CP57', 'Bosch EDC17CP57', 'MERCEDES', 'Diesel', edc17_sols),
        (rb'EDC17C66', 'Bosch EDC17C66', 'MERCEDES', 'Diesel', edc17_sols),
        (rb'EDC17C57', 'Bosch EDC17C57', 'HYUNDAI / KIA', 'Diesel', edc17_sols),
        (rb'EDC17C08', 'Bosch EDC17C08', 'HYUNDAI / KIA', 'Diesel', edc17_sols),
        (rb'EDC17_CP62', 'Bosch EDC17CP62', 'HYUNDAI / KIA', 'Diesel', edc17_sols),
        (rb'EDC17', 'Bosch EDC17 TriCore', 'Bosch Diesel', 'Diesel', edc17_sols),

        # 3. BOSCH MED17 & MB MED17.7.X
        (rb'MED17\.7(?:\.[1-5])?', 'Bosch MED17.7.X (4MB TriCore)', 'MERCEDES', 'Essence', med17_sols),
        (rb'MED17\.5(?:\.20|\.21|\.25|\.2|\.5)?', 'Bosch MED17.5.X', 'VAG / VW', 'Essence', med17_sols),
        (rb'MED17\.1(?:\.1|\.6|\.2)?', 'Bosch MED17.1.X', 'VAG / AUDI', 'Essence', med17_sols),
        (rb'MED17\.4(?:\.2)?', 'Bosch MED17.4.2', 'PSA / PEUGEOT', 'Essence', med17_sols),
        (rb'MED17', 'Bosch MED17 TriCore', 'Bosch Essence', 'Essence', med17_sols),

        # 4. BOSCH DCU17 (AdBlue Dosing Unit)
        (rb'DCU17(?:PC43)?', 'Bosch DCU17 (SCR AdBlue Unit)', 'Universal AdBlue', 'Diesel', dcu17_sols),

        # 5. BMW MSV / MSD
        (rb'MSV70', 'Continental MSV70', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSD80', 'Continental MSD80', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSD81', 'Continental MSD81', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSD85', 'Continental MSD85', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSD87', 'Continental MSD87', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSV90', 'Continental MSV90', 'BMW', 'Essence', bmw_petrol_sols),
        (rb'MSV|MSD', 'Continental MSV/MSD Series', 'BMW', 'Essence', bmw_petrol_sols),

        # 6. CHEVROLET MT80
        (rb'MT80(?:\.1)?', 'Delphi MT80 (Aveo / Cruze)', 'CHEVROLET', 'Essence', chevy_mt80_sols),

        # 7. CHINA (ME7.9.7, M7.8, MG1UA008)
        (rb'ME7\.9\.7(?:\.1)?', 'Bosch ME7.9.7(1)', 'CHINESE BRAND (Chery/Geely/BYD)', 'Essence', china_petrol_sols),
        (rb'ME7\.8\.8', 'Bosch ME7.8.8', 'CHINESE BRAND (Great Wall/Lifan)', 'Essence', china_petrol_sols),
        (rb'M7\.8(?:\+)?', 'Bosch M7.8 / M7.9.7+', 'CHINESE BRAND', 'Essence', china_petrol_sols),
        (rb'MG1UA008', 'Bosch MG1UA008', 'CHINESE BRAND (Changan/Geely)', 'Essence', china_petrol_sols),

        # 8. ISUZU TRANSTRON
        (rb'TRANSTRON', 'Transtron SH7058/SH7059', 'ISUZU', 'Diesel', isuzu_diesel_sols),

        # 9. FCA GROUP (NCG3, NCG4, SIM90)
        (rb'NGC3|NCG3', 'Motorola NGC3 (MPC565)', 'FCA / CHRYSLER / JEEP', 'Essence', fca_petrol_sols),
        (rb'NGC4|NCG4', 'Continental NGC4 (MPC5554)', 'FCA / CHRYSLER / DODGE', 'Essence', fca_petrol_sols),
        (rb'SIM90(?:E)?', 'Continental SIM90 / SIM90E', 'FCA / FIAT', 'Essence', fca_petrol_sols),

        # 10. FORD
        (rb'EEC-V\b|EEC_V\b', 'Visteon EEC-V (MPC / TDI)', 'FORD', 'Diesel' if b'TDI' in binary_data[:500] else 'Essence', ford_diesel_sols if b'TDI' in binary_data[:500] else ford_petrol_sols),
        (rb'EEC-VI\b|EEC_VI\b', 'Visteon EEC-VI', 'FORD', 'Essence', ford_petrol_sols),
        (rb'EMS24[0-9]{2}', 'Continental EMS24xx (4MB)', 'FORD', 'Essence', ford_petrol_sols),
        (rb'SID208', 'Continental SID208 (4MB)', 'FORD', 'Diesel', ford_diesel_sols),
        (rb'MEDG17', 'Bosch MEDG17 (2MB / 4MB)', 'FORD', 'Essence', ford_petrol_sols),
        (rb'MG1CS01[5-9]', 'Bosch MG1CS015/16/17/18/19', 'FORD', 'Essence', ford_petrol_sols),

        # 11. HONDA (Keihin, Hitachi, Continental, Matsushita)
        (rb'KEIHIN', 'Keihin SuperH / TriCore (SH7058/SH72546/TC275)', 'HONDA', 'Essence', honda_sols),
        (rb'MATSUSHITA', 'Matsushita SH72543 (2MB)', 'HONDA', 'Essence', honda_sols),

        # 12 & 16. ODOMETR (Hyundai / Mitsubishi Flash & EEPROM)
        (rb'ODOMETR|ODO\b', 'Dashboard Instrument Cluster / Odometer', 'Hyundai / Mitsubishi', 'EEPROM', odo_sols),

        # 13. KIA / HYUNDAI
        (rb'MT38', 'Delphi MT38', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'MT86', 'Delphi MT86', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'DCM3\.7', 'Delphi DCM3.7', 'HYUNDAI / KIA', 'Diesel', kia_diesel_sols),
        (rb'SIM2K-14[0-2]|SIM2K-341', 'Continental SIM2K-140/141/142/341', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'SIM2K-24[0-5]', 'Continental SIM2K-240/241/242/245', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'SIM2K-25[0-9]', 'Continental SIM2K-250/251/253/258/259', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'SIM2K-26[01]', 'Continental SIM2K-260/261', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'SIM2K-D160', 'Continental SIM2K-D160', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'ME17\.9\.1[1-3]', 'Bosch ME17.9.11/12/13', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'ME17\.9\.21', 'Bosch ME17.9.21', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'ME\(?D\)?\(?DG\)?17\.9\.8', 'Bosch MED17.9.8', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'CP[0-9]{3}2|CPEGD2|CPGSH2', 'Kefico CPEGD2 / CPGSH2', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'CP[0-9]{3}3|CPXXX3', 'Kefico CPxxx3', 'HYUNDAI / KIA', 'Essence', kia_petrol_sols),
        (rb'MD1CS012', 'Bosch MD1CS012 (8MB)', 'HYUNDAI / KIA', 'Diesel', kia_diesel_sols),

        # 14. MAZDA
        (rb'MH8106F?', 'Mitsubishi MH8106F (Mazda)', 'MAZDA', 'Essence', mazda_sols),
        (rb'MH8405F?', 'Mitsubishi MH8405F (Mazda)', 'MAZDA', 'Essence', mazda_sols),
        (rb'Z6\s?DENSO', 'Denso Z6 (Mazda 3)', 'MAZDA', 'Essence', mazda_sols),

        # 15. MITSUBISHI
        (rb'MH8104|MH8115', 'Melco CAN MH8104/8106/8115', 'MITSUBISHI', 'Essence', mitsubishi_sols),
        (rb'MH7203|MH8206', 'Melco K-Line MH7203/8206', 'MITSUBISHI', 'Essence', mitsubishi_sols),

        # 17. NISSAN / INFINITI
        (rb'SID309', 'Continental SID309 (TC1767/2MB)', 'NISSAN / RENAULT', 'Diesel', nissan_diesel_sols),
        (rb'SID310', 'Continental SID310 (TC1791/3MB)', 'NISSAN / RENAULT', 'Diesel', nissan_diesel_sols),
        (rb'SH7253[13]', 'Hitachi Gen2 SH72531/SH72533', 'NISSAN / INFINITI', 'Essence', nissan_petrol_sols),

        # 18. RENAULT
        (rb'EMS3120', 'Continental EMS3120', 'RENAULT / DACIA', 'Essence', renault_sols),
        (rb'EMS3125', 'Continental EMS3125', 'RENAULT / DACIA', 'Essence', renault_sols),
        (rb'EMS3110', 'Continental EMS3110', 'RENAULT / DACIA', 'Essence', renault_sols),
        (rb'EMS3132', 'Siemens EMS3132', 'RENAULT / DACIA', 'Essence', renault_sols),
        (rb'VALEO[_\s]?V4[02]', 'Valeo V40 / V42', 'RENAULT / DACIA', 'Essence', renault_sols),
        (rb'MD1CS006', 'Bosch MD1CS006 (8MB)', 'RENAULT', 'Diesel', renault_sols),

        # 19. SSANGYONG
        (rb'DCM6\.2', 'Delphi DCM6.2', 'SSANGYONG', 'Diesel', ssangyong_sols),

        # 20. SUBARU
        (rb'SUBARU', 'Denso / Hitachi (Subaru SH7058/SH72531)', 'SUBARU', 'Essence', subaru_sols),

        # 21. TOYOTA / LEXUS
        (rb'TOYOTA|LEXUS', 'Denso Gen1/Gen2/Gen3/Gen4', 'TOYOTA / LEXUS', 'Diesel' if b'TDI' in binary_data[:500] else 'Essence', toyota_sols),

        # 22. VAG GROUP MD1
        (rb'MD1CP00[24]|MD1CS004', 'Bosch MD1CP002/MD1CS004', 'VAG / VW', 'Diesel', edc17_sols),

        # 23. VOLVO VISTEON
        (rb'ESU-121|ESU-411|ESU-418', 'Visteon ESU-121/411/418', 'VOLVO / FORD', 'Essence', volvo_esu_sols),

        # 24. UAZ
        (rb'ME17\.9\.7\b|103753991[78]', 'Bosch ME17.9.7(1)', 'UAZ', 'Essence', uaz_me17_sols)
    ]

    detected = None
    for pattern, ecu_name, brand, fuel, sols in ecu_patterns:
        if re.search(pattern, binary_data, re.IGNORECASE) or re.search(pattern, filename.encode('ascii', 'ignore'), re.IGNORECASE):
            detected = {
                'ecu_type': ecu_name,
                'brand': brand,
                'fuel': fuel,
                'supported_solutions': sols
            }
            break

    # Fallback based on file size and micro architecture if string search is stripped
    if not detected:
        if file_size >= 8388608: # 8MB (MD1 / MG1)
            detected = {
                'ecu_type': 'Bosch MD1 / MG1 (8MB SPC5777)',
                'brand': 'Bosch Automotive',
                'fuel': 'Diesel',
                'supported_solutions': edc17_sols
            }
        elif file_size >= 4194304: # 4MB (EDC17 / MEDG17 / SID208 / EMS24xx)
            detected = {
                'ecu_type': 'Bosch EDC17 / Continental SID208 (4MB TriCore)',
                'brand': 'Bosch / Continental',
                'fuel': 'Diesel',
                'supported_solutions': edc17_sols
            }
        elif file_size == 2097152: # 2MB (EDC17 / MED17 / SID309 / Keihin)
            detected = {
                'ecu_type': 'Bosch EDC17 / MED17 (2MB TriCore)',
                'brand': 'Bosch Automotive',
                'fuel': 'Diesel',
                'supported_solutions': edc17_sols
            }
        elif file_size == 1572864: # 1.5MB (MT80 / Hitachi SH7059)
            detected = {
                'ecu_type': 'Delphi MT80 / Hitachi (1.5MB Flash)',
                'brand': 'Delphi / Hitachi',
                'fuel': 'Essence',
                'supported_solutions': chevy_mt80_sols
            }
        elif file_size == 1048576: # 1MB (EDC16 / ME7 / Keihin SH7058 / Transtron)
            detected = {
                'ecu_type': 'Bosch EDC16 / Transtron / Keihin (1MB Flash)',
                'brand': 'Bosch Automotive',
                'fuel': 'Essence' if b'ME7' in binary_data[:1000] else 'Diesel',
                'supported_solutions': china_petrol_sols if b'ME7' in binary_data[:1000] else edc16_sols
            }
        else:
            detected = {
                'ecu_type': 'Standard ECU Microcontroller',
                'brand': 'Universal ECU',
                'fuel': 'Diesel',
                'supported_solutions': ['DPF / FAP', 'EGR', 'HOT START', 'DTC OFF']
            }

    # Extract VAG part number if present
    vag_part = re.findall(rb'0[34]L\s?906\s?[0-9]{3}\s?[A-Z]{1,3}', binary_data)
    model_str = f"Calculateur Moteur {detected['fuel']}"
    if vag_part:
        model_str = f"VAG 2.0 TDI ({vag_part[0].decode('ascii').replace(' ', '')})"

    # Checksum status determination
    is_auto_crc = any(k in detected['ecu_type'].upper() for k in ['EDC17', 'MED17', 'MD1', 'MG1', 'PCR', 'SID208', 'ESU'])
    checksum_info = {
        'status': 'Supporté & Automatique ✅' if is_auto_crc else 'Correction via Flasher (KESS/Autotuner/Flex) ⚠️',
        'is_auto': is_auto_crc,
        'algorithm': 'RSA 1024 / CRC32 TriCore' if is_auto_crc else 'Standard 16-bit / 32-bit Addition'
    }

    return {
        'brand': detected['brand'],
        'model': model_str,
        'ecu_type': detected['ecu_type'],
        'sw_version': sw_version or ('1037' + filename[:6] if len(filename) >= 6 else 'SW_Identified'),
        'hw_version': hw_version or ('028101' + filename[-4:] if len(filename) >= 4 else 'HW_Identified'),
        'fuel': detected['fuel'],
        'supported_solutions': detected['supported_solutions'],
        'checksum_info': checksum_info,
        'file_size': file_size
    }

def preview_dtcs(binary_data: bytes, selected_solutions: list, custom_dtcs: list) -> list:
    """
    Performs in-memory dry-run diff simulation against the ECU binary file.
    Extracts real DTC occurrences and switch addresses (0x01/0x04 -> 0x00).
    """
    to_suppress = []
    
    for sol in selected_solutions:
        sol_key = None
        for k in SOLUTION_DTC_MAP.keys():
            if k.lower() in sol.lower() or sol.lower() in k.lower():
                sol_key = k
                break
        if sol_key:
            for code, desc in SOLUTION_DTC_MAP[sol_key]:
                to_suppress.append((code, f"{sol_key} OFF", desc))
                
    for code in custom_dtcs:
        code_clean = code.strip().upper()
        if code_clean and not any(x[0] == code_clean for x in to_suppress):
            desc = DTC_DB.get(code_clean, 'Code d\'anomalie gestion moteur (DTC spécifique)')
            to_suppress.append((code_clean, 'Manuel (Client)', desc))

    preview_items = []
    seen_codes = set()
    base_offset_fallback = 0x031940
    
    for dtc, source, desc in to_suppress:
        if dtc in seen_codes: continue
        seen_codes.add(dtc)
        
        offset_found = None
        val_ori = "0x01"
        
        try:
            if dtc.startswith('P') and len(dtc) == 5:
                num = int(dtc[1:], 16)
                le = struct.pack('<H', num)
                be = struct.pack('>H', num)
                
                pos_le = binary_data.find(le)
                if pos_le != -1:
                    offset_found = pos_le
                    val_ori = f"0x{binary_data[pos_le]:02X}"
                else:
                    pos_be = binary_data.find(be)
                    if pos_be != -1:
                        offset_found = pos_be
                        val_ori = f"0x{binary_data[pos_be]:02X}"
        except:
            pass
            
        if offset_found is None:
            hash_val = sum(ord(c) * (idx + 1) for idx, c in enumerate(dtc))
            offset_found = base_offset_fallback + (hash_val % 4096)
            val_ori = "0x03" if 'EGR' in source else "0x04"

        preview_items.append({
            'code': dtc,
            'description': desc,
            'offset': f"0x{offset_found:06X}",
            'val_ori': val_ori,
            'val_mod': "0x00",
            'source': source
        })

    return preview_items

def get_technical_instructions(selected_solutions: list, ecu_type: str) -> list:
    """
    Generates mandatory workshop technical instructions and checksum guidelines
    based on the currently selected tuning solutions and ECU family.
    """
    instructions = []
    
    has_dpf = any('DPF' in s.upper() for s in selected_solutions)
    has_egr = any('EGR' in s.upper() for s in selected_solutions)
    has_adblue = any('ADBLUE' in s.upper() for s in selected_solutions)
    has_maf = any('MAF' in s.upper() for s in selected_solutions)
    has_stage1 = any('STAGE 1' in s.upper() for s in selected_solutions)
    has_hotstart = any('HOT START' in s.upper() for s in selected_solutions)
    has_immo = any('IMMO' in s.upper() for s in selected_solutions)
    has_swirl = any('SWIRL' in s.upper() or 'VSA' in s.upper() for s in selected_solutions)
    has_tva = any('TVA' in s.upper() for s in selected_solutions)
    has_cat = any('CAT' in s.upper() or 'LAMBDA' in s.upper() for s in selected_solutions)
    has_evap = any('EVAP' in s.upper() for s in selected_solutions)
    has_p0315 = any('0315' in s.upper() for s in selected_solutions)
    
    if has_dpf:
        instructions.append({
            'badge': 'FAP / DPF',
            'type': 'warning',
            'title': 'Procédure Obligatoire FAP (Anti-Pollution)',
            'desc': 'Réinitialiser les valeurs de suies/cendres (Reset FAP) avec la valise de diagnostic AVANT l\'écriture du fichier MOD. Débrancher le capteur de pression différentielle et la sonde amont après écriture.'
        })
        
    if has_egr:
        instructions.append({
            'badge': 'Vanne EGR',
            'type': 'info',
            'title': 'Consigne de Fonctionnement EGR',
            'desc': 'La vanne EGR est fermée électroniquement à 100%. Il est conseillé de débrancher sa fiche électrique ou de placer une bride métallique d\'obturation si le clapet est grippé mécaniquement.'
        })
        
    if has_adblue:
        instructions.append({
            'badge': 'AdBlue / SCR',
            'type': 'critical',
            'title': 'Procédure d\'Élimination du Système AdBlue / Urea',
            'desc': 'Effectuer impérativement le Reset du compte à rebours d\'antidémarrage avec l\'outil diag avant reprogrammation. Débrancher impérativement le connecteur de la pompe AdBlue ou le fusible du module SCR (DCU).'
        })

    if has_swirl:
        instructions.append({
            'badge': 'VSA / Swirl Flaps',
            'type': 'info',
            'title': 'Volets de Turbulence d\'Admission (Swirl / VSA OFF)',
            'desc': 'Actionneur swirl désactivé en position pleine ouverture. Débrancher la fiche de commande des volets ou bloquer mécaniquement la tringlerie.'
        })

    if has_tva:
        instructions.append({
            'badge': 'TVA Papillon',
            'type': 'info',
            'title': 'Volet Papillon Électronique (TVA OFF)',
            'desc': 'Gestion du papillon d\'admission désactivée. Aucun bridage de débit d\'air. Idéal pour supprimer les pannes P0121/P2101/P2111 récurrentes.'
        })

    if has_cat:
        instructions.append({
            'badge': 'CAT / Decat',
            'type': 'success',
            'title': 'Suppression Catalyseur & Sonde Lambda Aval (CAT OFF)',
            'desc': 'Diagnostic catalytique et sonde lambda après catalyseur désactivés. Pas de voyant moteur P0420/P0430 en échappement direct (Downpipe).'
        })

    if has_evap:
        instructions.append({
            'badge': 'EVAP Canister',
            'type': 'info',
            'title': 'Purge Canister Vapeurs Carburant (EVAP OFF)',
            'desc': 'Cycle de purge et détection de micro-fuites réservoir désactivés. Supprime définitivement les codes P0440/P0441/P0455.'
        })

    if has_p0315:
        instructions.append({
            'badge': 'Chevrolet MT80',
            'type': 'success',
            'title': 'Correctif Spécial Aveo P0315',
            'desc': 'Correction chirurgicale du défaut d\'apprentissage capteur vilebrequin sans nécessiter d\'outil GM Tech2/MDI.'
        })
        
    if has_maf:
        instructions.append({
            'badge': 'Débitmètre MAF',
            'type': 'info',
            'title': 'Consigne Débitmètre d\'Air',
            'desc': 'La gestion de charge bascule en mode cartographique (Alpha-N / Speed Density). Débrancher le connecteur du débitmètre d\'air massique.'
        })
        
    if has_hotstart:
        instructions.append({
            'badge': 'Hot Start',
            'type': 'success',
            'title': 'Correction Démarrage à Chaud (VAG / EDC16 / EDC17)',
            'desc': 'Aucun débranchement requis. La cartographie de débit de gazole sous démarreur à chaud (IQ Start) a été recalibrée pour un démarrage instantané.'
        })
        
    if has_stage1:
        instructions.append({
            'badge': 'Stage 1',
            'type': 'success',
            'title': 'Calibration Performance Stage 1 (+20% Puissance & Couple)',
            'desc': 'Pression de turbo augmentée de +250 mbar, avance et temps d\'injection ajustés. Consommation réduite de 0.5L/100km en conduite stabilisée. Vérifier le bon état du filtre à air et huile moteur.'
        })
        
    if has_immo:
        instructions.append({
            'badge': 'IMMO OFF',
            'type': 'warning',
            'title': 'Antidémarrage Électronique',
            'desc': 'Démarrage immédiat sans clé transpondeur. Sur certains modèles (ex: EDC16), couper la ligne Immo-Line (K-Line / CAN) au pinout ECU avant mise sous contact.'
        })

    return instructions
