import sys
import os
import uuid

import config
import openai
import pinecone
from openai.error import APIError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

openai.api_key = config.OPENAI_API_KEY

def get_embedding(text):
    num_retries = 10
    for attempt in range(num_retries):
        backoff = 2 ** (attempt + 2)
        try:
            return openai.Embedding.create(
                input=[text], model="text-embedding-ada-002"
            )["data"][0]["embedding"]
        except RateLimitError:
            pass
        except APIError as e:
            if e.http_status == 502:
                pass
            else:
                raise
            if attempt == num_retries - 1:
                raise
        time.sleep(backoff)

def create_memory(content, metadata):
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
    table_name = os.getenv("PINECONE_TABLE_NAME")

    dimension = 1536
    metric = "cosine"
    pod_type = "p1"

    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

    # Smoke test connection
    pinecone.whoami()

    if table_name not in pinecone.list_indexes():
        pinecone.create_index(table_name, dimension=dimension, metric=metric, pod_type=pod_type)

    index = pinecone.Index(table_name)

    vector = get_embedding(content)
    new_uuid = str(uuid.uuid4())
    result = index.upsert([(new_uuid, vector, metadata)])

    return result

# TODO: commit_to_memory_and_summarise_page_text (ie. general summary of page text, no question)
