"""
src/domain/exceptions.py — AbyssEmpire 도메인 커스텀 예외 계층

Clean Architecture Domain Layer에 위치하며, 비즈니스 규칙 위반 시 발생하는
명시적 예외 클래스들을 정의한다.
"""

class AbyssEmpireError(Exception):
    """AbyssEmpire 시스템 최상위 베이스 예외"""
    pass

class DomainError(AbyssEmpireError):
    """도메인 비즈니스 규칙 위반 베이스 예외"""
    pass

class InvalidGeneValueError(DomainError):
    """유전자 발현도 또는 가중치가 허용 수치 범위를 벗어났을 때 발생"""
    def __init__(self, gene_id: str, value: float, min_val: float = 0.0, max_val: float = 1.0) -> None:
        super().__init__(
            f"Gene '{gene_id}' value {value} is out of valid range [{min_val}, {max_val}]."
        )

class InvalidPressureStageError(DomainError):
    """텐션 압력 스테이지 단계가 유효하지 않을 때 발생"""
    def __init__(self, stage_val: int) -> None:
        super().__init__(f"Pressure stage value {stage_val} is invalid (must be 1 to 5).")

class InvalidTensorMatrixError(DomainError):
    """텐서 매트릭스 계수가 음수이거나 불능 상태일 때 발생"""
    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid Tensor Matrix: {message}")
