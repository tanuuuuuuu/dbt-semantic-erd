"""dbt Cloud Discovery APIとの通信を担当"""

import os
from typing import Any

from dotenv import load_dotenv
import requests

# .envファイルを読み込む
load_dotenv()
DBT_ENVIRONMENT_ID = os.getenv("DBT_ENVIRONMENT_ID")
DBT_DISCOVERY_API_KEY = os.getenv("DBT_DISCOVERY_API_KEY")
DBT_DISCOVERY_API_ENDPOINT = os.getenv("DBT_DISCOVERY_API_ENDPOINT")


def fetch_semantic_model_total(query_file_path: str) -> int:
    """DBT Cloudからセマンティックモデルの総数を取得する"""
    with open(query_file_path, "r") as f:
        graphql_query = f.read()
    query_variables = {"environmentId": DBT_ENVIRONMENT_ID}
    response = requests.post(
        DBT_DISCOVERY_API_ENDPOINT,
        headers={
            "authorization": f"Bearer {DBT_DISCOVERY_API_KEY}",
            "content-type": "application/json",
        },
        json={"query": graphql_query, "variables": query_variables},
    )
    response_data = response.json()
    return response_data["data"]["environment"]["definition"]["semanticModels"][
        "totalCount"
    ]


def fetch_semantic_model_details(
    query_file_path: str, model_count: int
) -> list[dict[str, Any]]:
    """セマンティックモデルの詳細情報を取得する"""
    with open(query_file_path, "r") as f:
        graphql_query = f.read()
    query_variables = {"environmentId": DBT_ENVIRONMENT_ID, "first": model_count}
    response = requests.post(
        DBT_DISCOVERY_API_ENDPOINT,
        headers={
            "authorization": f"Bearer {DBT_DISCOVERY_API_KEY}",
            "content-type": "application/json",
        },
        json={"query": graphql_query, "variables": query_variables},
    )
    response_data = response.json()
    return response_data["data"]["environment"]["definition"]["semanticModels"]["edges"]
