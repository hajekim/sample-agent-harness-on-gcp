# Terraform 스켈레톤: Vertex AI Agent Engine 배포

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_vertex_ai_reasoning_engine" "agent_engine" {
  display_name = "enterprise-harness-agent"
  location     = var.region

  spec {
    package_spec {
      # ADK 에이전트 패키지 경로
      pickle_object_gcs_uri = "gs://${var.bucket_name}/agents/agent.pkl"
    }
  }
}

variable "project_id" { type = string }
variable "region"     { type = string default = "us-central1" }
variable "bucket_name" { type = string }
