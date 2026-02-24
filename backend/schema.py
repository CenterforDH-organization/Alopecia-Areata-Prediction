"""Shared schema/configuration for the Korean AA prediction app."""

from __future__ import annotations

RISK_THRESHOLD_PERCENT = 42.0
INPUT_FACTOR = 33

FEATURE_NAMES_MODEL = [
    "SEX",
    "AGE",
    "REGION",
    "INCOME",
    "BP_HIGH",
    "BP_LWST",
    "BLDS",
    "TOT_CHOLE",
    "HMG",
    "SGOT_AST",
    "SGPT_ALT",
    "GAMMA_GTP",
    "BMI",
    "SMK_STAT",
    "DRINK_FREQ",
    "EXERCI_FREQ",
    "HIS_T2DM",
    "HIS_STROKE",
    "HIS_HYPERTENSION",
    "HIS_AA",
    "HIS_T1DM",
    "HIS_VD",
    "HIS_CKD",
    "HIS_DEP",
    "HIS_CTD",
    "HIS_SD",
    "HIS_PSU",
    "HIS_RA",
    "HIS_AS",
    "HIS_AD",
    "HIS_ASTHMA",
    "HIS_AR",
    "VISIT",
]

SEX_OPTIONS = [
    {"value": "0", "label": "여성"},
    {"value": "1", "label": "남성"},
]

REGION_OPTIONS = [
    {"value": "0", "label": "농촌"},
    {"value": "1", "label": "도시"},
]

INCOME_OPTIONS = [{"value": str(i), "label": str(i)} for i in range(11)]

SMOKE_OPTIONS = [
    {"value": "1", "label": "금연"},
    {"value": "2", "label": "과거 흡연"},
    {"value": "3", "label": "현재 흡연"},
]

ALCOHOL_OPTIONS = [
    {"value": "1", "label": "거의 안함"},
    {"value": "2", "label": "가끔 (월 2~3회)"},
    {"value": "3", "label": "때때로 (주 1~2회)"},
    {"value": "4", "label": "자주 (주 3회 이상)"},
]

EXERCISE_OPTIONS = [
    {"value": "1", "label": "안함"},
    {"value": "2", "label": "가끔 (월 1~2회)"},
    {"value": "3", "label": "때때로 (주 3~4회)"},
    {"value": "4", "label": "자주 (주 5회 이상)"},
]

HISTORY_OPTIONS = [
    {"value": "0", "label": "없음"},
    {"value": "1", "label": "있음"},
]

KR_FIELDS = [
    {"id": "uv_value1", "label": "성별", "kind": "select", "options": SEX_OPTIONS},
    {"id": "uv_value2", "label": "나이", "kind": "number", "unit": "세"},
    {"id": "uv_value3", "label": "지역", "kind": "select", "options": REGION_OPTIONS},
    {
        "id": "uv_value4",
        "label": "가구소득",
        "kind": "select",
        "options": INCOME_OPTIONS,
        "description": (
            "0~10 구간 코드로 입력합니다. "
            "원본 연구 기준의 월 소득 구간 인덱스입니다."
        ),
    },
    {"id": "uv_value5", "label": "수축기 혈압", "kind": "number", "unit": "mmHg"},
    {"id": "uv_value6", "label": "이완기 혈압", "kind": "number", "unit": "mmHg"},
    {"id": "uv_value7", "label": "공복혈당", "kind": "number", "unit": "mg/dL"},
    {"id": "uv_value8", "label": "총 콜레스테롤", "kind": "number", "unit": "mg/dL"},
    {"id": "uv_value9", "label": "혈색소", "kind": "number", "unit": "g/dL"},
    {"id": "uv_value10", "label": "SGOT_AST", "kind": "number", "unit": "U/L"},
    {"id": "uv_value11", "label": "SGPT_ALT", "kind": "number", "unit": "U/L"},
    {"id": "uv_value12", "label": "감마 GTP", "kind": "number", "unit": "U/L"},
    {"id": "uv_value13", "label": "BMI", "kind": "number", "unit": "kg/m^2"},
    {"id": "uv_value14", "label": "흡연 상태", "kind": "select", "options": SMOKE_OPTIONS},
    {"id": "uv_value15", "label": "음주량", "kind": "select", "options": ALCOHOL_OPTIONS},
    {"id": "uv_value16", "label": "운동 빈도", "kind": "select", "options": EXERCISE_OPTIONS},
    {
        "id": "uv_value17",
        "label": "제2형 당뇨병 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {"id": "uv_value18", "label": "뇌졸중 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {"id": "uv_value19", "label": "고혈압 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {"id": "uv_value20", "label": "원형탈모 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {
        "id": "uv_value21",
        "label": "제1형 당뇨병 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value22",
        "label": "비타민 D 결핍 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value23",
        "label": "만성 신장 질환 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {"id": "uv_value24", "label": "우울증 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {
        "id": "uv_value25",
        "label": "결합조직질환 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
        "description": (
            "전신성 홍반성 루푸스, 피부다발성근염, 전신성 경화증, 쇼그렌 증후군, "
            "혼합결합조직질환, 베체트병, 류마티스성 다발성 근육통, 혈관염, 건선 포함"
        ),
    },
    {"id": "uv_value26", "label": "수면장애 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {
        "id": "uv_value27",
        "label": "정신활성물질 사용 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value28",
        "label": "류마티스 관절염 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value29",
        "label": "강직성 척추염 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value30",
        "label": "아토피 피부염 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {"id": "uv_value31", "label": "천식 병력", "kind": "select", "options": HISTORY_OPTIONS},
    {
        "id": "uv_value32",
        "label": "알레르기성 비염 병력",
        "kind": "select",
        "options": HISTORY_OPTIONS,
    },
    {
        "id": "uv_value33",
        "label": "1년 내 병원 방문 횟수",
        "kind": "number",
        "unit": "회",
    },
]

if len(KR_FIELDS) != INPUT_FACTOR:
    raise ValueError("KR_FIELDS length must be 33.")

