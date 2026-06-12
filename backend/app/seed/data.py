"""가상(synthetic) 시드 데이터: 약물 마스터 + 환자.

한국 중형 종합병원(300베드) 맥락의 가짜 데이터. 실제 진료 사용 불가.
약물의 ingredient/drug_class/flags는 app/cdss/rules/*.json의 토큰과 일치해야 한다.
"""
from __future__ import annotations

# ── 약물 마스터 (50종+) ─────────────────────────────────────────────
# 키: code, name, ingredient, drug_class, default_dose, route,
#     renal_adjust, pregnancy_category, beers, flags
DRUGS: list[dict] = [
    # 항응고제
    {"code": "warfarin", "name": "와파린", "ingredient": "warfarin", "drug_class": "anticoagulant", "default_dose": "5 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "X", "beers": False, "flags": ["bleeding_risk"]},
    {"code": "apixaban", "name": "아픽사반", "ingredient": "apixaban", "drug_class": "anticoagulant", "default_dose": "5 mg bid", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["bleeding_risk", "doac"]},
    {"code": "rivaroxaban", "name": "리바록사반", "ingredient": "rivaroxaban", "drug_class": "anticoagulant", "default_dose": "20 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["bleeding_risk", "doac"]},
    # 항혈소판제
    {"code": "aspirin", "name": "아스피린", "ingredient": "aspirin", "drug_class": "antiplatelet", "default_dose": "100 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": False, "flags": ["bleeding_risk"]},
    {"code": "clopidogrel", "name": "클로피도그렐", "ingredient": "clopidogrel", "drug_class": "antiplatelet", "default_dose": "75 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": ["bleeding_risk"]},
    # NSAID
    {"code": "ibuprofen", "name": "이부프로펜", "ingredient": "ibuprofen", "drug_class": "NSAID", "default_dose": "400 mg tid", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["bleeding_risk", "nephrotoxic"]},
    {"code": "naproxen", "name": "나프록센", "ingredient": "naproxen", "drug_class": "NSAID", "default_dose": "500 mg bid", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["bleeding_risk", "nephrotoxic"]},
    {"code": "ketorolac", "name": "케토롤락", "ingredient": "ketorolac", "drug_class": "NSAID", "default_dose": "30 mg", "route": "IV", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["bleeding_risk", "nephrotoxic"]},
    {"code": "celecoxib", "name": "세레콕시브", "ingredient": "celecoxib", "drug_class": "NSAID", "default_dose": "200 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["nephrotoxic"]},
    # 페니실린계
    {"code": "amoxicillin", "name": "아목시실린", "ingredient": "amoxicillin", "drug_class": "penicillin", "default_dose": "500 mg tid", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "amox_clav", "name": "아목시실린/클라불란산", "ingredient": "amoxicillin_clavulanate", "drug_class": "penicillin", "default_dose": "625 mg tid", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "pip_tazo", "name": "피페라실린/타조박탐", "ingredient": "piperacillin_tazobactam", "drug_class": "penicillin", "default_dose": "4.5 g q6h", "route": "IV", "renal_adjust": True, "pregnancy_category": "B", "beers": False, "flags": []},
    # 세팔로스포린계
    {"code": "cefazolin", "name": "세파졸린", "ingredient": "cefazolin", "drug_class": "cephalosporin", "default_dose": "1 g q8h", "route": "IV", "renal_adjust": True, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "ceftriaxone", "name": "세프트리악손", "ingredient": "ceftriaxone", "drug_class": "cephalosporin", "default_dose": "2 g qd", "route": "IV", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "cefepime", "name": "세페핌", "ingredient": "cefepime", "drug_class": "cephalosporin", "default_dose": "2 g q12h", "route": "IV", "renal_adjust": True, "pregnancy_category": "B", "beers": False, "flags": []},
    # 매크로라이드
    {"code": "azithromycin", "name": "아지스로마이신", "ingredient": "azithromycin", "drug_class": "macrolide", "default_dose": "500 mg qd", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": ["qt_prolong"]},
    {"code": "clarithromycin", "name": "클래리스로마이신", "ingredient": "clarithromycin", "drug_class": "macrolide", "default_dose": "500 mg bid", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["qt_prolong", "enzyme_inhibitor"]},
    # 플루오로퀴놀론
    {"code": "ciprofloxacin", "name": "시프로플록사신", "ingredient": "ciprofloxacin", "drug_class": "fluoroquinolone", "default_dose": "500 mg bid", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["qt_prolong"]},
    {"code": "levofloxacin", "name": "레보플록사신", "ingredient": "levofloxacin", "drug_class": "fluoroquinolone", "default_dose": "750 mg qd", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["qt_prolong"]},
    # 글리코펩타이드 / 아미노글리코사이드
    {"code": "vancomycin", "name": "반코마이신", "ingredient": "vancomycin", "drug_class": "glycopeptide", "default_dose": "1 g q12h", "route": "IV", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["nephrotoxic"]},
    {"code": "gentamicin", "name": "겐타마이신", "ingredient": "gentamicin", "drug_class": "aminoglycoside", "default_dose": "5 mg/kg qd", "route": "IV", "renal_adjust": True, "pregnancy_category": "D", "beers": False, "flags": ["nephrotoxic"]},
    # 설폰아마이드 / 카바페넴 / 니트로이미다졸
    {"code": "tmp_smx", "name": "트리메토프림/설파메톡사졸", "ingredient": "trimethoprim_sulfamethoxazole", "drug_class": "sulfonamide", "default_dose": "960 mg bid", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["hyperkalemia"]},
    {"code": "meropenem", "name": "메로페넴", "ingredient": "meropenem", "drug_class": "carbapenem", "default_dose": "1 g q8h", "route": "IV", "renal_adjust": True, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "metronidazole", "name": "메트로니다졸", "ingredient": "metronidazole", "drug_class": "nitroimidazole", "default_dose": "500 mg tid", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    # 스타틴
    {"code": "atorvastatin", "name": "아토르바스타틴", "ingredient": "atorvastatin", "drug_class": "statin", "default_dose": "20 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "X", "beers": False, "flags": []},
    {"code": "simvastatin", "name": "심바스타틴", "ingredient": "simvastatin", "drug_class": "statin", "default_dose": "20 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "X", "beers": False, "flags": []},
    {"code": "rosuvastatin", "name": "로수바스타틴", "ingredient": "rosuvastatin", "drug_class": "statin", "default_dose": "10 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "X", "beers": False, "flags": []},
    # ACEi / ARB
    {"code": "ramipril", "name": "라미프릴", "ingredient": "ramipril", "drug_class": "ACEi", "default_dose": "5 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": False, "flags": ["hyperkalemia"]},
    {"code": "enalapril", "name": "에날라프릴", "ingredient": "enalapril", "drug_class": "ACEi", "default_dose": "10 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "D", "beers": False, "flags": ["hyperkalemia"]},
    {"code": "losartan", "name": "로사르탄", "ingredient": "losartan", "drug_class": "ARB", "default_dose": "50 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": False, "flags": ["hyperkalemia"]},
    {"code": "valsartan", "name": "발사르탄", "ingredient": "valsartan", "drug_class": "ARB", "default_dose": "80 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": False, "flags": ["hyperkalemia"]},
    # 칼륨보존 이뇨제 / 칼륨보충제
    {"code": "spironolactone", "name": "스피로노락톤", "ingredient": "spironolactone", "drug_class": "potassium_sparing_diuretic", "default_dose": "25 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["hyperkalemia"]},
    {"code": "kcl", "name": "염화칼륨", "ingredient": "potassium_chloride", "drug_class": "electrolyte", "default_dose": "40 mEq", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["hyperkalemia"]},
    # 베타차단제
    {"code": "propranolol", "name": "프로프라놀롤", "ingredient": "propranolol", "drug_class": "beta_blocker_nonselective", "default_dose": "40 mg bid", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "bisoprolol", "name": "비소프롤롤", "ingredient": "bisoprolol", "drug_class": "beta_blocker_selective", "default_dose": "5 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "metoprolol", "name": "메토프롤롤", "ingredient": "metoprolol", "drug_class": "beta_blocker_selective", "default_dose": "50 mg bid", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    # 심혈관
    {"code": "digoxin", "name": "디곡신", "ingredient": "digoxin", "drug_class": "cardiac_glycoside", "default_dose": "0.125 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "amiodarone", "name": "아미오다론", "ingredient": "amiodarone", "drug_class": "antiarrhythmic", "default_dose": "200 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": False, "flags": ["qt_prolong", "enzyme_inhibitor"]},
    {"code": "furosemide", "name": "푸로세미드", "ingredient": "furosemide", "drug_class": "loop_diuretic", "default_dose": "40 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "hctz", "name": "히드로클로로티아지드", "ingredient": "hydrochlorothiazide", "drug_class": "thiazide_diuretic", "default_dose": "25 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "amlodipine", "name": "암로디핀", "ingredient": "amlodipine", "drug_class": "calcium_channel_blocker", "default_dose": "5 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    # 벤조디아제핀
    {"code": "lorazepam", "name": "로라제팜", "ingredient": "lorazepam", "drug_class": "benzodiazepine", "default_dose": "1 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": True, "flags": []},
    {"code": "diazepam", "name": "디아제팜", "ingredient": "diazepam", "drug_class": "benzodiazepine", "default_dose": "5 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "D", "beers": True, "flags": []},
    # 진통/마약성
    {"code": "tramadol", "name": "트라마돌", "ingredient": "tramadol", "drug_class": "opioid", "default_dose": "50 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["serotonergic"]},
    {"code": "morphine", "name": "모르핀", "ingredient": "morphine", "drug_class": "opioid", "default_dose": "10 mg", "route": "IV", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "acetaminophen", "name": "아세트아미노펜", "ingredient": "acetaminophen", "drug_class": "analgesic", "default_dose": "650 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    # 정신/신경
    {"code": "fluoxetine", "name": "플루옥세틴", "ingredient": "fluoxetine", "drug_class": "SSRI", "default_dose": "20 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["serotonergic", "enzyme_inhibitor"]},
    {"code": "sertraline", "name": "설트랄린", "ingredient": "sertraline", "drug_class": "SSRI", "default_dose": "50 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": ["serotonergic"]},
    {"code": "haloperidol", "name": "할로페리돌", "ingredient": "haloperidol", "drug_class": "antipsychotic", "default_dose": "1 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": True, "flags": ["qt_prolong"]},
    {"code": "gabapentin", "name": "가바펜틴", "ingredient": "gabapentin", "drug_class": "anticonvulsant", "default_dose": "300 mg tid", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": []},
    # 소화기
    {"code": "omeprazole", "name": "오메프라졸", "ingredient": "omeprazole", "drug_class": "ppi", "default_dose": "20 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "pantoprazole", "name": "판토프라졸", "ingredient": "pantoprazole", "drug_class": "ppi", "default_dose": "40 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "ondansetron", "name": "온단세트론", "ingredient": "ondansetron", "drug_class": "antiemetic", "default_dose": "4 mg", "route": "IV", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": ["qt_prolong"]},
    # 내분비/기타
    {"code": "metformin", "name": "메트포르민", "ingredient": "metformin", "drug_class": "biguanide", "default_dose": "500 mg bid", "route": "PO", "renal_adjust": True, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "insulin_glargine", "name": "인슐린 글라진", "ingredient": "insulin_glargine", "drug_class": "insulin", "default_dose": "10 U", "route": "SC", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": []},
    {"code": "allopurinol", "name": "알로푸리놀", "ingredient": "allopurinol", "drug_class": "xanthine_oxidase_inhibitor", "default_dose": "100 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": []},
    {"code": "diphenhydramine", "name": "디펜히드라민", "ingredient": "diphenhydramine", "drug_class": "antihistamine_1st", "default_dose": "25 mg", "route": "PO", "renal_adjust": False, "pregnancy_category": "B", "beers": True, "flags": ["anticholinergic"]},
    {"code": "fluconazole", "name": "플루코나졸", "ingredient": "fluconazole", "drug_class": "antifungal", "default_dose": "150 mg", "route": "PO", "renal_adjust": True, "pregnancy_category": "C", "beers": False, "flags": ["qt_prolong", "enzyme_inhibitor"]},
    {"code": "iodinated_contrast", "name": "요오드 조영제", "ingredient": "iodinated_contrast", "drug_class": "contrast", "default_dose": "100 mL", "route": "IV", "renal_adjust": False, "pregnancy_category": "B", "beers": False, "flags": ["nephrotoxic"]},
]


# ── 가상 환자 (11명) ────────────────────────────────────────────────
# 각 환자: id, name, age, sex, weight_kg, egfr, creatinine, pregnant,
#          encounter_type, ward, bed, allergies[], conditions[(code,display)],
#          labs[(code,display,value,unit,abnormal,ref_low,ref_high)],
#          medications[drug_code]
PATIENTS: list[dict] = [
    {
        "id": "P001", "name": "김영수", "age": 72, "sex": "M", "weight_kg": 65.0,
        "egfr": 28.0, "creatinine": 2.3, "pregnant": False,
        "encounter_type": "inpatient", "ward": "본관 7동", "bed": "705-1",
        "allergies": [], "conditions": [("ckd", "만성콩팥병 4기"), ("afib", "심방세동"), ("hypertension", "고혈압")],
        "labs": [("eGFR", "추정 사구체여과율", 28.0, "mL/min/1.73㎡", True, 60, None),
                 ("K", "혈청 칼륨", 4.8, "mmol/L", False, 3.5, 5.1),
                 ("INR", "INR", 2.4, "", False, 2.0, 3.0)],
        "medications": ["warfarin", "digoxin", "furosemide"],
    },
    {
        "id": "P002", "name": "이순자", "age": 81, "sex": "F", "weight_kg": 52.0,
        "egfr": 55.0, "creatinine": 1.0, "pregnant": False,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("insomnia", "불면증"), ("hypertension", "고혈압")],
        "labs": [("eGFR", "추정 사구체여과율", 55.0, "mL/min/1.73㎡", True, 60, None)],
        "medications": ["bisoprolol"],
    },
    {
        "id": "P003", "name": "박철호", "age": 68, "sex": "M", "weight_kg": 74.0,
        "egfr": 70.0, "creatinine": 1.1, "pregnant": False,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("afib", "심방세동")],
        "labs": [("INR", "INR", 2.6, "", False, 2.0, 3.0)],
        "medications": ["warfarin"],
    },
    {
        "id": "P004", "name": "최민정", "age": 45, "sex": "F", "weight_kg": 60.0,
        "egfr": 95.0, "creatinine": 0.7, "pregnant": False,
        "encounter_type": "inpatient", "ward": "본관 5동", "bed": "512-2",
        "allergies": ["penicillin"], "conditions": [("pneumonia", "지역사회획득폐렴")],
        "labs": [("WBC", "백혈구", 13.2, "10^3/µL", True, 4.0, 10.0)],
        "medications": [],
    },
    {
        "id": "P005", "name": "정해린", "age": 29, "sex": "F", "weight_kg": 58.0,
        "egfr": 100.0, "creatinine": 0.6, "pregnant": True,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("hypertension", "임신성 고혈압")],
        "labs": [("BP", "혈압(수축기)", 150.0, "mmHg", True, 90, 140)],
        "medications": [],
    },
    {
        "id": "P006", "name": "한상우", "age": 58, "sex": "M", "weight_kg": 70.0,
        "egfr": 82.0, "creatinine": 0.9, "pregnant": False,
        "encounter_type": "inpatient", "ward": "본관 6동", "bed": "601-3",
        "allergies": [], "conditions": [("liver_disease", "간경변(대상성)")],
        "labs": [("ALT", "ALT", 120.0, "U/L", True, 0, 40),
                 ("AST", "AST", 95.0, "U/L", True, 0, 40)],
        "medications": [],
    },
    {
        "id": "P007", "name": "김도윤", "age": 7, "sex": "M", "weight_kg": 24.0,
        "egfr": 110.0, "creatinine": 0.4, "pregnant": False,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("pneumonia", "소아 폐렴")],
        "labs": [],
        "medications": [],
    },
    {
        "id": "P008", "name": "오금자", "age": 75, "sex": "F", "weight_kg": 58.0,
        "egfr": 50.0, "creatinine": 1.2, "pregnant": False,
        "encounter_type": "inpatient", "ward": "본관 7동", "bed": "710-2",
        "allergies": [], "conditions": [("heart_failure", "심부전"), ("hypertension", "고혈압"), ("diabetes", "2형 당뇨")],
        "labs": [("K", "혈청 칼륨", 5.2, "mmol/L", True, 3.5, 5.1),
                 ("eGFR", "추정 사구체여과율", 50.0, "mL/min/1.73㎡", True, 60, None)],
        "medications": ["ramipril", "spironolactone", "metformin", "furosemide"],
    },
    {
        "id": "P009", "name": "윤지호", "age": 34, "sex": "M", "weight_kg": 80.0,
        "egfr": 98.0, "creatinine": 0.8, "pregnant": False,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("asthma", "기관지천식"), ("hypertension", "고혈압")],
        "labs": [],
        "medications": [],
    },
    {
        "id": "P010", "name": "서영광", "age": 63, "sex": "M", "weight_kg": 72.0,
        "egfr": 75.0, "creatinine": 1.0, "pregnant": False,
        "encounter_type": "inpatient", "ward": "본관 5동", "bed": "508-1",
        "allergies": [], "conditions": [("afib", "심방세동")],
        "labs": [("QTc", "보정 QT 간격", 460.0, "ms", True, 350, 450)],
        "medications": ["amiodarone"],
    },
    {
        "id": "P011", "name": "강민서", "age": 70, "sex": "F", "weight_kg": 62.0,
        "egfr": 65.0, "creatinine": 0.9, "pregnant": False,
        "encounter_type": "outpatient", "ward": None, "bed": None,
        "allergies": [], "conditions": [("hyperlipidemia", "고지혈증"), ("hypertension", "고혈압")],
        "labs": [("LDL", "LDL 콜레스테롤", 165.0, "mg/dL", True, 0, 130)],
        "medications": ["simvastatin", "losartan"],
    },
]
