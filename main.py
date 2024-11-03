"""メインの実行処理"""

from src.dbt_client import fetch_semantic_model_total, fetch_semantic_model_details
from src.erd_generator import generate_mermaid_erd


def main() -> str:
    # セマンティックモデルの総数を取得
    model_count = fetch_semantic_model_total(
        query_file_path="queries/get_total_semantic_models.graphql"
    )
    # セマンティックモデルの詳細情報を取得
    model_details = fetch_semantic_model_details(
        query_file_path="queries/get_semantic_model_metadata.graphql",
        model_count=model_count,
    )
    # mermaid.js形式のER図を生成
    return generate_mermaid_erd(model_details)


if __name__ == "__main__":
    mermaid_diagram = main()
    print(mermaid_diagram)
