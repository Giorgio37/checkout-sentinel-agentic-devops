import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const FINAL = "C:/Users/Jonat/Documents/Codex/2026-08-16/wan/outputs/Checkout_Sentinel_Capstone_Presentation.pptx";
const RENDER = "C:/Users/Jonat/Documents/Codex/2026-08-16/wan/work/capstone-agentic-devops/presentation/build/rendered";

const C = {
  white: "#FFFFFF",
  ink: "#17202A",
  muted: "#65727E",
  panel: "#EDEDED",
  rule: "#B8BCC4",
  blue: "#2F6FED",
  blueLight: "#DCE8FF",
  teal: "#007A70",
  tealLight: "#D8F0ED",
  red: "#B42318",
  redLight: "#FBE5E2",
  amber: "#A15C00",
};

const FONT = "Arial";

function rect(slide, name, left, top, width, height, fill, line = "none") {
  return slide.shapes.add({
    geometry: "rect",
    name,
    position: { left, top, width, height },
    fill,
    line: line === "none" ? { style: "solid", fill: "none", width: 0 } : { style: "solid", fill: line, width: 1 },
  });
}

function line(slide, name, left, top, width, height = 0, color = C.rule, weight = 1) {
  return slide.shapes.add({
    geometry: "straightConnector1",
    name,
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: color, width: weight },
  });
}

function text(slide, name, value, left, top, width, height, size = 20, color = C.ink, bold = false, align = "left") {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = value;
  shape.text.style = {
    fontSize: size,
    typeface: FONT,
    color,
    bold,
    alignment: align,
    verticalAlignment: "middle",
    autoFit: "shrinkText",
  };
  return shape;
}

function addChrome(slide, number, kicker, title) {
  slide.background.fill = C.white;
  text(slide, `kicker-${number}`, `${String(number).padStart(2, "0")} / ${kicker.toUpperCase()}`, 52, 28, 420, 25, 15, C.teal, true);
  text(slide, `title-${number}`, title, 52, 63, 1176, 68, 38, C.ink, true);
  line(slide, `header-rule-${number}`, 52, 139, 1176, 0, C.rule, 1);
  text(slide, `footer-${number}`, `CHECKOUT SENTINEL   |   ${number}`, 1038, 677, 190, 20, 11, C.muted, false, "right");
}

function addNotes(slide, talkTrack, sources) {
  const sourceLines = sources.map((item) => `- ${item}`).join("\n");
  slide.speakerNotes.textFrame.setText(`${talkTrack}\n\n[Sources]\n${sourceLines}`);
  slide.speakerNotes.setVisible(true);
}

function addBulletList(slide, items, left, top, width, rowHeight = 58, size = 21) {
  items.forEach((item, index) => {
    rect(slide, `bullet-${left}-${top}-${index}`, left, top + index * rowHeight + 10, 8, 8, index === 0 ? C.blue : C.teal);
    text(slide, `bullet-text-${left}-${top}-${index}`, item, left + 24, top + index * rowHeight, width - 24, rowHeight - 4, size, C.ink, false);
  });
}

function addStat(slide, number, label, left, top, color = C.teal) {
  text(slide, `stat-${number}-${left}`, number, left, top, 220, 78, 54, color, true);
  text(slide, `stat-label-${number}-${left}`, label, left, top + 72, 220, 52, 18, C.muted, false);
}

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

async function main() {
  await fs.mkdir(RENDER, { recursive: true });
  await fs.mkdir("C:/Users/Jonat/Documents/Codex/2026-08-16/wan/outputs", { recursive: true });
  const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });

  // 1. Minimal title slide, derived from Codex Grid slide 01.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    text(s, "cover-kicker", "CSE 636  /  AGENTIC DEVOPS CAPSTONE", 52, 46, 560, 32, 18, C.teal, true);
    text(s, "cover-title", "Checkout Sentinel", 52, 195, 980, 120, 70, C.ink, true);
    text(s, "cover-subtitle", "A policy-constrained release workflow that fails, repairs, approves, detects, and rolls back", 52, 350, 910, 105, 28, C.muted, false);
    rect(s, "cover-accent", 1035, 195, 150, 150, C.blue);
    rect(s, "cover-accent-2", 1100, 315, 85, 85, C.teal);
    text(s, "cover-name", "Jonathan  |  August 19, 2026", 52, 610, 460, 32, 17, C.ink, false);
    addNotes(s, "Open with the outcome: this is not seven disconnected weekly exercises. It is one release that moves from a failing build to a safe rollback, with human approval and audit evidence at every boundary.", ["Internal: README.md", "Internal: CSE 636 Capstone brief"]);
  }

  // 2. Problem framing.
  {
    const s = deck.slides.add();
    addChrome(s, 2, "Problem", "Speed without boundaries is operational risk");
    text(s, "problem-left-title", "What teams want", 74, 188, 470, 42, 26, C.ink, true);
    addBulletList(s, ["Faster review and test generation", "Automated remediation of routine failures", "Immediate response to service anomalies"], 74, 246, 470, 72, 22);
    line(s, "problem-divider", 640, 178, 0, 410, C.rule, 2);
    text(s, "problem-right-title", "What can go wrong", 712, 188, 470, 42, 26, C.ink, true);
    addBulletList(s, ["Agents execute untrusted instructions", "A repair expands beyond the failing component", "A release reaches 100% before evidence is reviewed"], 712, 246, 470, 72, 22);
    rect(s, "problem-thesis", 74, 548, 1108, 72, C.ink);
    text(s, "problem-thesis-text", "The design target: more automation, smaller authority, stronger evidence.", 98, 557, 1060, 54, 27, C.white, true, "center");
    addNotes(s, "The problem is not whether agents can act. The problem is how to let them act without silently increasing risk. My design uses narrow tool permissions, explicit blast-radius limits, integrity-bound approval, and telemetry that can reconstruct every decision.", ["Internal: docs/ARCHITECTURE.md", "Internal: docs/SECURITY.md"]);
  }

  // 3. Architecture diagram. Connectors are created before nodes.
  {
    const s = deck.slides.add();
    addChrome(s, 3, "Architecture", "One release ID connects every agent action");
    const xs = [50, 255, 460, 665, 870, 1075];
    for (let i = 0; i < xs.length - 1; i += 1) line(s, `arch-edge-${i}`, xs[i] + 150, 316, 55, 0, C.rule, 2);
    const nodes = [
      ["Candidate", "broken config", C.blue],
      ["CI Agent", "test + repair", C.teal],
      ["Risk Agent", "score 52", C.teal],
      ["Human gate", "hash + time", C.blue],
      ["Canary", "10 / 50 / 100", C.red],
      ["SRE Agent", "rollback + ITSM", C.teal],
    ];
    nodes.forEach(([a, b, color], i) => {
      rect(s, `arch-node-${i}`, xs[i], 255, 150, 124, color);
      text(s, `arch-node-title-${i}`, a, xs[i] + 10, 271, 130, 34, 20, C.white, true, "center");
      text(s, `arch-node-body-${i}`, b, xs[i] + 10, 309, 130, 48, 16, C.white, false, "center");
    });
    rect(s, "arch-crosscut", 110, 442, 1060, 72, C.panel);
    text(s, "arch-crosscut-text", "OpenTelemetry traces + service metrics + structured audit + SLSA provenance", 130, 454, 1020, 48, 24, C.ink, true, "center");
    text(s, "arch-boundary", "Terraform plan  →  OPA policy  →  human approval  →  optional apply", 180, 550, 920, 42, 21, C.muted, false, "center");
    addNotes(s, "Walk left to right. The same release identifier and evidence trail move through CI, risk scoring, approval, canary, and SRE response. Terraform follows the same policy-before-action pattern, but real apply remains outside this local demonstration.", ["Internal: docs/ARCHITECTURE.md", "Internal: config/agents.json"]);
  }

  // 4. Autonomy levels.
  {
    const s = deck.slides.add();
    addChrome(s, 4, "Guardrails", "Autonomy grows only when blast radius shrinks");
    const cols = [70, 440, 810];
    const agents = [
      ["CI Review Agent", "ON-LOOP", "May patch one field\nin a runtime copy", "Cannot touch source,\ncredentials, or production", C.blue],
      ["Release Risk Agent", "HUMAN-IN-THE-LOOP", "May calculate score\nand select strategy", "Cannot deploy; approval\nis mandatory", C.teal],
      ["SRE Response Agent", "ON-LOOP", "May rollback a canary\nat or below 50%", "Must escalate broader\nactions", C.red],
    ];
    agents.forEach(([name, mode, allowed, denied, color], i) => {
      text(s, `agent-name-${i}`, name, cols[i], 190, 320, 40, 25, C.ink, true);
      rect(s, `agent-mode-${i}`, cols[i], 244, 320, 48, color);
      text(s, `agent-mode-text-${i}`, mode, cols[i] + 10, 250, 300, 34, 16, C.white, true, "center");
      text(s, `agent-allowed-title-${i}`, "ALLOWED", cols[i], 326, 320, 30, 15, C.teal, true);
      text(s, `agent-allowed-${i}`, allowed, cols[i], 356, 320, 86, 20, C.ink, false);
      line(s, `agent-rule-${i}`, cols[i], 458, 320, 0, C.rule, 1);
      text(s, `agent-denied-title-${i}`, "DENIED / ESCALATE", cols[i], 478, 320, 30, 15, C.red, true);
      text(s, `agent-denied-${i}`, denied, cols[i], 508, 320, 86, 20, C.ink, false);
    });
    addNotes(s, "These are software agents with explicit contracts, not general-purpose assistants. The CI and SRE agents have pre-authorized narrow actions. The release agent produces a recommendation but cannot deploy. The broader the impact, the more authority returns to the human.", ["Internal: config/agents.json", "Internal: prompts/*.md"]);
  }

  // 5. CI evidence.
  {
    const s = deck.slides.add();
    addChrome(s, 5, "CI/CD", "A failing build becomes a proven repair");
    s.charts.add("bar", {
      position: { left: 62, top: 184, width: 610, height: 400 },
      categories: ["Attempt 1", "Attempt 2"],
      series: [{ name: "Passing checks", values: [0, 2], fill: C.blue, points: [{ idx: 0, fill: C.red }, { idx: 1, fill: C.teal }] }],
      barOptions: { direction: "column", grouping: "clustered", gapWidth: 70 },
      hasLegend: false,
      yAxis: { min: 0, max: 2, majorUnit: 1, majorGridlines: { style: "solid", fill: C.panel, width: 1 }, textStyle: { fontSize: 14, fill: C.muted } },
      xAxis: { textStyle: { fontSize: 16, fill: C.ink } },
      dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 17, fill: C.ink, bold: true } },
      chartFill: C.white,
      chartLine: { style: "solid", fill: C.white, width: 0 },
      plotAreaFill: { type: "none" },
      plotAreaLine: { style: "solid", fill: C.white, width: 0 },
    });
    text(s, "ci-fail", "FAIL", 730, 188, 180, 62, 42, C.red, true);
    text(s, "ci-fail-detail", "threshold = 0\n$20 order ships free", 730, 250, 420, 72, 21, C.ink, false);
    line(s, "ci-middle-rule", 730, 344, 430, 0, C.rule, 1);
    text(s, "ci-action", "ONE-FIELD REPAIR", 730, 368, 420, 32, 17, C.blue, true);
    text(s, "ci-action-detail", "runtime copy only\nthreshold 0 → 50", 730, 405, 420, 70, 21, C.ink, false);
    text(s, "ci-pass", "PASS", 730, 506, 180, 62, 42, C.teal, true);
    text(s, "ci-injection", "Prompt injection: BLOCKED", 910, 520, 260, 36, 17, C.red, true);
    addNotes(s, "Attempt one fails two checks. The CI agent creates a regression specification and changes exactly one allowlisted field in the generated runtime copy. Attempt two passes. In the same run, a malicious support ticket tries to disable approval and reveal a credential; it is classified as untrusted data and blocked.", ["Internal: artifacts/build/ci_result.json", "Internal: artifacts/build/generated_test.json", "Internal: fixtures/untrusted_ticket.txt"]);
  }

  // 6. Risk score.
  {
    const s = deck.slides.add();
    addChrome(s, 6, "Risk and FinOps", "Risk 52 forces canary and human approval");
    addStat(s, "52", "MEDIUM RISK", 78, 180, C.blue);
    text(s, "risk-formula", "20 base  +  12 files  +  20 IaC  +  10 security  -  10 tests", 78, 320, 1050, 54, 26, C.ink, true);
    line(s, "risk-score-rule", 78, 398, 1080, 0, C.rule, 1);
    const labels = [
      ["Release strategy", "CANARY 10 / 50 / 100", C.teal],
      ["Approval", "REQUIRED", C.blue],
      ["Cost estimate", "$0.22 / MONTH*", C.amber],
    ];
    labels.forEach(([label, value, color], i) => {
      const x = 78 + i * 365;
      text(s, `risk-label-${i}`, label, x, 438, 330, 30, 16, C.muted, true);
      text(s, `risk-value-${i}`, value, x, 474, 330, 54, 25, color, true);
    });
    text(s, "risk-footnote", "*Illustrative 10 GB storage and low request volume; verify live pricing before production.", 78, 585, 1050, 28, 14, C.muted, false);
    addNotes(s, "The score is transparent, not model intuition. It totals 52 from documented inputs, so the policy selects a 10/50/100 canary and still requires human approval. The cost figure is an illustrative planning estimate, clearly labeled as not live pricing.", ["Internal: artifacts/release/risk_assessment.json"]);
  }

  // 7. Approval boundary.
  {
    const s = deck.slides.add();
    addChrome(s, 7, "Human gate", "Approval is a cryptographic boundary");
    text(s, "approval-pending", "PENDING", 82, 196, 300, 72, 48, C.amber, true);
    text(s, "approval-pending-detail", "Deployment command returns\nPermissionError without approval", 82, 282, 470, 82, 22, C.ink, false);
    line(s, "approval-divider", 640, 184, 0, 390, C.rule, 2);
    text(s, "approval-bound", "BOUND TO", 710, 196, 360, 34, 17, C.teal, true);
    addBulletList(s, ["Release 2.3.1 and environment", "Risk assessment SHA-256", "Request SHA-256", "Approver identity and UTC timestamp"], 710, 244, 450, 66, 21);
    rect(s, "approval-gate", 82, 510, 1078, 70, C.ink);
    text(s, "approval-gate-text", "If the request changes after approval, deployment is blocked.", 105, 521, 1030, 48, 25, C.white, true, "center");
    addNotes(s, "This is the live human-in-the-loop moment. The pipeline is currently stopped here. Approval is not a loose checkbox: it records the approver and UTC time, and binds that decision to the exact request and risk hashes. A changed request invalidates the approval.", ["Internal: src/checkout_sentinel/approval.py", "Internal: artifacts/approval/request.json"]);
  }

  // 8. Canary anomaly chart.
  {
    const s = deck.slides.add();
    addChrome(s, 8, "Observability", "The 50% canary trips both SLO guardrails");
    s.charts.add("bar", {
      position: { left: 58, top: 184, width: 660, height: 405 },
      categories: ["10% traffic", "50% traffic"],
      series: [{ name: "Error rate", values: [1, 20], fill: C.teal, points: [{ idx: 1, fill: C.red }] }],
      barOptions: { direction: "column", grouping: "clustered", gapWidth: 65 },
      hasLegend: false,
      yAxis: { min: 0, max: 25, majorUnit: 5, numberFormatCode: "0\"%\"", majorGridlines: { style: "solid", fill: C.panel, width: 1 }, textStyle: { fontSize: 14, fill: C.muted } },
      xAxis: { textStyle: { fontSize: 16, fill: C.ink } },
      dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 17, fill: C.ink, bold: true } },
      chartFill: C.white,
      chartLine: { style: "solid", fill: C.white, width: 0 },
      plotAreaFill: { type: "none" },
      plotAreaLine: { style: "solid", fill: C.white, width: 0 },
    });
    text(s, "slo-error-label", "ERROR RATE", 786, 194, 370, 26, 16, C.muted, true);
    text(s, "slo-error", "20%  >  5%", 786, 226, 390, 62, 38, C.red, true);
    line(s, "slo-rule", 786, 316, 390, 0, C.rule, 1);
    text(s, "slo-latency-label", "P95 LATENCY", 786, 350, 370, 26, 16, C.muted, true);
    text(s, "slo-latency", "480 ms  >  350 ms", 786, 382, 390, 62, 34, C.red, true);
    rect(s, "slo-decision", 786, 492, 390, 72, C.red);
    text(s, "slo-decision-text", "ANOMALY → STOP", 806, 504, 350, 48, 26, C.white, true, "center");
    addNotes(s, "At 10 percent, the canary is healthy: one percent errors and 140 milliseconds p95. At 50 percent, the controlled fault raises errors to 20 percent and p95 latency to 480 milliseconds. Both thresholds trip, so rollout stops before 100 percent.", ["Internal: artifacts/telemetry/metrics.jsonl", "Internal: src/checkout_sentinel/observability.py"]);
  }

  // 9. SRE response timeline, Codex Grid timeline silhouette.
  {
    const s = deck.slides.add();
    addChrome(s, 9, "Agentic SRE", "Rollback happens before full traffic exposure");
    line(s, "sre-timeline", 92, 330, 1060, 0, C.ink, 2);
    const points = [120, 390, 660, 930];
    const data = [
      ["OBSERVE", "20% errors\n480 ms p95", C.red],
      ["AUTHORIZE", "allowlisted tool\nscope = 50%", C.blue],
      ["ACT", "2.3.1 → 2.3.0\nrollback succeeds", C.teal],
      ["RECORD", "INC-CAPSTONE-001\npostmortem linked", C.ink],
    ];
    data.forEach(([label, detail, color], i) => {
      rect(s, `sre-dot-${i}`, points[i], 322, 16, 16, color);
      text(s, `sre-label-${i}`, label, points[i] - 4, 240, 220, 32, 17, color, true);
      text(s, `sre-detail-${i}`, detail, points[i] - 4, 360, 240, 92, 20, C.ink, false);
    });
    rect(s, "sre-result", 92, 520, 1060, 62, C.tealLight);
    text(s, "sre-result-text", "Final state: ROLLED_BACK   |   maximum affected traffic: 50%   |   stable version remained 2.3.0", 110, 528, 1024, 44, 23, C.teal, true, "center");
    addNotes(s, "The SRE agent records a concise observation, policy, selected action, and outcome. The runtime authorizes only rollback_canary and enforces a 50 percent ceiling. It rolls back to 2.3.0, creates one ITSM incident, and writes a postmortem. It never receives a general shell tool.", ["Internal: artifacts/release/rollback.json", "Internal: artifacts/itsm/INC-CAPSTONE-001.json", "Internal: src/checkout_sentinel/sre_agent.py"]);
  }

  // 10. IaC evidence table.
  {
    const s = deck.slides.add();
    addChrome(s, 10, "IaC and policy", "Terraform and OPA prove the infrastructure gate");
    const tableRows = [
      ["Evidence", "Result", "Policy outcome", "What it proves"],
      ["Terraform validate", "SUCCESS", "Configuration valid", "IaC is syntactically valid"],
      ["Real authenticated plan", "1 add / 0 change / 0 destroy", "5 / 5 PASS", "Secure GCS plan reaches policy gate"],
      ["Negative staging fixture", "4 pass / 1 fail", "BLOCKED", "environment label is enforced"],
      ["GCP apply", "ATTEMPTED; BILLING 403", "APPROVED first", "Blocked before creation; state empty"],
      ["Sandbox apply", "1 add / 0 change / 0 destroy", "3 / 3 PASS", "Approved apply succeeded locally"],
    ];
    const tableX = 58;
    const tableY = 176;
    const widths = [250, 270, 250, 394];
    const rowHeight = 58;
    tableRows.forEach((row, rowIndex) => {
      let x = tableX;
      row.forEach((value, colIndex) => {
        const fill = rowIndex === 0 ? C.ink : (rowIndex % 2 === 0 ? C.panel : C.white);
        const color = rowIndex === 0 ? C.white : C.ink;
        rect(s, `iac-cell-${rowIndex}-${colIndex}`, x, tableY + rowIndex * rowHeight, widths[colIndex], rowHeight, fill, C.rule);
        text(s, `iac-cell-text-${rowIndex}-${colIndex}`, value, x + 10, tableY + rowIndex * rowHeight + 6, widths[colIndex] - 20, rowHeight - 12, rowIndex === 0 ? 17 : 16, color, rowIndex === 0);
        x += widths[colIndex];
      });
    });
    text(s, "iac-controls-title", "OPA checks five cloud controls; sandbox negative case also blocks approved=false", 58, 535, 850, 34, 18, C.teal, true);
    text(s, "iac-controls", "capstone label  |  terraform label  |  uniform access  |  public prevention  |  versioning", 58, 570, 1120, 40, 17, C.ink, false);
    addNotes(s, "This track separates three outcomes. Terraform 1.15.8 authenticated to the course GCP project and planned one secure bucket with no changes or destroys; Conftest passed all five checks and the staging-label fixture was blocked. After explicit human approval, I attempted the GCP apply. Billing returned 403 accountDisabled before creation, Terraform state stayed empty, and no cloud resource exists. To prove the gate without pretending cloud success, an approved local terraform_data plan passed three of three policy checks and applied one resource; approved=false was blocked by OPA.", ["Internal: artifacts/iac/verification-summary.json", "Internal: artifacts/iac/gcp-apply-attempt.json", "Internal: artifacts/iac/sandbox-apply-summary.json", "Internal: iac/policy/gcs.rego"]);
  }

  // 11. Telemetry and governance.
  {
    const s = deck.slides.add();
    addChrome(s, 11, "Governance", "Telemetry makes every action reconstructable");
    addStat(s, "OTel", "SERVICE + AGENT SPANS", 70, 178, C.blue);
    addStat(s, "JSONL", "STRUCTURED AUDIT", 380, 178, C.teal);
    addStat(s, "SLSA", "PROVENANCE V1", 690, 178, C.ink);
    addStat(s, "UTC", "APPROVAL TIMESTAMPS", 1000, 178, C.red);
    line(s, "gov-rule", 70, 332, 1100, 0, C.rule, 1);
    text(s, "gov-trace-title", "Trace hierarchy", 70, 368, 400, 32, 20, C.ink, true);
    text(s, "gov-trace", "invoke_agent ci-review-agent\n  execute_tool inspect_untrusted_text\n  execute_tool patch_checkout_config\ncheckout POST /checkout", 70, 410, 520, 150, 19, C.ink, false);
    text(s, "gov-record-title", "Every audit event", 680, 368, 400, 32, 20, C.ink, true);
    addBulletList(s, ["actor + action + outcome", "request and response SHA-256", "bounded details; no prompt or secret", "incident and provenance links"], 680, 408, 460, 48, 18);
    addNotes(s, "The service and the agents share OpenTelemetry-style trace context. Agent spans use invoke_agent; tool spans use execute_tool. Audit events store actor, action, outcome, and input/output hashes. Approval adds identity and UTC time. Provenance identifies the artifact and materials by digest. This is local Build L1-style existence, not signed hosted L2 or L3.", ["https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md", "https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/", "https://slsa.dev/spec/draft/build-provenance", "Internal: artifacts/governance/slsa-provenance.intoto.json"]);
  }

  // 12. Lessons and close.
  {
    const s = deck.slides.add();
    addChrome(s, 12, "Lessons", "The next improvement is stronger identity");
    text(s, "lesson-main", "Agents should move quickly\ninside small, testable boundaries.", 70, 190, 650, 150, 42, C.ink, true);
    line(s, "lesson-divider", 758, 184, 0, 390, C.rule, 2);
    text(s, "improve-title", "Next improvements", 818, 190, 360, 38, 24, C.teal, true);
    addBulletList(s, ["OIDC and short-lived cloud identity", "Signed provenance on a hosted builder", "OTLP backend with trace-to-incident links", "Real traffic replay in non-production"], 818, 246, 370, 68, 20);
    rect(s, "lesson-close", 70, 494, 650, 90, C.ink);
    text(s, "lesson-close-text", "Human control remains at apply, publish, and submit.", 95, 509, 600, 60, 24, C.white, true, "center");
    text(s, "questions", "Questions", 818, 548, 360, 48, 32, C.blue, true);
    addNotes(s, "Close by returning to the design principle: automation can increase when authority is smaller and evidence is stronger. The most important production improvement is not more autonomous behavior; it is stronger workload identity, signed hosted provenance, retained telemetry, and real non-production traffic validation. Then invite questions.", ["Internal: docs/AI_COLLABORATION.md", "Internal: technical report, page 5"]);
  }

  for (const [index, slide] of deck.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await writeBlob(`${RENDER}/${stem}.png`, await deck.export({ slide, format: "png", scale: 1 }));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(`${RENDER}/${stem}.layout.json`, await layout.text());
  }
  await writeBlob(`${RENDER}/montage.webp`, await deck.export({ format: "webp", montage: true, scale: 1 }));
  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(FINAL);
  console.log(FINAL);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
