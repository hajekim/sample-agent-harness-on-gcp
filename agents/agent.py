from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import ToolContext

# 1. 에이전트별 인스트럭션 정의 (Ralph Loop 패턴)
PLANNER_INSTRUCTION = """
당신은 복잡한 작업을 분해하는 플래너 에이전트입니다.
사용자의 목표를 분석하고, 실행 가능한 마이크로 태스크 리스트를 작성하십시오.
결과는 state['plan']에 저장됩니다.
"""

WORKER_INSTRUCTION = """
당신은 배정된 태스크를 수행하는 워커 에이전트입니다.
state['plan']에 명시된 단일 태스크에 집중하여 처리하십시오.
도구(Remote MCP, RAG) 사용이 필요하면 적극적으로 호출하십시오.
결과는 state['execution_result']에 저장됩니다.
"""

CHECKER_INSTRUCTION = """
당신은 품질 관리 및 무한 루프 방지(Guardrail)를 담당하는 체커 에이전트입니다.
state['execution_result']의 품질을 평가하십시오.
목표가 달성되었거나 치명적인 오류가 발생한 경우, escalate 도구를 호출하여 루프를 중단합니다.
그렇지 않으면 다음 태스크 진행을 위해 plan을 갱신합니다.
"""

# 2. 도구 (에스컬레이션/루프 종료용 Guardrail Tool)
def escalate_issue(reason: str, tool_context: ToolContext) -> str:
    """작업이 완료되었거나 품질 기준 미달, 무한 루프 위험 시 호출하여 루프를 중단합니다."""
    tool_context.actions.escalate = True
    return f"Loop terminated by Checker. Reason: {reason}"

# 3. ADK 기반 에이전트 정의
planner = Agent(
    name="planner",
    model="gemini-3-pro-preview",
    instruction=PLANNER_INSTRUCTION,
    output_key="plan"
)

worker = Agent(
    name="worker",
    model="gemini-3-flash-preview",
    instruction=WORKER_INSTRUCTION,
    output_key="execution_result"
)

checker = Agent(
    name="checker",
    model="gemini-3-flash-preview",
    instruction=CHECKER_INSTRUCTION,
    tools=[escalate_issue]
)

# 4. 하이브리드 오케스트레이션 (Sequential Pipeline)
pipeline = SequentialAgent(
    name="enterprise_pipeline",
    description="플래닝 -> 실행 -> 검증의 마이크로 태스크 사이클",
    sub_agents=[planner, worker, checker]
)

# 5. 자율 오케스트레이션 (Ralph Loop with Guardrails)
ralph_loop = LoopAgent(
    name="enterprise_ralph_loop",
    description="무한 루프 방지 및 ZDR을 지원하는 자율 실행 루프",
    sub_agents=[pipeline],
    max_iterations=10, # 엔터프라이즈 비용 통제 Guardrail
)

# Agent Engine 배포를 위한 전역 변수 (ADK Entry Point)
root_agent = ralph_loop

if __name__ == "__main__":
    print("Ralph Loop (Orchestrator) initialized. Ready for Agent Engine deployment.")
