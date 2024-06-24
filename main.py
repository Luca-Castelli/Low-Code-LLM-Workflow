import json
import logging
import os
import sys
from importlib import import_module
from typing import Any

import yaml

from helpers.utils import save_model_items

# Configure logging
logging.basicConfig(level=logging.INFO)

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def save_output(step_name: str, output_data: Any) -> None:
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{step_name}.json")
    if isinstance(output_data, list):
        save_model_items(output_data, file_path)
    else:
        with open(file_path, "w") as file:
            json.dump(output_data, file, indent=4, default=str)


def execute_step(step: dict, data: Any) -> Any:
    try:
        module_path, func_name = step["function"].rsplit(".", 1)
        module = import_module(module_path)
        function = getattr(module, func_name)

        input_type = step["input_type"]
        output_type = step["output_type"]

        # Handling input
        if input_type == "raw":
            input_data = data[step["input_var"]] if "input_var" in step else data
        elif input_type.startswith("List["):
            input_model_module, input_model_name = input_type[5:-1].rsplit(".", 1)
            InputModel = getattr(import_module(input_model_module), input_model_name)
            input_data = [InputModel.parse_obj(item) for item in data]
        else:
            input_model_module, input_model_name = input_type.rsplit(".", 1)
            InputModel = getattr(import_module(input_model_module), input_model_name)
            input_data = InputModel.parse_obj(data)

        # Function execution
        output_data = function(input_data)

        # Handling output
        if output_type != "raw":
            if output_type.startswith("List["):
                output_model_module, output_model_name = output_type[5:-1].rsplit(
                    ".", 1
                )
                OutputModel = getattr(
                    import_module(output_model_module), output_model_name
                )
                output_data = [
                    OutputModel.parse_obj(item.dict()) for item in output_data
                ]
            else:
                output_model_module, output_model_name = output_type.rsplit(".", 1)
                OutputModel = getattr(
                    import_module(output_model_module), output_model_name
                )
                output_data = OutputModel.parse_obj(output_data.dict())

        # Save output
        save_output(step["step_name"], output_data)

        return output_data

    except Exception as e:
        logging.error(f"Error executing step {step['step_name']}: {e}")
        raise


def run_workflow(workflow_file: str, initial_data: str):
    workflow = load_yaml(workflow_file)
    data = initial_data  # Initial input as a raw string

    step_outputs = {}

    for step in workflow["steps"]:
        if "input_var" in step:
            step_inputs = step_outputs[step["input_var"]]
        else:
            step_inputs = data

        step_outputs[step["output_var"]] = execute_step(step, step_inputs)
        logging.info(
            f"Step {step['step_name']} output: {step_outputs[step['output_var']]}"
        )

    final_output_var = workflow.get("final_output_var", "final_output")
    final_output = step_outputs.get(final_output_var, {})
    logging.info(f"Final output: {final_output}")


if __name__ == "__main__":
    # workflow_choice = input(
    #     "Enter the workflow to run (e.g., user/google_search/company_article_summary): "
    # ).strip()
    workflow_choice = "company_article_summary"
    initial_data = input("Enter the initial data: ").strip()

    workflow_file = f"workflows/{workflow_choice}_workflow.yml"
    if os.path.exists(workflow_file):
        run_workflow(workflow_file, initial_data)
    else:
        logging.error("Invalid workflow choice or workflow file does not exist")
