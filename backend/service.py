"""Business logic for Korean AA prediction API."""

from __future__ import annotations

from typing import Any

import numpy as np

from backend.model import predict_probability
from backend.schema import KR_FIELDS, RISK_THRESHOLD_PERCENT


def _is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _is_finite_number(value: float) -> bool:
    return bool(np.isfinite(value))


def _format_number(value: float) -> str:
    if not _is_finite_number(value):
        return "-"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _option_label(field: dict[str, Any], value_str: str) -> str:
    for opt in field.get("options", []):
        if opt["value"] == value_str:
            return opt["label"]
    return value_str


def parse_kr_payload(payload: dict[str, Any]) -> tuple[np.ndarray, list[dict[str, str]]]:
    if not isinstance(payload, dict):
        raise ValueError("JSON 객체 형식으로 요청해야 합니다.")

    values: list[float] = []
    patient_info: list[dict[str, str]] = []

    for field in KR_FIELDS:
        field_id = field["id"]
        label = field["label"]
        kind = field["kind"]

        if field_id not in payload:
            raise ValueError(f"'{label}' 입력값({field_id})이 없습니다.")

        raw_value = payload[field_id]

        if _is_blank(raw_value):
            numeric = np.nan
            display = "-"
        elif kind == "select":
            value_str = str(raw_value)
            valid_values = {opt["value"] for opt in field["options"]}
            if value_str not in valid_values:
                raise ValueError(f"'{label}' 값이 허용 범위를 벗어났습니다: {raw_value}")
            numeric = float(value_str)
            display = _option_label(field, value_str)
        else:
            try:
                numeric = float(raw_value)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"'{label}'는 숫자여야 합니다.") from exc
            display = _format_number(numeric)

        values.append(numeric)
        patient_info.append({"id": field_id, "label": label, "value": display})

    return np.asarray(values, dtype=np.float64), patient_info


def _prediction_summary(probability: float) -> dict[str, Any]:
    probability_percent = probability * 100.0
    label = "정상" if probability_percent <= RISK_THRESHOLD_PERCENT else "원형탈모"
    return {
        "label": label,
        "probability_percent": round(probability_percent, 2),
        "threshold_percent": RISK_THRESHOLD_PERCENT,
    }


def _apply_lifestyle_improvements(values: np.ndarray) -> tuple[np.ndarray, list[str]]:
    improved = values.copy()
    changes: list[str] = []

    sex = improved[0]
    sbp = improved[4]
    dbp = improved[5]
    fbg = improved[6]
    tc = improved[7]
    hmg = improved[8]
    ast = improved[9]
    alt = improved[10]
    ggt = improved[11]
    bmi = improved[12]
    smoking = improved[13]
    alcohol = improved[14]
    exercise = improved[15]
    visit = improved[32]

    if _is_finite_number(sbp) and _is_finite_number(dbp) and (sbp > 120.0 or dbp > 80.0):
        improved[4] = 120.0
        improved[5] = 80.0
        changes.append("혈압을 120/80 mmHg 이하로 낮추기")

    if _is_finite_number(fbg) and fbg > 100.0:
        improved[6] = 100.0
        changes.append("공복혈당을 100 mg/dL 이하로 낮추기")

    if _is_finite_number(tc) and tc > 200.0:
        improved[7] = 200.0
        changes.append("총 콜레스테롤을 200 mg/dL 이하로 낮추기")

    if _is_finite_number(hmg) and hmg > 12.0:
        improved[8] = 12.0
        changes.append("혈색소를 12 g/dL 이하로 조정하기")

    if _is_finite_number(ast) and ast > 43.0:
        improved[9] = 43.0
        changes.append("AST를 43 U/L 이하로 낮추기")

    if _is_finite_number(alt) and alt > 45.0:
        improved[10] = 45.0
        changes.append("ALT를 45 U/L 이하로 낮추기")

    if _is_finite_number(ggt) and _is_finite_number(sex):
        if sex == 0.0 and ggt > 36.0:
            improved[11] = 36.0
            changes.append("감마 GTP를 36 U/L 이하(여성 기준)로 낮추기")
        if sex == 1.0 and ggt > 61.0:
            improved[11] = 61.0
            changes.append("감마 GTP를 61 U/L 이하(남성 기준)로 낮추기")

    if _is_finite_number(bmi) and (bmi < 18.5 or bmi > 25.0):
        improved[12] = 22.0
        changes.append("BMI를 22 근처로 조정하기")

    if _is_finite_number(smoking) and smoking == 3.0:
        improved[13] = 2.0
        changes.append("흡연 상태를 현재 흡연에서 과거 흡연/금연으로 전환하기")

    if _is_finite_number(alcohol) and alcohol in (3.0, 4.0):
        improved[14] = alcohol - 2.0
        changes.append("음주 빈도 줄이기")

    if _is_finite_number(exercise) and exercise in (1.0, 2.0):
        improved[15] = exercise + 2.0
        changes.append("운동 빈도 늘리기")

    if _is_finite_number(visit) and visit > 5.0:
        improved[32] = 3.0
        changes.append("1년 내 병원 방문 횟수 3회 이하로 관리하기")

    return improved, changes


def run_kr_prediction(payload: dict[str, Any]) -> dict[str, Any]:
    values, patient_info = parse_kr_payload(payload)
    current_prob = predict_probability(values)
    current = _prediction_summary(current_prob)

    improved_values, recommendations = _apply_lifestyle_improvements(values)
    improved = None
    if recommendations:
        improved_prob = predict_probability(improved_values)
        improved = _prediction_summary(improved_prob)

    return {
        "current": current,
        "improved": improved,
        "recommendations": recommendations,
        "patient_info": patient_info,
    }

