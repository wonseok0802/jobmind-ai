from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

# React 연결을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "AI 채용공고 분석 에이전트 서버 실행 중"}

@app.post("/analyze")
def analyze(request: QueryRequest):
    result = run_agent(request.question)
    return {
        "question": request.question,
        "answer": result["final_output"],
        "input_type": result["input_type"]
    }

@app.get("/jobs")
def get_jobs():
    jobs = [
        {"id": "1", "company": "카카오", "title": "AI 엔지니어", "tags": ["Python", "LangChain", "RAG"], "level": "경력 2년"},
        {"id": "2", "company": "네이버", "title": "AI 서비스 기획자", "tags": ["기획", "데이터 분석", "SQL"], "level": "신입 가능"},
        {"id": "3", "company": "토스", "title": "머신러닝 엔지니어", "tags": ["PyTorch", "TensorFlow", "MLOps"], "level": "경력 3년"},
        {"id": "4", "company": "라인", "title": "AI 프로덕트 매니저", "tags": ["PM", "AI 서비스", "영어"], "level": "경력 2년"},
        {"id": "5", "company": "당근마켓", "title": "AI 엔지니어", "tags": ["Python", "MLOps", "RAG"], "level": "신입 가능"},
    ]
    return {"jobs": jobs}
