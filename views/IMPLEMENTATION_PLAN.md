# IMPLEMENTATION_PLAN.md — AbyssEmpire 웹 스튜디오 UI 컴포넌트 모듈화 및 원형 복원

| 항목 | 내용 |
| :--- | :--- |
| **문서 ID** | `PLAN-MODULAR-UI-001` |
| **문서 버전** | `v1.0.0` |
| **작성 일자** | `2026-09-02` |
| **상태** | `APPROVED (사용자 승인 완료)` |
| **작성자 / 승인자** | `AI Architect` / `Human Lead` |

---

## 📁 1. 변경 대상 파일 목록 (File Scope)

| 변경 구분 | 대상 파일 경로 | 변경 목적 및 구현 내용 |
| :---: | :--- | :--- |
| `[NEW]` | `src/presentation/web/static/css/style.css` | Glassmorphism, 네온 효과, 레이아웃 커스텀 스타일 분리 |
| `[NEW]` | `src/presentation/web/static/js/api.js` | Clean 4-Tier 백엔드 비동기 통신 클라이언트 모듈 |
| `[NEW]` | `src/presentation/web/static/js/views/lobby.js` | [View 1] 웅장한 메인 허브 및 액티브 캐릭터 스포트라이트 뷰 |
| `[NEW]` | `src/presentation/web/static/js/views/play.js` | [View 2] 1:1 서사 롤플레이 룸, 대화 이력 및 전술 선택지 뷰 |
| `[NEW]` | `src/presentation/web/static/js/views/vault.js` | [View 3] 캐릭터 보관소 그리드, 갑주 필터 및 검색 뷰 |
| `[NEW]` | `src/presentation/web/static/js/views/somatic.js` | 17대 생체 텐서, 압력 궤적, Kinematic Chain 실시간 게이지 뷰 |
| `[NEW]` | `src/presentation/web/static/js/components/modal.js` | 마스터 프롬프트, 단부루 태그, 캐릭터 수정 팝업 모달 |
| `[NEW]` | `src/presentation/web/static/js/app.js` | 메인 앱 부트스트랩 및 3대 뷰 라우팅 총괄 |
| `[NEW]` | `src/presentation/web/templates/index.html` | 3대 뷰 통합 베이스 HTML 템플릿 |
| `[MODIFY]` | `src/presentation/web/server.py` | 정적 에셋 서빙 및 Clean 4-Tier API 라우터 연동 |
| `[MODIFY]` | `views/IMPLEMENTATION_STATUS.md` | 현황 갱신 |
| `[MODIFY]` | `views/CURRENT_STATE.md` | 진행 좌표 및 상태 동기화 |

---

## 🛠️ 2. 단계별 구현 순서 (Execution Steps)

1. **[1단계: static/ 및 templates/ 모듈화 디렉토리 구축]**:
   - `style.css`, `api.js`, `views/` 4대 뷰 모듈, `components/` 컴포넌트 분할 작성.
2. **[2단계: templates/index.html 뼈대 및 모듈 결합]**:
   - 원형의 초호화 메인 로비, 롤플레이 룸, 캐릭터 스튜디오 레이아웃 통합.
3. **[3단계: server.py 정적 파일 서빙 및 API 연동 정밀화]**:
   - `/static/` 정적 파일 MIME 타입 완벽 지원 및 4계층 백엔드 API 연동.
4. **[4단계: 단위 테스트 및 실측 검증 (AI Proof)]**:
   - `tests/unit/` 전체 테스트 실행 및 31개 단위 테스트 100% Pass 확인.
5. **[5단계: Git 자동 푸시 및 사용자 인도]**:
   - `auto_push.py` 실행 및 가동 명령어 전달.

---

## 🧪 3. 검증 계획 (Verification Plan)
- **명령어**: `py -3 -m unittest discover -s tests/unit -v`
- **기준**: 전체 단위 테스트 100% Pass (0 errors) & 입증 등급 `PROVEN`
