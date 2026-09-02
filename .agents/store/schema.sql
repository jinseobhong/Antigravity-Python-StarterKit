-- ====================================================================
-- Antigravity-Common-Core: SQLite Store Schema (state.db)
-- 경량화된 AI 아키텍트 거버넌스 및 개발 이력 관리용 스키마
-- ====================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. 작업 주기 및 상태 추적 테이블 (Tasks)
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    current_phase TEXT NOT NULL, -- Understand, Plan, Execute, Completed, Blocked
    implementation_auth TEXT NOT NULL DEFAULT 'PENDING', -- PENDING, APPROVED
    proof_status TEXT NOT NULL DEFAULT 'UNPROVEN', -- UNPROVEN, PARTIALLY_PROVEN, PROVEN
    decision_status TEXT NOT NULL DEFAULT 'IN_PROGRESS', -- IN_PROGRESS, FINAL_ACCEPTED, REWORK_REQUIRED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 전체 컴포넌트 구현 현황도 (Component Status Map)
CREATE TABLE IF NOT EXISTS component_status (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_name TEXT NOT NULL UNIQUE,
    module_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'TODO', -- TODO, WIP, DONE, DEPRECATED
    description TEXT,
    last_verified_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. AI 입증 및 테스트 실행 로그 (Verification Logs)
CREATE TABLE IF NOT EXISTS verification_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    command TEXT NOT NULL,
    exit_code INTEGER NOT NULL,
    raw_log TEXT NOT NULL,
    proof_grade TEXT NOT NULL, -- PROVEN, PARTIALLY_PROVEN, UNPROVEN
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

-- 4. 5W1H 예외 처리 및 사용자 결정 로그 (Decision Overrides)
CREATE TABLE IF NOT EXISTS decision_overrides (
    override_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    who_decided TEXT NOT NULL,
    when_decided TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    where_affected TEXT NOT NULL,
    what_skipped TEXT NOT NULL,
    why_skipped TEXT NOT NULL,
    how_handled TEXT NOT NULL,
    user_confirmed INTEGER DEFAULT 1,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL
);

-- 5. 에이전트 스킬 및 규칙 변경 이력 (Agent Asset Mutations)
CREATE TABLE IF NOT EXISTS agent_asset_mutations (
    mutation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_path TEXT NOT NULL,
    change_type TEXT NOT NULL, -- 'CREATE', 'UPDATE', 'DELETE'
    approval_keyword TEXT NOT NULL, -- 'APPROVE', '승인', etc.
    diff_summary TEXT NOT NULL,
    patch_content TEXT,
    applied_by TEXT DEFAULT 'AI_AGENT', -- 'AI_AGENT', 'USER'
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 에이전트 런타임 세션 스냅샷 (Agent Session Snapshots)
CREATE TABLE IF NOT EXISTS agent_session_snapshots (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    active_track TEXT NOT NULL, -- 'Quick', 'Spike', 'Standard', 'Advisory'
    last_action TEXT,
    snapshot_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

