from google import genai
from google.genai import types
from pydantic import BaseModel
import os

# 1. 응답 구조 정의 (Pydantic)
class AgentResponse(BaseModel):
    analysis: str
    thought_process: str
    next_steps: list[str]
    confidence_score: float

# 2. 모델 하네스 클래스
class ModelHarness:
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        self.client = genai.Client(
            vertexai=True,
            project=project_id or os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=location,
        )
        # Note: us-central1 리전의 안정적인 API 지원을 위해 2.5-flash를 사용합니다.
        self.model_id = "gemini-2.5-flash"

    def generate(self, prompt: str, system_instruction: str = None) -> AgentResponse:
        """구조화된 추론 수행"""
        
        resp = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=AgentResponse,
                # 엔터프라이즈 안전 설정
                safety_settings=[
                    types.SafetySetting(
                        category='HARM_CATEGORY_HATE_SPEECH',
                        threshold='BLOCK_ONLY_HIGH',
                    ),
                    types.SafetySetting(
                        category='HARM_CATEGORY_DANGEROUS_CONTENT',
                        threshold='BLOCK_ONLY_HIGH',
                    )
                ]
            ),
        )
        return resp.parsed

if __name__ == "__main__":
    # 간단한 테스트 실행
    harness = ModelHarness()
    result = harness.generate(
        prompt="Analyze the potential risks of deploying a new agent to production.",
        system_instruction="You are a Senior SRE and Security Architect."
    )
    print(f"Analysis: {result.analysis}")
    print(f"Next Steps: {result.next_steps}")
