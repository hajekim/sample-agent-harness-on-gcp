# Project Context: ai-harness-gcp-sample

## Project Overview
이 프로젝트는 "Google AI 에이전트 아키텍처 및 엔터프라이즈 개발 가이드"를 기반으로 한 엔터프라이즈급 AI 에이전트 하네스 구현 샘플입니다. 조직 레벨에서 확장 가능한 에이전트 시스템을 구축하고, Vertex AI Agent Engine에 배포 가능한 구조를 지향합니다.

## Tech Stack
- **Language**: Python (>= 3.10)
- **AI Models**: Gemini 3 Flash / Pro
- **SDK**: Google Gen AI SDK (google-genai)
- **Framework**: Agent Development Kit (ADK)
- **Infrastructure**: Vertex AI Agent Engine, Terraform, Cloud Build
- **Protocol**: Model Context Protocol (MCP)

## Directory Structure
- `prompts/`: 프롬프트 템플릿 (YAML, text)
- `policies/`: 안전, 톤앤매너 등 정책 정의
- `agents/`: ADK 기반 에이전트 로직 및 Ralph Loop 오케스트레이션
- `tools/`: 공통 도구 정의 및 MCP 서버 연동 설정
- `eval/`: 평가용 골든 데이터셋 및 설정
- `infra/`: Terraform 기반 인프라 정의 (Agent Engine, IAM)
- `ci-cd/`: Cloud Build 기반 CI/CD 파이프라인

## Core Logic
1. **Model Harness**: `google-genai`를 이용한 추론 추상화.
2. **Autonomous Loop (Ralph Loop)**: 상태 기반 자율 작업 완수 루프.
3. **Compounding**: 평가 피드백을 통한 지속적 성능 개선.
4. **ZDR (Zero-Downtime Resilience)**: 상태 재구성(Rehydrate)을 통한 복원력.

## Coding Conventions
- **Clean Code**: SRP(Single Responsibility Principle) 준수.
- **Surgical Patching**: `.agent` 도구를 이용한 최소 단위 수정.
- **Type Hinting**: 모든 Python 함수에 타입 힌트 필수 적용.
- **Async First**: 대규모 처리를 위한 비동기(asyncio) 패턴 권장.
