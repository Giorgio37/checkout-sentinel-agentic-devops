# INC-CAPSTONE-001 Postmortem

## Impact

The 2.3.1 canary reached 50% simulated traffic before rollback. Stable 2.3.0 remained available.

## Detection

Error rate reached 20%, above the 5% SLO guardrail; p95 latency reached 480 ms.

## Response

The SRE agent selected the allowlisted rollback tool. The runtime enforced a 50% blast-radius ceiling and recorded the action.

## Follow-up

Add production traffic replay and signed hosted provenance before a real deployment.
