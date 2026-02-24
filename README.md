# 원형탈모 예측 웹앱 (KR 전용, 정적 프론트 + Python API)

이 프로젝트는 기존 Flask 템플릿 기반 앱과 별도로 아래 구조를 추가했습니다.

- `frontend/`: 정적 웹 페이지 (GitHub Pages/Vercel 배포용)
- `backend/`: Python API (Render/Railway/Cloud Run 배포용)

사용자는 브라우저에서 URL만 열면 되고, 로컬에서 Python을 실행할 필요가 없습니다.

## 1) 로컬 실행

### 백엔드 API

```bash
cd /Users/seungha/Desktop/KHU/Lab/7_alopecia/code/web_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python3 -m backend.app
```

- 기본 URL: `http://127.0.0.1:9999`
- 상태 확인: `http://127.0.0.1:9999/api/health`

### 프론트엔드 정적 페이지

```bash
cd /Users/seungha/Desktop/KHU/Lab/7_alopecia/code/web_app
python3 -m http.server 8080 --directory frontend
```

- 접속: `http://127.0.0.1:8080`
- API 주소는 `frontend/config.js`의 `API_BASE_URL`로 설정합니다.

## 2) 배포 권장 구성

### 백엔드 (Render 예시)

1. 새 Web Service 생성
2. Build Command: `pip install -r backend/requirements.txt`
3. Start Command: `gunicorn backend.app:app`
4. 환경변수(선택): `ALLOWED_ORIGINS=https://<프론트도메인>`

### 프론트엔드 (GitHub Pages 예시)

1. `frontend/` 내용을 정적 호스팅에 배포
2. `frontend/config.js`의 `API_BASE_URL`을 배포된 백엔드 URL로 변경
3. 배포 URL 접속 후 바로 사용

## 3) API 명세

- `GET /api/health` : 서버 헬스체크
- `GET /api/schema/kr` : 폼 필드 스키마
- `POST /api/predict/kr` : 예측 수행

요청 본문(`POST /api/predict/kr`)은 `uv_value1`~`uv_value33` 키를 포함한 JSON입니다.

## 4) 참고

- LIME 기능은 제외했습니다(요청사항 반영).
- 한국어(KR) 경로만 구현했습니다.
- 기존 `web_app.py`, `templates/` 기반 코드는 그대로 남겨두었습니다.

