terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 7.0"
    }
  }
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

resource "google_vertex_ai_reasoning_engine" "agent_engine" {
  provider     = google-beta
  display_name = "enterprise-harness-agent"
  region       = var.region

  spec {
    agent_framework = "google-adk"

    source_code_spec {
      inline_source {
        source_archive = filebase64("${path.module}/source.tar.gz")
      }
      python_spec {
        # Agent Engine 파이썬 런타임 최적화 (ADK 래퍼와 호환성 보장)
        version           = "3.13"
        # ADK CLI가 동적으로 생성하는 웹 서버 엔드포인트 명시
        entrypoint_module = "agents.agent_engine_app"
        entrypoint_object = "adk_app"
        requirements_file = "requirements.txt"
      }
    }
    
    deployment_spec {
      env {
        # ZDR 및 모델 하네스: 인프라와 무관하게 Gemini 3의 글로벌 엔드포인트를 타도록 강제
        name  = "GOOGLE_CLOUD_LOCATION"
        value = "global"  
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      # 엔터프라이즈 모니터링 (Trace/Logs) 활성화
      env {
        name  = "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY"
        value = "true"
      }
      env {
        name  = "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"
        value = "true"
      }
    }
  }
}

variable "project_id" {
  type        = string
  description = "GCP 프로젝트 ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "에이전트 엔진 컨테이너 배포 리전"
}
