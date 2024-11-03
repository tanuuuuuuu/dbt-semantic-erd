"""mermaid.js形式のER図生成を担当"""

from typing import Any


def append_primary_key_fields(
    entity_list: list[dict[str, str]], diagram_lines: list[str]
) -> None:
    """主キーフィールドを図に追加する"""
    for field in entity_list:
        if field["type"] == "primary":
            field_name = field["name"]
            diagram_lines.append(f"  {field_name} int64 PK")


def append_foreign_key_fields(
    entity_list: list[dict[str, str]], diagram_lines: list[str]
) -> None:
    """外部キーフィールドを図に追加する"""
    for field in entity_list:
        if field["type"] == "foreign":
            field_name = field["name"]
            diagram_lines.append(f"  {field_name} int64 FK")


def append_dimension_fields(
    dimension_list: list[dict[str, str]], diagram_lines: list[str]
) -> None:
    """ディメンションフィールドを図に追加する"""
    for field in dimension_list:
        field_name = field["name"]
        field_type = field["type"]
        diagram_lines.append(f"  {field_name} {field_type}")


def append_measure_fields(
    measure_list: list[dict[str, str]], diagram_lines: list[str]
) -> None:
    """メジャーフィールドを図に追加する"""
    for field in measure_list:
        field_name = field["name"]
        diagram_lines.append(f"  {field_name} int64")


def identify_fact_table(table_name: str) -> bool:
    """命名規則に基づいてファクトテーブルかどうかを判定する"""
    return table_name.endswith("_fact")


def extract_dimension_tables(model_details: list[dict[str, Any]]) -> list[str]:
    """セマンティックモデルの詳細からディメンションテーブルのリストを抽出する"""
    return [
        model["node"]["name"]
        for model in model_details
        if not identify_fact_table(model["node"]["name"])
    ]


def extract_fact_tables(model_details: list[dict[str, Any]]) -> list[str]:
    """セマンティックモデルの詳細からファクトテーブルのリストを抽出する"""
    return [
        model["node"]["name"]
        for model in model_details
        if identify_fact_table(model["node"]["name"])
    ]


def generate_table_relationships(model_details: list[dict[str, Any]]) -> list[str]:
    """階層構造を考慮してテーブル間のリレーションシップを生成する"""
    relationship_definitions: list[str] = []
    dimension_tables = extract_dimension_tables(model_details)
    fact_tables = extract_fact_tables(model_details)
    # ディメンションテーブルを上位層と下位層に分割
    split_point = len(dimension_tables) // 2
    upper_dimension_tables = dimension_tables[:split_point]
    lower_dimension_tables = dimension_tables[split_point:]
    # ファクトテーブルごとにリレーションシップを作成
    for fact_table in fact_tables:
        fact_table_model = next(
            model for model in model_details if model["node"]["name"] == fact_table
        )
        foreign_key_list = [
            entity["name"]
            for entity in fact_table_model["node"]["entities"]
            if entity["type"] == "foreign"
        ]
        for foreign_key in foreign_key_list:
            target_table = foreign_key.replace("_key", "_dimension")
            if "dimension" not in target_table:
                target_table = foreign_key.replace("_key", "")
            # ディメンション層に基づいてリレーションシップの方向を定義
            if target_table in upper_dimension_tables:
                relationship_definitions.append(
                    f'{target_table} ||--o{{ {fact_table} : "{foreign_key}"'
                )
            else:
                relationship_definitions.append(
                    f'{fact_table} }}o--|| {target_table} : "{foreign_key}"'
                )
    return relationship_definitions


def generate_mermaid_erd(model_details: list[dict[str, Any]]) -> str:
    """mermaid.js形式のER図を生成する"""
    diagram_lines: list[str] = ["erDiagram", ""]
    # テーブルスキーマの追加
    for model in model_details:
        # テーブル名の追加
        table_name = model["node"]["name"]
        diagram_lines.append(f"{table_name} {{")
        # テーブルフィールドの追加
        table_def = model["node"]
        append_primary_key_fields(table_def["entities"], diagram_lines)
        append_foreign_key_fields(table_def["entities"], diagram_lines)
        append_dimension_fields(table_def["dimensions"], diagram_lines)
        append_measure_fields(table_def["measures"], diagram_lines)
        diagram_lines.extend(["}", ""])
    # リレーションシップの追加
    diagram_lines.extend(generate_table_relationships(model_details) + [""])
    # スタイルの追加
    diagram_lines.extend(
        [
            "%%{init: {",
            '  "theme": "neutral",',
            '  "themeCSS": [',
            '    ".er.relationshipLabel { fill: black; }",',
            '    ".er.relationshipLabelBox { fill: white; }",',
            '    ".er.entityBox { fill: light; }",',
            '    "[id*=dimension] .er.entityBox { fill: #ffbf00; }",',
            '    "[id*=fact] .er.entityBox { fill: lightblue; }"',
            "  ]",
            "}}%%",
        ]
    )
    return "\n".join(diagram_lines)
