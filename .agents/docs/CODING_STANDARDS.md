# CODING_STANDARDS.md — 파이썬 코딩 표준 및 엔지니어링 구현 규격서

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | SPEC-CODE-001 |
| **표준 버전** | 1.0.0 (Strict Typing & Pure Domain Edition) |
| **적용 범위** | src/, 	ests/, 파이썬 스크립트 및 모든 프로덕션 코드 |
| **상태** | ENFORCED (상시 강제 적용) |
| **최종 개정일** | 2026-09-02 |

---

## 📌 1. 목적 및 철학 (Purpose & Philosophy)

본 규격서는 Antigravity 아키텍처 환경에서 개발되는 모든 파이썬 코드의 **결함 원천 배제**, **타입 안전성 보장**, **Clean Architecture 계층 간 결합도 최소화** 및 **자동화된 입증(AI Proof) 가능성 극대화**를 위한 7대 코딩 표준을 확립한다.

---

## 🏛️ 2. 파이썬 7대 핵심 코딩 규약 (7 Core Coding Standards)

### 2.1 엄격한 정적 타입 힌트 (Strict Static Typing - PEP 484/585/604)
1. **타입 어노테이션 누락 금지**: 모든 함수/메서드의 인자(Arguments)와 반환값(Return Types)에 명시적인 타입 어노테이션을 **MUST** 적용한다.
2. **Any 타입 원천 배제**: 	yping.Any의 사용을 원칙적으로 금지하며, 제네릭(TypeVar), 유니온(T | None), 프로토콜(	yping.Protocol)을 통해 타입을 엄밀히 한정한다.
3. **모던 파이썬 유니온 문법 준수**: Optional[T] 대신 T | None, Union[A, B] 대신 A | B를 사용한다.

`python
# [GOOD] 엄격한 타입 정의
def calculate_pressure_delta(
    current_pressure: float,
    action_weight: float,
    decay_rate: float = 0.05
) -> float:
    return max(0.0, current_pressure + action_weight - decay_rate)
`

---

### 2.2 도메인 순수성 및 불변성 (Pure Domain & Immutability)
1. **외부 프레임워크 의존성 0**: src/domain/ 내부의 모든 엔티티(Entities)와 값 객체(Value Objects)는 외부 DB, HTTP, OS 관련 서드파티 라이브러리를 일체 임포트하지 아니한다.
2. **불변 값 객체 패턴**: 도메인 상태를 표현하는 객체는 @dataclass(frozen=True)로 선언하여 부수 효과(Side-Effect)를 원천 차단한다. 상태 변경 시 기존 인스턴스를 변형하지 않고 새로운 인스턴스를 반환한다.

`python
# [GOOD] 불변 도메인 모델
from dataclasses import dataclass

@dataclass(frozen=True)
class SomaticGene:
    gene_id: str
    expression_level: float
    is_active: bool = True

    def evolve(self, delta: float) -> "SomaticGene":
        new_level = max(0.0, min(1.0, self.expression_level + delta))
        return SomaticGene(
            gene_id=self.gene_id,
            expression_level=new_level,
            is_active=self.is_active
        )
`

---

### 2.3 계층별 명시적 커스텀 예외 (Explicit Custom Exceptions)
1. **날것의 예외 발생 금지**: 코드 내부에서 범용 Exception, KeyError, ValueError를 직접 aise하는 행위를 금지한다.
2. **도메인 예외 계층 구조 준수**: 모든 예외는 시스템 최상위 베이스 예외 및 도메인 전용 베이스 예외를 상속한다.

`python
class AbyssEmpireError(Exception):
    """시스템 최상위 기본 예외"""
    pass

class DomainError(AbyssEmpireError):
    """도메인 비즈니스 규칙 위반 베이스 예외"""
    pass

class InvalidGeneExpressionError(DomainError):
    """유전자 발현 수치가 허용 범위를 벗어났을 때 발생"""
    def __init__(self, gene_id: str, value: float):
        super().__init__(f"Gene '{gene_id}' expression level {value} is out of bounds [0.0, 1.0].")
`

---

### 2.4 Arrange-Act-Assert (AAA) 테스트 패턴 및 100% 실측
1. **AAA 구조 분리**: 모든 단위 테스트(	ests/unit/)는 **준비(Arrange)**, **실행(Act)**, **단언(Assert)** 3개 블록으로 명확히 구분하여 작성한다.
2. **결정론적 테스트**: 테스트는 네트워크, 실측 시간 등에 의존하지 않는 순수 결정론적(Deterministic) 함수여야 한다.

`python
def test_somatic_gene_evolution_caps_at_maximum():
    # Arrange (준비)
    initial_gene = SomaticGene(gene_id="GENE_001", expression_level=0.95)
    delta = 0.10

    # Act (실행)
    evolved_gene = initial_gene.evolve(delta)

    # Assert (단언)
    assert evolved_gene.expression_level == 1.0
    assert evolved_gene.gene_id == "GENE_001"
`

---

### 2.5 클린 아키텍처 의존성 역전 (Dependency Inversion)
1. **의존성 방향 단방향 강제**:
   - Presentation ➔ Application ➔ Domain
   - Infrastructure ➔ Domain / Application (인터페이스 구현)
2. **도메인 계층의 독립성**: 도메인은 하위 계층(DB, LLM 클라이언트, 웹 프레임워크)의 존재를 일체 알지 못하며, 인터페이스(Protocol/ABC)를 통해 협력한다.

---

### 2.6 표준 Google-Style Docstring 의무화
공개 모듈, 클래스, 함수에는 목적, 매개변수, 반환값, 발생 가능한 예외를 명시하는 Google Style Docstring을 작성한다:

`python
def render_narrative_prompt(
    character_name: str,
    stage_level: int
) -> str:
    """캐릭터 상태에 기반하여 렌더링된 LLM 프롬프트 문자열을 생성한다.

    Args:
        character_name: 대상 캐릭터 식별자.
        stage_level: 현재 텐션 압력 스테이지 레벨 (1~5).

    Returns:
        최종 조립된 완성형 프롬프트 텍스트.

    Raises:
        InvalidStageLevelError: stage_level이 1 미만 또는 5 초과인 경우.
    """
`

---

### 2.7 포매팅, 린팅 및 코드 위생 (Formatting & Hygiene)
1. **라인 길이**: 100자 기준으로 엄격히 제한한다.
2. **와일드카드 임포트 금지**: rom module import *는 전면 금지하며, 사용할 심볼을 명시적으로 임포트한다.
3. **태만 생략(Lazy Truncation) 전면 금지**: // TODO, ... (기존 코드 동일) 등의 불완전 코드는 일체 허용하지 않는다.
