# Sample Enterprise AI Agent Harness on Google Cloud

이 프로젝트는 **Google AI 에이전트 아키텍처 및 엔터프라이즈 개발 가이드** 를 기반으로 구축된 샘플 에이전트 시스템입니다. 조직 수준에서 확장 가능하고 안전한 AI 에이전트 운영을 위한 표준 구조와 코드 레벨의 구현 패턴을 제공합니다.

---

## 📖 1. 개요

이 프로젝트를 이해하기 위해 필요한 구글의 최신 엔터프라이즈 AI 아키텍처 핵심 개념입니다.

*   **Agent Engine 기반 아키텍처**: 에이전트를 컨테이너로 감싸 배포하고, 세션, Memory Bank, 평가, 보안(IAM/VPC-SC)을 통제하는 완전 관리형 런타임 환경입니다.
*   **ADK (Agent Development Kit)**: 복잡한 멀티 에이전트 로직을 코드로 짜기 위한 프레임워크입니다. Planner, Worker, Checker 등 역할을 분리한 에이전트들을 파이프라인이나 루프 형태로 엮을 수 있습니다.
*   **MCP (Model Context Protocol)**: 에이전트가 사내 데이터베이스나 외부 API와 통신하기 위한 표준 연동 규약입니다. 엔터프라이즈에서는 중앙 집중형 **Remote MCP (OneMCP)** 사용을 권장합니다.
*   **자율 오케스트레이션 (Ralph Loops)**: 사용자의 1회성 질문에 답하는 챗봇이 아니라, 에이전트가 상태(State)를 가지며 스스로 과업을 분해하고 완수할 때까지 무한 루프를 도는 패턴입니다.
*   **ZDR (Zero-Downtime Resilience)**: 시스템 다운이나 재배포 시에도 외부 저장소에 기록된 상태를 즉시 재구성(Rehydrate)하여 에이전트의 기억 상실 없이 작업을 이어가는 **무중단 복원력**입니다.

---

## 💡 2. 핵심 기술 컨셉

본 프로젝트의 아키텍처를 관통하는 두 가지 핵심 사상은 **하네스(Harness)** 와 **자율 루프(Ralph Loop)** 입니다.

### 2.1. 모델 하네스 (Model Harness)
엔터프라이즈 에이전트는 단순한 LLM 호출 코드가 아니라 모델을 감싸는 **소프트웨어 비계(Scaffolding)** 인 '하네스' 구조를 가져야 합니다.
- **역할**: 모델 추론 전후에 보안 정책(Policy) 적용, 도구(Tool) 실행, 세션 상태 보존, 입출력 스키마 강제 등을 수행하는 제어부 역할을 합니다.
- **장점**: 모델 파라미터나 프롬프트가 변경되어도 외부 시스템과의 연동 규격은 일정하게 유지되는 **인터페이스 격리** 효과를 제공합니다.

### 2.2. 자율 실행 루프 (Ralph Loop)
사용자가 일일이 "다음은 뭐 해?"라고 묻지 않아도, 에이전트가 스스로 목표 달성 여부를 판단하며 반복 실행하는 패턴입니다.
- **Iteration > Perfection**: 한 번의 완벽한 답변을 기대하기보다, `실행 → 결과 확인 → 실패 시 재시도` 사이클을 돌며 정답을 찾아갑니다.
- **Micro-task Focus**: 전체 목표를 아주 작은 단위의 작업(TODO)으로 쪼개어 하나씩 해결함으로써, 컨텍스트 윈도우가 넘치거나 모델이 길을 잃는 '컨텍스트 오염'을 원천적으로 방지합니다.
- **Persistence**: 모든 작업 진행 상황이 외부에 저장되므로, 인프라 장애 시에도 마지막 작업 시점부터 즉시 재개되는 무중단 복원력(ZDR)의 핵심 기반이 됩니다.

---

## 📁 3. 디렉토리 구조

```text
/ai-harness-gcp-sample/
├── prompts/             # 시스템 인스트럭션 및 정책 템플릿
├── policies/            # 안전 및 가드레일 정책
├── agents/              # ADK 기반 에이전트 로직 (Ralph Loop, Harness)
├── tools/               # MCP 연동, Policy Engine, Grounding 툴
├── eval/                # LLM-as-a-judge 자동 평가 스크립트
├── infra/               # Terraform 및 Memory Bank 설정
├── ci-cd/               # Cloud Build 기반 CI/CD 파이프라인
├── pyproject.toml       # 의존성 관리
├── README.md            # 본 가이드 문서
└── ISSUES.md            # 리전 충돌 이슈 및 로드맵 문서
```

---

## 🏛️ 4. 아키텍처 및 코드 상세 설명

본 프로젝트는 다음과 같은 계층(Layer) 구조로 설계 및 코딩되었습니다.

### 4.1. Orchestration Layer (`agents/agent.py`)
에이전트의 두뇌와 작업 흐름을 제어합니다.
*   **하이브리드 오케스트레이션**: `Planner`(작업 분해) → `Worker`(작업 수행) → `Checker`(품질 검증)로 이어지는 `SequentialAgent` 파이프라인을 구축했습니다.
*   **Ralph Loop & Guardrails**: 이 파이프라인을 다시 `LoopAgent`로 감싸 자율 실행 루프를 만들었습니다. 무한 루프 방지를 위해 `max_iterations=10` 제한을 두었으며, `Checker` 에이전트가 품질 미달 시 `escalate` 도구를 호출해 강제 종료하는 **가드레일(Guardrails)** 패턴을 구현했습니다.

### 4.2. Harness Layer (`agents/harness.py`)
`google-genai` SDK를 활용하여 모델 추론을 추상화합니다.
*   **Thinking & Safety**: 모델 호출 시 `ThinkingConfig(MEDIUM)`을 통해 추론 깊이를 제어하고, `safety_settings`를 적용해 엔터프라이즈 환경의 혐오/위험 콘텐츠를 차단합니다.
*   **Structured Output**: Pydantic 스키마(`AgentResponse`)를 `response_schema`에 강제하여 항상 안정적인 JSON을 반환하도록 설계되었습니다.

### 4.3. Tooling & Security Layer (`tools/`)
에이전트가 세상을 조작하는 손과 발입니다.
*   `mcp_client.py`: 사내 서비스와의 안전한 연동을 위해 로컬 방식이 아닌 **Remote MCP (SSE Client)** 연동 뼈대를 제공합니다.
*   `policy_engine.py`: 에이전트가 파괴적인 명령(예: `rm -rf`, `drop table`)을 실행하기 전, 문법과 권한을 검증하는 **SRE Interception Layer** 데코레이터 패턴입니다.
*   `grounding.py`: 환각(Hallucination) 방지를 위해 Vertex AI Search / RAG Engine을 찔러 사내 문서를 검색하는 그라운딩(Grounding) 래퍼입니다.

### 4.4. Persistence & Memory (`infra/memory_bank_config.py`, `agents/ralph_loop.py`)
*   `RalphLoopManager`: 로컬/GCS 파일 시스템에 상태를 지속적으로 기록하여 **ZDR(무중단 복원력)** 을 보장합니다.
*   `memory_bank_config.py`: Agent Engine 배포 시 `USER_PERSONAL_INFO`, `USER_PREFERENCES` 등의 **Managed Topic**을 설정하여 컨텍스트 오염 없이 장기 기억을 구조화하는 Terraform 연동 코드입니다.

---

## 🚀 5. 배포 및 실행 (Getting Started)

### 5.1. 환경 설정 및 종속성 설치
```bash
# 가상 환경 생성 및 진입
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -e .

# Google Cloud 환경 변수 설정 (개인 프로젝트 ID로 변경)
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### 5.2. Agent Engine 배포
ADK CLI를 활용하여 Vertex AI Agent Engine에 서버리스 형태로 배포합니다.
```bash
adk deploy agent_engine agents \
  --project $GOOGLE_CLOUD_PROJECT \
  --region $GOOGLE_CLOUD_LOCATION \
  --display_name "enterprise-harness-agent" \
  --validate-agent-import
```

![](img/img-00.png)

---

## 🔍 6. Observability
### 6.1 Telemetry Collection 설정

엔터프라이즈 환경에서는 에이전트가 어떤 프롬프트를 받았고 어떤 사고 과정을 거쳤는지 **Cloud Trace 및 Cloud Logging**에 남기는 것이 필수적입니다. Agent Engine 배포 전, `agents/.env` 파일에 아래 두 가지 환경 변수를 반드시 세팅해야 Telemetry 옵션이 활성화됩니다.

```env
# 1. OpenTelemetry 기반의 Trace 및 Log 수집 활성화
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true

# 2. 보안상 기본적으로 숨겨지는 프롬프트 입력값 및 모델 응답값 캡처 허용
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```
*(주의: 본 프로젝트에는 `.env.example`이 제공됩니다. 복사하여 `agents/.env`로 구성하세요.)*

---

## 🤖 7. 에이전트 시나리오 및 테스트 프롬프트

본 배포된 에이전트(`enterprise_ralph_loop`)는 단순한 질의응답(Q&A) 챗봇이 아닙니다. **"복잡한 목표를 스스로 쪼개고 검증하며 완수하는 자율 오케스트레이터"** 역할을 수행합니다.

에이전트가 성공적으로 배포되었다면, 아래의 프롬프트들을 입력하여 **Planner → Worker → Checker**로 이어지는 컴파운딩 루프를 직접 테스트해 보세요.

![](img/img-01.png)

### 시나리오 A: SRE 장애 조사 (자동화된 문제 해결)
> "최근 결제 API(Payment API)에서 500 내부 서버 에러가 급증하고 있다는 알람이 발생했어. 이 문제를 해결하기 위해 어떤 지표를 확인해야 하는지, 그리고 임시 조치(Mitigation)부터 근본 원인 파악까지의 전체 조사 과정을 수행해 줘."
*   **관전 포인트**: Planner가 조사 단계를 나누고, Worker가 각 단계의 해결책을 추론하며, Checker가 계획이 완수되었는지 검증할 때까지 루프를 돕니다. 도구 호출 시 파괴적 명령이 섞여 있다면 `Policy Engine`이 이를 인터셉트(차단)합니다.

### 시나리오 B: 엔터프라이즈 아키텍처 플래닝
> "현재 온프레미스에 있는 레거시 모놀리식 데이터베이스를 Google Cloud Spanner로 마이그레이션하려고 해. 다운타임을 최소화하기 위한 마이그레이션 전략을 3단계로 나누어 세우고 검증해 줘."
*   **관전 포인트**: 매우 거대한 목표를 받았을 때, 에이전트가 어떻게 마이크로 태스크 단위로 쪼개어 단계별로 실행하고 결과물을 취합하는지 관찰합니다.

### 시나리오 C: 자기 검증(Self-Correction) 및 가드레일 테스트
> "엔터프라이즈 AI 보안 가이드라인에 대한 짧은 안내문을 작성해줘. 단, 반드시 '환각 방지', '데이터 암호화', '접근 통제' 이 3가지 키워드가 모두 포함되어야 해. 만약 하나라도 빠졌다면 다시 작성해."
*   **관전 포인트**: Worker가 초안을 작성하면, Checker 에이전트가 3가지 키워드가 모두 있는지 평가합니다. 누락되었다면 Checker가 루프 종료를 거부하고, Worker에게 다시 작성하도록 지시하는 **'무한 루프 방지 및 검증(Guardrail)'** 사이클을 확인할 수 있습니다.
