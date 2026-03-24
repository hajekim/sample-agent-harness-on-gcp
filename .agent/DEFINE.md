# Task Definition List (DEFINE)

## [Scaffolding]
- [ ] `mkdir -p prompts policies agents tools eval infra ci-cd`
- [ ] Create `pyproject.toml` with `google-adk` and `google-genai`
- [ ] Create initial `README.md`

## [Agents]
- [ ] Implement `agents/harness.py` with `ThinkingConfig` and `safety_settings`
- [ ] Implement `agents/agent.py` using `adk` primitives
- [ ] Implement `agents/worker.py` (Subagent example)
- [ ] Implement `agents/ralph_loop.py` for persistence logic

## [Tools]
- [ ] Create `tools/mcp_client.py`
- [ ] Implement a sample `tools/policy_engine.py` (Interception Layer)

## [Infrastructure]
- [ ] Basic `infra/main.tf` for Agent Engine
- [ ] `ci-cd/cloudbuild.yaml` template

## [Documentation]
- [ ] Complete `README.md` with diagram (mermaid) and guide link
