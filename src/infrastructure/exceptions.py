"""
src/infrastructure/exceptions.py — 인프라 계층 베이스 예외
"""

from src.domain.exceptions import AppError


class InfrastructureError(AppError):
    """인프라 및 영구 저장소 베이스 예외"""
    pass


class DatabaseConnectionError(InfrastructureError):
    """데이터베이스 연결 실패 시 발생"""
    pass


class EntityNotFoundError(InfrastructureError):
    """저장소에서 요청한 엔티티를 찾을 수 없을 때 발생"""
    def __init__(self, entity_name: str, entity_id: str) -> None:
        super().__init__(f"{entity_name} with ID '{entity_id}' not found in database.")
