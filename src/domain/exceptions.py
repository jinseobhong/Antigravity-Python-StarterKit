"""
src/domain/exceptions.py — 애플리케이션 최상위 및 도메인 베이스 예외 계층
"""


class AppError(Exception):
    """애플리케이션 시스템 최상위 베이스 예외 (All errors inherit from this)"""
    pass


class DomainError(AppError):
    """도메인 비즈니스 규칙 위반 시 발생하는 베이스 예외"""
    pass


class EntityValidationError(DomainError):
    """도메인 엔티티 속성 검증 실패 시 발생"""
    pass
