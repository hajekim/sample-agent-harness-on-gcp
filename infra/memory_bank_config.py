from vertexai.types import (
    ReasoningEngineContextSpecMemoryBankConfig as MemoryBankConfig,
    MemoryBankCustomizationConfig as CustomizationConfig,
    MemoryBankCustomizationConfigMemoryTopic as MemoryTopic,
    MemoryBankCustomizationConfigMemoryTopicManagedMemoryTopic as ManagedMemoryTopic,
    MemoryBankCustomizationConfigMemoryTopicCustomMemoryTopic as CustomMemoryTopic,
    ManagedTopicEnum,
    ReasoningEngineContextSpecMemoryBankConfigTtlConfig as TtlConfig
)

def get_enterprise_memory_bank_config() -> MemoryBankConfig:
    """
    가이드 8. Agent Engine 기능 활용 (Memory Bank)
    - USER_PERSONAL_INFO 등 Managed Topic과 커스텀 Topic으로 지식을 구조화하여 
      컨텍스트 오염을 방지하는 엔터프라이즈 메모리 뱅크 설정입니다.
    """
    
    # 1. 커스텀라이징 설정: 추출할 메모리의 주제(Topic)를 명시적으로 제한합니다.
    customization_config = CustomizationConfig(
        memory_topics=[
            # Managed Topic: 사용자 개인 정보 (이름, 선호도 등)
            MemoryTopic(
                managed_memory_topic=ManagedMemoryTopic(
                    managed_topic_enum=ManagedTopicEnum.USER_PERSONAL_INFO
                )
            ),
            # Managed Topic: 사용자 선호도
            MemoryTopic(
                managed_memory_topic=ManagedMemoryTopic(
                    managed_topic_enum=ManagedTopicEnum.USER_PREFERENCES
                )
            ),
            # Custom Topic: 조직 내 정책이나 결재 정보에 한정된 기억
            MemoryTopic(
                custom_memory_topic=CustomMemoryTopic(
                    label="enterprise_approval_rules",
                    description="특정 시스템 배포나 결재 라인에 대한 규칙이나 사용자 지정 예외 사항"
                )
            )
        ],
        # 에이전트가 3인칭(The user uses...)이 아닌 1인칭으로 기억하도록 설정 (기본값)
        enable_third_person_memories=False 
    )

    # 2. TTL (Time-To-Live) 설정: 오래된 정보 자동 삭제(보안/규정 준수)
    ttl_config = TtlConfig(
        default_ttl="2592000s"  # 30일 보관
    )

    # 3. 최종 Memory Bank 설정 조립
    memory_bank_config = MemoryBankConfig(
        customization_configs=[customization_config],
        ttl_config=ttl_config
    )
    
    return memory_bank_config

# 이 설정은 ADK AdkApp 배포 시 context_spec 인자로 전달됩니다.
# 예: agent_engine = client.agent_engines.create(..., config={"context_spec": {"memory_bank_config": get_enterprise_memory_bank_config()}})
