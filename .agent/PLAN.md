# Project Execution Plan - Enterprise AI Harness Sample

## Goals
- [x] "Google AI 에이전트 아키텍처" 가이드를 실제 작동하는 코드 구조로 구현
- [x] GitHub에 즉시 업로드 가능한 수준의 문서화 및 코드 완성도 확보
- [x] ADK 및 Agent Engine 배포 프로세스 포함

## Phases

### Phase 1: Scaffolding & Environment Setup
- [x] 1.1. 가이드에 정의된 표준 디렉토리 구조 생성
- [x] 1.2. `pyproject.toml` 환경 설정 (google-adk, google-genai 등 의존성 정의)
- [x] 1.3. 기본 `README.md` 작성 (아키텍처 개요 및 시작 방법)

### Phase 2: Core Agent Harness (Pro-code)
- [x] 2.1. `agents/harness.py`: Gemini 3 + google-genai 기반 베이스 하네스 구현
- [x] 2.2. `agents/agent.py`: ADK `SequentialAgent` 기반 오케스트레이터 정의
- [x] 2.3. `prompts/`: 시스템 인스트럭션 및 정책 템플릿 작성

### Phase 3: Tools & Integration (MCP)
- [x] 3.1. `tools/`: MCP 클라이언트 연동 및 커스텀 툴 래퍼 구현
- [x] 3.2. SRE Interception Layer (Policy Engine) 예시 구현

### Phase 4: Autonomous Loop & Memory (Ralph Loop)
- [x] 4.1. `agents/ralph_loop.py`: 상태 영속성 및 ZDR(무중단 복원력) 로직 구현
- [x] 4.2. Memory Bank (Managed Topics) 연동 코드 추가

### Phase 5: Deployment & CI/CD
- [x] 5.1. `infra/`: Agent Engine 배포를 위한 Terraform 코드 스켈레톤
- [x] 5.2. `ci-cd/`: 자동 평가 및 배포를 위한 Cloud Build 설정

---
**Status**: Completed 🚀
