from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from agent import run_agent, get_all_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class FilterRequest(BaseModel):
    field: Optional[str] = None
    level: Optional[str] = None
    tags: Optional[List[str]] = None
    keyword: Optional[str] = None

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
    return {"jobs": get_all_jobs()}

@app.post("/jobs/filter")
def filter_jobs(request: FilterRequest):
    jobs = get_all_jobs()

    if request.field and request.field != "전체":
        jobs = [j for j in jobs if j["field"] == request.field]

    if request.level and request.level != "전체":
        if request.level == "신입":
            jobs = [j for j in jobs if "신입" in j["level"]]
        elif request.level == "경력":
            jobs = [j for j in jobs if "경력" in j["level"]]

    if request.tags:
        jobs = [j for j in jobs if any(tag in j["tags"] for tag in request.tags)]

    if request.keyword:
        kw = request.keyword.lower()
        jobs = [j for j in jobs if
                kw in j["company"].lower() or
                kw in j["title"].lower() or
                kw in j["text"].lower() or
                any(kw in tag.lower() for tag in j["tags"])]

    return {"jobs": jobs, "total": len(jobs)}

@app.get("/fields")
def get_fields():
    return {"fields": ["전체", "NLP/LLM", "컴퓨터비전", "ML/추천시스템", "MLOps", "데이터 분석", "AI 기획/PM", "강화학습"]}
