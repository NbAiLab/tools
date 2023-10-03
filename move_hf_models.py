#!/usr/bin/env python3

import requests
import argparse
import fnmatch

def list_models(organization, token):
    url = "https://huggingface.co/api/models"
    params = {"author": organization}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Response Text: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

def move_models(pattern, src_organization, dest_organization, token, execute):
    if not pattern.startswith(src_organization):
        pattern = f"{src_organization}/{pattern}"
        
    models = list_models(src_organization, token)

    if models:
        filtered_models = [model['modelId'] for model in models if fnmatch.fnmatch(model['modelId'], pattern)]

        if filtered_models:
            print("Models that will be moved:")
            for model in filtered_models:
                print(f"{src_organization}/{model.split('/')[-1]} -> {dest_organization}/{model.split('/')[-1]}")
        else:
            print("No models match the given pattern.")

        if execute:
            print("Executing the model transfer... (not implemented)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move models from one HF organization to another.')
    parser.add_argument('--pattern', required=True, help='Pattern to match models.')
    parser.add_argument('--src_organization', default='NbAiLab', help='Source organization.')
    parser.add_argument('--dest_organization', default='NbAiLabArchive', help='Destination organization.')
    parser.add_argument('--token', required=True, help='Hugging Face API token.')
    parser.add_argument('--execute', action='store_true', help='Execute the model transfer.')

    args = parser.parse_args()
    move_models(args.pattern, args.src_organization, args.dest_organization, args.token, args.execute)

