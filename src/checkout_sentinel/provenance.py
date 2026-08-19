from __future__ import annotations

from .common import ARTIFACTS, PROJECT_ROOT, digest, utc_now, write_json


def generate_provenance() -> dict:
    subject = {
        "name": "checkout-sentinel-2.3.1.json",
        "version": "2.3.1",
        "components": ["checkout-api", "ci-review-agent", "release-risk-agent", "sre-response-agent"],
    }
    write_json(ARTIFACTS / "build" / subject["name"], subject)
    material_files = [
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "iac" / "gcs.tf",
        PROJECT_ROOT / "iac" / "policy" / "gcs.rego",
    ]
    materials = [
        {"uri": path.relative_to(PROJECT_ROOT).as_posix(), "digest": {"sha256": digest(path.read_bytes())}}
        for path in material_files
    ]
    statement = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": subject["name"], "digest": {"sha256": digest(subject)}}],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://example.edu/checkout-sentinel/build/v1",
                "externalParameters": {"target": "capstone-demo", "release": "2.3.1"},
                "internalParameters": {"runner": "local-reproducible-demo"},
                "resolvedDependencies": materials,
            },
            "runDetails": {
                "builder": {"id": "https://example.edu/builders/checkout-sentinel-local/v1"},
                "metadata": {"invocationId": digest({"time": utc_now(), "subject": subject})[:24], "startedOn": utc_now()},
            },
        },
    }
    write_json(ARTIFACTS / "governance" / "slsa-provenance.intoto.json", statement)
    return statement

