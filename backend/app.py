"""Flask API server for Korean AA prediction."""

from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, request

from backend.schema import KR_FIELDS
from backend.service import run_kr_prediction


def _allowed_origins() -> Any:
    raw = os.getenv("ALLOWED_ORIGINS", "*").strip()
    if raw == "*" or raw == "":
        return "*"
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app() -> Flask:
    app = Flask(__name__)
    cors_origins = _allowed_origins()

    @app.after_request
    def add_cors_headers(response: Any) -> Any:
        if request.path.startswith("/api/"):
            if cors_origins == "*":
                response.headers["Access-Control-Allow-Origin"] = "*"
            else:
                req_origin = request.headers.get("Origin", "")
                if req_origin in cors_origins:
                    response.headers["Access-Control-Allow-Origin"] = req_origin

            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    @app.get("/api/health")
    def health() -> Any:
        return jsonify({"status": "ok"})

    @app.get("/api/schema/kr")
    def schema_kr() -> Any:
        return jsonify({"fields": KR_FIELDS})

    @app.post("/api/predict/kr")
    def predict_kr() -> Any:
        payload = request.get_json(silent=True) or {}
        try:
            result = run_kr_prediction(payload)
            return jsonify(result)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500

    @app.get("/")
    def index() -> Any:
        return jsonify(
            {
                "message": "Alopecia Areata KR Prediction API",
                "health": "/api/health",
                "schema": "/api/schema/kr",
                "predict": "/api/predict/kr",
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "9999"))
    app.run(host="0.0.0.0", port=port)
