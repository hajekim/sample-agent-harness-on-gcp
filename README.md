# Enterprise AI Agent Harness Sample (Google Cloud)

이 프로젝트는 **"Google AI 에이전트 아키텍처 및 엔터프라이즈 개발 가이드"**를 기반으로 구축된 공식 샘플 에이전트 시스템입니다. 조직 수준에서 확장 가능하고 안전한 AI 에이전트 운영을 위한 표준 구조와 코드 레벨의 구현 패턴을 제공합니다.

---

## 💡 1. 핵심 기술 컨셉 (Core Concepts)

본 프로젝트의 아키텍처는 **하네스(Harness)**와 **자율 루프(Ralph Loop)**의 긴밀한 결합을 통해 엔터프라이즈급 안정성을 확보합니다.

### 1.1. 모델 하네스 (Model Harness)
단순한 LLM 호출 코드가 아니라 모델을 안전하게 감싸는 **소프트웨어 비계(Scaffolding)** 역할을 합니다.
- **역할**: 모델 추론 전후에 보안 정책(Policy) 적용, 도구(Tool) 실행 인터셉트, 세션 상태 관리, 입출력 스키마 강제 등을 수행합니다.
- **인터페이스 격리**: 하네스는 외부 시스템과의 통신 규격을 고정합니다. 내부 모델(Gemini 3.0)이나 프롬프트가 변경되어도 연동 규격은 일정하게 유지됩니다.

### 1.2. 자율 실행 루프 (Ralph Loop)
사용자의 1회성 질문에 답하는 수준을 넘어, 스스로 목표 달성 여부를 판단하며 반복 실행하는 패턴입니다.
- **마이크로 태스크 지향**: 전체 목표를 아주 작은 단위의 작업(TODO)으로 쪼개어 하나씩 해결함으로써 컨텍스트 오염을 방지하고 추론 성공률을 높입니다.
- **긴밀한 결합**: 자율 루프가 폭주하거나 환각에 빠지지 않도록, **하네스**가 실시간으로 정책을 검증하고 가드레일을 칩니다. 하네스가 '선로'라면, 랄프 루프는 그 위를 달리는 '자율주행 열차'입니다.

### 1.3. 컴파운딩 (Compounding)
시간이 흐를수록 에이전트가 더 똑똑해지는 **복리 효과**를 쌓아가는 과정입니다.
- **Micro (루프 내)**: `Checker` 에이전트의 피드백이 루프 상태(State)에 기록되어 다음 실행 시 동일한 실수를 반복하지 않습니다.
- **Macro (세션 간)**: 유의미한 결과물과 유저 선호도는 **Agent Engine Memory Bank**의 Managed Topic에 저장되어 다음 작업의 맥락이 됩니다.
- **Enterprise (조직)**: 실행 트레이스(Trace)를 기반으로 골든 데이터셋을 구축하고, CI/CD 단계에서 **LLM-as-a-judge** 평가를 거쳐 에이전트의 로직을 지속적으로 고도화합니다.

---

## 🏛️ 2. 아키텍처 레이어 설명

### 2.1. Orchestration Layer (`agents/agent.py`)
- **Planner → Worker → Checker** 구조의 ADK 파이프라인을 구축했습니다.
- `LoopAgent`를 최상위에 배치하여 자율 실행과 `max_iterations` 가드레일을 동시에 구현했습니다.

### 2.2. Harness Layer (`agents/harness.py`)
- `google-genai` SDK를 사용하여 Gemini 3 추론을 추상화합니다.
- `ThinkingConfig`와 `safety_settings`를 통해 엔터프라이즈급 품질과 안전성을 강제합니다.

### 2.3. Tooling & Security Layer (`tools/`)
- **Remote MCP**: `mcp_client.py`를 통해 인증과 권한 관리가 일원화된 외부 도구 서버와 연동합니다.
- **Interception Layer**: `policy_engine.py`가 모든 도구 호출 전 파괴적 명령을 검증하여 시스템을 보호합니다.
- **Grounding**: `grounding.py`가 Vertex AI Search를 활용해 사내 지식 기반의 답변을 보장합니다.

---

## 📁 3. 디렉토리 구조

```text
/ai-harness-gcp-sample/
├── .agent/              # 에이전트 개발 협업 및 계획 컨텍스트 (PLAN, DEFINE, ACTION)
│   ├── rules/           # 로컬 프로젝트 규칙
│   ├── skills/          # 에이전트 스킬 메모리
│   └── workflows/       # 메모리 관리 워크플로우
├── agents/              # 핵심 로직 (Ralph Loop, Harness, 리전별 설정)
│   ├── agent.py         # 전체 오케스트레이션 및 루프 정의
│   ├── harness.py       # 모델 호출 추상화 클래스
│   └── ralph_loop.py    # 상태 관리 및 ZDR 로직
├── ci-cd/               # Cloud Build 기반 CI/CD 파이프라인
│   └── cloudbuild.yaml
├── eval/                # 평가용 골든 데이터셋 및 평가 스크립트
│   └── run_eval.py
├── infra/               # Terraform 및 Memory Bank 상세 설정
│   ├── main.tf
│   └── memory_bank_config.py
├── prompts/             # 시스템 인스트럭션 및 정책 템플릿
│   └── system_instruction.txt
├── tools/               # 도구 연동 및 보안 레이어
│   ├── grounding.py     # RAG 및 환각 방지 연동
│   ├── mcp_client.py    # Remote MCP (SSE) 연동
│   └── policy_engine.py # SRE Interception Layer
├── .env.example         # 환경 변수 템플릿
├── .gitignore           # Git 제외 규칙
├── pyproject.toml       # 패키지 빌드 설정
├── requirements.txt     # Python 의존성 목록
└── README.md            # 본 가이드 문서
```

---

## 🚀 4. 시작하기 (Getting Started)

### 4.1. 환경 설정
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 4.2. Agent Engine 배포
```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="us-central1"

adk deploy agent_engine agents \
  --project $GOOGLE_CLOUD_PROJECT \
  --region $GOOGLE_CLOUD_LOCATION \
  --display_name "enterprise-harness-agent" \
  --validate-agent-import
```

---

## 🔍 5. Observability (Telemetry)

엔터프라이즈 모니터링을 위해 `agents/.env`에 다음 설정을 권장합니다.
```env
# 1. OpenTelemetry 기반의 Trace 및 Log 수집 활성화
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true

# 2. 보안상 기본적으로 숨겨지는 프롬프트 입력값 및 모델 응답값 캡처 허용
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

# 3. [리전 이슈 우회] Agent Engine은 us-central1에 배포하되, Gemini 3 모델은 global 엔드포인트에서 호출
GOOGLE_CLOUD_LOCATION=global
```

---

## 🤖 6. 테스트 시나리오

배포된 에이전트에게 다음과 같은 복합 과업을 지시해 보세요.
1. **SRE 장애 조사**: "결제 API의 500 에러 원인을 분석하고 조치 계획을 세워줘."
2. **아키텍처 설계**: "기존 DB를 Spanner로 옮기기 위한 3단계 전략을 짜고 검증해줘."
3. **자기 검증**: "보안 안내문을 작성하되 특정 키워드가 누락되면 다시 수정해줘."
