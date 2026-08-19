# Capstone Submission Checklist

## Required deliverables

- [x] Code repository snapshot with pipeline, IaC modules, agent configurations, OPA policies, observability, tests, and evidence.
- [x] Five-page technical report: `Agentic_DevOps_Capstone_Technical_Report.docx`.
- [x] Twelve-slide presentation: `Checkout_Sentinel_Capstone_Presentation.pptx`.
- [ ] 15-minute recorded end-to-end walkthrough. Use `Capstone_Recording_Guide_and_Script_CN.md`.

## Evidence checks completed

- [x] Five unit tests pass.
- [x] End-to-end evidence verification passes.
- [x] Prompt injection, unknown tool, missing approval, blast-radius, and OPA negative paths are tested.
- [x] Authenticated GCP Terraform plan is 1 add / 0 change / 0 destroy and passes 5/5 OPA controls.
- [x] Real GCP apply was explicitly approved and attempted; billing 403 stopped it before creation and state remained empty.
- [x] Approved local sandbox apply succeeded 1/0/0; `approved=false` was blocked by OPA.
- [x] Report is exactly five pages and visually reviewed.
- [x] Presentation is twelve slides, visually reviewed, and passes overflow detection.
- [x] Final archives are re-extracted, scanned for excluded files and credential markers, and checksum-verified.

## Before recording

- [ ] Turn on Windows Do Not Disturb.
- [ ] Set recording to 1920x1080 at 30 fps and verify the microphone.
- [ ] Reset the dashboard to `AWAITING APPROVAL` only after preserving the final evidence package.
- [ ] Keep credential files, browser account menus, and private notifications off-screen.
- [ ] Capture the approver name, approval, canary anomaly, rollback, and IaC evidence slide.

## Before final submission

- [ ] Publish the code repository to the approved school-accessible location and confirm visibility.
- [ ] Upload or attach the 15-minute video.
- [ ] Attach the report and presentation.
- [ ] Confirm the Classroom item is the Capstone, not the separate Lab_Wk7 exercise.
- [ ] Review the attachment list and select **Turn in** only after final confirmation.

## Honest boundary to state

The GCP plan and apply attempt are real. The cloud apply did not create a resource because the course project's billing account was disabled. The successful Terraform apply is a no-cost local `terraform_data` sandbox proving that only an OPA-approved, human-approved plan is applied. Traffic, anomaly injection, rollback, and ITSM are controlled local simulations.
