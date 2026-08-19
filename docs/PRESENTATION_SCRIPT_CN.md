# Checkout Sentinel 15 分钟录屏操作单与英文逐字稿

## 录制前 5 分钟准备

1. Windows 设置 → 系统 → 通知：临时打开“请勿打扰”。
2. 录屏软件选择 1920×1080、30 fps；录制“整个屏幕”和麦克风，不录系统密码管理器或浏览器账号栏。
3. 将显示缩放保持 100% 或 125%，浏览器缩放 100%。
4. 打开 PowerPoint：`Checkout_Sentinel_Capstone_Presentation.pptx`，停在第 1 页。
5. 打开 Chrome：`http://127.0.0.1:8765`，确认顶部状态是 `AWAITING APPROVAL`。
6. 打开项目文件夹，准备以下文件但先不要遮挡演示：
   - `artifacts/itsm/INC-CAPSTONE-001.json`
   - `artifacts/audit/events.jsonl`
   - `artifacts/iac/verification-summary.json`
   - `artifacts/iac/gcp-apply-attempt.json`
   - `artifacts/iac/sandbox-apply-summary.json`
   - `iac/policy/gcs.rego`
7. 麦克风试录 15 秒，确认声音没有爆音；鼠标移动放慢，点击后停半秒。

## 时间结构

- 0:00–3:00：问题、目标、架构和自治边界。
- 3:00–11:00：端到端演示，包括真实的人类批准。
- 11:00–14:00：安全、可观测性、经验和改进。
- 14:00–15:00：结论与问题。

## 0:00–3:00 问题和设计

### 0:00–0:40｜幻灯片 1

操作：在 PowerPoint 点击“幻灯片放映”→“从头开始”。

说：

> Hello, this project is Checkout Sentinel, my end-to-end agentic DevOps capstone. Instead of showing seven disconnected weekly exercises, I built one release story. It starts with a failing checkout build, uses constrained agents to repair and assess it, stops for human approval, deploys through a canary, detects a controlled anomaly, and rolls back with complete telemetry and governance evidence.

### 0:40–1:25｜幻灯片 2

操作：按右方向键进入第 2 页，先指左侧，再指右侧，最后指底部黑色结论条。

说：

> The problem is not whether an agent can take action. The problem is how to get speed without silently increasing operational risk. Teams want faster reviews, generated tests, routine remediation, and immediate incident response. But an agent can also follow untrusted instructions, modify more than the failing component, or expose all traffic before evidence is reviewed. My design target is more automation, smaller authority, and stronger evidence.

### 1:25–2:15｜幻灯片 3

操作：进入第 3 页，鼠标从左到右沿着六个方块移动。

说：

> One release identifier connects the complete chain. The CI agent tests and repairs the candidate. The risk agent calculates a score and chooses a strategy. A human gate binds approval to the request and risk hashes. The release then uses a ten, fifty, one-hundred percent canary. When the anomaly appears, the SRE agent performs a bounded rollback and opens an ITSM incident. OpenTelemetry, audit logs, and SLSA provenance cover every stage. Terraform follows the same plan, policy, approve, and optional apply pattern.

### 2:15–3:00｜幻灯片 4

操作：进入第 4 页，依次指三个 Agent 的彩色自治模式条。

说：

> Autonomy depends on blast radius. The CI agent is on-loop, but it may change only one allowlisted field in a generated runtime copy. The release risk agent is human-in-the-loop and cannot deploy. The SRE agent may roll back only an allowlisted canary at or below fifty percent traffic. It must escalate anything broader. The agents never receive raw cloud credentials or a general shell tool.

## 3:00–11:00 端到端演示

### 3:00–4:00｜幻灯片 5：失败构建和自动修复

操作：进入第 5 页。先指图表的 Attempt 1，再指 Attempt 2；最后指右下角 `Prompt injection: BLOCKED`。

说：

> The release candidate intentionally sets the free shipping threshold to zero, so a twenty-dollar order incorrectly ships for free. Attempt one fails two checks. The CI agent generates a boundary regression specification and changes exactly one field from zero to fifty in the runtime copy. Attempt two passes the same checks. In the same run, an untrusted support ticket tells the agent to disable approval and reveal credentials. The security guard treats that text as data, blocks the injection, and does not log the raw prompt.

### 4:00–4:45｜幻灯片 6：风险和成本

操作：进入第 6 页，按顺序指 `52`、计算公式、`CANARY`、`REQUIRED` 和成本脚注。

说：

> The risk score is deterministic: twenty base points, twelve for four changed files, twenty for infrastructure, ten for the security signal, and minus ten because final tests pass. The result is fifty-two, so policy selects a ten, fifty, one-hundred canary and still requires human approval. The cost estimate is clearly marked illustrative rather than live pricing.

### 4:45–6:10｜切换到 Chrome：执行真实批准

操作：按 `Alt+Tab` 切到 Chrome 的 Checkout Sentinel 页面。

1. 指顶部 `AWAITING APPROVAL`。
2. 指 `Build PASS` 下方的 `Attempt 1 FAIL; repair APPLIED`。
3. 指风险 `52` 和流程中的 `Human approval: WAITING`。
4. 点击右侧 `Approver name` 输入框，输入你在学校使用的真实姓名。
5. 点击绿色 **Approve release**。
6. 等页面刷新，指顶部 `APPROVED` 和流程中的 `APPROVED`。

说：

> This is the real human-in-the-loop boundary. The pipeline is stopped and the deployment action is disabled. I will enter my name and approve this exact release. The decision records my identity, a UTC timestamp, the request hash, and the risk hash. If the request changes later, the integrity check blocks deployment even though an old approval exists.

### 6:10–7:35｜执行金丝雀和 SRE 响应

操作：

1. 点击 **Continue deployment**。
2. 等待提示变成 `Anomaly detected at 50%; rollback and ITSM evidence recorded.`。
3. 指 `Canary evidence` 表：10% 行是 `CONTINUE`，50% 行是 `ROLLBACK`。
4. 指流程最后两格：`ANOMALY DETECTED` 和 `ROLLED BACK`。
5. 指 OTel spans、metric records 和 audit events 计数。

说：

> I will now continue the approved deployment. At ten percent traffic the error rate is one percent and p95 latency is one hundred forty milliseconds, so the canary continues. At fifty percent, a controlled fault raises the error rate to twenty percent and p95 latency to four hundred eighty milliseconds. Both SLO guardrails trip. The rollout stops before one hundred percent. The SRE agent verifies its tool allowlist and fifty-percent ceiling, rolls back version 2.3.1 to stable 2.3.0, creates one ITSM incident, and records the outcome.

### 7:35–8:30｜幻灯片 9：解释 SRE 爆炸半径

操作：`Alt+Tab` 回 PowerPoint，进入第 9 页。从 Observe 指到 Record。

说：

> The SRE record is intentionally concise: observation, policy, selected action, and outcome. It does not expose hidden chain-of-thought. The runtime authorizes only rollback_canary at or below fifty percent traffic. The stable version remains available, the incident is resolved, and the postmortem links the telemetry, rollback, and audit evidence.

### 8:30–9:40｜幻灯片 10：真实 Terraform/OPA 证据

操作：进入第 10 页，逐行指表格；先指 `GCP apply: ATTEMPTED; BILLING 403`，再指 `Sandbox apply: 1 add / 0 change / 0 destroy`。

说：

> The infrastructure track separates plan, policy, approval, and apply evidence. Terraform 1.15.8 authenticated to the course GCP project and planned one secure storage bucket: one add, zero changes, and zero destroys. Conftest passed all five cloud controls, and a negative staging-label fixture was blocked. After my explicit approval, the real GCP apply was attempted, but the project returned billing error four-zero-three before resource creation, and Terraform state remained empty. I did not label that as cloud success. Instead, a no-cost local terraform-data plan carried the same approval hash: its three policy checks passed and one resource applied, while approved-equals-false was blocked by OPA.

### 9:40–11:00｜幻灯片 11：可观测性和治理

操作：进入第 11 页。指顶部四个词，再指左侧 trace hierarchy 和右侧 audit event。

说：

> Both the checkout service and the agents emit OpenTelemetry spans. Agent operations use invoke_agent and tool operations use execute_tool, so service and agent activity share one reconstructable timeline. Structured audit events include actor, action, outcome, and SHA-256 hashes of inputs and outputs. Approval adds identity and UTC time. The in-toto statement uses the official SLSA provenance version one predicate. I describe this honestly as local Build L1-style provenance existence, not signed hosted Build L2 or L3.

## 11:00–14:00 经验和改进

### 11:00–12:20｜安全和准确边界回顾

操作：可回到第 4 页快速指三条限制，或保持第 11 页。

说：

> The strongest evidence in this project is negative evidence. An unapproved deployment fails. A malicious prompt is blocked. An unknown tool is denied. A rollback above fifty percent is denied. A non-compliant Terraform plan is blocked. These tests show that guardrails enforce behavior rather than appearing only in documentation. I also separate real evidence from simulation: the GCP plan is real, while traffic and ITSM are controlled local simulations.

### 12:20–14:00｜幻灯片 12：经验和下一步

操作：进入第 12 页，先读左侧结论，再逐条指右侧改进。

说：

> My main lesson is that agents should move quickly only inside small, testable boundaries. The billing failure also showed why honest evidence boundaries matter: an authorized attempt is not a successful cloud deployment. I would replace the service-account key with OIDC and short-lived workload identity, generate signed provenance on a hosted hardened builder, export OTLP to a retained backend, and retry in an authorized non-production cloud project. Human control still remains at infrastructure apply, external publication, and final coursework submission.

## 14:00–15:00 结论和问题

操作：保持第 12 页，鼠标停在 `Questions`，不要继续切换窗口。

说：

> Checkout Sentinel demonstrates the full capstone chain: agentic CI review and remediation, transparent risk scoring, canary deployment, service and agent telemetry, anomaly detection, bounded SRE response, Terraform and OPA policy, human approval, ITSM, structured audit, and SLSA provenance. The project increases automation without hiding limits or claiming actions that were not performed. Thank you. I am ready for questions.

## 录完后的检查

1. 总时长控制在 14:30–15:30；如果超时，优先缩短第 11 页的标准说明，不删除端到端演示。
2. 回看批准动作是否清楚拍到姓名输入、Approve、Continue deployment 和 ROLLED BACK。
3. 确认视频中没有出现 GCP 服务账号 JSON、`terraform.tfvars`、浏览器账号菜单或私人通知。
4. 检查声音覆盖全部画面，不出现超过 5 秒的无解释等待。
5. 导出 MP4 后从头播放一次，确认文字可读、鼠标可见、声音同步，再上传。
