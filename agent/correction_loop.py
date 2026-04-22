import os
import json
from agent.validator import run_validation
from agent.error_interpreter import interpret_errors

def write_files(workspace: str, code: dict):
    os.makedirs(workspace, exist_ok=True)
    file_map = {
        "main_tf":      "main.tf",
        "variables_tf": "variables.tf",
        "outputs_tf":   "outputs.tf",
        "tfvars":       "terraform.tfvars"
    }
    for key, filename in file_map.items():
        if key in code:
            filepath = os.path.join(workspace, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code[key])

def apply_corrections(code: dict, corrections: dict) -> dict:
    file_key_map = {
        "main_tf":      "main_tf",
        "variables_tf": "variables_tf",
        "outputs_tf":   "outputs_tf",
        "tfvars":       "tfvars"
    }
    for key in file_key_map:
        corrected_content = corrections.get(key, "")
        if corrected_content.strip():
            code[key] = corrected_content
            print(f"  Applied correction to {key}")
    return code

def run_correction_loop(code: dict, workspace: str, max_iterations: int = 3) -> dict:
    trace = {
        "iterations": 0,
        "errors_per_iteration": [],
        "final_status": "pending"
    }

    for i in range(max_iterations):
        trace["iterations"] = i + 1
        print(f"\n  --- Iteration {i + 1} ---")
        write_files(workspace, code)

        validation = run_validation(workspace)
        trace["errors_per_iteration"].append(validation["errors"])

        if validation["passed"]:
            trace["final_status"] = "approved"
            print("  Validation passed.")
            return {"code": code, "trace": trace}

        print(f"  {len(validation['errors'])} error(s) found. Interpreting...")
        corrections = interpret_errors(validation["errors"], code)

        for cause in corrections.get("root_causes", []):
            print(f"  Root cause: {cause}")

        code = apply_corrections(code, corrections)

    trace["final_status"] = "failed_max_iterations"
    print("\n  Max iterations reached without passing validation.")
    return {"code": code, "trace": trace}