# 🔮 JobMind AI — AI 채용공고 분석 에이전트

> LangGraph · RAG · Claude API 기반 채용공고 분석 및 지원 전략 제안 서비스

---

## 📌 프로젝트 개요

취업 준비생이 채용공고를 효율적으로 분석하고 맞춤형 지원 전략을 받을 수 있도록 설계한 AI 에이전트 서비스입니다.

단순 채용공고 나열이 아닌, **AI가 직접 공고를 분석하고 핵심 역량 및 지원 전략을 제안**합니다.

---

## 🎯 핵심 기능

| 기능 | 설명 |
|------|------|
| 채용공고 검색 | RAG 기반 시맨틱 검색으로 조건에 맞는 공고 탐색 |
| AI 공고 분석 | 핵심 요구 역량, 우대 사항, 지원 전략 자동 분석 |
| 질문 답변 | AI PM/엔지니어 취준 관련 일반 질문 답변 |
| 타 사이트 비교 | 사람인, 원티드 대비 차별화 기능 비교 표 |

---

## 🛠 기술 스택

### Backend
- **FastAPI** — REST API 서버
- **LangGraph** — 에이전트 흐름 설계 (노드, 엣지, 조건 분기)
- **Claude API (claude-sonnet-4-5)** — 자연어 분석 및 답변 생성
- **Voyage AI** — 한국어 최적화 임베딩 모델
- **ChromaDB** — 벡터 데이터베이스

### Frontend
- **React** — UI 프레임워크
- **Axios** — API 통신

---

## 🏗 시스템 아키텍처

```
사용자 입력
    ↓
[React Frontend]
    ↓ HTTP POST /analyze
[FastAPI Backend]
    ↓
[LangGraph 오케스트레이터]
    ↓
┌─────────────────────────────┐
│  분류 노드 (입력 타입 판단)  │
└──────┬──────────────┬───────┘
       ↓              ↓
  채용공고 관련    일반 질문
       ↓
  [RAG 검색 노드]
  Voyage AI 임베딩
  ChromaDB 벡터 검색
       ↓
  ┌────┴────┐
  분석 노드  답변 노드
       ↓
  최종 답변 → React UI
```

---

## ⚙️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/본인계정/jobmind-ai.git
cd jobmind-ai
```

### 2. 환경변수 설정
```bash
# backend/.env 파일 생성
ANTHROPIC_API_KEY=your_key
VOYAGE_API_KEY=your_key
```

### 3. 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### 4. 프론트엔드 실행
```bash
cd frontend
npm install
npm start
```

---

## 📁 프로젝트 구조

```
jobmind-ai/
├── backend/
│   ├── main.py        # FastAPI 서버 및 API 엔드포인트
│   ├── agent.py       # LangGraph + RAG 에이전트 엔진
│   └── .env           # 환경변수 (API 키)
├── frontend/
│   ├── src/
│   │   ├── App.js     # 메인 React 컴포넌트
│   │   └── App.css    # 스타일
│   └── package.json
└── README.md
```

---

## 🔍 LangGraph 에이전트 흐름

```
classify_node     입력 타입 분류 (채용공고검색 / 공고분석 / 일반질문)
    ↓
rag_search_node   Voyage AI 임베딩 → ChromaDB 벡터 검색
    ↓
analyze_node      채용공고 상세 분석 (역량, 우대사항, 전략)
response_node     검색 결과 기반 답변 생성
general_node      일반 질문 답변
```

---

## 💡 기획 의도

> "취준생이 가장 힘든 건 수백 개의 공고 중 나에게 맞는 걸 찾고, 어떻게 준비해야 할지 모르는 것"

기존 채용 플랫폼은 공고 나열에 그칩니다. JobMind AI는 **AI가 직접 분석하고 전략까지 제안**하는 차별화된 서비스를 목표로 합니다.

---

## 👤 개발자

- GitHub: [@본인계정](https://github.com/본인계정)
