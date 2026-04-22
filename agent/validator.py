import subprocess
import os
import json

def run_validation(workspace_dir: str) -> dict:
    results = {"passed": True, "errors": []}

    # Step 1 — terraform init
    init = subprocess.run(
        ["terraform", "init", "-backend=false"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )
    if init.returncode != 0:
        results["passed"] = False
        results["errors"].append({
            "stage": "init",
            "output": init.stderr
        })
        return results

    # Step 2 — terraform validate
    validate = subprocess.run(
        ["terraform", "validate", "-json"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )
    try:
        val_json = json.loads(validate.stdout)
        if not val_json.get("valid"):
            results["passed"] = False
            for diag in val_json.get("diagnostics", []):
                results["errors"].append({
                    "stage":    "validate",
                    "severity": diag.get("severity"),
                    "summary":  diag.get("summary"),
                    "detail":   diag.get("detail", ""),
                    "range":    diag.get("range", {})
                })
    except json.JSONDecodeError:
        results["passed"] = False
        results["errors"].append({
            "stage":  "validate",
            "output": validate.stderr
        })

    # Step 3 — tflint
    tflint = subprocess.run(
        ["tflint", "--format=json"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )
    if tflint.returncode != 0 and tflint.stdout:
        try:
            lint_json = json.loads(tflint.stdout)
            for issue in lint_json.get("issues", []):
                results["errors"].append({
                    "stage":    "tflint",
                    "severity": issue["rule"]["severity"],
                    "summary":  issue["message"]
                })
            results["passed"] = False
        except json.JSONDecodeError:
            pass

    return results