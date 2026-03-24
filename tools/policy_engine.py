import re

class PolicyEngine:
    """SRE Interception Layer: 도구 호출 전 권한 및 정책 검증"""
    
    def __init__(self):
        # 파괴적인 명령 리스트 (예시)
        self.forbidden_patterns = [
            r"rm -rf",
            r"delete cluster",
            r"drop table",
            r"shutdown"
        ]

    def validate_command(self, command: str) -> bool:
        """명령어가 안전한지 검증"""
        for pattern in self.forbidden_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                print(f"⚠️ Policy Violation Detected: {command}")
                return False
        return True

    def interception_wrapper(self, func):
        """데코레이터 형태의 인터셉션 레이어"""
        def wrapper(*args, **kwargs):
            command = kwargs.get('command') or args[0]
            if self.validate_command(command):
                return func(*args, **kwargs)
            else:
                raise PermissionError("Policy Engine에 의해 차단된 작업입니다.")
        return wrapper

# 글로벌 정책 엔진 인스턴스
global_policy = PolicyEngine()
