/**
 * SCORPION REMAP PRO V3.2.0 - Internationalization Dictionary (i18n)
 * Languages: French (fr), English (en), Arabic (ar)
 * Technical automotive keywords (DPF/FAP, EGR, AdBlue/SCR, IMMO, Stage 1/2, DTC, etc.) are strictly preserved.
 */

window.APP_TRANSLATIONS = {
  fr: {
    brand_badge: "PRO v3.2.0",
    nav: {
      studio: "🛠️ Studio Remap",
      expert: "🧰 Outils Expert",
      flexfuel: "🌿 FlexFuel E85",
      catalog: "📚 Catalogue",
      history: "📜 Historique",
      credits: "💳 Forfaits Crédits",
      changelog: "📋 Changelog",
      my_tickets: "🎫 Mes Signalements",
      admin: "⚙️ Administration",
      donate: "Faire un Don",
      connecting: "Connexion...",
      tester_badge: "TESTEUR PRO",
      credits_label: "Crédits",
      switch_account: "Changer de compte"
    },
    announcement: {
      action_required: "Action requise :",
      profile_completion: "Sécurisez votre atelier avec votre adresse e-mail et un mot de passe personnel pour sauvegarder vos crédits et recevoir le lien permanent du serveur.",
      secure_account_btn: "🔒 Sécuriser mon compte",
      view_changelog: "📋 Voir le Changelog →"
    },
    sim2k_promo: {
      badge_hot: "🔥 EXCLUSIF & EN LIGNE",
      badge_ecu: "CONTINENTAL SIM2K-510",
      badge_models: "KIA & HYUNDAI 2021–2026",
      title: "NOUVEAUTÉ EN LIGNE : CONTINENTAL SIM2K-510 (KIA & HYUNDAI 2021–2026)",
      features_html: "<strong>Pack Full Tout-en-Un :</strong> AdBlue OFF + Start & Stop OFF + OPF/GPF OFF + EGR OFF + Decat/Lambda OFF.",
      instant_text: "⚡ Paiement direct sécurisé : 120,00 € (Stripe) ou 35 000 DZD (Edahabia / CIB). Téléchargement instantané en 30 secondes.",
      btn_cta: "📤 Glisser un fichier SIM2K-510 maintenant →"
    },
    studio: {
      drop_title: "Glissez-déposez votre fichier binaire ECU (.bin, .ori)",
      drop_subtitle: "Ou cliquez pour parcourir vos fichiers (Continental SID, Bosch EDC16/17/MD1, Delphi, Marelli...)",
      file_analyzed: "Fichier Analysé",
      detected_ecu: "Marque / Calculateur Détecté",
      high_confidence: "Haute Compatibilité",
      medium_confidence: "Compatibilité Moyenne",
      change_file: "🔄 Changer de fichier",
      fuel_detecting: "⛽ Moteur : Détection...",
      fuel_diesel: "⛽ Moteur : Diesel (HDi / TDI / dCi / CRDi)",
      fuel_gasoline: "⛽ Moteur : Essence / Turbo Essence",
      report_detection_error: "⚠️ Erreur de détection ? Signaler",
      unknown_title: "CALCULATEUR NON RECONNU AUTOMATIQUEMENT",
      unknown_desc: "Le dump est marqué comme \"Unknown\". Les modifications sont bloquées pour éviter toute erreur.<br><span style=\"color:#fde047; font-weight:700;\">👉 Vous devez obligatoirement sélectionner votre marque et le modèle exact de calculateur</span> dans le cadre ci-dessous pour déverrouiller le patch.",
      adjust_label: "⚙️ Ajuster si nécessaire :",
      brand_label: "Marque",
      ecu_label: "Calculateur (ECU)",
      select_options_title: "⚙️ Sélectionnez les modifications à appliquer",
      custom_dtc_title: "⚠️ Suppression de Codes Défauts DTC Sur-Mesure",
      custom_dtc_btn: "🔍 Examiner la Table DTC (ON / OFF)",
      custom_dtc_desc: "Entrez n'importe quel code OBD-II (ex: P20EE, P2201, P0420) ou ouvrez l'afficheur interactif ci-dessus pour inspecter l'état actuel de la table DTC du dump.",
      custom_dtc_placeholder: "Exemple : P20EE, P2201, P0420",
      total_required: "Total Requis :",
      current_balance: "Solde actuel :",
      btn_process: "⚡ Patcher & Générer (.MOD)",
      btn_processing: "⏳ Patch en cours...",
      stage_match_title: "🔥 Calibration Matchée Détectée !",
      stage_match_sub: "Une cartographie exacte Stage 1 / FlexFuel a été trouvée pour ce calculateur.",
      stage_match_badge: "100% Compatible"
    },
    options: {
      dpf_title: "💨 DPF / FAP OFF",
      dpf_desc: "Désactivation cycles régénération FAP, capteur différentiel et sondes EGT.",
      egr_title: "🔄 EGR OFF",
      egr_desc: "Fermeture permanente de la vanne EGR (hystérésis zéro & masques défauts).",
      adblue_title: "💧 AdBlue / SCR OFF",
      adblue_desc: "Suppression complète de la pompe urée, sondes NOx et alertes redémarrage.",
      start_stop_title: "⚡ Start & Stop OFF",
      start_stop_desc: "Mémorisation de la coupure automatique au démarrage du moteur.",
      vmax_title: "🚀 VMax (Speed Limiter OFF)",
      vmax_desc: "Débridage de la vitesse maximale du véhicule.",
      flaps_title: "🌪️ Swirl Flaps / TVA OFF",
      flaps_desc: "Neutralisation des volets d'admission d'air et boîtier papillon.",
      stage1_title: "🏁 Stage 1 Remap (+25% à +35%)",
      stage1_desc: "Reprogrammation moteur calibrée (couple, injection, pression turbo).",
      stage2_title: "🏁 Stage 2 Remap (Sport / Downpipe)",
      stage2_desc: "Pour véhicule avec admission, échangeur ou échappement libre.",
      flexfuel_title: "🌽 FlexFuel E85 (Bioéthanol)",
      flexfuel_desc: "Conversion pour rouler à 100% au Superéthanol E85 ou sans plomb.",
      decat_title: "🔥 Decat / Sonde Lambda OFF",
      decat_desc: "Suppression défaut catalyseur (P0420) et sonde lambda aval O2.",
      pop_bang_title: "💥 Pop & Bang (Burble Map)",
      pop_bang_desc: "Retard à l'allumage à la décélération pour crépitements à l'échappement.",
      immo_off_title: "🔑 IMMO OFF (Antidémarrage)",
      immo_off_desc: "Désactivation antidémarrage électronique (Bosch TriCore MEDC17, Toyota Denso Gen 1-4, Patrol, etc.).",
      credits: "Crédits"
    },
    results: {
      success_title: "✅ Fichier patché avec succès !",
      success_count: "modifications appliquées",
      already_applied_title: "ℹ️ Fichier déjà patché (0 octet à modifier) !",
      already_applied_summary: "Ce fichier binaire intègre déjà toutes les solutions demandées.<br>Le moteur a vérifié que les maps, switchs physiques et codes défauts sont déjà calibrés sur OFF dans ce dump.<br><b>Sécurité Garantie : 0 crédit débité</b> (Solde intact : {balance} crédits).",
      failed_title: "❌ ATTENTION : 0 octet modifié (Fichier intact) !",
      failed_summary: "Aucune modification n'a été appliquée à ce fichier.<br>Les signatures cartographiques ou tables DTC connues pour cet ECU n'ont pas été trouvées dans ce dump binaire.<br><b>Sécurité : Aucun crédit n'a été débité</b> (Solde intact : {balance} crédits).",
      workshop_instructions: "🔧 Consignes d'Atelier Après Flash :",
      btn_download: "📥 Télécharger le Fichier Modifié (.bin)",
      btn_donate: "💖 Faire un Don / Support Us",
      btn_new_file: "🔄 Traiter un autre fichier",
      btn_report: "🚨 Signaler une anomalie / Résultat incorrect",
      btn_report_info: "ℹ️ Informations cartographie",
      diff_title: "Détails des Offsets Modifiés :",
      col_address: "Adresse Hex",
      col_desc: "Description",
      col_original: "Original",
      col_modified: "Modifié",
      no_diffs_already: "Toutes les maps et switchs sont déjà conformes aux solutions sélectionnées. Aucun offset modifié (0 octet altéré).",
      no_diffs_identical: "Aucun offset modifié. Le fichier d'origine et le fichier cible sont 100% identiques."
    },
    instructions: {
      dpf: "FAP / DPF : Débrancher le capteur de pression différentielle et les sondes de température FAP si le filtre est vidé.",
      egr: "EGR : Débrancher le connecteur électrique de la vanne EGR ou poser une plaque d'obturation étanche.",
      adblue: "AdBlue / SCR : Débrancher impérativement la pompe / calculateur AdBlue après écriture du fichier pour éviter tout réarmement.",
      clear_dtc: "Atelier : Réaliser un effacement mémoire des codes défauts (DTC Clear) après l'écriture du fichier avant tout démarrage moteur.",
      checksum_tricore: "Checksum TriCore Autosar : Signature vérifiée avec succès par le moteur matériel."
    },
    expert: {
      title: "🧰 Boîte à Outils Spécialisés Atelier",
      subtitle: "Fonctions expertes avancées (1 Crédit par opération)",
      pcr_title: "VAG Continental PCR 2.1 OBD Unlocker",
      pcr_desc: "Déverrouille le statut de protection OBD dans l'EEPROM 95640 pour autoriser la reprogrammation par la prise diag sans démontage. Détecte la signature Simos, le VIN et le type moteur (CAYC, CAYD...).",
      pcr_btn: "Choisir EEPROM PCR 2.1 (8 Ko ou 136 Ko)",
      cold_title: "Renault Cold Start Fix",
      cold_desc: "Corrige définitivement le problème de démarrage difficile à froid sur les calculateurs Renault EMS3110, EMS3125, EMS3132 et Valeo V42.",
      cold_btn: "Choisir Flash Renault (.bin)",
      valeo_title: "Renault Valeo V42 Fan Mod",
      valeo_desc: "Abaisse le seuil de déclenchement du moto-ventilateur GMV (stock 105°C) pour fiabiliser le refroidissement moteur.",
      valeo_temp_label: "Consigne :",
      valeo_btn: "Choisir Flash Valeo V42",
      pop_title: "Pop & Bang (Retard à l'allumage)",
      pop_desc: "Configure les retours de flamme et claquements à l'échappement lors des décélérations (overrun ignition retard).",
      pop_btn: "Choisir Flash Essence (.bin)",
      airbag_title: "Airbag Crash Data Reset",
      airbag_desc: "Réinitialise les secteurs d'enregistrement de choc dans les dumps EEPROM de boîtiers Airbag pour remise à l'état vierge.",
      airbag_btn: "Choisir EEPROM Airbag",
      toyota_immo_title: "Toyota Denso & Patrol IMMO OFF",
      toyota_immo_desc: "Désactive l'antidémarrage électronique sur Toyota Denso (Gen 1, Gen 2, Gen 3, Gen 4) et Nissan Patrol V8 (switch mémoire 20 36 5A A5 ➔ 20 36 A5 5A et block clear).",
      toyota_immo_btn: "Choisir Flash Toyota / Patrol (.bin)",
      toyota_hardcut_title: "Toyota D-4D Popcorn / Hardcut",
      toyota_hardcut_desc: "Configure un rupteur électronique net (Hardcut rev limiter / popcorn) sur moteurs diesel Toyota D-4D (1KD, 2KD, 1GD, 2GD) par coupure d'injection immédiate.",
      toyota_hardcut_rpm: "Régime coupure :",
      toyota_hardcut_btn: "Choisir Flash Toyota Denso (.bin)"
    },
    catalog: {
      title: "📚 Catalogue Complet des Calculateurs Supportés",
      search_placeholder: "🔍 Rechercher une marque ou un calculateur (ex: EDC17, SID310, Delphi DCM, Tata, Mahindra, VAG...)"
    },
    history: {
      title: "📜 Historique de vos Fichiers Modifiés",
      col_date: "Date",
      col_ecu: "Calculateur",
      col_options: "Options",
      col_credits: "Crédits",
      col_file: "Fichier Modifié",
      col_action: "Action",
      btn_download: "Télécharger",
      status_completed: "Succès",
      status_failed: "0 modif",
      empty: "Aucun fichier modifié pour le moment."
    },
    credits: {
      title: "💳 Gestion & Forfaits de Crédits",
      desc: "Rechargez votre compte pour effectuer vos modifications ECU, remaps Stage et déconnexions.",
      balance_label: "Votre Solde Disponible",
      credits_unit: "Crédits",
      beta_alert_title: "Politique de Crédits Bêta-Test :",
      beta_alert_text: "Pendant la phase de test, les crédits sont gérés exclusivement par l'administrateur master. Vos 100 crédits initiaux sont alloués dès validation de votre atelier. Pour toute recharge supplémentaire, demandez directement à votre administrateur.",
      pricing_title: "⚡ Forfaits de Crédits (Tarifs Indicatifs)",
      pack_discovery: "Pack Découverte",
      pack_discovery_sub: "Idéal pour 3 à 5 véhicules",
      pack_discovery_btn: "Ajouter 50 Crédits",
      pack_pro: "Pack Atelier Pro",
      pack_pro_badge: "Plus Populaire",
      pack_pro_sub: "Recommandé pour professionnels",
      pack_pro_btn: "Ajouter 150 Crédits",
      pack_master: "Pack Master Illimité",
      pack_master_sub: "Pour reprogrammateurs intensifs",
      pack_master_btn: "Ajouter 500 Crédits",
      custom_title: "⚙️ Montant Personnalisé",
      custom_desc: "Spécifiez exactement le nombre de crédits souhaité :",
      custom_btn: "Recharger",
      transactions_title: "📜 Historique Récent des Mouvements de Crédits",
      col_trans_date: "Date & Heure",
      col_trans_op: "Opération / Description",
      col_trans_var: "Variation",
      col_trans_stat: "Statut"
    },
    modals: {
      close: "Fermer",
      cancel: "Annuler",
      save: "Enregistrer",
      login_title: "SCORPION REMAP PRO V3.2.0",
      login_sub: "Bienvenue sur la plateforme de test. Identifiez votre atelier pour débloquer vos <b>100 crédits de test offerts</b>.",
      garage_label: "🏢 Nom de votre Atelier ou Adresse E-mail :",
      garage_placeholder: "Ex: YOUNESINTIL NET ou contact@garage.com",
      code_label: "🔑 Code d'accès Testeur :",
      code_sub: "Code par défaut : <code>BETA2026</code>",
      btn_enter: "🚀 Continuer vers l'Atelier",
      securing_title: "Sécurisation de votre atelier :",
      securing_desc: "Renseignez votre e-mail pour recevoir le nouveau lien permanent du serveur en cas de coupure et définissez votre mot de passe pour sécuriser vos crédits.",
      selected_garage_label: "🏢 Atelier sélectionné :",
      email_label: "📧 Votre Adresse E-mail :",
      email_placeholder: "ex: contact@garagediag.fr",
      email_sub: "Servira à vous contacter et à diffuser le lien permanent du serveur.",
      define_pwd_label: "🔑 Définir votre Mot de passe :",
      define_pwd_placeholder: "Min. 6 caractères",
      confirm_pwd_label: "🔑 Confirmer le Mot de passe :",
      confirm_pwd_placeholder: "Retapez votre mot de passe",
      btn_save_profile: "💾 Enregistrer mon compte & Accéder au Studio",
      btn_switch_garage: "⬅️ Changer d'atelier",
      secured_title: "Atelier sécurisé :",
      secured_desc: "Cet atelier est protégé par mot de passe. Entrez votre mot de passe personnel pour accéder à votre espace et vos crédits.",
      workshop_pwd_label: "🔑 Mot de passe de votre atelier :",
      btn_unlock_workshop: "🚀 Déverrouiller l'Atelier",
      btn_choose_other_garage: "⬅️ Choisir un autre atelier",
      admin_toggle_link: "🔐 Vous êtes l'administrateur ? Connexion Master",
      pwd_modal_title: "🔑 Changer mon mot de passe",
      pwd_current: "Ancien mot de passe :",
      pwd_new: "Nouveau mot de passe :",
      pwd_new_placeholder: "Min. 8 car. (lettres + chiffres)",
      pwd_confirm: "Confirmer le mot de passe :",
      pwd_confirm_placeholder: "Retapez votre nouveau mot de passe",
      btn_save_pwd: "Enregistrer",
      report_title: "🚨 Signaler une anomalie technique",
      report_file_label: "📄 Fichier concerné :",
      report_loading: "Chargement des données du dump...",
      report_tester_name: "Votre Nom ou Atelier / Garage :",
      report_tester_placeholder: "Ex: Atelier Auto Perf 69, Alex Diag",
      report_cat_label: "Type d'anomalie rencontrée :",
      report_cat_no_mod: "0 modification appliquée / Switch non trouvé dans le dump",
      report_cat_wrong_det: "Calculateur ou Marque mal détecté",
      report_cat_dtc_present: "Code défaut (DTC) toujours présent au diag après écriture",
      report_cat_limp: "Mode dégradé ou voyant moteur persistant",
      report_cat_tool_err: "Refus de l'outil de flash (Kess, Autotuner, CMD, Foxflash)",
      report_cat_other: "Autre remarque / suggestion technique",
      report_comment_label: "Précisions de l'atelier (Codes DTC restants, outil de lecture...) :",
      report_comment_placeholder: "Ex: Le DTC P2002 est toujours actif après avoir injecté le MOD. Lu et écrit au Kess 3 en Bench.",
      btn_submit_report: "🚀 Envoyer le rapport & Archiver le dump",
      my_tickets_title: "🎫 Mes Signalements Techniques & Réponses Support",
      my_tickets_loading: "Chargement de vos signalements...",
      dtc_title: "Inspecteur de Table DTC",
      dtc_subtitle: "Analyse binaire en temps réel de la cartographie. Détecte les codes d'erreur actifs et ceux déjà désactivés (OFF).",
      dtc_codes_label: "Codes :",
      dtc_filter_all: "Tous",
      dtc_filter_active: "🟢 Actifs (ON)",
      dtc_filter_disabled: "🔴 Déjà OFF",
      dtc_search_placeholder: "🔎 Rechercher un code ou composant (ex: 0420, P2002, Catalyseur, Sonde, FAP...)",
      dtc_col_dtc: "Code DTC",
      dtc_col_state: "État dans l'ECU",
      dtc_col_desc: "Description / Système Associé",
      dtc_col_offset: "Offset Dump",
      dtc_loading: "Chargement et scan de la table DTC...",
      dtc_selected_suffix: "code(s) sélectionné(s) pour suppression.",
      dtc_btn_apply: "➕ Ajouter les DTCs cochés à la demande"
    },

    flexfuel: {
      tab_title: "Studio FlexFuel E85 & Cold Start Pro (Stock Lab)",
      tab_subtitle: "Laboratoire de recalibration volumétrique Bioéthanol (+28%), démarrage à froid paramétrique & avances allumage RON 105.",
      btn_coverage: "Calculateurs Supportés (85+ Familles)",
      btn_guide: "Guide d'Utilisation Atelier",
      badge_anti_diesel: "🛡️ Sécurité Anti-Diesel Active",

      drop_title: "Déposer votre dump Flash Essence ici (.bin, .ori)",
      drop_subtitle: "Compatible Bosch MED17, MED9, MEV17, Sagem S3000, Continental EMS, Ford EcoBoost, Delco, etc.",
      btn_browse: "📁 Parcourir mes fichiers",
      analyzing_spinner: "Analyse du dump et identification de la cartographie essence...",

      diesel_title: "Action Interdite : Motorisation DIESEL Détectée",
      diesel_desc_prefix: "Le dump analysé correspond à un moteur",
      diesel_desc_suffix: "Pour préserver l'intégrité mécanique et éviter la destruction du moteur, la conversion Bioéthanol E85 est strictement verrouillée sur ce fichier.",
      diesel_guarantee: "🛡️ Intégrité garantie : aucun crédit débité, fichier d'origine 100% intact.",

      eligible_title: "Dump Essence Validé — Éligible FlexFuel E85",
      eligible_subtitle: "Moteur thermique compatible Bioéthanol / E85",
      eligible_badge: "✨ Prêt pour Calibration",

      meta_filename: "Nom du Fichier",
      meta_filesize: "Taille Flash",
      meta_brand: "Marque Détectée",
      meta_ecu: "Calculateur (ECU)",
      meta_tier: "Génération / Tarif",

      section_title: "Options Exclusives FlexFuel E85 & Cold Start (Stock Lab)",

      card_bicarb_title: "🌿 FlexFuel E85 (Bi-carburation)",
      card_bicarb_desc: "Recalibration volumétrique du débit massique d'injection. Permet de rouler au SP95, SP98 ou E85 pur sans boîtier.",
      label_enrichment: "Enrichissement de base :",
      label_presets: "Mélanges :",
      label_ai: "AI Adaptive Trims (optimisation dynamique STFT / LTFT)",

      card_coldstart_title: "❄️ Cold Start Hiver Pro",
      card_coldstart_desc: "Cartographies d'enrichissement démarrage à froid sur les axes température eau de -30°C à +80°C. Élimine les démarrages difficiles l'hiver.",
      label_coldstart: "Palier de démarrage à froid :",
      cs_lvl1: "Level 1 : +15 % Cranking (Climat tempéré / Sud)",
      cs_lvl2: "Level 2 : +25 % Cranking (Standard E85)",
      cs_lvl3: "Level 3 : +35 % Cranking (Recommandé Mi-Saison / Hiver)",
      cs_lvl4: "Level 4 : +45 % Cranking (Froid 0°C à 10°C)",
      cs_lvl5: "Level 5 : +55 % Cranking (Grand froid)",
      cs_hard: "Hard-Start : +80 % Cranking (Gel sévère < -5°C)",

      card_oilfix_title: "🛡️ Protection Oil-Fix (Anti-Dilution)",
      card_oilfix_desc: "Crucial pour injection directe (PSA 1.2 PureTech & VAG TSI) : réduit les post-injections pour empêcher la dilution de l'éthanol dans l'huile moteur.",
      oilfix_badge: "Protection mécanique active",

      card_stage_title: "⚡ E85 + Stage 1 Performance",
      card_stage_desc: "Optimise l'avance à l'allumage (+4.5°) en exploitant le pouvoir anti-cliquetis de l'éthanol (Indice RON 105). Gain de couple et réactivité moteur.",
      label_stage: "Niveau de puissance :",
      stage_1: "Stage 1 FlexFuel (Avance allumage +4.5°)",
      stage_2: "Stage 2 FlexFuel (Avance +6.5° & Pression Turbo)",
      stage_none: "Sans Stage (Avances d'origine)",

      card_lambda_title: "🔍 Surveillance Sondes & Catalyseur",
      card_lambda_desc: "Configuration sélective des boucles Lambda et neutralisation automatique des DTCs catalyseur pour zéro voyant moteur.",
      o2_aval: "Sonde 2 Aval Off (Surveillance Catalyseur)",
      o2_amont: "Sonde 1 Amont Off (Régulation)",
      o2_both: "Both 1 & 2 Off (Décatalysé complet)",
      o2_none: "Boucle Fermée Standard (Sondes Actives)",
      chk_cat: "CAT OFF (22 DTCs)",
      chk_richness: "DTC Richesse (27 DTCs)",
      chk_evap: "EVAP OFF (8 DTCs)",

      cost_label: "Coût de la prestation atelier",
      credits_unit: "Crédits",
      btn_launch: "🚀 Lancer la Calibration FlexFuel E85",
      processing: "Application de la calibration E85 et calcul du Checksum Autosar...",
      report_title: "Rapport Technique de Modification (Stock Lab Pro)",
      btn_download: "Télécharger le Fichier Calibré E85 (.bin)",
      checksum_badge: "✓ Checksum TriCore / Autosar Validé à 100%",

      cov_modal_title: "Liste Complète des Calculateurs & Motorisations Essence Supportés",
      cov_modal_sub: "Moteur FlexFuel E85 Pro Studio Remap — Base 889 Patches VAG Exacts + Algorithme Procédural Dynamique",
      cov_search_placeholder: "Rechercher par calculateur, marque, moteur ou modèle (ex: PureTech, MED17, Simos 18, Clio, THP, Golf, BMW...)",
      cov_btn_close: "Fermer la Liste",
      guide_btn_close: "Fermer le Guide",
      guide: {
        modal_title: "Guide Technique & Protocole d'Atelier — FlexFuel E85",
        modal_subtitle: "Calibration Bioéthanol, Calcul des Mélanges, Paliers Cold Start & Sécurités Mécaniques",
        ch1_title: "<i class=\"fa-solid fa-leaf\" style=\"color:var(--accent-green)\"></i> 1. Principe Stœchiométrique & Auto-Apprentissage Trims (STFT / LTFT)",
        ch1_body: "<p>L'éthanol pur (E100) ou le Superéthanol de pompe (E85 été/hiver) nécessite un rapport stœchiométrique d'environ <strong>9.7:1</strong>, contre <strong>14.7:1</strong> pour l'essence sans-plomb standard (SP98/SP95).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Enrichissement volumétrique de base (+28 %) :</strong> C'est la valeur d'or étalonnée sur banc. Elle apporte le débit massique requis sans saturer le duty cycle des injecteurs d'origine.</li>\n  <li><strong>AI Adaptive Trims actif :</strong> Permet au calculateur moteur d'adapter dynamiquement ses corrections à court terme (STFT) et à long terme (LTFT). Le client peut ainsi mélanger SP95, SP98 ou E85 dans n'importe quelle proportion sans aucun boîtier additionnel.</li>\n</ul>",
        ch2_title: "<i class=\"fa-solid fa-calculator\" style=\"color:#f59e0b\"></i> 2. Formule & Calcul des Pourcentages de Mélange (50/50, 60/40, 70/30, 80/20, 100%)",
        ch2_body: "<p>Tous les clients ne roulent pas à 100 % d'E85 pur. Pour les véhicules avec des injecteurs d'origine à faible débit ou pour adapter le mélange sur-mesure, voici le calcul exact du besoin en carburant :</p>\n<div style=\"background:#090e17; border:1px solid #1e293b; border-radius:8px; padding:12px; margin:10px 0; font-family:'Consolas', monospace; font-size:13px; color:#38bdf8;\">\n  <strong>Formule Stœchiométrique :</strong> Enrichissement Requis (%) = (% Éthanol dans réservoir / 100) × 28 %\n</div>\n<div style=\"overflow-x:auto; margin-top:10px;\">\n  <table style=\"width:100%; border-collapse:collapse; font-size:12px; text-align:left;\">\n    <thead>\n      <tr style=\"border-bottom:1px solid #334155; color:#94a3b8;\">\n        <th style=\"padding:8px;\">Mélange réservoir</th>\n        <th style=\"padding:8px;\">Ratio Éthanol / SP</th>\n        <th style=\"padding:8px;\">Enrichissement Calculé</th>\n        <th style=\"padding:8px;\">Réglage Slider Recommandé</th>\n      </tr>\n    </thead>\n    <tbody style=\"color:#cbd5e1;\">\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>50 % E85 / 50 % SP</strong></td>\n        <td style=\"padding:8px;\">Moitié / Moitié</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+14 %</td>\n        <td style=\"padding:8px;\">Curseur à <strong>+14 %</strong> (idéal petits injecteurs)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>60 % E85 / 40 % SP</strong></td>\n        <td style=\"padding:8px;\">60% Éthanol / 40% SP</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+17 %</td>\n        <td style=\"padding:8px;\">Curseur à <strong>+17 %</strong> (compromis économique très stable)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>70 % E85 / 30 % SP</strong></td>\n        <td style=\"padding:8px;\">70% Éthanol / 30% SP</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+20 %</td>\n        <td style=\"padding:8px;\">Curseur à <strong>+20 %</strong> (très populaire pour l'hiver)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>80 % E85 / 20 % SP</strong></td>\n        <td style=\"padding:8px;\">80% Éthanol / 20% SP</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+23 %</td>\n        <td style=\"padding:8px;\">Curseur à <strong>+23 %</strong> (équivalent E85 station hiver)</td>\n      </tr>\n      <tr>\n        <td style=\"padding:8px;\"><strong>100 % E85 (Pur)</strong></td>\n        <td style=\"padding:8px;\">Plein total Bioéthanol</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+28 %</td>\n        <td style=\"padding:8px;\"><strong>Point d'or FlexFuel :</strong> avec <em>AI Adaptive Trims</em> actif, le moteur absorbe TOUS les mélanges ci-dessus automatiquement !</td>\n      </tr>\n    </tbody>\n  </table>\n</div>\n<div style=\"margin-top:12px; font-size:12px; color:#cbd5e1; background:rgba(245, 158, 11, 0.12); border-left:3px solid #f59e0b; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#f59e0b;\">💡 Pourquoi le réglage à +28% suffit dans 95% des cas ?</strong><br>\n  Grâce à l'option <strong>AI Adaptive Trims</strong>, les sondes Lambda du véhicule corrigent en direct (STFT/LTFT jusqu'à ±25%). Donc même avec le slider à +28%, si le client met 50/50 ou du SP pur, le calculateur s'auto-ajuste tout seul sans voyant ! Le réglage manuel (+14%, +20%) sert principalement pour les préparateurs qui veulent brider un mélange fixe ou protéger de petits injecteurs.\n</div>",
        ch3_title: "<i class=\"fa-solid fa-snowflake\" style=\"color:var(--accent-cyan)\"></i> 3. Paliers de Démarrage à Froid (Cold Start Hiver Pro)",
        ch3_body: "<p>L'éthanol possède une tension de vapeur très basse et ne se vaporise pas spontanément en dessous de 12°C - 15°C. Notre solution recalibre l'enrichissement au démarreur (cranking) sur toute la courbe de température d'eau (-30°C à +80°C).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Level 1 (+15%) :</strong> Climat tempéré / Régions chaudes du Sud en été (&gt; 20°C).</li>\n  <li><strong>Level 2 (+25%) :</strong> Printemps et automne doux (15°C à 20°C).</li>\n  <li><strong>Level 3 (+35%) [Recommandé par défaut] :</strong> Idéal mi-saison et automne/hiver (5°C à 15°C). Démarrage au quart de tour au 1er coup de clé.</li>\n  <li><strong>Level 4 (+45%) :</strong> Hiver froid standard (0°C à 5°C).</li>\n  <li><strong>Level 5 & Hard-Start (+75% à +80%) :</strong> Régions montagneuses ou gel négatif continu (&lt; 0°C).</li>\n</ul>",
        ch4_title: "<i class=\"fa-solid fa-shield-halved\" style=\"color:var(--accent-orange)\"></i> 4. Injections Directes & Protection Oil-Fix (Anti-Dilution Huile)",
        ch4_body: "<p>Sur les moteurs modernes à injection directe (ex: <strong>PSA 1.2 PureTech / THP</strong>, <strong>VAG 1.4 / 2.0 TSI TFSI</strong>, <strong>Ford EcoBoost</strong>, <strong>Renault TCe</strong>) :</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Le risque mécanique :</strong> À froid, l'éthanol imbrûlé peut lessiver le film protecteur d'huile sur la chemise des cylindres et couler dans le carter, provoquant une dilution de l'huile moteur et une chute de viscosité.</li>\n  <li><strong>L'action Oil-Fix :</strong> Notre algorithme réduit les post-injections superflues à basse température et accélère la mise en chauffe de la chambre.</li>\n  <li><strong>Consigne d'atelier :</strong> Conseillez à votre client de rapprocher ses vidanges d'huile moteur à <strong>10 000 km ou 15 000 km maximum</strong> avec une huile de synthèse homologuée constructeur.</li>\n</ul>",
        ch5_title: "<i class=\"fa-solid fa-magnifying-glass-chart\" style=\"color:#06b6d4\"></i> 5. Surveillance Sondes Lambda & Catalyseur (Zéro Voyant Moteur Garanti)",
        ch5_body: "<p>L'éthanol modifie la température et la composition des gaz d'échappement (davantage de vapeur d'eau et rapport stœchiométrique différent). Sans calibration spécifique des boucles de surveillance, le tableau de bord peut s'allumer avec de faux défauts antipollution.</p>\n<ul style=\"margin-top:6px; margin-bottom:8px;\">\n  <li><strong>Sonde 1 Amont (Avant Cata) — Préservée à 100 % :</strong> C'est la sonde régulatrice vitale. Elle mesure la richesse en continu et pilote la boucle fermée (Closed-Loop) pour adapter l'injection en temps réel.</li>\n  <li><strong>Sonde 2 Aval Off (Après Cata) :</strong> Désactive uniquement le diagnostic d'efficacité catalytique. Elle supprime définitivement le faux défaut <strong>P0420 / P0430</strong> (Efficacité catalyseur sous le seuil).</li>\n  <li><strong>CAT OFF (22 DTCs) :</strong> Neutralise chirurgicalement toute la table d'erreurs liée au convertisseur catalytique. Permet aussi d'installer un échappement sport ou un Downpipe décatalysé sans allumer de voyant.</li>\n  <li><strong>DTC Richesse / Lambda Trims (27 DTCs) :</strong> Masque les alertes de dérive extrême (ex: <strong>P0171, P0174, P2177, P2179</strong> — Mélange trop pauvre). Évite tout voyant pendant la phase transitoire quand le client passe brutalement du SP98 pur à 100% d'E85.</li>\n  <li><strong>EVAP OFF (8 DTCs) :</strong> Neutralise les défauts du système de récupération des vapeurs de carburant (Canister P0440 à P0455). L'éthanol ayant une pression de vapeur différente, cela élimine les faux positifs de purge réservoir.</li>\n</ul>\n<div style=\"font-size:12px; color:#cbd5e1; background:rgba(6, 182, 212, 0.12); border-left:3px solid #06b6d4; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#06b6d4;\">✅ Bénéfice Client & Atelier :</strong> Le véhicule passe le contrôle technique sans aucun code défaut enregistré dans la mémoire OBD, conserve toute sa réactivité d'injection grâce à la sonde amont, et garantit un tableau de bord 100% éteint.\n</div>",
        ch6_title: "<i class=\"fa-solid fa-list-check\" style=\"color:#c084fc\"></i> 6. Checklist Atelier & Protocole de Remise au Client",
        ch6_body: "<p>Pour un résultat 100% garanti sans retour client, appliquez ce protocole en atelier :</p>\n<div class=\"guide-step-box\">\n  <div class=\"step-item\">\n    <div class=\"step-num\">Étape 1</div>\n    <div class=\"step-title\">Écriture Flash</div>\n    <div class=\"step-desc\">Injectez le fichier MOD avec votre outil. Le Checksum est calculé automatiquement.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Étape 2</div>\n    <div class=\"step-title\">DTC Clear</div>\n    <div class=\"step-desc\">Réalisez obligatoirement un effacement complet de la mémoire défauts avant tout démarrage.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Étape 3</div>\n    <div class=\"step-title\">Plein E85</div>\n    <div class=\"step-desc\">Mettre au moins 50% à 70% d'éthanol pour le 1er test (ou 100% direct).</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Étape 4</div>\n    <div class=\"step-title\">Ralenti 3 min</div>\n    <div class=\"step-desc\">Laisser tourner 3 min au ralenti sans accélérer pour l'auto-apprentissage initial.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Étape 5</div>\n    <div class=\"step-title\">Essai Routier</div>\n    <div class=\"step-desc\">Essai de 5 à 10 min : accélérations franches, vérification de la réactivité et zéro voyant.</div>\n  </div>\n</div>"
      }
    }
  },

  en: {
    brand_badge: "PRO v3.2.0",
    nav: {
      studio: "🛠️ Studio Remap",
      expert: "🧰 Expert Tools",
      flexfuel: "🌿 FlexFuel E85",
      catalog: "📚 Catalog",
      history: "📜 Job History",
      credits: "💳 Credits & Plans",
      changelog: "📋 Changelog",
      my_tickets: "🎫 My Reports",
      admin: "⚙️ Administration",
      donate: "Donate",
      connecting: "Connecting...",
      tester_badge: "TESTER PRO",
      credits_label: "Credits",
      switch_account: "Switch Account"
    },
    announcement: {
      action_required: "Action required:",
      profile_completion: "Secure your workshop account with your email address and personal password to protect your credits and receive the permanent server link.",
      secure_account_btn: "🔒 Secure my account",
      view_changelog: "📋 View Changelog →"
    },
    sim2k_promo: {
      badge_hot: "🔥 NEW & EXCLUSIVE",
      badge_ecu: "CONTINENTAL SIM2K-510",
      badge_models: "KIA & HYUNDAI 2021–2026",
      title: "ONLINE RELEASE: CONTINENTAL SIM2K-510 (KIA & HYUNDAI 2021–2026)",
      features_html: "<strong>All-in-One Full Pack:</strong> AdBlue OFF + Start & Stop OFF + OPF/GPF OFF + EGR OFF + Decat/Lambda OFF.",
      instant_text: "⚡ Secure direct checkout: 120.00 € (Stripe) or 35,000 DZD (Edahabia / CIB). Instant download in 30 seconds.",
      btn_cta: "📤 Drop a SIM2K-510 file now →"
    },
    studio: {
      drop_title: "Drag & drop your ECU binary file (.bin, .ori)",
      drop_subtitle: "Or click to browse your files (Continental SID, Bosch EDC16/17/MD1, Delphi, Marelli...)",
      file_analyzed: "Analyzed File",
      detected_ecu: "Detected Brand / ECU",
      high_confidence: "High Compatibility",
      medium_confidence: "Medium Compatibility",
      change_file: "🔄 Change file",
      fuel_detecting: "⛽ Engine: Detecting...",
      fuel_diesel: "⛽ Engine: Diesel (HDi / TDI / dCi / CRDi)",
      fuel_gasoline: "⛽ Engine: Petrol / Turbo Petrol",
      report_detection_error: "⚠️ Detection error? Report it",
      unknown_title: "ECU NOT RECOGNIZED AUTOMATICALLY",
      unknown_desc: "The dump is flagged as \"Unknown\". Modifications are locked to prevent any potential error.<br><span style=\"color:#fde047; font-weight:700;\">👉 You must select your exact brand and ECU model</span> in the box below to unlock patching.",
      adjust_label: "⚙️ Adjust if necessary:",
      brand_label: "Brand",
      ecu_label: "ECU Model",
      select_options_title: "⚙️ Select tuning solutions to apply",
      custom_dtc_title: "⚠️ Custom DTC Code Deletion",
      custom_dtc_btn: "🔍 Inspect DTC Table (ON / OFF)",
      custom_dtc_desc: "Enter any standard OBD-II code (e.g., P20EE, P2201, P0420) or click the inspector above to examine active DTC table entries in the dump.",
      custom_dtc_placeholder: "Example: P20EE, P2201, P0420",
      total_required: "Total Required:",
      current_balance: "Current Balance:",
      btn_process: "⚡ Patch & Generate (.MOD)",
      btn_processing: "⏳ Patching in progress...",
      stage_match_title: "🔥 Matched Calibration Detected!",
      stage_match_sub: "An exact Stage 1 / FlexFuel remap calibration was matched for this ECU.",
      stage_match_badge: "100% Compatible"
    },
    options: {
      dpf_title: "💨 DPF / FAP OFF",
      dpf_desc: "Deactivates DPF regeneration cycles, differential pressure sensor, and EGT temperature probes.",
      egr_title: "🔄 EGR OFF",
      egr_desc: "Permanent closure of the EGR valve (zero hysteresis & fault mask clearing).",
      adblue_title: "💧 AdBlue / SCR OFF",
      adblue_desc: "Complete removal of urea pump, NOx sensors, and countdown no-restart warnings.",
      start_stop_title: "⚡ Start & Stop OFF",
      start_stop_desc: "Memorizes automatic engine cut-off status at startup.",
      vmax_title: "🚀 VMax (Speed Limiter OFF)",
      vmax_desc: "Removes electronic maximum vehicle speed limits.",
      flaps_title: "🌪️ Swirl Flaps / TVA OFF",
      flaps_desc: "Neutralization of intake manifold flaps and electronic throttle body.",
      stage1_title: "🏁 Stage 1 Remap (+25% to +35%)",
      stage1_desc: "Dyno-calibrated engine remapping (torque, injection, boost pressure).",
      stage2_title: "🏁 Stage 2 Remap (Sport / Downpipe)",
      stage2_desc: "For vehicles with upgraded intake, intercooler, or decat downpipe.",
      flexfuel_title: "🌽 FlexFuel E85 (Bioethanol)",
      flexfuel_desc: "Conversion to run on 100% E85 ethanol or standard unleaded gasoline.",
      decat_title: "🔥 Decat / O2 Lambda OFF",
      decat_desc: "Removes catalytic converter efficiency error (P0420) and downstream O2 sensor.",
      pop_bang_title: "💥 Pop & Bang (Burble Map)",
      pop_bang_desc: "Deceleration overrun ignition retard for distinctive exhaust burble effects.",
      immo_off_title: "🔑 IMMO OFF (Immobilizer Delete)",
      immo_off_desc: "Electronic immobilizer bypass (Bosch TriCore MEDC17, Toyota Denso Gen 1-4, Patrol, etc.).",
      credits: "Credits"
    },
    results: {
      success_title: "✅ File patched successfully!",
      success_count: "modifications applied",
      already_applied_title: "ℹ️ File already patched (0 bytes to modify)!",
      already_applied_summary: "This binary file already includes all requested solutions.<br>The engine verified that maps, physical switches, and DTC codes are already set to OFF in this dump.<br><b>Guaranteed Security: 0 credits charged</b> (Balance intact: {balance} credits).",
      failed_title: "❌ WARNING: 0 bytes modified (File intact)!",
      failed_summary: "No modifications were applied to this file.<br>The map patterns or DTC tables for this ECU were not found in this binary dump.<br><b>Security: No credits debited</b> (Balance intact: {balance} credits).",
      workshop_instructions: "🔧 Workshop Instructions After Flashing:",
      btn_download: "📥 Download Modified File (.bin)",
      btn_donate: "💖 Support Us / Donate",
      btn_new_file: "🔄 Process another file",
      btn_report: "🚨 Report issue / Incorrect result",
      btn_report_info: "ℹ️ Calibration info",
      diff_title: "Modified Hex Offsets Details:",
      col_address: "Hex Address",
      col_desc: "Description",
      col_original: "Original",
      col_modified: "Modified",
      no_diffs_already: "All maps and switches already comply with the selected options. No offset modified (0 bytes altered).",
      no_diffs_identical: "No offsets modified. The original file and target file are 100% identical."
    },
    instructions: {
      dpf: "DPF / FAP: Disconnect the differential pressure sensor and exhaust temperature probes if the filter core is emptied.",
      egr: "EGR: Unplug the electrical connector of the EGR valve or install a blind blocking plate.",
      adblue: "AdBlue / SCR: Imperatively disconnect the AdBlue dosing pump / SCR module after flashing to avoid re-arming.",
      clear_dtc: "Workshop: Perform a full diagnostic fault code erase (DTC Clear) after writing the file before starting the engine.",
      checksum_tricore: "TriCore Autosar Checksum: Signature verified successfully by hardware engine."
    },
    expert: {
      title: "🧰 Workshop Specialized Toolbox",
      subtitle: "Advanced expert functions (1 Credit per operation)",
      pcr_title: "VAG Continental PCR 2.1 OBD Unlocker",
      pcr_desc: "Unlocks OBD flashing protection in EEPROM 95640 to allow OBD port remapping without opening the ECU. Detects Simos signature, VIN, and engine code (CAYC, CAYD...).",
      pcr_btn: "Select PCR 2.1 EEPROM (8 KB or 136 KB)",
      cold_title: "Renault Cold Start Fix",
      cold_desc: "Permanently solves hard cold-start issues on Renault EMS3110, EMS3125, EMS3132, and Valeo V42 ECUs.",
      cold_btn: "Select Renault Flash (.bin)",
      valeo_title: "Renault Valeo V42 Fan Mod",
      valeo_desc: "Lowers the radiator cooling fan triggering threshold (stock 105°C) to improve engine cooling reliability.",
      valeo_temp_label: "Set temperature:",
      valeo_btn: "Select Valeo V42 Flash",
      pop_title: "Pop & Bang (Ignition Retard)",
      pop_desc: "Configures flame pops and burble crackles on deceleration (overrun ignition retard).",
      pop_btn: "Select Petrol Flash (.bin)",
      airbag_title: "Airbag Crash Data Reset",
      airbag_desc: "Resets crash recording sectors in Airbag module EEPROM dumps back to virgin factory state.",
      airbag_btn: "Select Airbag EEPROM",
      toyota_immo_title: "Toyota Denso & Patrol IMMO OFF",
      toyota_immo_desc: "Disables electronic immobilizer on Toyota Denso (Gen 1, Gen 2, Gen 3, Gen 4) and Nissan Patrol V8 (switch 20 36 5A A5 ➔ 20 36 A5 5A and block clear).",
      toyota_immo_btn: "Select Toyota / Patrol Flash (.bin)",
      toyota_hardcut_title: "Toyota D-4D Popcorn / Hardcut",
      toyota_hardcut_desc: "Sets a sharp electronic rev limiter (Hardcut rev limiter / popcorn) on Toyota D-4D diesel engines (1KD, 2KD, 1GD, 2GD) via immediate injection cutoff.",
      toyota_hardcut_rpm: "Cutoff RPM:",
      toyota_hardcut_btn: "Select Toyota Denso Flash (.bin)"
    },
    catalog: {
      title: "📚 Complete Catalog of Supported ECUs",
      search_placeholder: "🔍 Search a brand or ECU (e.g., EDC17, SID310, Delphi DCM, Tata, Mahindra, VAG...)"
    },
    history: {
      title: "📜 Your Modified Files History",
      col_date: "Date",
      col_ecu: "ECU",
      col_options: "Options",
      col_credits: "Credits",
      col_file: "Modified File",
      col_action: "Action",
      btn_download: "Download",
      status_completed: "Success",
      status_failed: "0 mods",
      empty: "No modified files recorded yet."
    },
    credits: {
      title: "💳 Credit Management & Plans",
      desc: "Top up your account to perform ECU modifications, Stage remaps, and sensor deletes.",
      balance_label: "Your Available Balance",
      credits_unit: "Credits",
      beta_alert_title: "Beta-Testing Credit Policy:",
      beta_alert_text: "During the testing phase, credits are managed exclusively by the master administrator. Your initial 100 credits are granted upon workshop approval. For extra refills, contact your administrator directly.",
      pricing_title: "⚡ Credit Packages (Indicative Rates)",
      pack_discovery: "Discovery Pack",
      pack_discovery_sub: "Ideal for 3 to 5 vehicles",
      pack_discovery_btn: "Add 50 Credits",
      pack_pro: "Workshop Pro Pack",
      pack_pro_badge: "Most Popular",
      pack_pro_sub: "Recommended for professionals",
      pack_pro_btn: "Add 150 Credits",
      pack_master: "Unlimited Master Pack",
      pack_master_sub: "For high-volume tuners",
      pack_master_btn: "Add 500 Credits",
      custom_title: "⚙️ Custom Amount",
      custom_desc: "Specify exactly how many credits you need:",
      custom_btn: "Top Up",
      transactions_title: "📜 Recent Credit Transactions History",
      col_trans_date: "Date & Time",
      col_trans_op: "Operation / Description",
      col_trans_var: "Change",
      col_trans_stat: "Status"
    },
    modals: {
      close: "Close",
      cancel: "Cancel",
      save: "Save",
      login_title: "SCORPION REMAP PRO V3.2.0",
      login_sub: "Welcome to the testing platform. Identify your workshop to unlock your <b>100 free test credits</b>.",
      garage_label: "🏢 Workshop Name or Email Address:",
      garage_placeholder: "e.g.: MY WORKSHOP or contact@garage.com",
      code_label: "🔑 Tester Access Code:",
      code_sub: "Default code: <code>BETA2026</code>",
      btn_enter: "🚀 Continue to Workshop Studio",
      securing_title: "Securing your workshop account:",
      securing_desc: "Enter your email to receive permanent server link updates and set a password to secure your credits.",
      selected_garage_label: "🏢 Selected Workshop:",
      email_label: "📧 Your Email Address:",
      email_placeholder: "e.g.: contact@garagediag.com",
      email_sub: "Used to contact you and broadcast permanent server links.",
      define_pwd_label: "🔑 Set your Password:",
      define_pwd_placeholder: "Min. 6 characters",
      confirm_pwd_label: "🔑 Confirm Password:",
      confirm_pwd_placeholder: "Retype your password",
      btn_save_profile: "💾 Save Account & Access Studio",
      btn_switch_garage: "⬅️ Switch workshop",
      secured_title: "Secured Workshop:",
      secured_desc: "This workshop is password-protected. Enter your personal password to access your space and credits.",
      workshop_pwd_label: "🔑 Workshop Password:",
      btn_unlock_workshop: "🚀 Unlock Workshop",
      btn_choose_other_garage: "⬅️ Choose another workshop",
      admin_toggle_link: "🔐 Are you the administrator? Master Login",
      pwd_modal_title: "🔑 Change Password",
      pwd_current: "Current password:",
      pwd_new: "New password:",
      pwd_new_placeholder: "Min. 8 chars (letters + numbers)",
      pwd_confirm: "Confirm password:",
      pwd_confirm_placeholder: "Retype your new password",
      btn_save_pwd: "Save",
      report_title: "🚨 Report a Technical Issue",
      report_file_label: "📄 Target File:",
      report_loading: "Loading binary dump information...",
      report_tester_name: "Your Name or Workshop / Garage:",
      report_tester_placeholder: "e.g.: Pro Auto Diag, Alex Tuning",
      report_cat_label: "Issue category encountered:",
      report_cat_no_mod: "0 modification applied / Switch not found in dump",
      report_cat_wrong_det: "Wrong Brand or ECU detected",
      report_cat_dtc_present: "Fault code (DTC) still present on diagnosis after flashing",
      report_cat_limp: "Limp mode or engine check light persisting",
      report_cat_tool_err: "Flash tool rejected file (Kess, Autotuner, CMD, Foxflash)",
      report_cat_other: "Other technical remark / suggestion",
      report_comment_label: "Workshop details (Remaining DTC codes, flash tool used...):",
      report_comment_placeholder: "e.g.: DTC P2002 is still active after flashing MOD. Read/written with Kess 3 in Bench.",
      btn_submit_report: "🚀 Submit Report & Archive Dump",
      my_tickets_title: "🎫 My Technical Reports & Support Answers",
      my_tickets_loading: "Loading your reports...",
      dtc_title: "DTC Table Inspector",
      dtc_subtitle: "Real-time binary dump analysis. Detects active error codes and already disabled (OFF) ones.",
      dtc_codes_label: "Codes:",
      dtc_filter_all: "All",
      dtc_filter_active: "🟢 Active (ON)",
      dtc_filter_disabled: "🔴 Already OFF",
      dtc_search_placeholder: "🔎 Search code or component (e.g.: 0420, P2002, Catalyst, Sensor, DPF...)",
      dtc_col_dtc: "DTC Code",
      dtc_col_state: "State in ECU",
      dtc_col_desc: "Description / Associated System",
      dtc_col_offset: "Dump Offset",
      dtc_loading: "Scanning and loading DTC table...",
      dtc_selected_suffix: "code(s) selected for deletion.",
      dtc_btn_apply: "➕ Add checked DTCs to request"
    },

    flexfuel: {
      tab_title: "FlexFuel E85 & Cold Start Pro Studio (Stock Lab)",
      tab_subtitle: "Bioethanol volumetric recalibration (+28%), parametric cold start & RON 105 ignition timing maps.",
      btn_coverage: "Supported ECUs (85+ Families)",
      btn_guide: "Workshop User Guide",
      badge_anti_diesel: "🛡️ Anti-Diesel Guard Active",

      drop_title: "Drop your Petrol Flash dump here (.bin, .ori)",
      drop_subtitle: "Compatible with Bosch MED17, MED9, MEV17, Sagem S3000, Continental EMS, Ford EcoBoost, Delco, etc.",
      btn_browse: "📁 Browse files",
      analyzing_spinner: "Analyzing dump and identifying petrol engine map...",

      diesel_title: "Action Prohibited: DIESEL Engine Detected",
      diesel_desc_prefix: "The analyzed dump corresponds to a",
      diesel_desc_suffix: "To prevent mechanical damage and engine destruction, Bioethanol E85 conversion is strictly locked on this file.",
      diesel_guarantee: "🛡️ Guaranteed safety: 0 credit deducted, original file 100% untouched.",

      eligible_title: "Petrol Dump Validated — Eligible for FlexFuel E85",
      eligible_subtitle: "Internal combustion engine compatible with Bioethanol / E85",
      eligible_badge: "✨ Ready for Calibration",

      meta_filename: "File Name",
      meta_filesize: "Flash Size",
      meta_brand: "Detected Brand",
      meta_ecu: "ECU Model",
      meta_tier: "Generation / Pricing",

      section_title: "Exclusive FlexFuel E85 & Cold Start Options (Stock Lab)",

      card_bicarb_title: "🌿 FlexFuel E85 (Dual-Fuel)",
      card_bicarb_desc: "Volumetric recalibration of mass injection flow. Allows running on pump petrol (RON 95/98) or pure E85 without piggyback box.",
      label_enrichment: "Base enrichment:",
      label_presets: "Blends:",
      label_ai: "AI Adaptive Trims (dynamic STFT / LTFT optimization)",

      card_coldstart_title: "❄️ Cold Start Winter Pro",
      card_coldstart_desc: "Cold start cranking maps mapped over coolant temp from -30°C to +80°C. Eliminates harsh cold winter starts.",
      label_coldstart: "Cold start level:",
      cs_lvl1: "Level 1: +15% Cranking (Warm / Mild climate)",
      cs_lvl2: "Level 2: +25% Cranking (Standard E85)",
      cs_lvl3: "Level 3: +35% Cranking (Recommended Mid-Season / Winter)",
      cs_lvl4: "Level 4: +45% Cranking (Cold 0°C to 10°C)",
      cs_lvl5: "Level 5: +55% Cranking (Severe cold)",
      cs_hard: "Hard-Start: +80% Cranking (Deep freezing < -5°C)",

      card_oilfix_title: "🛡️ Oil-Fix Protection (Anti-Dilution)",
      card_oilfix_desc: "Crucial for direct injection (PSA 1.2 PureTech & VAG TSI): limits post-injection to prevent ethanol oil thinning.",
      oilfix_badge: "Active engine protection",

      card_stage_title: "⚡ E85 + Stage 1 Performance",
      card_stage_desc: "Optimizes ignition timing (+4.5°) leveraging the anti-knock capability of high-octane E85 (RON 105). Enhanced torque and response.",
      label_stage: "Power level:",
      stage_1: "Stage 1 FlexFuel (Ignition advance +4.5°)",
      stage_2: "Stage 2 FlexFuel (Ignition advance +6.5° & Boost)",
      stage_none: "Stock Power (OEM timing)",

      card_lambda_title: "🔍 Oxygen Sensors & Catalyst Monitoring",
      card_lambda_desc: "Selective Lambda loop configuration and automatic catalyst DTC clearing for zero check engine lights.",
      o2_aval: "Downstream O2 Sensor 2 Off (Cat Monitoring)",
      o2_amont: "Upstream O2 Sensor 1 Off (Regulation)",
      o2_both: "Both 1 & 2 Off (Full Decat)",
      o2_none: "Standard Closed Loop (Sensors Active)",
      chk_cat: "CAT OFF (22 DTCs)",
      chk_richness: "Fuel Trim DTCs (27 DTCs)",
      chk_evap: "EVAP OFF (8 DTCs)",

      cost_label: "Workshop service cost",
      credits_unit: "Credits",
      btn_launch: "🚀 Launch FlexFuel E85 Calibration",
      processing: "Applying E85 calibration & computing Autosar Checksum...",
      report_title: "Technical Modification Report (Stock Lab Pro)",
      btn_download: "Download Calibrated E85 File (.bin)",
      checksum_badge: "✓ TriCore / Autosar Checksum 100% Validated",

      cov_modal_title: "Complete List of Supported Petrol ECUs & Engines",
      cov_modal_sub: "FlexFuel E85 Pro Studio Engine — 889 Exact VAG Patches + Dynamic Procedural Algorithm",
      cov_search_placeholder: "Search by ECU, brand, engine or model (e.g.: PureTech, MED17, Simos 18, Clio, THP, Golf, BMW...)",
      cov_btn_close: "Close List",
      guide_btn_close: "Close Guide",
      guide: {
        modal_title: "Technical Guide & Workshop Protocol — FlexFuel E85",
        modal_subtitle: "Bioethanol Calibration, Fuel Blending Math, Cold Start Stages & Engine Safety",
        ch1_title: "<i class=\"fa-solid fa-leaf\" style=\"color:var(--accent-green)\"></i> 1. Stoichiometric Ratio & Trims Self-Learning (STFT / LTFT)",
        ch1_body: "<p>Pure ethanol (E100) or pump Superethanol (E85 summer/winter) requires a stoichiometric AFR of approximately <strong>9.7:1</strong>, compared to <strong>14.7:1</strong> for standard unleaded petrol (RON 95/98).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Base volumetric enrichment (+28%):</strong> The dyno-proven golden reference. Delivers the required mass flow without maxing out original injector duty cycles.</li>\n  <li><strong>Active AI Adaptive Trims:</strong> Enables the ECU to dynamically adapt short-term (STFT) and long-term (LTFT) fuel trims. Drivers can blend pump petrol and E85 in any ratio with zero piggyback box.</li>\n</ul>",
        ch2_title: "<i class=\"fa-solid fa-calculator\" style=\"color:#f59e0b\"></i> 2. Formula & Fuel Blend Calculations (50/50, 60/40, 70/30, 80/20, 100%)",
        ch2_body: "<p>Not all customers run on 100% pure E85. For vehicles with small factory injectors or custom fuel blends, here is the exact fuel demand calculation:</p>\n<div style=\"background:#090e17; border:1px solid #1e293b; border-radius:8px; padding:12px; margin:10px 0; font-family:'Consolas', monospace; font-size:13px; color:#38bdf8;\">\n  <strong>Stoichiometric Formula:</strong> Required Enrichment (%) = (% Ethanol in tank / 100) × 28%\n</div>\n<div style=\"overflow-x:auto; margin-top:10px;\">\n  <table style=\"width:100%; border-collapse:collapse; font-size:12px; text-align:left;\">\n    <thead>\n      <tr style=\"border-bottom:1px solid #334155; color:#94a3b8;\">\n        <th style=\"padding:8px;\">Tank Blend</th>\n        <th style=\"padding:8px;\">Ethanol / Petrol Ratio</th>\n        <th style=\"padding:8px;\">Calculated Enrichment</th>\n        <th style=\"padding:8px;\">Recommended Slider Setting</th>\n      </tr>\n    </thead>\n    <tbody style=\"color:#cbd5e1;\">\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>50% E85 / 50% Petrol</strong></td>\n        <td style=\"padding:8px;\">Half &amp; Half</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+14%</td>\n        <td style=\"padding:8px;\">Slider at <strong>+14%</strong> (ideal for small injectors)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>60% E85 / 40% Petrol</strong></td>\n        <td style=\"padding:8px;\">60% Ethanol / 40% Petrol</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+17%</td>\n        <td style=\"padding:8px;\">Slider at <strong>+17%</strong> (very stable economic compromise)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>70% E85 / 30% Petrol</strong></td>\n        <td style=\"padding:8px;\">70% Ethanol / 30% Petrol</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+20%</td>\n        <td style=\"padding:8px;\">Slider at <strong>+20%</strong> (popular for winter)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>80% E85 / 20% Petrol</strong></td>\n        <td style=\"padding:8px;\">80% Ethanol / 20% Petrol</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+23%</td>\n        <td style=\"padding:8px;\">Slider at <strong>+23%</strong> (winter pump grade E85)</td>\n      </tr>\n      <tr>\n        <td style=\"padding:8px;\"><strong>100% E85 (Pure)</strong></td>\n        <td style=\"padding:8px;\">Full Bioethanol tank</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+28%</td>\n        <td style=\"padding:8px;\"><strong>FlexFuel Golden Point:</strong> with <em>AI Adaptive Trims</em> active, the engine handles ALL above blends automatically!</td>\n      </tr>\n    </tbody>\n  </table>\n</div>\n<div style=\"margin-top:12px; font-size:12px; color:#cbd5e1; background:rgba(245, 158, 11, 0.12); border-left:3px solid #f59e0b; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#f59e0b;\">💡 Why is the +28% setting optimal in 95% of cases?</strong><br>\n  With <strong>AI Adaptive Trims</strong>, factory oxygen sensors adjust trims in real-time (STFT/LTFT up to ±25%). Therefore, even with the slider at +28%, if the client fills up with 50/50 or pure petrol, the ECU auto-adapts without CEL! Manual presets (+14%, +20%) are mainly for tuners who want a capped fixed blend or small injector protection.\n</div>",
        ch3_title: "<i class=\"fa-solid fa-snowflake\" style=\"color:var(--accent-cyan)\"></i> 3. Cold Start Stages (Winter Pro Cold Start)",
        ch3_body: "<p>Ethanol has a very low vapor pressure and does not vaporize spontaneously below 12°C - 15°C. Our solution recalibrates starter cranking enrichment across the full coolant temp curve (-30°C to +80°C).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Level 1 (+15%):</strong> Mild climate / Warm southern regions in summer (&gt; 20°C).</li>\n  <li><strong>Level 2 (+25%):</strong> Mild spring and autumn (15°C to 20°C).</li>\n  <li><strong>Level 3 (+35%) [Default Recommendation]:</strong> Ideal mid-season and autumn/winter (5°C to 15°C). Instant first-turn engine start.</li>\n  <li><strong>Level 4 (+45%):</strong> Standard cold winter (0°C to 5°C).</li>\n  <li><strong>Level 5 & Hard-Start (+75% to +80%):</strong> Mountain areas or continuous freezing weather (&lt; 0°C).</li>\n</ul>",
        ch4_title: "<i class=\"fa-solid fa-shield-halved\" style=\"color:var(--accent-orange)\"></i> 4. Direct Injection & Oil-Fix Protection (Anti-Dilution)",
        ch4_body: "<p>On modern direct injection engines (e.g.: <strong>PSA 1.2 PureTech / THP</strong>, <strong>VAG 1.4 / 2.0 TSI TFSI</strong>, <strong>Ford EcoBoost</strong>, <strong>Renault TCe</strong>):</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>Mechanical risk:</strong> During cold phases, unburnt ethanol can wash away the protective oil film on cylinder walls and seep into the oil sump, causing oil thinning and viscosity loss.</li>\n  <li><strong>Oil-Fix mechanism:</strong> Our algorithm trims unnecessary post-injections at low temperatures and accelerates combustion chamber warmup.</li>\n  <li><strong>Workshop recommendation:</strong> Advise customers to shorten engine oil service intervals to <strong>10,000 km or 15,000 km maximum</strong> using manufacturer-approved synthetic oil.</li>\n</ul>",
        ch5_title: "<i class=\"fa-solid fa-magnifying-glass-chart\" style=\"color:#06b6d4\"></i> 5. Oxygen Sensors & Catalyst Monitoring (Zero CEL Guaranteed)",
        ch5_body: "<p>Ethanol changes exhaust gas temperature and chemical composition (more water vapor and different stoichiometric ratio). Without dedicated monitoring loop calibration, false emissions warning lights may trigger on the dash.</p>\n<ul style=\"margin-top:6px; margin-bottom:8px;\">\n  <li><strong>Upstream O2 Sensor 1 (Pre-Cat) — 100% Preserved:</strong> Vital regulating sensor. Constantly measures mixture richness and drives closed-loop feedback to adjust fueling in real time.</li>\n  <li><strong>Downstream O2 Sensor 2 Off (Post-Cat):</strong> Deactivates only catalyst efficiency diagnostics. Permanently removes false code <strong>P0420 / P0430</strong> (Catalyst system efficiency below threshold).</li>\n  <li><strong>CAT OFF (22 DTCs):</strong> Surgically disables all fault codes related to catalytic converter efficiency. Also allows installation of sport exhausts or catless downpipes with zero CEL.</li>\n  <li><strong>Fuel Trim DTCs (27 DTCs):</strong> Suppresses extreme fuel trim drift alerts (e.g.: <strong>P0171, P0174, P2177, P2179</strong> — System too lean). Prevents CEL during transient phases when rapidly switching from petrol to 100% E85.</li>\n  <li><strong>EVAP OFF (8 DTCs):</strong> Clears fuel vapor recovery system faults (Canister P0440 to P0455). Different ethanol vapor pressure won't trigger false tank purge errors.</li>\n</ul>\n<div style=\"font-size:12px; color:#cbd5e1; background:rgba(6, 182, 212, 0.12); border-left:3px solid #06b6d4; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#06b6d4;\">✅ Client & Workshop Benefit:</strong> Vehicle passes emissions inspection with clean OBD memory, maintains crisp throttle response via the upstream sensor, and ensures a completely clear dashboard.\n</div>",
        ch6_title: "<i class=\"fa-solid fa-list-check\" style=\"color:#c084fc\"></i> 6. Workshop Checklist & Customer Handover Protocol",
        ch6_body: "<p>For a 100% guaranteed outcome with zero client returns, follow this workshop protocol:</p>\n<div class=\"guide-step-box\">\n  <div class=\"step-item\">\n    <div class=\"step-num\">Step 1</div>\n    <div class=\"step-title\">Flash Writing</div>\n    <div class=\"step-desc\">Write the MOD file with your tuning tool. Checksum is computed automatically.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Step 2</div>\n    <div class=\"step-title\">Clear DTCs</div>\n    <div class=\"step-desc\">Mandatory full fault code memory clearing before starting the engine.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Step 3</div>\n    <div class=\"step-title\">E85 Fill-up</div>\n    <div class=\"step-desc\">Fill at least 50% to 70% bioethanol for initial test (or 100% straight).</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Step 4</div>\n    <div class=\"step-title\">3 Min Idle</div>\n    <div class=\"step-desc\">Let engine idle for 3 minutes without touching throttle for initial trim learning.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">Step 5</div>\n    <div class=\"step-title\">Road Test</div>\n    <div class=\"step-desc\">5 to 10 min road test: sharp accelerations, throttle response check, and verify zero CEL.</div>\n  </div>\n</div>"
      }
    }
  },

  ar: {
    brand_badge: "PRO v3.2.0",
    nav: {
      studio: "🛠️ استوديو البرمجة",
      expert: "🧰 أدوات متقدمة",
      flexfuel: "🌿 فليكس فيول E85",
      catalog: "📚 دليل الكمبيوترات",
      history: "📜 سجل العمليات",
      credits: "💳 باقات الرصيد",
      changelog: "📋 سجل التحديثات",
      my_tickets: "🎫 بلاغاتي الفنية",
      admin: "⚙️ لوحة الإدارة",
      donate: "دعم المنصة",
      connecting: "جارٍ الاتصال...",
      tester_badge: "مختبر ورشة",
      credits_label: "رصيد",
      switch_account: "تبديل الحساب"
    },
    announcement: {
      action_required: "إجراء مطلوب:",
      profile_completion: "يرجى تأمين حساب ورشتكم عبر البريد الإلكتروني وكلمة مرور خاصة لحفظ رصيدكم واستلام الرابط الدائم للخادم.",
      secure_account_btn: "🔒 تأمين حسابي الآن",
      view_changelog: "📋 عرض التحديثات ←"
    },
    sim2k_promo: {
      badge_hot: "🔥 جديد وحصري",
      badge_ecu: "CONTINENTAL SIM2K-510",
      badge_models: "كيا وهيونداي 2021–2026",
      title: "جديد وحصري على المنصة : CONTINENTAL SIM2K-510 (كيا وهيونداي)",
      features_html: "<strong>باقة متكاملة شاملة :</strong> حذف AdBlue + إلغاء Start & Stop + حذف فلتر البنزين OPF/GPF + حذف EGR + حذف حساسات الكاتاليزور Decat/Lambda.",
      instant_text: "⚡ دفع مباشر فوري وآمن : 120,00 € (فيزا/ماستركارد) أو 35 000 دج (البطاقة الذهبية / CIB). تحميل فوري في 30 ثانية.",
      btn_cta: "📤 اسحب أو اختر ملف SIM2K-510 الآن ←"
    },
    studio: {
      drop_title: "اسحب وأفلت ملف كمبيوتر السيارة (.bin, .ori)",
      drop_subtitle: "أو انقر لاختيار الملف من جهازك (Continental SID, Bosch EDC16/17/MD1, Delphi, Marelli...)",
      file_analyzed: "الملف المفحوص",
      detected_ecu: "الشركة / الكمبيوتر المكتشف",
      high_confidence: "توافق عالي ومؤكد",
      medium_confidence: "توافق متوسط",
      change_file: "🔄 تغيير الملف",
      fuel_detecting: "⛽ نوع المحرك: جارٍ الفحص...",
      fuel_diesel: "⛽ المحرك: ديزل (HDi / TDI / dCi / CRDi)",
      fuel_gasoline: "⛽ المحرك: بنزين / تيربو بنزين",
      report_detection_error: "⚠️ خطأ في التعرف على الملف؟ إبلاغ",
      unknown_title: "لم يتم التعرف على الكمبيوتر تلقائياً",
      unknown_desc: "تم تصنيف هذا الملف كـ \"Unknown\". تم قفل التعديل تلقائياً لحماية الملف من أي خطأ.<br><span style=\"color:#fde047; font-weight:700;\">👉 يجب عليكم اختيار نوع السيارة والكمبيوتر يدوياً</span> من القائمة أدناه لفتح التعديل.",
      adjust_label: "⚙️ ضبط يدوي إذا لزم الأمر:",
      brand_label: "الشركة المصنعة",
      ecu_label: "كمبيوتر السيارة (ECU)",
      select_options_title: "⚙️ اختر الحلول البرمجية المطلوب تطبيقها",
      custom_dtc_title: "⚠️ حذف أكواد الأعطال المخصصة (DTC OFF)",
      custom_dtc_btn: "🔍 فحص جدول الأعطال DTC (مفعل / ملغي)",
      custom_dtc_desc: "أدخل أي كود عطل OBD-II (مثال: P20EE, P2201, P0420) أو اضغط على زر الفحص أعلاه لمشاهدة حالة أكواد الأعطال في الملف.",
      custom_dtc_placeholder: "مثال: P20EE, P2201, P0420",
      total_required: "الرصيد المطلوب:",
      current_balance: "رصيدكم الحالي:",
      btn_process: "⚡ تعديل وتوليد الملف (.MOD)",
      btn_processing: "⏳ جارٍ التعديل والحساب...",
      stage_match_title: "🔥 تم العثور على خريطة معايرة متطابقة!",
      stage_match_sub: "تم إيجاد ملف Stage 1 / FlexFuel مطابق 100% لهذا الكمبيوتر.",
      stage_match_badge: "متوافق 100%"
    },
    options: {
      dpf_title: "💨 إلغاء DPF / FAP OFF",
      dpf_desc: "إلغاء دورات تجديد فلتر الجسيمات وحساسات الضغط التفاضلي والحرارة EGT.",
      egr_title: "🔄 إلغاء صمام EGR OFF",
      egr_desc: "إغلاق دائم لصمام إعادة تدوير الغازات EGR وإلغاء مسارات الأعطال التابعة له.",
      adblue_title: "💧 إلغاء نظام AdBlue / SCR OFF",
      adblue_desc: "حذف مضخة اليوريا، حساسات NOx ورسائل منع التشغيل نهائياً.",
      start_stop_title: "⚡ إلغاء نظام Start & Stop OFF",
      start_stop_desc: "حفظ حالة إيقاف النظام تلقائياً عند تشغيل المحرك.",
      vmax_title: "🚀 فك السرعة القصوى (VMax OFF)",
      vmax_desc: "إلغاء محدد السرعة الإلكتروني VMax للسيارة.",
      flaps_title: "🌪️ إلغاء بوابات الهواء Swirl Flaps OFF",
      flaps_desc: "إلغاء عمل بوابات مجمع السحب وبوابة الهواء الإلكترونية TVA.",
      stage1_title: "🏁 برمجة قوة Stage 1 (+25% إلى +35%)",
      stage1_desc: "تعديل احترافي متوازن لعزم الدوران، حقن الوقود وضغط شاحن التيربو.",
      stage2_title: "🏁 برمجة قوة Stage 2 (سبورت / داون بايب)",
      stage2_desc: "مخصصة للمركبات المزودة بنظام سحب رياضي، إنتركولر أو عادم مفرغ.",
      flexfuel_title: "🌽 تحويل FlexFuel E85 (إيثانول)",
      flexfuel_desc: "برمجة للعمل على وقود إيثانول E85 أو بنزين عادي بنسب متغيرة.",
      decat_title: "🔥 إلغاء حساس الشكمان Decat / O2 OFF",
      decat_desc: "إلغاء كود ضعف الكاتالايزر (P0420) وحساس الأكسجين الخلفي O2.",
      pop_bang_title: "💥 نظام Pop & Bang (طرب الشكمان)",
      pop_bang_desc: "تأخير شرارة الإشعال عند رفع القدم عن الوقود لإحداث أصوات مفرقعات رياضية.",
      immo_off_title: "🔑 إلغاء نظام مانع التشغيل IMMO OFF",
      immo_off_desc: "إلغاء تشفير المفتاح (Bosch TriCore MEDC17, Toyota Denso Gen 1-4, Nissan Patrol V8 وغيرها).",
      credits: "نقاط رصيد"
    },
    results: {
      success_title: "!تم تعديل الملف بنجاح تام ✅",
      success_count: "تعديلات مطبقة",
      already_applied_title: "ℹ️ الملف معدل مسبقاً (0 بايت للتعديل) !",
      already_applied_summary: "هذا الملف يحتوي مسبقاً على جميع الحلول المطلوبة.<br>قام المحرك بالتأكد من أن الخرائط، السويتشات وأكواد الأعطال بحالة OFF بالفعل.<br><b>أمان مضمون: تم خصم 0 رصيد</b> (رصيدكم سليم: {balance} نقطة).",
      failed_title: "❌ تنبيه: تم تعديل 0 بايت (الملف لم يتغير) !",
      failed_summary: "لم يتم تطبيق أي تعديل على هذا الملف.<br>لم يتم العثور على سويتشات أو جداول DTC مطابقة لهذا الكمبيوتر في هذا الدامب.<br><b>أمان: لم يتم خصم أي رصيد</b> (رصيدكم سليم: {balance} نقطة).",
      workshop_instructions: "🔧 تعليمات الورشة الفنية بعد البرمجة:",
      btn_download: "📥 تحميل الملف المعدل (.bin)",
      btn_donate: "💖 دعم المنصة / التبرع",
      btn_new_file: "🔄 تعديل ملف آخر",
      btn_report: "🚨 الإبلاغ عن مشكلة في الملف",
      btn_report_info: "ℹ️ تفاصيل الخريطة",
      diff_title: "تفاصيل العناوين المعدلة (Hex Offsets):",
      col_address: "عنوان الذاكرة Hex",
      col_desc: "الوصف الفني",
      col_original: "الأصلي",
      col_modified: "المعدل",
      no_diffs_already: "جميع الخرائط والسويتشات مطابقة مسبقاً للخيارات المطلوبة. لم يتم تعديل أي عنوان (0 بايت تم تغييره).",
      no_diffs_identical: "لم يتم تعديل أي عنوان. الملف الأصلي والملف الهدف متطابقان 100%."
    },
    instructions: {
      dpf: "فلتر البيئة DPF / FAP: فصل قابس حساس الضغط التفاضلي وحساسات حرارة العادم إذا تم تفريغ الفلتر.",
      egr: "صمام EGR: فصل القابس الكهربائي لصمام EGR أو وضع صفيحة عزل محكمة.",
      adblue: "نظام AdBlue / SCR: يجب حتماً فصل قابس مضخة اليوريا / كمبيوتر AdBlue بعد برمجة الملف لتفادي إعادة التفعيل.",
      clear_dtc: "تعليمات الورشة: إجراء مسح شامل لذاكرة الأعطال (DTC Clear) بجهاز الفحص بعد البرمجة وقبل تشغيل المحرك.",
      checksum_tricore: "معادلة Checksum TriCore Autosar: تم فحص وتصحيح التوقيع بنجاح عبر المحرك العتادي."
    },
    expert: {
      title: "🧰 صندوق أدوات الورشة المتقدمة",
      subtitle: "وظائف برمجية متطورة وسريعة (1 رصيد لكل عملية)",
      pcr_title: "فك حماية VAG Continental PCR 2.1 OBD",
      pcr_desc: "فك حماية برمجة OBD في إيبروم 95640 للسماح بالبرمجة عبر فيشة التشخيص بدون فك الكمبيوتر. يتعرف على شفرة Simos ورقم الشاسيه ونوع المحرك (CAYC, CAYD...).",
      pcr_btn: "اختر إيبروم PCR 2.1 (8 كيلوبايت أو 136)",
      cold_title: "حل مشكلة التشغيل على البارد في رينو (Cold Start)",
      cold_desc: "حل نهائي لمشكلة صعوبة بدء التشغيل صباحاً في كمبيوترات رينو EMS3110, EMS3125, EMS3132 و Valeo V42.",
      cold_btn: "اختر فلاش رينو (.bin)",
      valeo_title: "تعديل مروحة التبريد Renault Valeo V42",
      valeo_desc: "تخفيض درجة حرارة تشغيل مروحة الردياتير (الأصلية 105°C) لحماية المحرك من السخونة الزائدة.",
      valeo_temp_label: "حرارة التشغيل:",
      valeo_btn: "اختر فلاش Valeo V42",
      pop_title: "برمجة شكمان طرب Pop & Bang",
      pop_desc: "تأخير شرارة الإشعال عند التباطؤ لإصدار فرقعات رياضية مع خروج نيران من العادم.",
      pop_btn: "اختر فلاش بنزين (.bin)",
      airbag_title: "تصفير حساسات الإيرباج Airbag Crash Reset",
      airbag_desc: "مسح سجلات الحوادث في ملفات إيبروم كمبيوترات الإيرباج وإعادتها لحالة الوكالة.",
      airbag_btn: "اختر إيبروم الإيرباج",
      toyota_immo_title: "إلغاء تشفير تويوتا وباترول IMMO OFF",
      toyota_immo_desc: "إلغاء مانع التشغيل لكمبيوترات Toyota Denso (Gen 1, 2, 3, 4) ونيسان باترول V8 بتبديل السويتش وتصفير البلوكات.",
      toyota_immo_btn: "اختر فلاش تويوتا / باترول (.bin)",
      toyota_hardcut_title: "قاطع ديزل تويوتا D-4D Popcorn / Hardcut",
      toyota_hardcut_desc: "تفعيل قاطع دوران حاد وسريع (Hardcut Limiter) على محركات تويوتا ديزل D-4D (1KD, 2KD, 1GD, 2GD) بقطع فوري لحقن الديزل.",
      toyota_hardcut_rpm: "دوران القاطع:",
      toyota_hardcut_btn: "اختر فلاش تويوتا Denso (.bin)"
    },
    catalog: {
      title: "📚 الدليل الشامل لكمبيوترات السيارات المدعومة",
      search_placeholder: "🔍 ابحث عن ماركة أو كمبيوتر (مثال: EDC17, SID310, Delphi DCM, Tata, Mahindra, Toyota...)"
    },
    history: {
      title: "📜 سجل الملفات المعدلة الخاصة بكم",
      col_date: "التاريخ",
      col_ecu: "الكمبيوتر",
      col_options: "الخيارات",
      col_credits: "الرصيد",
      col_file: "الملف المعدل",
      col_action: "إجراء",
      btn_download: "تحميل",
      status_completed: "ناجح",
      status_failed: "0 تعديل",
      empty: "لا توجد ملفات معدلة مسجلة حتى الآن."
    },
    credits: {
      title: "💳 إدارة باقات وشحن الرصيد",
      desc: "شحن رصيد حسابكم لتنفيذ تعديلات المحرك، برمجة القوة وحذف الأنظمة البيئية.",
      balance_label: "رصيدكم المتاح حالياً",
      credits_unit: "نقطة رصيد",
      beta_alert_title: "سياسة نقاط الرصيد في مرحلة التجربة:",
      beta_alert_text: "خلال الفترة التجريبية، يتم إدارة وتوزيع الرصيد حصرياً من قِبل إدارة المنصة. تمنحكم المنصة 100 نقطة مجانية فور قبول حساب ورشتكم. لطلب رصيد إضافي، تواصلوا مباشرة مع الإدارة.",
      pricing_title: "⚡ باقات شحن الرصيد (أسعار استرشادية)",
      pack_discovery: "باقة البداية (Discovery)",
      pack_discovery_sub: "مناسبة لتعديل 3 إلى 5 سيارات",
      pack_discovery_btn: "إضافة 50 نقطة",
      pack_pro: "باقة الورشة الاحترافية (Pro)",
      pack_pro_badge: "الأكثر طلباً",
      pack_pro_sub: "موصى بها لأصحاب الورش",
      pack_pro_btn: "إضافة 150 نقطة",
      pack_master: "باقة ماستر غير المحدودة",
      pack_master_sub: "للورش ذات النشاط العالي",
      pack_master_btn: "إضافة 500 نقطة",
      custom_title: "⚙️ شحن كمية مخصصة",
      custom_desc: "حدد عدد النقاط المطلوب بدقة:",
      custom_btn: "شحن الرصيد",
      transactions_title: "📜 سجل حركات الرصيد الأخيرة",
      col_trans_date: "التاريخ والوقت",
      col_trans_op: "العملية / الوصف",
      col_trans_var: "التغيير",
      col_trans_stat: "الحالة"
    },
    modals: {
      close: "إغلاق",
      cancel: "إلغاء",
      save: "حفظ",
      login_title: "SCORPION REMAP PRO V3.2.0",
      login_sub: "أهلاً بكم في منصة البرمجة والتعديل. سجل اسم ورشتك للحصول على <b>100 نقطة رصيد مجانية</b>.",
      garage_label: "🏢 اسم الورشة أو البريد الإلكتروني:",
      garage_placeholder: "مثال: ورشة الإخلاص أو contact@garage.com",
      code_label: "🔑 كود الدخول الخاص:",
      code_sub: "الكود الافتراضي: <code>BETA2026</code>",
      btn_enter: "🚀 الدخول إلى استوديو الورشة",
      securing_title: "تأمين حساب ورشتكم:",
      securing_desc: "أدخل بريدك الإلكتروني لاستلام رابط الخادم الدائم في حال التحديث وعيّن كلمة مرور لحماية رصيدك.",
      selected_garage_label: "🏢 الورشة المحددة:",
      email_label: "📧 عنوان البريد الإلكتروني:",
      email_placeholder: "مثال: contact@garagediag.com",
      email_sub: "يستخدم للتواصل معكم وإرسال روابط المنصة الدائمة.",
      define_pwd_label: "🔑 تعيين كلمة المرور:",
      define_pwd_placeholder: "6 أحرف كحد أدنى",
      confirm_pwd_label: "🔑 تأكيد كلمة المرور:",
      confirm_pwd_placeholder: "أعد كتابة كلمة المرور",
      btn_save_profile: "💾 حفظ الحساب والدخول للاستوديو",
      btn_switch_garage: "⬅️ تغيير الورشة",
      secured_title: "ورشة محمية بكلمة مرور:",
      secured_desc: "هذه الورشة محمية بكلمة مرور. أدخل كلمة المرور الخاصة بك للوصول إلى مساحتك ورصيدك.",
      workshop_pwd_label: "🔑 كلمة مرور الورشة:",
      btn_unlock_workshop: "🚀 فتح استوديو الورشة",
      btn_choose_other_garage: "⬅️ اختيار ورشة أخرى",
      admin_toggle_link: "🔐 هل أنت مسؤول المنصة؟ تسجيل دخول Master",
      pwd_modal_title: "🔑 تغيير كلمة المرور",
      pwd_current: "كلمة المرور الحالية:",
      pwd_new: "كلمة المرور الجديدة:",
      pwd_new_placeholder: "8 خانات على الأقل (أحرف + أرقام)",
      pwd_confirm: "تأكيد كلمة المرور:",
      pwd_confirm_placeholder: "أعد كتابة كلمة المرور الجديدة",
      btn_save_pwd: "حفظ",
      report_title: "🚨 إبلاغ عن مشكلة فنية",
      report_file_label: "📄 الملف المعني:",
      report_loading: "جارٍ تحميل بيانات الملف...",
      report_tester_name: "اسمك أو اسم الورشة / المركز:",
      report_tester_placeholder: "مثال: ورشة الإخلاص، فني الدياج",
      report_cat_label: "نوع المشكلة التي واجهتك:",
      report_cat_no_mod: "0 تعديل مطبق / لم يتم العثور على السويتش في الملف",
      report_cat_wrong_det: "خطأ في التعرف على ماركة السيارة أو الكمبيوتر",
      report_cat_dtc_present: "كود العطل (DTC) ما زال ظاهراً بجهاز الفحص بعد البرمجة",
      report_cat_limp: "المحرك في وضع الطوارئ أو لمبة الفحص مستمرة",
      report_cat_tool_err: "رفض جهاز البرمجة للملف (Kess, Autotuner, CMD, Foxflash)",
      report_cat_other: "ملاحظة أو اقتراح فني آخر",
      report_comment_label: "تفاصيل الفني (الأكواد المتبقية، جهاز القراءة المستخدم...):",
      report_comment_placeholder: "مثال: كود P2002 ما زال ظاهراً بعد كتابة الملف المعدل. القراءة والكتابة تمت بجهاز Kess 3 على البنش.",
      btn_submit_report: "🚀 إرسال التقرير وأرشفة الملف",
      my_tickets_title: "🎫 بلاغاتي الفنية وردود الدعم الفني",
      my_tickets_loading: "جارٍ تحميل قائمة البلاغات...",
      dtc_title: "فاحص جدول أكواد الأعطال DTC",
      dtc_subtitle: "تحليل ثنائي مباشر للملف. يكشف أكواد الأعطال النشطة وتلك الملغاة مسبقاً (OFF).",
      dtc_codes_label: "الأكواد:",
      dtc_filter_all: "الكل",
      dtc_filter_active: "🟢 نشطة (ON)",
      dtc_filter_disabled: "🔴 ملغاة مسبقاً (OFF)",
      dtc_search_placeholder: "🔎 ابحث عن كود أو حساس (مثال: 0420, P2002, بيئة, حساس, دبة...)",
      dtc_col_dtc: "كود العطل DTC",
      dtc_col_state: "الحالة في الكمبيوتر",
      dtc_col_desc: "الوصف والنظام التابع له",
      dtc_col_offset: "عنوان الذاكرة (Offset)",
      dtc_loading: "جارٍ فحص وتحميل جدول أكواد الأعطال...",
      dtc_selected_suffix: "كود محدد للحذف.",
      dtc_btn_apply: "➕ إضافة الأكواد المحددة للطلب"
    },

    flexfuel: {
      tab_title: "استوديو فليكس فيول E85 وتشغيل الشتاء الاحترافي (Stock Lab)",
      tab_subtitle: "معمل إعادة المعايرة الحجمية للوقود الحيوي (+28%)، تشغيل المحرك البارد التكيفي وتقديم الإشعال RON 105.",
      btn_coverage: "الكمبيوترات المدعومة (85+ عائلة)",
      btn_guide: "دليل استخدام الورش",
      badge_anti_diesel: "🛡️ نظام حماية محركات الديزل نشط",

      drop_title: "اسحب ملف فلاش البنزين هنا (.bin, .ori)",
      drop_subtitle: "متوافق مع Bosch MED17, MED9, MEV17, Sagem S3000, Continental EMS, Ford EcoBoost, Delco وغيرها.",
      btn_browse: "📁 تصفح الملفات",
      analyzing_spinner: "جارٍ فحص الملف وتحديد خريطة محرك البنزين...",

      diesel_title: "إجراء محظور: تم اكتشاف محرك ديزل",
      diesel_desc_prefix: "الملف المفحوص يخص محرك",
      diesel_desc_suffix: "لحماية أجزاء المحرك الميكانيكية وتفادي التلف، تم قفل تعديل الإيثانول E85 بشكل صارم لهذا الملف.",
      diesel_guarantee: "🛡️ أمان مضمون: لم يتم خصم أي رصيد، والملف الأصلي سليم 100%.",

      eligible_title: "تم التحقق من ملف البنزين — مؤهل لتعديل FlexFuel E85",
      eligible_subtitle: "محرك احتراق داخلي متوافق مع الوقود الحيوي / E85",
      eligible_badge: "✨ جاهز للمعايرة",

      meta_filename: "اسم الملف",
      meta_filesize: "حجم الفلاش",
      meta_brand: "الشركة المصنعة",
      meta_ecu: "طراز الكمبيوتر (ECU)",
      meta_tier: "الجيل / الفئة السعرية",

      section_title: "الخيارات الحصرية لفليكس فيول E85 وتشغيل الشتاء (Stock Lab)",

      card_bicarb_title: "🌿 فليكس فيول E85 (نظام وقود مزدوج)",
      card_bicarb_desc: "إعادة معايرة حجمية لتدفق الحقن الكتلي. يتيح تشغيل السيارة ببنزين 95 أو 98 أو E85 الخالص دون الحاجة لجهاز خارجي.",
      label_enrichment: "نسبة الزيادة الأساسية:",
      label_presets: "خلطات سريعة:",
      label_ai: "AI Adaptive Trims (تحسين ذكي تكيفي لنسب الوقود STFT / LTFT)",

      card_coldstart_title: "❄️ تشغيل الشتاء الاحترافي (Cold Start Pro)",
      card_coldstart_desc: "خرائط تشغيل المحرك على البارد لدرجات حرارة من -30°C حتى +80°C. يقضي نهائياً على صعوبة التشغيل شتاءً.",
      label_coldstart: "مستوى التشغيل البارد:",
      cs_lvl1: "المستوى 1: +15 % Cranking (مناخ دافئ / معتدل)",
      cs_lvl2: "المستوى 2: +25 % Cranking (قياسي E85)",
      cs_lvl3: "المستوى 3: +35 % Cranking (موصى به للخريف والشتاء)",
      cs_lvl4: "المستوى 4: +45 % Cranking (طقس بارد 0°C إلى 10°C)",
      cs_lvl5: "المستوى 5: +55 % Cranking (طقس شديد البرودة)",
      cs_hard: "تشغيل قاسي (Hard-Start): +80 % Cranking (صقيع وانجماد < -5°C)",

      card_oilfix_title: "🛡️ حماية الزيت Oil-Fix (منع تخفيف الزيت)",
      card_oilfix_desc: "ضروري لمحركات الحقن المباشر (PSA 1.2 PureTech & VAG TSI): يحد من الحقن اللاحق لمنع تسرب الإيثانول لزيت المحرك.",
      oilfix_badge: "حماية ميكانيكية نشطة",

      card_stage_title: "⚡ E85 + ستيج 1 قوة وأداء",
      card_stage_desc: "تقديم توقيت الإشعال (+4.5°) بالاستفادة من رقم الأوكتان العالي للإيثانول (RON 105). زيادة ملحوظة في العزم والاستجابة.",
      label_stage: "مستوى القوة:",
      stage_1: "ستيج 1 فليكس فيول (تقديم الإشعال +4.5°)",
      stage_2: "ستيج 2 فليكس فيول (تقديم الإشعال +6.5° وضغط التيربو)",
      stage_none: "بدون ستيج (توقيت إشعال الوكالة الأصلي)",

      card_lambda_title: "🔍 مراقبة حساسات الأكسجين والكتالايزر",
      card_lambda_desc: "ضبط انتقائي لدوائر اللامبدا وإلغاء أعطال الكاتالايزر تلقائياً لمنع إضاءة لمبة فحص المحرك Check Engine.",
      o2_aval: "إلغاء الحساس السفلي رقم 2 (مراقبة الكتالايزر)",
      o2_amont: "إلغاء الحساس العلوي رقم 1 (تنظيم الاحتراق)",
      o2_both: "إلغاء الحساسين 1 و 2 (تفريغ عادم كامل)",
      o2_none: "دائرة مغلقة قياسية (الحساسات نشطة)",
      chk_cat: "إلغاء الكتالايزر CAT OFF (22 كود)",
      chk_richness: "أكواد خليط الوقود (27 كود)",
      chk_evap: "إلغاء نظام التبخير EVAP OFF (8 أكواد)",

      cost_label: "تكلفة الخدمة للورشة",
      credits_unit: "نقطة رصيد",
      btn_launch: "🚀 بدء معايرة فليكس فيول E85",
      processing: "جارٍ تطبيق معايرة E85 وحساب الشيكسم Autosar...",
      report_title: "التقرير الفني للتعديل (Stock Lab Pro)",
      btn_download: "تحميل ملف E85 المعدل (.bin)",
      checksum_badge: "✓ تم التحقق من الشيكسم TriCore / Autosar بنسبة 100%",

      cov_modal_title: "دليل الكمبيوترات والمحركات البنزين المدعومة بالكامل",
      cov_modal_sub: "محرك فليكس فيول E85 الاحترافي — قاعدة 889 باتش VAG دقيق + خوارزميات إجرائية تكيفية",
      cov_search_placeholder: "ابحث باسم الكمبيوتر، الشركة، المحرك أو الطراز (مثال: PureTech, MED17, Simos 18, Clio, THP, Golf, BMW...)",
      cov_btn_close: "إغلاق القائمة",
      guide_btn_close: "إغلاق الدليل",
      guide: {
        modal_title: "الدليل الفني وبروتوكول الورشة — فليكس فيول E85",
        modal_subtitle: "معايرة الوقود الحيوي، حساب خلطات الوقود، مراحل التشغيل البارد ومعايير الأمان الميكانيكي",
        ch1_title: "<i class=\"fa-solid fa-leaf\" style=\"color:var(--accent-green)\"></i> 1. النسبة التكافئية والتعلم الذاتي لتصحيحات الوقود (STFT / LTFT)",
        ch1_body: "<p>يتطلب الإيثانول النقي (E100) أو وقود الإيثانول في المحطات (E85 صيف/شتاء) نسبة هواء إلى وقود تكافئية تبلغ حوالي <strong>9.7:1</strong>، مقارنة بـ <strong>14.7:1</strong> للبنزين الخالي من الرصاص التقليدي (بنزين 95/98).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>الزيادة الحجمية الأساسية (+28 %):</strong> هي القيمة القياسية الذهبية المضبوطة على أجهزة الداينو، حيث توفر تدفق الوقود الكتلي المطلوب دون إجهاد بخاخات الوكالة.</li>\n  <li><strong>نظام AI Adaptive Trims التكيفي:</strong> يُمكّن كمبيوتر المحرك من تعديل تصحيحات الوقود اللحظية (STFT) والطويلة المدى (LTFT) ديناميكياً. وبذلك يستطيع العميل خلط البنزين والإيثانول بأي نسبة دون الحاجة إلى أي جهاز خارجي.</li>\n</ul>",
        ch2_title: "<i class=\"fa-solid fa-calculator\" style=\"color:#f59e0b\"></i> 2. المعادلة وحساب نسب خلط الوقود (50/50, 60/40, 70/30, 80/20, 100%)",
        ch2_body: "<p>ليس كل العملاء يزودون سياراتهم بـ 100% إيثانول خالص. للسيارات المزودة ببخاخات وكالة صغيرة السعة أو لضبط خلطات محددة حسب الطلب، إليك الحساب الدقيق لاحتياج الوقود:</p>\n<div style=\"background:#090e17; border:1px solid #1e293b; border-radius:8px; padding:12px; margin:10px 0; font-family:'Consolas', monospace; font-size:13px; color:#38bdf8;\">\n  <strong>المعادلة التكافئية:</strong> نسبة الزيادة المطلوبة (%) = (% نسبة الإيثانول في الخزان / 100) × 28 %\n</div>\n<div style=\"overflow-x:auto; margin-top:10px;\">\n  <table style=\"width:100%; border-collapse:collapse; font-size:12px; text-align:right;\">\n    <thead>\n      <tr style=\"border-bottom:1px solid #334155; color:#94a3b8;\">\n        <th style=\"padding:8px;\">خلطة الخزان</th>\n        <th style=\"padding:8px;\">نسبة الإيثانول / البنزين</th>\n        <th style=\"padding:8px;\">نسبة الزيادة المحسوبة</th>\n        <th style=\"padding:8px;\">ضبط المؤشر الموصى به</th>\n      </tr>\n    </thead>\n    <tbody style=\"color:#cbd5e1;\">\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>50 % E85 / 50 % بنزين</strong></td>\n        <td style=\"padding:8px;\">نصف بنصف</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+14 %</td>\n        <td style=\"padding:8px;\">المؤشر على <strong>+14 %</strong> (مثالي للبخاخات الصغيرة)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>60 % E85 / 40 % بنزين</strong></td>\n        <td style=\"padding:8px;\">60% إيثانول / 40% بنزين</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+17 %</td>\n        <td style=\"padding:8px;\">المؤشر على <strong>+17 %</strong> (حل اقتصادي فائق الاستقرار)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>70 % E85 / 30 % بنزين</strong></td>\n        <td style=\"padding:8px;\">70% إيثانول / 30% بنزين</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+20 %</td>\n        <td style=\"padding:8px;\">المؤشر على <strong>+20 %</strong> (شائع جداً في فصل الشتاء)</td>\n      </tr>\n      <tr style=\"border-bottom:1px solid #1e293b;\">\n        <td style=\"padding:8px;\"><strong>80 % E85 / 20 % بنزين</strong></td>\n        <td style=\"padding:8px;\">80% إيثانول / 20% بنزين</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+23 %</td>\n        <td style=\"padding:8px;\">المؤشر على <strong>+23 %</strong> (مطابق لوقود المحطات الشتوي)</td>\n      </tr>\n      <tr>\n        <td style=\"padding:8px;\"><strong>100 % E85 (خالص)</strong></td>\n        <td style=\"padding:8px;\">خزان كامل إيثانول</td>\n        <td style=\"padding:8px; color:var(--accent-green); font-weight:700;\">+28 %</td>\n        <td style=\"padding:8px;\"><strong>النقطة الذهبية لفليكس فيول:</strong> مع تفعيل <em>AI Adaptive Trims</em>، يتعامل المحرك مع كافة الخلطات السابقة تلقائياً!</td>\n      </tr>\n    </tbody>\n  </table>\n</div>\n<div style=\"margin-top:12px; font-size:12px; color:#cbd5e1; background:rgba(245, 158, 11, 0.12); border-left:3px solid #f59e0b; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#f59e0b;\">💡 لماذا يعتبر ضبط +28% كافياً في 95% من الحالات؟</strong><br>\n  بفضل خيار <strong>AI Adaptive Trims</strong>، تقوم حساسات اللامبدا بتصحيح نسب الوقود في الوقت الفعلي (STFT/LTFT حتى ±25%). لذلك حتى لو كان المؤشر على +28%، وقام العميل بتعبئة 50/50 أو بنزين نقي، يتكيف الكمبيوتر تلقائياً وبسلاسة دون إضاءة أي لمبة عطل!\n</div>",
        ch3_title: "<i class=\"fa-solid fa-snowflake\" style=\"color:var(--accent-cyan)\"></i> 3. مراحل التشغيل البارد (Cold Start Hiver Pro)",
        ch3_body: "<p>يمتلك الإيثانول ضغط تبخر منخفضاً جداً ولا يتبخر تلقائياً في درجات حرارة أقل من 12°C - 15°C. تقوم خوارزميتنا بإعادة معايرة كمية الحقن أثناء تشغيل السلف (Cranking) عبر منحنى حرارة سائل التبريد بالكامل (-30°C حتى +80°C).</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>المستوى 1 (+15 %):</strong> مناخ معتدل / مناطق دافئة صيفاً (&gt; 20°C).</li>\n  <li><strong>المستوى 2 (+25 %):</strong> ربيع وخريف معتدل (15°C إلى 20°C).</li>\n  <li><strong>المستوى 3 (+35 %) [الافتراضي الموصى به]:</strong> مثالي للخريف والشتاء (5°C إلى 15°C). تشغيل فوري وسلس من أول نقرة سلف.</li>\n  <li><strong>المستوى 4 (+45 %):</strong> شتاء بارد قياسي (0°C إلى 5°C).</li>\n  <li><strong>المستوى 5 و Hard-Start (+75 % إلى +80 %):</strong> مناطق جبلية أو صقيع وانجماد مستمر (&lt; 0°C).</li>\n</ul>",
        ch4_title: "<i class=\"fa-solid fa-shield-halved\" style=\"color:var(--accent-orange)\"></i> 4. الحقن المباشر ونظام حماية الزيت Oil-Fix (منع تخفيف الزيت)",
        ch4_body: "<p>في المحركات الحديثة ذات الحقن المباشر (مثل: <strong>PSA 1.2 PureTech / THP</strong>, <strong>VAG 1.4 / 2.0 TSI TFSI</strong>, <strong>Ford EcoBoost</strong>, <strong>Renault TCe</strong>):</p>\n<ul style=\"margin-top:6px; margin-bottom:6px;\">\n  <li><strong>الخطر الميكانيكي:</strong> في البدايات الباردة، يمكن للإيثانول غير المحترق أن يزيل طبقة الزيت الواقية على جدران الأسطوانات ويتسرب إلى كارتير الزيت، مما يؤدي إلى تخفيف لزوجة زيت المحرك.</li>\n  <li><strong>وظيفة Oil-Fix:</strong> تقلل خوارزميتنا الحقن اللاحق غير الضروري في درجات الحرارة المنخفضة وتسرع وصول غرفة الاحتراق إلى الحرارة المثالية.</li>\n  <li><strong>توجيه الورشة للعميل:</strong> انصح العميل بتقريب مواعيد تغيير زيت المحرك إلى <strong>10,000 كم أو 15,000 كم كحد أقصى</strong> مع استخدام زيت تخليقي معتمد من الشركة المصنعة.</li>\n</ul>",
        ch5_title: "<i class=\"fa-solid fa-magnifying-glass-chart\" style=\"color:#06b6d4\"></i> 5. مراقبة حساسات الأكسجين والكتالايزر (ضمان انطفاء لمبة المحرك 100%)",
        ch5_body: "<p>يغير الإيثانول درجة حرارة وتركيب غازات العادم (زيادة بخار الماء واختلاف النسبة التكافئية). وبدون معايرة دقيقة لدوائر المراقبة، قد تضيء لمبة فحص المحرك (Check Engine) بأعطال بيئية وهمية.</p>\n<ul style=\"margin-top:6px; margin-bottom:8px;\">\n  <li><strong>الحساس العلوي رقم 1 (قبل الكتالايزر) — محفوظ بنسبة 100 %:</strong> هو الحساس الحيوي المنظم للاحتراق. يقيس الخليط باستمرار ويقود الدائرة المغلقة (Closed-Loop) لتعديل الحقن فورياً.</li>\n  <li><strong>إلغاء الحساس السفلي رقم 2 (بعد الكتالايزر):</strong> يعطل تشخيص كفاءة دبة التلوث فقط، مما يقضي نهائياً على العطل الوهمي الشائع <strong>P0420 / P0430</strong>.</li>\n  <li><strong>إلغاء الكتالايزر CAT OFF (22 كود):</strong> يحذف جدول الأعطال المرتبط بدبة البيئة، ويتيح أيضاً تركيب داون بايب مفرغ أو عادم رياضي دون أي تحذير.</li>\n  <li><strong>أكواد خليط الوقود (27 كود):</strong> يخفي تنبيهات فقر الوقود المؤقتة (مثل: <strong>P0171, P0174, P2177, P2179</strong>). يمنع ظهور اللمبة في المرحلة الانتقالية عند التحول المفاجئ للبنزين إلى E85.</li>\n  <li><strong>إلغاء نظام التبخير EVAP OFF (8 أكواد):</strong> يلغي أعطال علبة الكانستر (Canister P0440 إلى P0455) نظراً لاختلاف ضغط تبخر الإيثانول.</li>\n</ul>\n<div style=\"font-size:12px; color:#cbd5e1; background:rgba(6, 182, 212, 0.12); border-left:3px solid #06b6d4; padding:10px 14px; border-radius:6px; line-height:1.5;\">\n  <strong style=\"color:#06b6d4;\">✅ فائدة العميل والورشة:</strong> تجتاز السيارة الفحص الدوري دون أي كود عطل في ذاكرة OBD، مع الحفاظ على استجابة المحرك التامة ولوحة قيادة خالية 100% من أي لمبة تحذيرية.\n</div>",
        ch6_title: "<i class=\"fa-solid fa-list-check\" style=\"color:#c084fc\"></i> 6. قائمة فحص الورشة وبروتوكول تسليم السيارة للعميل",
        ch6_body: "<p>للحصول على نتيجة مضمونة 100% بدون أي رجوع من العميل، اتبع الخطوات التالية في الورشة:</p>\n<div class=\"guide-step-box\">\n  <div class=\"step-item\">\n    <div class=\"step-num\">الخطوة 1</div>\n    <div class=\"step-title\">كتابة الفلاش</div>\n    <div class=\"step-desc\">برمج ملف التعديل بجهازك المعتمد، ويتم تصحيح الشيكسم تلقائياً.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">الخطوة 2</div>\n    <div class=\"step-title\">مسح الأعطال DTC</div>\n    <div class=\"step-desc\">قم بمسح شامل لكافة أعطال الذاكرة قبل محاولة تشغيل المحرك لأول مرة.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">الخطوة 3</div>\n    <div class=\"step-title\">تعبئة وقود E85</div>\n    <div class=\"step-desc\">عبئ 50% إلى 70% على الأقل من الإيثانول للتجربة الأولى (أو 100% مباشرة).</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">الخطوة 4</div>\n    <div class=\"step-title\">تشغيل 3 دقائق</div>\n    <div class=\"step-desc\">اترك المحرك يدور على السلانسيه لمدة 3 دقائق دون لمس دواسة البنزين للمعايرة الذاتية.</div>\n  </div>\n  <div class=\"step-item\">\n    <div class=\"step-num\">الخطوة 5</div>\n    <div class=\"step-title\">تجربة على الطريق</div>\n    <div class=\"step-desc\">تجربة قيادة من 5 إلى 10 دقائق: تسارعات قوية، والتأكد من سرعة الاستجابة وانطفاء أي تحذير.</div>\n  </div>\n</div>"
      }
    }
  }
};

// ==============================================================================
// I18N CONTROLLER & DOM APPLIER
// ==============================================================================
(function() {
  const urlLang = (typeof window !== "undefined" && window.location) ? new URLSearchParams(window.location.search).get("lang") : null;
  let currentLang = (urlLang && ['fr', 'en', 'ar'].includes(urlLang)) ? urlLang : (localStorage.getItem("scorpion_lang") || "fr");
  if (urlLang && ['fr', 'en', 'ar'].includes(urlLang)) {
    localStorage.setItem("scorpion_lang", urlLang);
  }

  function getTranslation(key, lang) {
    const l = lang || currentLang;
    const dict = window.APP_TRANSLATIONS[l] || window.APP_TRANSLATIONS['fr'];
    const parts = key.split('.');
    let cur = dict;
    for (const p of parts) {
      if (cur && typeof cur === 'object' && p in cur) {
        cur = cur[p];
      } else {
        return null;
      }
    }
    return cur;
  }

  window.t = function(key, fallback) {
    const res = getTranslation(key, currentLang);
    if (res !== null && res !== undefined) return res;
    const resFr = getTranslation(key, 'fr');
    if (resFr !== null && resFr !== undefined) return resFr;
    return fallback !== undefined ? fallback : key;
  };

  window.getCurrentLanguage = function() {
    return currentLang;
  };

  window.setAppLanguage = function(lang) {
    if (!['fr', 'en', 'ar'].includes(lang)) lang = 'fr';
    currentLang = lang;
    localStorage.setItem("scorpion_lang", lang);
    applyLanguageToDom(lang);
  };

  function applyLanguageToDom(lang) {
    lang = lang || currentLang;
    document.documentElement.lang = lang;
    document.documentElement.dir = (lang === 'ar') ? 'rtl' : 'ltr';
    if (document.body) {
      document.body.dir = (lang === 'ar') ? 'rtl' : 'ltr';
    }

    // Update active state on language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Translate standard text nodes
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const val = getTranslation(key, lang);
      if (val) el.innerText = val;
    });

    // Translate HTML nodes
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const key = el.getAttribute('data-i18n-html');
      const val = getTranslation(key, lang);
      if (val) el.innerHTML = val;
    });

    // Translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const val = getTranslation(key, lang);
      if (val) el.placeholder = val;
    });

    // Translate titles / tooltips
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      const val = getTranslation(key, lang);
      if (val) el.title = val;
    });

    // Trigger app.js custom refresh if defined
    if (window.onLanguageChanged && typeof window.onLanguageChanged === 'function') {
      window.onLanguageChanged(lang);
    }
  }

  window.applyAppLanguage = function() {
    applyLanguageToDom(currentLang);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => applyLanguageToDom(currentLang));
  } else {
    applyLanguageToDom(currentLang);
  }
})();

