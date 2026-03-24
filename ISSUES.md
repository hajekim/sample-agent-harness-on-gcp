# Known Issues & Roadmaps

본 프로젝트를 구현하고 배포하는 과정에서 확인된 주요 이슈와 해결 방안, 그리고 향후 로드맵을 기록합니다.

## 1. Agent Engine과 Gemini 3 모델 간의 리전(Region) 충돌 이슈

### 🚨 이슈 현상 (Issue Description)
Vertex AI Agent Engine(Reasoning Engine)을 특정 리전(예: `us-central1`)에 배포한 후, ADK 내에서 **Gemini 3 Preview 계열 모델 (`gemini-3-pro-preview`, `gemini-3-flash-preview`)**을 호출할 때 다음과 같은 `404 NOT_FOUND` 에러가 발생합니다.

```text
ERROR: Error during async stream generation: 404 NOT_FOUND. 
Publisher Model `projects/[PROJECT_NUMBER]/locations/us-central1/publishers/google/models/gemini-3-pro-preview` was not found...
```

### 🔍 원인 분석 (Root Cause)
1. **단일 환경 변수 의존성**: ADK 및 `google-genai` SDK는 현재 모델 호출 엔드포인트를 결정할 때 `GOOGLE_CLOUD_LOCATION` 단일 환경 변수만 참조합니다.
2. **Gemini 3 Global 전용 정책**: Gemini 3 Preview 모델들은 현재 `global` 엔드포인트에서만 서비스되고 있습니다.
3. **Agent Engine 배포 제약**: Agent Engine 인프라 및 Memory Bank는 `global` 리전 배포를 지원하지 않으며, 반드시 `us-central1`, `europe-west4` 등 물리적 리전을 지정해야 합니다.
4. **ADK 객체 주입 제약**: 이를 우회하기 위해 `genai.Client(location="global")` 클라이언트를 별도로 생성하여 ADK `Agent` 객체에 주입(`api_client`)하려 시도했으나, 현재 ADK(v1.27.3)의 내부 Pydantic 검증 로직에서 이를 허용하지 않아(`Extra inputs are not permitted`) 배포가 차단됩니다.

### 💥 영향 (Impact)
* 현재 구조에서는 완전한 엔터프라이즈 보안(Vertex AI 모드, VPC-SC)을 유지한 상태로, `us-central1`에 배포된 Agent Engine 위에서 `global` 전용인 Gemini 3 Preview 모델을 네이티브하게 호출할 수 없습니다.

### 🛡️ 현재 프로젝트의 해결책 (Current Workaround)
* 본 샘플 코드(`agents/agent.py`, `agents/harness.py`)는 `us-central1` 리전에서 가장 안정적으로 서비스되는 **`gemini-2.5-pro`** 및 **`gemini-2.5-flash`** 모델을 기본값으로 사용하도록 하드코딩되어 있습니다. 이를 통해 다운로드 즉시 에러 없이 배포 및 작동(Out-of-the-box)을 보장합니다.

### 🛣️ 향후 로드맵 (Roadmap)
Google 내부적으로 해당 이슈에 대한 논의(YAQS 등)가 활발히 진행 중이며, 다음과 같은 업데이트가 예정되어 있습니다.

1. **단기 로드맵 (SDK 업데이트)**:
   * ADK `Agent` 클래스 스키마 업데이트를 통해 커스텀 `api_client`의 명시적 주입 허용.
   * `google-genai` SDK에서 `GOOGLE_GENAI_LOCATION`과 같은 독립적인 환경 변수를 도입하여 인프라 리전과 모델 리전을 분리.
2. **중장기 로드맵 (Agent Engine 업데이트)**:
   * Agent Engine 런타임 자체에서 지능형 크로스 리전(Cross-Region) 라우팅을 지원. 즉, 코드가 `us-central1`에 있더라도 모델이 `global` 전용인 경우 내부 프록시가 자동으로 `global` 엔드포인트로 요청을 라우팅.

### 💡 대안책: Developer API 모드 사용 (권장하지 않음)
만약 보안 요건(VPC-SC)이 엄격하지 않은 환경에서 반드시 Gemini 3를 사용해야 한다면, `.env` 파일의 설정을 다음과 같이 변경하여 Vertex AI 모드를 끄고 Developer API(AI Studio) 모드를 사용할 수 있습니다.
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="your-ai-studio-api-key"
```
이 경우 지역(Location) 제약을 받지 않는 Global 퍼블릭 엔드포인트를 타게 되어 Gemini 3 호출이 가능해집니다.
