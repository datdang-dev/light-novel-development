## 1. Architecture Evaluation

### 1.1 Extensibility (Khả năng mở rộng)

**Nhận định tổng quan**

LND Studio là một hệ thống agentic theo phong cách BMAD, trong đó:

- Orchestrator `Director K` được định nghĩa trong `studio/agents/lnd-orchestrator.agent.yaml`.
- Các specialist agents được định nghĩa trong `studio/agents/*.agent.yaml`.
- Pipeline chính `gooner-alchemist` được mô tả trong:
  - `.agent/workflows/gooner-alchemist.md`
  - `studio/services/gooner-alchemist/workflow.md`
  - Cùng với các capability workflows chuẩn BMAD trong `studio/workflows/capabilities/*` (panel-forensic, prose-adapter, gooner-audit, bible-sync).

**Thêm agent mới**

- Mẫu agent tương đối thống nhất và khai báo tốt:
  - `metadata`: id, name, title, icon, module, hasSidecar.
  - `persona`: role, identity, communication_style, principles.
  - `critical_actions`: các hành vi bắt buộc (đọc config, đọc docs, dùng tool).
  - `menu`: trigger → action (path tới workflow hoặc tool) + description.
- Ví dụ:
  - `studio/agents/lnd-orchestrator.agent.yaml`
  - `studio/agents/manga-adapter.agent.yaml`
  - `studio/agents/lewd-writer.agent.yaml`
  - `studio/agents/panel-forensic-analyst.agent.yaml`
- Về mặt cấu trúc, việc tạo thêm một agent mới khá dễ:
  - Chỉ cần tạo file `*.agent.yaml` theo schema trên.
  - Trỏ `menu[].action` tới một `workflow.md` hoặc script/tool tương ứng.

**Coupling ẩn / phụ thuộc ngầm**

Tuy nhiên, `critical_actions` của nhiều agent đang tạo ra phụ thuộc ngầm:

- Yêu cầu phải tồn tại các tài liệu/asset cụ thể:
  - `studio/docs/architecture/dynamic_design/service_manga_adapter/sq_v6_1_gooner_alchemist_pipeline.puml`
  - `studio/docs/protocols/delegation-protocol.md`
  - Các rule `.agent/rules/*.md`.
- Yêu cầu phải tồn tại tools/khả năng runtime:
  - Tool `sequential-thinking`.
  - Tool `view_file`.
  - Khả năng RAG đọc từ `studio/knowledge/` (“fetish-db”, “style-guides”).
  - “Hentai Lexicon database” cho Fetish scan.

Những phụ thuộc này hiện **không được khai báo trong một “capability manifest” máy-đọc-được**, mà chỉ ghi bằng chữ trong prompt, dẫn tới:

- Nếu môi trường runtime không có đủ tool, agent sẽ buộc phải “giả vờ” đã chạy tool hoặc hallucinate kết quả.
- Việc thêm agent/pipeline mới có thể dễ “chạy được”, nhưng không dễ bảo đảm tính đầy đủ/correctness của toàn hệ.

**Thêm pipeline mới**

- `Director K` hard-code toàn bộ menu pipeline trong `lnd-orchestrator.agent.yaml`:
  - `GA` → `{project-root}/studio/services/gooner-alchemist/workflow.md`
  - `RA` → `{project-root}/studio/services/renpy-adaptation/workflow.md`
  - `CC` → `{project-root}/studio/services/chapter-composer/workflow.md`
  - `CB` → `{project-root}/studio/services/character-builder/workflow.md`
  - `RG` → `{project-root}/studio/services/rpg-adapter/workflow.md`
  - `PT`, `PR` (party-mode, performance-review), v.v.
- Để thêm pipeline mới, hiện tại dev phải:
  - Tạo `studio/services/<pipeline>/workflow.md` hoặc tương đương.
  - Thêm entry vào `menu` của `Director K`.
- Không có một registry trung tâm kiểu YAML/CSV để Orchestrator load động danh sách pipeline/capability. Điều này tạo coupling chặt chiều ngược: orchestrator phải “biết” tất cả pipelines, thay vì pipelines tự khai báo và đăng ký.

**Coupling giữa spec và thực thi**

- `studio/services/gooner-alchemist/workflow.md` mô tả pipeline V6:
  - Bước 1: `step-01-initialize.md`.
  - Bước 1b: `step-01b-context-horizon.md` với tool `generate_horizon.py`.
  - Bước 3: gọi `studio/core/transformation-engine/workflow.md` làm “Core Transformation Engine”.
- Tuy nhiên, theo `Walkthrough.md`:
  - Step 1b đang bị “orphan” – control-flow thực tế không luôn invoke bước này.
  - `core/transformation-engine` mới chỉ có 1 bước implement, trong khi docs mô tả là full engine (Prose Generation → Quality Audit → Rewrite).
- Điều này thể hiện pattern quan trọng:
  - **Spec trong `workflow.md` không phải lúc nào cũng khớp hoàn toàn với control-flow thực tế trong step files.**
  - Khi bổ sung/đổi pipeline, dev phải chỉnh ở nhiều lớp (spec, step files, có thể cả `.agent/workflows`) → tăng rủi ro drift.

**Kết luận về extensibility**

- Điểm mạnh:
  - Mẫu agent rõ ràng, dễ nhân bản.
  - Pipeline và capability được chia nhỏ theo BMAD (step-file, capability vs pipeline).
- Điểm yếu:
  - Orchestrator hard-code nhiều pipeline → khó “plugin hóa”.
  - Nhiều phụ thuộc ngầm (tool, knowledge, module) chỉ được mô tả bằng ngôn ngữ tự nhiên.
  - Chưa có một layer contract/capability khai báo tập trung.

=> **Extensibility tốt ở lớp prompt/khai báo, nhưng còn thiếu một tầng “contract manifest” và registry trung tâm để mở rộng an toàn và ít drift khi số lượng agent/pipeline tăng.**

---

### 1.2 Maintainability (Khả năng bảo trì)

**State file-based: dễ debug nhưng dễ phình to & lệch chuẩn**

- Mô hình state được mô tả rõ trong `Walkthrough.md` và các workflow:
  - `_lnd-output/_pipeline/.../state.yaml` chứa trạng thái pipeline.
  - `_analysis`, `_prose`, `_bible`, `_forensics`, `_release` chứa artifacts từng giai đoạn.
  - Frontmatter `stepsCompleted` trong mỗi step file (chuẩn BMAD v6).
- Ưu điểm:
  - Dễ quan sát, dễ debug: chỉ cần xem filesystem để biết pipeline đang ở đâu, đã sinh ra artifact gì.
  - Phù hợp với “micro-file / JIT loading” của BMAD (mỗi lần chỉ load step hiện tại).
- Nhược điểm (đã được chính tác giả nêu trong `Walkthrough.md`):
  - Không có một validator tự động đảm bảo:
    - Tên file đúng pattern (ví dụ `page_003_forensics.md` vs `003_forensics.md` vs `page-003-forensics.md`).
    - Quan hệ 1:1 giữa page và output ở mỗi stage như rule `one_page_one_file.md` yêu cầu.
    - Directory conventions thống nhất (`_forensics` vs `_analysis`, `_prose` vs `_prose/_audit`, v.v.).
  - Nhầm lẫn nhỏ ở naming hoặc path dễ không bị phát hiện cho tới rất muộn trong pipeline.

**Tổ chức thư mục & nhiều lớp orchestration**

- `studio/README.md` mô tả kiến trúc chuẩn:

  - `studio/workflows/capabilities/`
    - `panel-forensic/`
    - `prose-adapter/`
    - `gooner-audit/`
    - `bible-sync/`
  - `studio/workflows/pipelines/gooner-alchemist/`
  - `studio/agents/`, `studio/knowledge/`, `studio/docs/`.

- Nhưng thực tế còn:
  - `studio/services/gooner-alchemist/` với workflow riêng.
  - `_bmad/` với `workflow.xml` chạy song song.
  - `studio/core/*` (VD: `transformation-engine`, `lewd-writer`).
- `Walkthrough.md` chỉ rõ:
  - Có “multiple orchestration engines in parallel”:
    - LND step-file workflows.
    - BMAD XML workflows.
    - Ad-hoc tool scripts trong `studio/services/*/tools` và `studio/tools`.
- Điều này làm tăng complexity bảo trì:
  - Khi đổi pipeline, dev phải kiểm tra ít nhất:
    - Spec trong `studio/services/.../workflow.md`.
    - BMAD workflows trong `studio/workflows/...`.
    - Các `.agent/workflows/*.md` tương ứng.
  - Nguy cơ “orchestration drift” là có thật (đã tồn tại với step 1b context horizon, transformation-engine).

**Separation of concerns: rõ ràng về mặt ý tưởng, chưa chặt về rule/policy**

- Phân tầng conceptual:
  - Orchestrator: `Director K`.
  - Specialist: Kana, Prof. Atomic, Suki, Riko, Aria, Luna, v.v.
  - Workflows:
    - Capabilities: panel-forensic, prose-adapter, gooner-audit, bible-sync.
    - Pipelines: gooner-alchemist, party-mode, chapter-composer, release-compiler.
  - Rules toàn cục: `.agent/rules/*.md` (VD `delegation_protocol.md`, `one_page_one_file.md`).
  - Lessons-learned / retrospective: `studio/docs/lessons-learned.md`.
- Vấn đề maintainability chính:
  - **Rule & policy bị trùng lặp và phân tán**:
    - Ngôn ngữ output, SFX, ZERO HALLUCINATION, sensory density, audit thresholds… xuất hiện ở nhiều nơi:
      - `studio/config/config.yaml`
      - `studio/README.md`
      - `studio/docs/lessons-learned.md`
      - `.agent/rules/*.md`
      - Prompt riêng của `lewd-writer`, `gooner-audit`.
  - Không có một “rule hierarchy” rõ ràng (file nào thắng khi có conflict).
  - Khi số agent/pipeline tăng, việc cập nhật policy (ví dụ đổi sensory target hay threshold audit) sẽ đòi hỏi sửa nhiều file → dễ sinh technical debt và policy drift.

**Kết luận về maintainability**

- Điểm mạnh:
  - Cấu trúc thư mục logic, chia capability vs pipeline, có docs kiến trúc rõ ràng.
  - State file-based và step-based giúp dễ debug/run lại từng đoạn.
- Điểm yếu:
  - Nhiều lớp orchestration song song (services, workflows, bmad core) → dễ drift.
  - Rule/policy phân tán, không có nguồn chân lý duy nhất.
  - Thiếu tool validator tự động cho contracts (tên file, path, schema state).

---

### 1.3 AI Cognitive Load (Góc nhìn từ LLM)

**Prompt phân tầng dày đặc → dễ bloat context window**

Hiện tại, để thực thi một pipeline, LLM có thể phải “thấy”:

- Agent prompt:
  - `persona.role`, `identity`, `communication_style`, `principles` – thường dài, giàu ẩn dụ (Đặc biệt Suki và Prof. Atomic).
  - `critical_actions` với nhiều yêu cầu “READ ARCHITECTURE”, “Load config”, “Load delegation protocol”, “READ Lewd Writing Mechanics”, “CONSULT lexicon”, v.v.
- Workflow prompt:
  - `studio/services/gooner-alchemist/workflow.md` – mô tả V6 pipeline, context horizon, core transformation engine.
  - `studio/workflows/capabilities/*/workflow.md` – cho panel-forensic, prose-adapter, gooner-audit, bible-sync.
- Global rules:
  - `.agent/rules/delegation_protocol.md`, `.agent/rules/one_page_one_file.md`, các rule khác.
- Lessons learned:
  - `studio/docs/lessons-learned.md` – file rất dài, chứa nhiều checklist & retrospective.

Nếu runtime thực sự tuân thủ tất cả `critical_actions` (“Always load and read ...”), mỗi lần gọi agent, context có thể bùng nổ lên hàng nghìn token, dễ:

- Vượt giới hạn context practical của model.
- Khi bị cắt context, các rule ở “đuôi” dễ bị drop → hành vi không còn deterministic.

**Context fragmentation vs repetition**

- BMAD “micro-file/JIT loading” giúp hạn chế việc load toàn bộ workflow cùng lúc.
- Nhưng các rule quan trọng lại xuất hiện:
  - Trong agent prompt.
  - Trong workflow.
  - Trong `.agent/rules`.
  - Trong `lessons-learned`.
- Kết quả:
  - Một số rule (như ZERO HALLUCINATION, ONE PAGE=ONE FILE) bị nhắc nhiều lần, nhưng không có “bản canon rút gọn”.
  - Khi nhiều phiên bản hơi khác nhau của cùng rule cùng tồn tại, LLM phải tự resolve conflict, tăng cognitive load.

**Instruction collision & xung đột chính sách gây nhiễu cho model**

Ví dụ điển hình:

- Hallucination vs Inference:
  - `lessons-learned.md`:
    - “ZERO HALLUCINATION PROTOCOL”.
    - “No Phantom Elements”.
  - `lewd-writer.agent.yaml`:
    - `INFERENCE PROTOCOL`: “you are authorized to INFER ... Never leave a scene dry.”
    - “Context overrides Raw Data - if forensic data contradicts the mood, trust the Context.”
  - Hai hướng dẫn này mâu thuẫn trên cùng trục: một bên cấm đoán fabrication, bên kia khuyến khích suy diễn + override forensic khi “mood” đòi hỏi.
- Language policy:
  - `config.yaml`: `document_output_language: "English"`.
  - `gooner-audit`, `bible-sync`, `lessons-learned`, `lewd-writer`: “ALWAYS speak in Vietnamese”, dialogue bắt buộc tiếng Việt, không kana/kanji, SFX Latin/romaji.
  - Nếu cả config + rules cùng trong context, model phải tự đoán rule nào ưu tiên.

**Đề xuất giảm cognitive load**

- Tạo một file **canon rule ngắn** (ví dụ `studio/rules/canon-short.md`):
  - 1–2 trang, tổng hợp:
    - Ngôn ngữ output (dialogue, narration).
    - SFX policy.
    - ZERO HALLUCINATION.
    - ONE PAGE = ONE FILE.
    - Audit thresholds.
    - Sensory density.
  - Mọi agent/workflow chỉ load file này, thay vì tham chiếu nhiều nguồn.
- Rút gọn persona:
  - Giữ 2–3 câu identity/role, 3–5 principles ngắn, bỏ bớt “lore” dài.
  - Chuyển “lore” vào `studio/knowledge/agent-lore/*.md` và chỉ dùng khi thật sự cần flavour.
- Chuẩn hóa `critical_actions`:
  - Thay vì bắt agent tự “READ ARCHITECTURE: ...” mỗi lần, tạo tool/tầng trung gian:
    - `load_architecture_summary(pipeline_id)` → trả về summary vài trăm token.
    - `load_policy_summary()` → trả về list rule quan trọng.
- Tách rule “dễ kích hoạt hallucination” như INFERENCE khỏi prompt thường xuyên:
  - Chỉ bật thông qua cờ/state cụ thể khi forensic/bible đánh dấu `[ALLOW_INFERENCE]`.

---

## 2. Prompt Engineering Evaluation

### 2.1 Chiến lược prompt & cấu trúc

**Phân vai và ranh giới tương đối rõ**

- Orchestrator:
  - `Director K` (LND Orchestrator) trong `lnd-orchestrator.agent.yaml`.
  - Có rule `delegation_protocol.md` định nghĩa rõ: **MUST NEVER** trực tiếp làm image analysis, prose writing, dialogue, character profiles, audit, world-building.
- Specialist:
  - Kana (`manga-adapter.agent.yaml`) – beeld/visual ingestion & context POC.
  - Prof. Atomic (`panel-forensic-analyst.agent.yaml`) – forensic panel-level.
  - Suki (`lewd-writer.agent.yaml`) – R18 prose.
  - Riko (`gooner-editor`/`gooner-audit`) – QA/audit.
  - Aria (`character-architect`), Luna (`world-weaver`), v.v.
- `ENTRY_POINTS.md` mô tả mapping `/panel-forensic`, `/prose-adapter`, `/gooner-audit`, `/bible-sync` tương ứng với capability workflows.

Đây là điểm rất mạnh: **role boundaries rõ, delegation được thiết kế có chủ đích.**

**Instruction hierarchy nhưng thiếu formalization**

Các lớp instruction hiện tồn tại:

1. `.agent/rules/*.md` (có `trigger`, `description`, `priority`).
2. `studio/config/config.yaml` (paths, thresholds, ngôn ngữ).
3. `critical_actions` trong từng agent.
4. `workflow.md` cho capabilities/pipelines.
5. `studio/docs/lessons-learned.md`.

Nhưng không có nơi nào định nghĩa rõ ràng:

- Thứ tự ưu tiên khi xảy ra conflict.
- Phạm vi áp dụng (VD: rule toàn cục vs rule riêng cho pipeline này).

Điều này làm giảm tính determinism vì LLM phải “tự nghĩ” xem rule nào quan trọng hơn.

**Output expectations: bán-cấu trúc, chưa đủ machine-friendly**

- Một số workflow có mô tả input/output dạng YAML:
  - `gooner-audit/workflow.md`:
    - `input.prose_file` → `_prose/...page_{page_num}_prose.md`.
    - `output.audit_report` → `_prose/...page_{page_num}_audit.md`.
  - `bible-sync/workflow.md`: mô tả structure `_bible/{project}/...`.
- Tuy nhiên:
  - Schema nội dung của:
    - `forensic-state` (JSON/Markdown? fields?),
    - `draft-prose.json`,
    - `audit-report` (keys & types),
    - `state.yaml` của pipeline,
  - Chỉ được mô tả bằng prose, không có JSON Schema hay file contract chính thức.

Nếu muốn đạt **output deterministic** hơn, framework nên:

- Định nghĩa schemas trong `studio/schemas/*.json` hoặc `.yaml`.
- Các prompts agent:
  - Nhúng trực tiếp một snippet schema (rút gọn) + ví dụ.
  - Yêu cầu output phải valid JSON hợp schema.
- Orchestrator:
  - Luôn validate JSON trước khi chuyển bước (fail fast).

---

### 2.2 Wording quality & misleading instructions

**Ví dụ 1 – INFERENCE vs ZERO HALLUCINATION**

- `lewd-writer.agent.yaml`:
  - “INFERENCE PROTOCOL: If forensic data is missing a detail that *must* be there (...), you are authorized to INFER it ... Never leave a scene dry.”
  - “Context overrides Raw Data - if forensic data contradicts the mood, trust the Context.”
- `studio/docs/lessons-learned.md`:
  - “ZERO HALLUCINATION PROTOCOL”.
  - “No Phantom Elements”.
  - Nhiều ví dụ hậu kiểm về phantom figure, under-description, cross-page continuity.

Rủi ro:

- Với LLM, “INFER” + “Context overrides Raw Data” + “Never leave dry” rất dễ dịch thành:
  - “Nếu thiếu fluid thì cứ thêm vào cho hợp vibe” dù forensic không ghi nhận.
- Điều này **đi ngược mục tiêu anti-hallucination** ở tầng forensics và lessons-learned.

**Ví dụ 2 – Tool/DB không được bảo đảm tồn tại**

- `panel-forensic-analyst.agent.yaml`:
  - “FETISH SCAN: You MUST cross-reference the Hentai Lexicon database for every panel.”
- `manga-adapter.agent.yaml`:
  - “Query `{project-root}/studio/knowledge/` (fetish-db or style-guides) matching the Delta ...”.

Nếu runtime hiện tại **không có**:

- Tool `hentai_lexicon`.
- Cơ chế RAG chuẩn cho `studio/knowledge/`.

Thì LLM sẽ:

- Hoặc “giả vờ” đã scan DB.
- Hoặc tự bịa ra lexicon từ trí nhớ model, tạo cảm giác “đã tuân thủ rule” nhưng thực chất là hallucination.

**Ví dụ 3 – Xung đột ngôn ngữ**

- `studio/config/config.yaml`:
  - `document_output_language: "English"`.
- `studio/docs/lessons-learned.md`:
  - “ALL DIALOGUE = VIETNAMESE”.
  - SFX = English/Romaji.
- `gooner-audit/workflow.md`, `bible-sync/workflow.md`:
  - “ALWAYS speak in Vietnamese”.
- `lewd-writer.agent.yaml`:
  - “Prose/dialogue in Vietnamese.”

Trong cùng một context, LLM có thể:

- Ưu tiên config → viết tiếng Anh.
- Hoặc ưu tiên rules → viết tiếng Việt.

Điều này làm giảm tính nhất quán và dễ xuất hiện pha trộn EN/VI không mong muốn.

**Đề xuất chỉnh wording**

- Thay `Context overrides Raw Data` bằng:
  - “If forensic data appears inconsistent with context, FLAG `[CONFLICT]` and request forensic re-check. Do not overwrite forensic facts in prose.”
- Thay `INFERENCE PROTOCOL`:
  - Chỉ “authorized to infer” khi input mang cờ `[ALLOW_INFERENCE]` cho field cụ thể.
  - Mọi chi tiết suy diễn bắt buộc phải annotate `[INFERRED]` trong prose để audit có thể quyết định chấp nhận hay không.
- Thay “MUST cross-reference Hentai Lexicon database”:
  - Thành “IF the `hentai_lexicon` tool is available, you MUST use it. IF NOT available, keep description generic and DO NOT invent ultra-specific fetish terminology.”

---

### 2.3 Error handling & QA loop

**Cơ chế QA & loop hiện tại**

- `gooner-audit/workflow.md`:
  - Scoring 5 category, PASS/REVIEW/FAIL thresholds (>=85, 70–84, <70).
  - Banned words list (auto-fail).
  - Revision loop: “Loop until PASS or max attempts (3)”.
- `one_page_one_file.md`:
  - Forensic gate: “Prose generation is BLOCKED until a per-page forensic report exists.”
- `bible-sync/workflow.md`:
  - Chỉ SAVE sau khi gooner-audit PASS.
- `ENTRY_POINTS.md` + `studio/README.md` đưa ra luồng chuẩn:
  - panel-forensic → bible-sync LOAD → prose-adapter → gooner-audit → bible-sync SAVE.

**Điểm chưa chặt chẽ/deterministic**

- Số lần attempt audit/prose rewrite:
  - Được nêu trong prose (“max attempts (3)”) nhưng không thấy:
    - Schema state.yaml có field `attempt_count`.
    - Orchestrator logic cụ thể sẽ làm gì khi vượt quá 3 lần (escalate, fail pipeline, hỏi user?).
- Gates được mô tả bằng chữ:
  - “Verify `{output_folder}/_forensics/{page}_forensics.md` exists”.
  - Nhưng không có code/tool thực thi bắt buộc gate này trước khi gọi prose.
- Banned word & rubric scoring:
  - Nếu chỉ rely vào LLM để tự nhớ list và tự scoring trong text, QA vẫn mềm:
    - LLM có thể “quên” scan một từ.
    - Hoặc scoring dựa trên cảm tính hơn là checklist.

**Failure modes tiềm ẩn**

- Infinite/ping-pong rewrite loop:
  - Nếu không track attempt_count bằng state, LLM và orchestrator có thể audit→fail→rewrite→audit vô hạn.
- Gate bị bypass:
  - LLM không chạy check file tồn tại (hoặc “tin rằng” đã tồn tại), nhảy thẳng vào prose generation.
- Audit yếu:
  - Chỉ là một text prompt, không có tool thực thi banned-word scan hoặc check sensory counts.
- Recovery không rõ ràng:
  - Không mô tả cơ chế escalate khi audit fail nhiều lần (notify user, mark page as problematic, skip, v.v.).

---

## 3. Failure Modes & Risks

### 3.1 Orchestration drift & dead paths

- `Walkthrough.md` đã chỉ rõ:
  - `studio/services/gooner-alchemist/steps/step-01b-context-horizon.md` tồn tại nhưng không thực sự được chain trong main pipeline.
  - `core/transformation-engine` được mô tả là engine đầy đủ nhưng hiện chỉ có một step implement.
- Rủi ro:
  - Tài liệu & pipeline spec “hứa” behavior (context horizon, action dedupe, JSON gates) nhưng thực tế runtime chưa làm đầy đủ.
  - Khi dev khác dựa vào spec để xây thêm tool/agent, họ có thể giả định những điều chưa tồn tại.

### 3.2 Broken references & phantom tools

- `Walkthrough.md` liệt kê một số thiếu sót:
  - `studio/services/gooner-alchemist/tools/generate_poc.md` (được reference từ `manga-adapter.agent.yaml`) – missing.
  - `studio/agents/L2_developers/sillytavern-expert.md`, `studio/knowledge/roleplay/` – missing.
  - `studio/services/gooner-alchemist/resources/pipeline-state-template.yaml` – missing.
  - `studio/services/quality-audit/data/banned-words.txt` – missing.
- Trong runtime, khi agent “gọi” một asset/tool không tồn tại:
  - LLM sẽ bị buộc phải:
    - Hoặc nói “không tìm thấy file/tool” (nếu có kiểm tra).
    - Hoặc simply ignore/hallucinate (“giả sử đã chạy”).

### 3.3 Policy drift & inconsistency

- Nhiều rule được copy ở nhiều nơi:
  - Sensory targets.
  - Audit thresholds.
  - Language policy.
- Hiện tại các con số đang tương đối khớp nhau (85/100, 70/100, v.v.), nhưng:
  - Việc update trong tương lai rất dễ tạo lệch (sửa một nơi, quên nơi khác).
- `config.yaml` đặt `document_output_language: "English"` trong khi toàn bộ rule và docs yêu cầu output tiếng Việt.

### 3.4 Cognitive overload & rule omission

- Với quá nhiều rule & checklist trải rộng, LLM trên thực tế:
  - Sẽ ưu tiên tuân thủ các rule nổi bật (VD: tiếng Việt, SFX Latin, ZERO HALLUCINATION trong forensic).
  - Dễ bỏ sót các rule “chi tiết” như số lượng smell/sound per page, naming exact, mapping từng file page.
- Điều này làm cho pipeline **mang tính định hướng** hơn là “contract cứng”.

### 3.5 Thiếu observability & health checks tự động

- Không có workflow hay script riêng để:
  - Quét `_lnd-output` và list những page thiếu forensics/prose/audit.
  - Kiểm tra mismatch giữa số page input và số file output.
  - Kiểm tra links trong `*.agent.yaml`/`workflow.md` còn valid hay không.
- Việc phát hiện lỗi structural hiện phụ thuộc vào:
  - Developer đọc `Walkthrough.md`.
  - Manual inspection → khó scale.

---

## 4. Recommended Improvements

### 4.1 Chuẩn hóa “Contract Layer” duy nhất

**Mục tiêu**

- Có một nguồn chân lý (single source of truth) cho:
  - Schema `forensic-state`, `draft-prose`, `audit-report`, `bible-state`.
  - Naming & path conventions (ONE PAGE = ONE FILE, folder structure).
  - State của pipeline (`state.yaml`).

**Đề xuất kỹ thuật**

- Tạo thư mục `studio/contracts/` hoặc `studio/schemas/` chứa:
  - `forensic-state.schema.json`
  - `draft-prose.schema.json`
  - `audit-report.schema.json`
  - `bible-state.schema.json`
  - `pipeline-state.schema.json`
  - File khai báo naming rules (`naming-rules.yaml`).
- Bổ sung tooling:
  - Python scripts trong `studio/tools/`:
    - `validate_artifacts.py`:
      - Quét `_lnd-output`.
      - Check naming pattern.
      - Validate JSON/YAML theo schema.
    - `validate_workflow_links.py`:
      - Đọc `*.agent.yaml`, `workflow.md`, `.agent/workflows/*.md`.
      - Kiểm tra tất cả path refer tồn tại.
- Prompt agent:
  - Không cần copy toàn bộ luật bằng prose nữa, chỉ cần nhúng:
    - 1 snippet schema liên quan.
    - 1–2 ví dụ.
  - Orchestrator luôn validate JSON sau mỗi bước, fail fast nếu không hợp lệ.

---

### 4.2 Chuẩn hóa rule hierarchy & gom rule

**Defining precedence**

- Tạo file `studio/rules/hierarchy.md` mô tả:

  1. Global Canon Rules (hard law):
     - Ngôn ngữ output.
     - SFX policy.
     - ZERO HALLUCINATION.
     - ONE PAGE = ONE FILE.
     - Banned words list.
  2. Config (`studio/config/config.yaml`):
     - Paths, thresholds số học (min_audit_score, warn_score).
  3. Workflow-specific rules (trong `workflow.md`).
  4. Agent persona & stylistic principles.
  5. Lessons-learned (best practice khuyến nghị, không phải hard gate).

- Các prompt agent nên nhắc:
  - “Nếu có xung đột, luôn ưu tiên Global Canon Rules > Config > Workflow > Agent persona.”

**Gom và DRY hóa rule**

- Gom tất cả rule về language & SFX vào một file:
  - Ví dụ `studio/rules/language_and_sfx.md`.
- Cập nhật:
  - `lewd-writer`, `gooner-audit`, `lessons-learned`, `README` chỉ reference file này, không copy text.
- Đồng bộ `config.yaml`:
  - Đặt `document_output_language: "Vietnamese"` để tránh mâu thuẫn với canon.

---

### 4.3 Simplify & modularize prompts

**Persona lite**

- Rút gọn:
  - `identity` & `role` thành 2–3 câu rõ ràng.
  - Giữ lại 3–5 principles actionable (dạng mệnh lệnh ngắn).
- Phần “lore” (ví dụ ẩn dụ về “Gooner Logic”, “crime scene”, “altar/battlefield”) chuyển sang:
  - `studio/knowledge/agent-lore/*.md`.
  - Chỉ load khi user muốn role-play nặng flavour.

**Modular hóa critical_actions**

- Thay vì:
  - “READ ARCHITECTURE: Always comply with V6.1 ...” + “Load and read config.yaml” + “Load delegation-protocol.md”.
- Xây:
  - Tool `load_pipeline_context(pipeline_id)`:
    - Trả về JSON gồm:
      - Tóm tắt pipeline.
      - Path quan trọng.
      - Các rule/gate chính.
  - Tool `load_policy_summary()`:
    - Trả về list rule quan trọng từ Canon + hierarchy.
- Agent chỉ cần:
  - Gọi tools này → giảm token, giảm duplication, dễ update.

---

### 4.4 Cố định orchestration path & thêm test liên kết

**Chọn 1 con đường orchestration chính cho `gooner-alchemist`**

- Hai hướng:

  1. Thực sự implement `studio/core/transformation-engine/workflow.md` đầy đủ (Prose + Audit + Rewrite) và:
     - Dùng engine này cho mọi pipeline adaptation.
  2. Hoặc bỏ concept “transformation-engine” khỏi spec và:
     - Cho `gooner-alchemist` gọi trực tiếp:
       - panel-forensic → bible-sync LOAD → prose-adapter → gooner-audit → bible-sync SAVE.

- Sau khi quyết định:
  - Xóa các branch dead/không dùng để giảm drift.

**Automation nhỏ nhưng hữu ích**

- Viết script `studio/tools/validate_workflow_links.py`:
  - Đảm bảo:
    - Mọi `action` trong `menu` của `*.agent.yaml` trỏ tới file có tồn tại.
    - Mọi step được liệt kê trong `workflow.md` đều tồn tại trong `steps/`.
  - Có thể tích hợp vào CI/local check.

---

### 4.5 Cơ chế QA & error contract rõ ràng hơn

**Trạng thái pipeline có structure**

- Chuẩn hóa `state.yaml` của pipeline (ví dụ trong `_lnd-output/_pipeline/.../state.yaml`) để chứa:
  - `current_phase`.
  - `current_page`.
  - `audit_attempts_per_page: { page_id: count }`.
  - `forensic_completed_pages`, `prose_completed_pages`, `audit_completed_pages`.
  - `last_error` (type, message, step).

**Tooling hỗ trợ gate & loop**

- Trước khi vào prose:
  - Tool `check_forensic_gate(pages[])`:
    - Đảm bảo với mỗi page đều có file forensics tồn tại và valid theo schema.
    - Nếu thiếu → fail ngay với hướng dẫn cụ thể (chạy `/panel-forensic` trước).
- Sau mỗi audit:
  - Tool `update_audit_state(page_id, score)`:
    - Tăng `audit_attempts_per_page[page_id]`.
    - Nếu `count > 3` và score vẫn FAIL:
      - Orchestrator không loop nữa.
      - Ghi lại `last_error` + escalate (hỏi user, hoặc đánh dấu page problematic).

---

### 4.6 Kỷ luật rõ ràng giữa inference & hallucination

**Refactor cho Suki (lewd-writer)**

- Định nghĩa 2 mode:

  1. NORMAL MODE (mặc định):
     - Không được thêm chi tiết không xuất hiện trong:
       - Forensic report.
       - Bible context.
       - Context horizon (nếu có).
  2. INFERENCE MODE (chỉ bật khi pipeline cho phép):
     - Chỉ suy diễn với các field được đánh dấu `[ALLOW_INFERENCE]` (VD: fluid details nếu pipeline cho rằng “must exist”).
     - Mọi chi tiết suy diễn phải annotate `[INFERRED]` trong prose.

- Gooner-audit:
  - Có thể thêm rule:
    - Nếu `[INFERRED]` xuất hiện quá nhiều, hoặc trái ngược forensic/bible, hạ điểm mạnh/FAIL.

---

## 5. Strategic Insights

### 5.1 Blind spots kiến trúc

**Thiếu một capability/contract registry trung tâm**

- Thông tin về capabilities và pipelines hiện rải rác trong:
  - `studio/ENTRY_POINTS.md`.
  - `.agent/workflows/*.md`.
  - `studio/agents/*.agent.yaml`.
  - `studio/services/*/workflow.md`.
  - `_bmad/_config/agent-manifest.csv`.
- Gợi ý:
  - Tạo một file registry duy nhất, ví dụ:
    - `studio/config/capability_manifest.yaml`.
  - Mỗi entry gồm:
    - `id`, `type` (capability/pipeline), `owner`, `entry_command`, `workflow_path`, `required_schemas`, `required_tools`.
  - Orchestrator, UI, và docs có thể dựa vào manifest này, giảm drift.

**Observability & health check**

- Hiện chưa có workflow để:
  - Liệt kê các page/scene đã hoàn thành ở từng stage.
  - Báo cáo mismatch (VD: số page input vs số file forensics).
  - Báo các orphan artifacts hoặc missing links.
- Đề xuất:
  - Thêm một workflow `/pipeline-health`:
    - Scan `_lnd-output`.
    - Generate báo cáo health cho từng chapter/page.

---

### 5.2 Ứng dụng các agentic patterns nâng cao

**ReAct + Toolformer-style cho Orchestrator và Specialist**

- Thay vì viết trong `critical_actions` “READ file A, READ file B, dùng tool C”, có thể:
  - Định nghĩa một bộ tools chuẩn cho agent (view_file, list_pages, validate_state, load_policy_summary, query_lexicon).
  - Sử dụng pattern ReAct:
    - Thought → Tool → Observation → Thought → Action.
- Lợi ích:
  - Agent chủ động chọn tool cần thiết từ menu, thay vì tuân thủ một list text dài dễ bị bỏ sót.
  - Giảm hard-coding các “READ X/Y/Z” trong prompt, dễ maintain khi thêm tool mới.

**Hierarchical agents / sub-orchestrators**

- Hiện tại `Director K` gánh mọi thứ:
  - Gooner-alchemist.
  - RenPy adaptation.
  - RPG adapter.
  - Character-builder.
  - Release compiler.
  - Party-mode, performance-review.
- Có thể chia nhỏ:
  - `Pipeline Orchestrator` chuyên cho `/gooner-alchemist`.
  - `Adaptation Orchestrator` cho RenPy / RPG.
  - `Meta-Orchestrator (Director K)` chỉ chọn pipeline, điều phối high-level, không xử lý chi tiết từng step.

**Reflexion / self-critique có cấu trúc**

- Sau mỗi prose draft của Suki:
  - Thêm một bước self-check:
    - Suki tự chấm theo một rubric rút gọn (sensory counts, POV match, continuity).
    - Sinh ra block “Self-assessment” chuẩn hóa.
- Riko (gooner-audit) có thể:
  - Dùng block này để cross-check.
  - Nếu sai lệch lớn giữa self-assessment vs audit, raise cờ “Suki không đáng tin ở scene này”.

**Self-consistency sampling cho forensics**

- Đối với panel khó (dễ gây hallucination như ví dụ LL-002):
  - `panel-forensic` có thể chạy 2–3 lần độc lập (sampling).
  - Một “Forensic Aggregator” agent:
    - So sánh các bản.
    - Chọn các facts có consensus.
    - Mark `[UNCERTAIN]` cho phần không đồng thuận.
- Điều này giảm nguy cơ phantom elements đơn lẻ propagate sang prose/bible.

---

### 5.3 Thay đổi nhỏ, impact lớn

- **Đồng bộ lại `document_output_language`**:
  - Đặt `document_output_language: "Vietnamese"` trong `studio/config/config.yaml`.
  - Ghi rõ trong `studio/README.md` và Canon rules.
- **Tạo `studio/rules/canon-short.md`**:
  - Gom các rule cốt lõi:
    - Ngôn ngữ.
    - SFX.
    - ZERO HALLUCINATION.
    - ONE PAGE = ONE FILE.
    - Sensory & audit thresholds.
    - Banned words.
  - Mọi agent chỉ cần load file này, giảm token và tránh mâu thuẫn nhỏ giữa nhiều source.
- **Script checker nhẹ cho CI**:
  - `validate_workflow_links.py`:
    - Check broken paths trong `*.agent.yaml`, `workflow.md`, `.agent/workflows/*.md`.
  - `validate_output_structure.py`:
    - Check ONE PAGE = ONE FILE.
    - Check đầy đủ forensics/prose/audit cho mỗi page.
- **Chuẩn hóa schema `state.yaml`**:
  - Giúp UI hoặc các tools khác (ví dụ dashboard pipeline) dễ đọc và hiển thị progress, lỗi theo cách nhất quán.

---

## 6. Summary cho Dev Team

- Kiến trúc hiện tại có **phân tách role & pipeline rõ ràng**, dựa trên BMAD v6, với nhiều gate & rule chi tiết – đây là nền tảng rất tốt cho một multi-agent fiction studio.
- Các vấn đề chính tập trung vào:
  - **Drift** giữa spec và runtime (step 1b, transformation-engine, broken references).
  - **Rule/policy phân tán** và thiếu một “contract layer” duy nhất.
  - **Prompt quá dày & nhiều tầng**, gây cognitive load và instruction collision cho LLM.
  - **QA loop chưa được ràng buộc bằng state & tooling rõ ràng**, chủ yếu dựa vào ngôn ngữ tự nhiên.
- Nếu team ưu tiên:
  - Chuẩn hóa contract/schemas.
  - Gom & chuẩn hóa rule hierarchy.
  - Đơn giản hóa prompts + thêm tooling validator.
  - Cố định một orchestration path duy nhất cho mỗi pipeline.
- Thì framework có thể nâng cấp từ một “prompt-first experiment” thành một **agentic runtime có tính công nghiệp** hơn, dễ mở rộng, dễ bảo trì và ít drift khi số lượng dự án/agent tăng.
