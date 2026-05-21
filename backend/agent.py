from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from anthropic import Anthropic
import voyageai
import chromadb
import os
from typing import TypedDict

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# 벡터DB 초기화
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="job_postings")

job_postings = [
    {"id": "1", "text": "카카오 AI 엔지니어 채용. 필수: Python, LangChain, RAG 경험. 우대: LLM 파인튜닝, 벡터DB. 서울 근무. 경력 2년 이상."},
    {"id": "2", "text": "네이버 AI 서비스 기획자 채용. 필수: AI 서비스 기획 경험, 데이터 분석. 우대: 개발 경험자, SQL. 성남 근무. 신입 가능."},
    {"id": "3", "text": "토스 머신러닝 엔지니어 채용. 필수: PyTorch, TensorFlow, 모델 학습 경험. 우대: MLOps, 추천 시스템. 서울 근무. 경력 3년 이상."},
    {"id": "4", "text": "라인 AI 프로덕트 매니저 채용. 필수: PM 경험 2년, AI 서비스 이해. 우대: 개발 경험, 영어. 서울 근무. 경력 2년 이상."},
    {"id": "5", "text": "당근마켓 AI 엔지니어 채용. 필수: Python, MLOps, 모델 배포 경험. 우대: LLM, RAG, 벡터DB 경험. 서울 근무. 신입 가능."},
]

# 임베딩 저장
texts = [job["text"] for job in job_postings]
result = voyage.embed(texts, model="voyage-3", input_type="document")
for i, job in enumerate(job_postings):
    collection.add(
        ids=[job["id"]],
        embeddings=[result.embeddings[i]],
        documents=[job["text"]]
    )

# State 정의
class AgentState(TypedDict):
    user_input: str
    input_type: str
    retrieved_docs: str
    analysis: str
    final_output: str

# 분류 노드
def classify_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""다음 입력 유형을 판단해줘. 반드시 하나만 답해줘:
- 채용공고검색
- 공고분석
- 일반질문

입력: {state['user_input']}"""
        }]
    )
    return {"input_type": response.content[0].text.strip()}

# RAG 검색 노드
def rag_search_node(state: AgentState) -> AgentState:
    query_embedding = voyage.embed(
        [state["user_input"]], model="voyage-3", input_type="query"
    ).embeddings[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=2)
    retrieved_docs = "\n".join(results["documents"][0])
    return {"retrieved_docs": retrieved_docs}

# 분석 노드
def analyze_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""채용공고를 분석해줘.

[채용공고]
{state['retrieved_docs']}

[질문]
{state['user_input']}

1. 핵심 요구 역량
2. 우대 사항
3. 지원 전략"""
        }]
    )
    return {"final_output": response.content[0].text}

# 검색 결과 답변 노드
def response_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""검색된 채용공고를 바탕으로 답해줘.

[채용공고]
{state['retrieved_docs']}

[질문]
{state['user_input']}"""
        }]
    )
    return {"final_output": response.content[0].text}

# 일반 질문 노드
def general_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"AI 취준생 입장에서 도움되게 답변해줘: {state['user_input']}"
        }]
    )
    return {"final_output": response.content[0].text}

# 분기 함수
def route_input(state: AgentState) -> str:
    if "채용공고검색" in state["input_type"] or "공고분석" in state["input_type"]:
        return "rag_search"
    return "general"

def route_after_search(state: AgentState) -> str:
    if "공고분석" in state["input_type"]:
        return "analyze"
    return "response"

# 그래프 설계
graph = StateGraph(AgentState)
graph.add_node("classify", classify_node)
graph.add_node("rag_search", rag_search_node)
graph.add_node("analyze", analyze_node)
graph.add_node("response", response_node)
graph.add_node("general", general_node)

graph.set_entry_point("classify")
graph.add_conditional_edges("classify", route_input, {"rag_search": "rag_search", "general": "general"})
graph.add_conditional_edges("rag_search", route_after_search, {"analyze": "analyze", "response": "response"})
graph.add_edge("analyze", END)
graph.add_edge("response", END)
graph.add_edge("general", END)

app = graph.compile()

def run_agent(question: str) -> dict:
    return app.invoke({
        "user_input": question,
        "input_type": "",
        "retrieved_docs": "",
        "analysis": "",
        "final_output": ""
    })
