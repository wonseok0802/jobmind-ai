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
    # 대기업 AI 엔지니어
    {"id": "1", "company": "카카오", "title": "AI 엔지니어", "field": "NLP/LLM", "level": "경력 2년", "tags": ["Python", "LangChain", "RAG", "LLM"], "text": "카카오 AI 엔지니어 채용. 필수: Python, LangChain, RAG 경험. 우대: LLM 파인튜닝, 벡터DB. 서울 근무. 경력 2년 이상."},
    {"id": "2", "company": "네이버", "title": "AI 서비스 기획자", "field": "AI 기획/PM", "level": "신입 가능", "tags": ["기획", "데이터 분석", "SQL"], "text": "네이버 AI 서비스 기획자 채용. 필수: AI 서비스 기획 경험, 데이터 분석. 우대: 개발 경험자, SQL. 성남 근무. 신입 가능."},
    {"id": "3", "company": "토스", "title": "머신러닝 엔지니어", "field": "ML/추천시스템", "level": "경력 3년", "tags": ["PyTorch", "TensorFlow", "MLOps"], "text": "토스 머신러닝 엔지니어 채용. 필수: PyTorch, TensorFlow, 모델 학습 경험. 우대: MLOps, 추천 시스템. 서울 근무. 경력 3년 이상."},
    {"id": "4", "company": "라인", "title": "AI 프로덕트 매니저", "field": "AI 기획/PM", "level": "경력 2년", "tags": ["PM", "AI 서비스", "영어"], "text": "라인 AI 프로덕트 매니저 채용. 필수: PM 경험 2년, AI 서비스 이해. 우대: 개발 경험, 영어. 서울 근무. 경력 2년 이상."},
    {"id": "5", "company": "당근마켓", "title": "AI 엔지니어", "field": "MLOps", "level": "신입 가능", "tags": ["Python", "MLOps", "RAG", "LLM"], "text": "당근마켓 AI 엔지니어 채용. 필수: Python, MLOps, 모델 배포 경험. 우대: LLM, RAG, 벡터DB 경험. 서울 근무. 신입 가능."},
    {"id": "6", "company": "삼성전자", "title": "AI 연구원", "field": "컴퓨터비전", "level": "경력 3년", "tags": ["Python", "PyTorch", "컴퓨터비전", "딥러닝"], "text": "삼성전자 AI 연구원 채용. 필수: 딥러닝, 컴퓨터비전 연구 경험, PyTorch. 우대: 논문 실적, CUDA 프로그래밍. 수원 근무. 경력 3년 이상."},
    {"id": "7", "company": "LG AI연구원", "title": "LLM 연구원", "field": "NLP/LLM", "level": "경력 2년", "tags": ["Python", "LLM", "NLP", "PyTorch"], "text": "LG AI연구원 LLM 연구원 채용. 필수: NLP, LLM 연구 경험, PyTorch. 우대: 대규모 모델 학습, RLHF. 서울 근무. 경력 2년 이상."},
    {"id": "8", "company": "SK텔레콤", "title": "AI 서비스 개발자", "field": "AI 서비스", "level": "경력 2년", "tags": ["Python", "FastAPI", "LLM", "RAG"], "text": "SK텔레콤 AI 서비스 개발자 채용. 필수: Python, FastAPI, LLM 연동 경험. 우대: RAG, 멀티모달. 서울 근무. 경력 2년 이상."},
    {"id": "9", "company": "현대자동차", "title": "자율주행 AI 엔지니어", "field": "컴퓨터비전", "level": "경력 3년", "tags": ["Python", "C++", "컴퓨터비전", "ROS"], "text": "현대자동차 자율주행 AI 엔지니어 채용. 필수: 컴퓨터비전, C++, ROS. 우대: 자율주행 경험, CUDA. 의왕 근무. 경력 3년 이상."},
    {"id": "10", "company": "쿠팡", "title": "데이터 사이언티스트", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "SQL", "머신러닝", "A/B테스트"], "text": "쿠팡 데이터 사이언티스트 채용. 필수: Python, SQL, 머신러닝 경험. 우대: A/B 테스트, 추천 시스템. 서울 근무. 경력 2년 이상."},
    # 중견기업
    {"id": "11", "company": "뤼튼", "title": "LLM 엔지니어", "field": "NLP/LLM", "level": "신입 가능", "tags": ["Python", "LLM", "LangChain", "RAG"], "text": "뤼튼 LLM 엔지니어 채용. 필수: Python, LLM API 연동, LangChain. 우대: RAG 구현 경험, 프롬프트 엔지니어링. 서울 근무. 신입 가능."},
    {"id": "12", "company": "업스테이지", "title": "AI 엔지니어", "field": "NLP/LLM", "level": "경력 1년", "tags": ["Python", "PyTorch", "LLM", "파인튜닝"], "text": "업스테이지 AI 엔지니어 채용. 필수: Python, PyTorch, LLM 파인튜닝. 우대: RLHF, 한국어 NLP. 서울 근무. 경력 1년 이상."},
    {"id": "13", "company": "크래프톤", "title": "게임 AI 엔지니어", "field": "강화학습", "level": "경력 2년", "tags": ["Python", "강화학습", "Unity", "PyTorch"], "text": "크래프톤 게임 AI 엔지니어 채용. 필수: 강화학습, Python, PyTorch. 우대: Unity ML-Agents, 게임 AI 경험. 서울 근무. 경력 2년 이상."},
    {"id": "14", "company": "카카오페이", "title": "ML 엔지니어", "field": "ML/추천시스템", "level": "경력 2년", "tags": ["Python", "머신러닝", "SQL", "Spark"], "text": "카카오페이 ML 엔지니어 채용. 필수: Python, 머신러닝, SQL. 우대: Spark, 금융 도메인 지식. 서울 근무. 경력 2년 이상."},
    {"id": "15", "company": "하이퍼클로바X", "title": "AI 연구원", "field": "NLP/LLM", "level": "경력 3년", "tags": ["Python", "PyTorch", "LLM", "NLP"], "text": "하이퍼클로바X AI 연구원 채용. 필수: NLP, LLM 연구, PyTorch. 우대: 대규모 모델 학습, 멀티모달. 성남 근무. 경력 3년 이상."},
    {"id": "16", "company": "KT AI2XL", "title": "AI 플랫폼 개발자", "field": "MLOps", "level": "경력 2년", "tags": ["Python", "Kubernetes", "MLOps", "Docker"], "text": "KT AI2XL AI 플랫폼 개발자 채용. 필수: Python, Kubernetes, Docker, MLOps. 우대: Kubeflow, 클라우드. 서울 근무. 경력 2년 이상."},
    {"id": "17", "company": "카카오브레인", "title": "멀티모달 AI 연구원", "field": "컴퓨터비전", "level": "경력 2년", "tags": ["Python", "PyTorch", "멀티모달", "컴퓨터비전"], "text": "카카오브레인 멀티모달 AI 연구원 채용. 필수: 멀티모달 모델 연구, PyTorch. 우대: Diffusion 모델, 이미지 생성. 서울 근무. 경력 2년 이상."},
    {"id": "18", "company": "몰로코", "title": "ML 엔지니어", "field": "ML/추천시스템", "level": "경력 3년", "tags": ["Python", "머신러닝", "광고기술", "Scala"], "text": "몰로코 ML 엔지니어 채용. 필수: 머신러닝, Python, 광고 기술 이해. 우대: Scala, 실시간 추론. 서울 근무. 경력 3년 이상."},
    {"id": "19", "company": "스캐터랩", "title": "NLP 엔지니어", "field": "NLP/LLM", "level": "경력 1년", "tags": ["Python", "NLP", "PyTorch", "대화시스템"], "text": "스캐터랩 NLP 엔지니어 채용. 필수: NLP, Python, PyTorch. 우대: 대화 시스템, 감정 분석. 서울 근무. 경력 1년 이상."},
    {"id": "20", "company": "딥엑스", "title": "AI 칩 소프트웨어 엔지니어", "field": "MLOps", "level": "경력 2년", "tags": ["C++", "Python", "NPU", "CUDA"], "text": "딥엑스 AI 칩 소프트웨어 엔지니어 채용. 필수: C++, Python, CUDA. 우대: NPU 최적화, 모델 경량화. 서울 근무. 경력 2년 이상."},
    # AI PM/기획
    {"id": "21", "company": "네이버 클라우드", "title": "AI 서비스 PM", "field": "AI 기획/PM", "level": "경력 3년", "tags": ["PM", "AI 서비스", "클라우드", "기획"], "text": "네이버 클라우드 AI 서비스 PM 채용. 필수: PM 경험 3년, AI 서비스 이해, 클라우드 지식. 우대: 개발 경험, B2B. 성남 근무. 경력 3년 이상."},
    {"id": "22", "company": "카카오엔터프라이즈", "title": "AI 솔루션 기획자", "field": "AI 기획/PM", "level": "경력 2년", "tags": ["기획", "AI 서비스", "B2B", "SQL"], "text": "카카오엔터프라이즈 AI 솔루션 기획자 채용. 필수: AI 서비스 기획, B2B 경험. 우대: SQL, 개발 이해. 서울 근무. 경력 2년 이상."},
    {"id": "23", "company": "SK C&C", "title": "AI 컨설턴트", "field": "AI 기획/PM", "level": "경력 3년", "tags": ["AI 컨설팅", "기획", "프레젠테이션", "데이터 분석"], "text": "SK C&C AI 컨설턴트 채용. 필수: AI 컨설팅 경험 3년, 데이터 분석. 우대: 제조/금융 도메인. 서울 근무. 경력 3년 이상."},
    {"id": "24", "company": "LG CNS", "title": "AI 플랫폼 기획자", "field": "AI 기획/PM", "level": "경력 2년", "tags": ["기획", "AI 플랫폼", "데이터 분석", "SQL"], "text": "LG CNS AI 플랫폼 기획자 채용. 필수: AI 플랫폼 기획 경험, 데이터 분석. 우대: SQL, 개발 이해, 제조 도메인. 서울 근무. 경력 2년 이상."},
    {"id": "25", "company": "카카오", "title": "AI 프로덕트 오너", "field": "AI 기획/PM", "level": "경력 4년", "tags": ["PO", "AI 서비스", "애자일", "데이터 분석"], "text": "카카오 AI 프로덕트 오너 채용. 필수: PO 경험 4년, AI 서비스 이해, 데이터 기반 의사결정. 우대: 애자일, 개발 경험. 서울 근무. 경력 4년 이상."},
    # 데이터 엔지니어
    {"id": "26", "company": "배달의민족", "title": "데이터 엔지니어", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "Spark", "Kafka", "SQL"], "text": "배달의민족 데이터 엔지니어 채용. 필수: Python, Spark, SQL. 우대: Kafka, 실시간 파이프라인. 서울 근무. 경력 2년 이상."},
    {"id": "27", "company": "야놀자", "title": "AI 데이터 사이언티스트", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "SQL", "머신러닝", "추천시스템"], "text": "야놀자 AI 데이터 사이언티스트 채용. 필수: Python, SQL, 머신러닝. 우대: 추천 시스템, 여행 도메인. 서울 근무. 경력 2년 이상."},
    {"id": "28", "company": "직방", "title": "부동산 AI 엔지니어", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "머신러닝", "SQL", "부동산"], "text": "직방 부동산 AI 엔지니어 채용. 필수: Python, 머신러닝, SQL. 우대: 부동산 도메인, 가격 예측 모델. 서울 근무. 경력 2년 이상."},
    {"id": "29", "company": "무신사", "title": "패션 AI 엔지니어", "field": "컴퓨터비전", "level": "경력 2년", "tags": ["Python", "컴퓨터비전", "추천시스템", "PyTorch"], "text": "무신사 패션 AI 엔지니어 채용. 필수: 컴퓨터비전, Python, PyTorch. 우대: 패션 도메인, 이미지 검색. 서울 근무. 경력 2년 이상."},
    {"id": "30", "company": "버킷플레이스", "title": "인테리어 AI 엔지니어", "field": "컴퓨터비전", "level": "신입 가능", "tags": ["Python", "컴퓨터비전", "PyTorch", "추천시스템"], "text": "버킷플레이스 인테리어 AI 엔지니어 채용. 필수: Python, 컴퓨터비전. 우대: 3D 이해, 인테리어 도메인. 서울 근무. 신입 가능."},
    # 스타트업
    {"id": "31", "company": "뷰노", "title": "의료 AI 연구원", "field": "컴퓨터비전", "level": "경력 2년", "tags": ["Python", "딥러닝", "의료영상", "PyTorch"], "text": "뷰노 의료 AI 연구원 채용. 필수: 딥러닝, 의료 영상 처리, PyTorch. 우대: FDA 인허가, 임상 경험. 서울 근무. 경력 2년 이상."},
    {"id": "32", "company": "루닛", "title": "AI 연구 엔지니어", "field": "컴퓨터비전", "level": "경력 2년", "tags": ["Python", "PyTorch", "의료영상", "컴퓨터비전"], "text": "루닛 AI 연구 엔지니어 채용. 필수: 컴퓨터비전, 의료 영상, PyTorch. 우대: 논문 실적, 병원 협업. 서울 근무. 경력 2년 이상."},
    {"id": "33", "company": "에이슬립", "title": "수면 AI 엔지니어", "field": "데이터 분석", "level": "경력 1년", "tags": ["Python", "시계열", "신호처리", "머신러닝"], "text": "에이슬립 수면 AI 엔지니어 채용. 필수: Python, 시계열 분석, 신호 처리. 우대: 수면 도메인, 웨어러블. 서울 근무. 경력 1년 이상."},
    {"id": "34", "company": "코어닷투데이", "title": "금융 AI 엔지니어", "field": "ML/추천시스템", "level": "경력 2년", "tags": ["Python", "머신러닝", "금융", "시계열"], "text": "코어닷투데이 금융 AI 엔지니어 채용. 필수: Python, 머신러닝, 금융 도메인. 우대: 시계열 예측, 알고리즘 트레이딩. 서울 근무. 경력 2년 이상."},
    {"id": "35", "company": "마키나락스", "title": "제조 AI 엔지니어", "field": "MLOps", "level": "경력 2년", "tags": ["Python", "머신러닝", "제조", "이상탐지"], "text": "마키나락스 제조 AI 엔지니어 채용. 필수: Python, 머신러닝, 제조 도메인. 우대: 이상 탐지, 예지 보전. 서울 근무. 경력 2년 이상."},
    {"id": "36", "company": "스파크바이트", "title": "AI 챗봇 엔지니어", "field": "NLP/LLM", "level": "신입 가능", "tags": ["Python", "LLM", "챗봇", "RAG"], "text": "스파크바이트 AI 챗봇 엔지니어 채용. 필수: Python, LLM, 챗봇 개발. 우대: RAG, 대화 시스템. 서울 근무. 신입 가능."},
    {"id": "37", "company": "퓨리오사AI", "title": "AI 칩 컴파일러 엔지니어", "field": "MLOps", "level": "경력 3년", "tags": ["C++", "컴파일러", "NPU", "LLVM"], "text": "퓨리오사AI AI 칩 컴파일러 엔지니어 채용. 필수: C++, 컴파일러, LLVM. 우대: NPU 최적화, AI 가속기. 서울 근무. 경력 3년 이상."},
    {"id": "38", "company": "42마루", "title": "AI 보안 엔지니어", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "보안", "머신러닝", "이상탐지"], "text": "42마루 AI 보안 엔지니어 채용. 필수: Python, 보안, 머신러닝. 우대: 이상 탐지, 사이버 보안. 서울 근무. 경력 2년 이상."},
    {"id": "39", "company": "수퍼브에이아이", "title": "데이터 라벨링 PM", "field": "AI 기획/PM", "level": "경력 1년", "tags": ["PM", "데이터 라벨링", "AI 데이터", "기획"], "text": "수퍼브에이아이 데이터 라벨링 PM 채용. 필수: PM 경험, AI 데이터 이해. 우대: 데이터 라벨링 경험, 영어. 서울 근무. 경력 1년 이상."},
    {"id": "40", "company": "에이블리", "title": "패션 추천 AI 엔지니어", "field": "ML/추천시스템", "level": "경력 2년", "tags": ["Python", "추천시스템", "머신러닝", "패션"], "text": "에이블리 패션 추천 AI 엔지니어 채용. 필수: Python, 추천 시스템, 머신러닝. 우대: 패션 도메인, 개인화. 서울 근무. 경력 2년 이상."},
    {"id": "41", "company": "클로봇", "title": "로봇 AI 엔지니어", "field": "강화학습", "level": "경력 2년", "tags": ["Python", "ROS", "강화학습", "컴퓨터비전"], "text": "클로봇 로봇 AI 엔지니어 채용. 필수: ROS, Python, 강화학습. 우대: 실내 자율주행, 컴퓨터비전. 서울 근무. 경력 2년 이상."},
    {"id": "42", "company": "플리토", "title": "번역 AI 엔지니어", "field": "NLP/LLM", "level": "경력 2년", "tags": ["Python", "NLP", "번역", "LLM"], "text": "플리토 번역 AI 엔지니어 채용. 필수: NLP, Python, 번역 모델. 우대: LLM, 다국어 처리. 서울 근무. 경력 2년 이상."},
    {"id": "43", "company": "엔씨소프트", "title": "게임 AI 연구원", "field": "강화학습", "level": "경력 3년", "tags": ["Python", "강화학습", "게임AI", "PyTorch"], "text": "엔씨소프트 게임 AI 연구원 채용. 필수: 강화학습, Python, PyTorch. 우대: 게임 AI, 멀티에이전트. 성남 근무. 경력 3년 이상."},
    {"id": "44", "company": "솔트룩스", "title": "지식그래프 AI 엔지니어", "field": "NLP/LLM", "level": "경력 2년", "tags": ["Python", "지식그래프", "NLP", "RAG"], "text": "솔트룩스 지식그래프 AI 엔지니어 채용. 필수: 지식그래프, NLP, Python. 우대: RAG, 온톨로지. 서울 근무. 경력 2년 이상."},
    {"id": "45", "company": "원티드랩", "title": "HR AI 엔지니어", "field": "ML/추천시스템", "level": "경력 2년", "tags": ["Python", "추천시스템", "NLP", "HR"], "text": "원티드랩 HR AI 엔지니어 채용. 필수: Python, 추천 시스템, NLP. 우대: HR 도메인, 매칭 알고리즘. 서울 근무. 경력 2년 이상."},
    {"id": "46", "company": "하이퍼인사이트", "title": "AI 분석 컨설턴트", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "SQL", "데이터 분석", "시각화"], "text": "하이퍼인사이트 AI 분석 컨설턴트 채용. 필수: Python, SQL, 데이터 분석. 우대: 시각화, 리테일 도메인. 서울 근무. 경력 2년 이상."},
    {"id": "47", "company": "카카오헬스케어", "title": "헬스케어 AI PM", "field": "AI 기획/PM", "level": "경력 3년", "tags": ["PM", "헬스케어", "AI 서비스", "기획"], "text": "카카오헬스케어 헬스케어 AI PM 채용. 필수: PM 경험 3년, 헬스케어 도메인. 우대: AI 서비스 기획, 의료 규제 이해. 서울 근무. 경력 3년 이상."},
    {"id": "48", "company": "두나무", "title": "블록체인 AI 엔지니어", "field": "데이터 분석", "level": "경력 2년", "tags": ["Python", "블록체인", "시계열", "이상탐지"], "text": "두나무 블록체인 AI 엔지니어 채용. 필수: Python, 시계열 분석, 이상 탐지. 우대: 블록체인, 금융 도메인. 서울 근무. 경력 2년 이상."},
    {"id": "49", "company": "리멤버", "title": "명함 AI 엔지니어", "field": "컴퓨터비전", "level": "경력 1년", "tags": ["Python", "OCR", "컴퓨터비전", "NLP"], "text": "리멤버 명함 AI 엔지니어 채용. 필수: OCR, 컴퓨터비전, Python. 우대: NLP, 문서 이해. 서울 근무. 경력 1년 이상."},
    {"id": "50", "company": "클래스101", "title": "교육 AI 엔지니어", "field": "NLP/LLM", "level": "신입 가능", "tags": ["Python", "LLM", "교육", "추천시스템"], "text": "클래스101 교육 AI 엔지니어 채용. 필수: Python, LLM, 추천 시스템. 우대: 교육 도메인, 개인화 학습. 서울 근무. 신입 가능."},
]

# 임베딩 저장
print("채용공고 임베딩 중...")
texts = [job["text"] for job in job_postings]
result = voyage.embed(texts, model="voyage-3", input_type="document")
for i, job in enumerate(job_postings):
    collection.add(
        ids=[job["id"]],
        embeddings=[result.embeddings[i]],
        documents=[job["text"]]
    )
print(f"총 {len(job_postings)}개 채용공고 저장 완료!")

# State 정의
class AgentState(TypedDict):
    user_input: str
    input_type: str
    retrieved_docs: str
    analysis: str
    final_output: str

def classify_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=50,
        messages=[{"role": "user", "content": f"""다음 입력 유형을 판단해줘. 반드시 하나만 답해줘:
- 채용공고검색
- 공고분석
- 일반질문

입력: {state['user_input']}"""}]
    )
    return {"input_type": response.content[0].text.strip()}

def rag_search_node(state: AgentState) -> AgentState:
    query_embedding = voyage.embed([state["user_input"]], model="voyage-3", input_type="query").embeddings[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    retrieved_docs = "\n".join(results["documents"][0])
    return {"retrieved_docs": retrieved_docs}

def analyze_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": f"""채용공고를 상세하게 분석해줘.

[채용공고]
{state['retrieved_docs']}

[질문]
{state['user_input']}

아래 항목을 빠짐없이 분석해줘:
1. 핵심 요구 역량
2. 우대 사항
3. 근무 조건
4. 지원 전략
5. 준비해야 할 포트폴리오"""}]
    )
    return {"final_output": response.content[0].text}

def response_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": f"""검색된 채용공고를 바탕으로 상세하게 답해줘.

[채용공고]
{state['retrieved_docs']}

[질문]
{state['user_input']}"""}]
    )
    return {"final_output": response.content[0].text}

def general_node(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": f"AI 취준생 입장에서 도움되게 상세히 답변해줘: {state['user_input']}"}]
    )
    return {"final_output": response.content[0].text}

def route_input(state: AgentState) -> str:
    if "채용공고검색" in state["input_type"] or "공고분석" in state["input_type"]:
        return "rag_search"
    return "general"

def route_after_search(state: AgentState) -> str:
    if "공고분석" in state["input_type"]:
        return "analyze"
    return "response"

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

def get_all_jobs():
    return job_postings
