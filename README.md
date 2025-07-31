# 단어장 백엔드 API (Workbook Backend v2)

MongoDB와 OpenAI API를 활용한 단어 학습 관리 시스템의 백엔드 서버입니다.

## 🤖 AI 기반 개발 (Vibe Coding)

이 프로젝트는 **Claude Code**를 활용한 **바이브 코딩(Vibe Coding)** 방식으로 개발되었습니다!
- AI 어시스턴트와의 협업을 통한 효율적인 개발
- 자동화된 코드 생성과 구조 설계
- AI의 도움을 받아 완성된 현대적인 백엔드 아키텍처

## 📋 프로젝트 개요

이 프로젝트는 FastAPI를 기반으로 한 RESTful API 서버로, 단어 학습을 위한 CRUD 기능과 OpenAI API를 활용한 AI 기반 단어 데이터 생성 기능을 제공합니다.

## 🛠 기술 스택

- **웹 프레임워크**: FastAPI
- **데이터베이스**: MongoDB
- **AI 서비스**: OpenAI API (GPT-4.1-mini)
- **데이터 검증**: Pydantic
- **환경 변수 관리**: python-dotenv
- **CORS**: FastAPI CORS Middleware

## 📂 프로젝트 구조

```
workbook_BE_v2/
├── main.py              # 메인 애플리케이션 및 서버 설정
├── api.py               # 비즈니스 로직 및 데이터 처리
├── database.py          # MongoDB 연결 및 관리
├── models.py            # Pydantic 데이터 모델 정의
├── routers.py           # API 라우터 및 엔드포인트
├── openai_service.py    # OpenAI API 서비스
├── migrate_data.py      # 데이터 마이그레이션 스크립트
├── test_main.http       # API 테스트 파일
└── .env                 # 환경 변수 파일
```

## 🚀 주요 기능

### 1. 단어 관리 API
- **GET `/words`**: 모든 단어 조회
- **POST `/words`**: 새 단어 추가
- **DELETE `/words/{word_id}`**: 단어 삭제

### 2. AI 기반 단어 생성
- **POST `/words/generate`**: OpenAI API를 활용한 자동 단어 데이터 생성
- 컴퓨터 과학 및 보안 연구 분야에 특화된 용어 정의
- 한국어 의미, 영어 설명, 예문, 관련 단어 자동 생성

### 3. 데이터 모델
- **품사 분류**: 명사, 동사, 형용사, 부사, 대명사, 전치사, 접속사, 감탄사
- **단어 형태**: 원형과 변형된 형태들
- **예문**: 영어 예문과 한국어 번역
- **관련 단어**: 의미적으로 연관된 단어들

## 🔧 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install fastapi uvicorn pymongo python-dotenv openai pydantic
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```env
MONGODB_URL=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
```

### 3. 서버 실행
```bash
# 개발 서버 실행
python main.py

# 또는 uvicorn으로 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 `http://localhost:8000`에서 API에 접근할 수 있습니다.

## 📖 API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 테스트

### 데이터베이스 연결 테스트
```bash
curl http://localhost:8000/test-db
```

### 단어 생성 테스트
```bash
curl -X POST "http://localhost:8000/words/generate" \
     -H "Content-Type: application/json" \
     -d '{"word": "algorithm"}'
```

## 📄 주요 파일 설명

- **`main.py`**: FastAPI 애플리케이션 초기화, CORS 설정, 라이프사이클 관리
- **`models.py`**: 단어 데이터 구조를 정의하는 Pydantic 모델들
- **`database.py`**: MongoDB 연결 설정 및 컬렉션 관리
- **`api.py`**: 단어 CRUD 로직 및 AI 기반 단어 생성 로직
- **`routers.py`**: HTTP 요청을 처리하는 FastAPI 라우터
- **`openai_service.py`**: OpenAI API 호출 및 응답 처리

## 🔒 보안 고려사항

- API 키는 환경 변수로 관리
- 프로덕션 환경에서는 CORS 설정을 특정 도메인으로 제한
- 입력 데이터 검증을 위한 Pydantic 모델 사용

## 🔄 향후 개발 계획

- 사용자 인증 및 권한 관리
- 단어 학습 진도 추적
- 단어 검색 및 필터링 기능
- 배치 처리를 통한 대량 단어 생성
- 캐싱을 통한 성능 최적화

## 💡 개발 철학: 바이브 코딩

이 프로젝트는 전통적인 코딩 방식을 넘어선 **바이브 코딩(Vibe Coding)** 접근법으로 개발되었습니다:

- **🚀 빠른 프로토타이핑**: AI와의 실시간 대화를 통한 아이디어 구현
- **🧠 지능적 설계**: Claude Code가 제안하는 최적화된 아키텍처 패턴
- **⚡ 효율적 개발**: 반복적인 작업은 AI가, 창의적 결정은 개발자가
- **📚 학습 가속화**: AI 설명을 통한 즉시 피드백과 코드 이해

**바이브 코딩의 핵심**: 인간의 창의성과 AI의 효율성이 만나 시너지를 창출하는 새로운 개발 패러다임!

## 📝 라이선스

이 프로젝트는 개인 학습 목적으로 개발되었습니다.
**Powered by Claude Code** - AI와 함께하는 미래의 코딩 경험!