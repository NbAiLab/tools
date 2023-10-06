#!/usr/bin/env python3

import requests
import argparse
import fnmatch
from huggingface_hub import move_repo
from huggingface_hub import list_models

def list_all(src_organization, token):
    models = list_models(author=src_organization)
    return list(models)

def move_models(pattern, src_organization, dest_organization, token, execute):
    if not pattern.startswith(src_organization):
        pattern = f"{src_organization}/{pattern}"

    models = list_all(src_organization, token)
    if models:
        filtered_models = [model.modelId for model in models if fnmatch.fnmatch(model.modelId, pattern)]

        if filtered_models:
            for model in filtered_models:
                from_id = model  # model ID already includes organization
                to_id = model.replace(src_organization, dest_organization)
                print(f"Planning to move {from_id} to {to_id}")

                if execute:
                    try:
                        move_repo(from_id=from_id, to_id=to_id)
                        print(f"Moved model {from_id} to {to_id}")
                    except Exception as e:
                        print(f"Error: {e}")
        else:
            print("No models match the given pattern.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move models from one HF organization to another.')
    parser.add_argument('--pattern', required=True, help='Pattern to match models.')
    parser.add_argument('--src_organization', default='NbAiLab', help='Source organization.')
    parser.add_argument('--dest_organization', default='NbAiLabArchive', help='Destination organization.')
    parser.add_argument('--token', required=True, help='Hugging Face API token.')
    parser.add_argument('--execute', action='store_true', help='Execute the model transfer.')

    args = parser.parse_args()
    move_models(args.pattern, args.src_organization, args.dest_organization, args.token, args.execute)

