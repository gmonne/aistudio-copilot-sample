# Import necessary modules
from __future__ import annotations
import tempfile
from pprint import pprint
from dotenv import load_dotenv
import os
import sys
import asyncio
import platform
import json
import pathlib
import pandas as pd
from functools import partial
from azure.ai.resources.client import AIClient
from azure.ai.resources.entities.models import Model
from azure.ai.resources.entities.deployment import Deployment
from azure.identity import DefaultAzureCredential
from openai.types.chat import ChatCompletion
import argparse  # Import argparse

# Load environment variables
load_dotenv()

source_path = "./src"

# build the index using the product catalog docs from data/3-product-info
def build_cogsearch_index(index_name, path_to_data):
    api_endpoint = f"https://ai-gmonneai947472757823.openai.azure.com/openai/deployments/{os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT']}/embeddings?api-version={os.environ['OPENAI_API_VERSION']}"
    print(api_endpoint)
    
    try:
        from azure.ai.resources.operations._index_data_source import LocalSource, ACSOutputConfig
        from azure.ai.generative.index import build_index
        from azure.ai.resources.client import AIClient
        from azure.identity import DefaultAzureCredential

        # Set up environment variables for cog search SDK
        os.environ["AZURE_COGNITIVE_SEARCH_TARGET"] = os.environ["AZURE_AI_SEARCH_ENDPOINT"]
        os.environ["AZURE_COGNITIVE_SEARCH_KEY"] = os.environ["AZURE_AI_SEARCH_KEY"]

        client = AIClient.from_config(DefaultAzureCredential())

        # Use the same index name when registering the index in AI Studio
        index = build_index(
            output_index_name=index_name,
            vector_store="azure_cognitive_search",
            embeddings_model=f"azure_open_ai://deployment/{os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT']}/model/{os.environ['AZURE_OPENAI_EMBEDDING_MODEL']}",
            data_source_url="https://product_info.com",
            index_input_config=LocalSource(input_data=path_to_data),
            acs_config=ACSOutputConfig(
                acs_index_name=index_name,
            ),
        )

        # register the index so that it shows up in the project
        cloud_index = client.indexes.create_or_update(index)

        print(f"Created index '{cloud_index.name}'")
        print(f"Local Path: {index.path}")
        print(f"Cloud Path: {cloud_index.path}")

    except Exception as e:
        print(f"Failed to build cogsearch index for {index_name}.")
        print(f"Attempted API Endpoint: {api_endpoint}")
        print(f"Error: {e}")


# Define a main function to encapsulate the script's logic
def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Script description here.")
    # Define arguments
    parser.add_argument("--build-index", action="store_true", help="Build the cogsearch index.")
    # You can add more arguments here based on the operations you want to support

    # Parse the arguments
    args = parser.parse_args()

    # Check if the build-index flag is set and call the function accordingly
    if args.build_index:
        # build_cogsearch_index(os.getenv("AZURE_AI_SEARCH_INDEX_NAME"), "./data/3-product-info")
        build_cogsearch_index("product-info", "./data/3-product-info")
        # Add more conditions here for other functionalities based on the parsed arguments

if __name__ == "__main__":
    main()
