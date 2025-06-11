# 日本の休日・祝日情報MCP Server

日本の休日・祝日情報を提供するMCPサーバーです。26,298件の休日データから高速検索を実現しています。

## 実装済み機能

### MCPツール
- `get_next_holiday()`: 次の祝日を取得
- `get_holiday_info(target_date)`: 指定日の祝日情報を取得  
- `get_holidays_in_month(year, month)`: 指定月の祝日一覧を取得
- `get_business_days_count(year, month)`: 指定月の営業日数を取得

### パフォーマンス最適化
- **データキャッシュ**: 起動時に1回だけ読み込み（65.6倍高速化）
- **辞書インデックス**: O(1)日付検索（2,042倍高速化）
- **月別インデックス**: O(k)月別検索（293倍高速化）

### CI/CD・自動化
- GitHub Actionsによる自動Docker buildとpush
- 毎日8:00AMの自動ベースイメージ更新チェック
- プロジェクトスコープMCP設定（.mcp.json）

## データソース

data/calendar_holiday.jsonから休日カレンダー情報を取得する。
jsonの出力元となったBigQueryのtable情報は以下のとおり。

```json
[
    {
      "description": "日付",
      "mode": "NULLABLE",
      "name": "date",
      "type": "DATE"
    },
    {
      "fields": [
        {
          "description": "年",
          "mode": "NULLABLE",
          "name": "year",
          "type": "INTEGER"
        },
        {
          "description": "月",
          "mode": "NULLABLE",
          "name": "month",
          "type": "INTEGER"
        },
        {
          "description": "日",
          "mode": "NULLABLE",
          "name": "day",
          "type": "INTEGER"
        }
      ],
      "description": "年月日をint型として格納",
      "mode": "NULLABLE",
      "name": "date_int",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "曜日(日月火水木金土を1234567で表記)",
          "mode": "NULLABLE",
          "name": "int",
          "type": "INTEGER"
        },
        {
          "description": "曜日(日月火水木金土で表記)",
          "mode": "NULLABLE",
          "name": "name",
          "type": "STRING"
        }
      ],
      "description": "曜日",
      "mode": "NULLABLE",
      "name": "dayofweek",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "祝日かどうか",
          "mode": "NULLABLE",
          "name": "flag",
          "type": "BOOLEAN"
        },
        {
          "description": "祝日の名前",
          "mode": "NULLABLE",
          "name": "name",
          "type": "STRING"
        }
      ],
      "description": "祝日の情報",
      "mode": "NULLABLE",
      "name": "public_holiday",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "営業日かどうか",
          "mode": "NULLABLE",
          "name": "flag",
          "type": "BOOLEAN"
        }
      ],
      "description": "銀行営業日（一般的な休日）の情報",
      "mode": "NULLABLE",
      "name": "bank_holiday",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "該当月の経過した営業日数",
          "mode": "NULLABLE",
          "name": "up",
          "type": "INTEGER"
        },
        {
          "description": "該当月の残りの営業日数",
          "mode": "NULLABLE",
          "name": "down",
          "type": "INTEGER"
        }
      ],
      "description": "営業日の情報",
      "mode": "NULLABLE",
      "name": "business_date_count",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "前日が祝日かどうか",
          "mode": "NULLABLE",
          "name": "flag",
          "type": "BOOLEAN"
        }
      ],
      "description": "前日が祝日かどうかの情報",
      "mode": "NULLABLE",
      "name": "day_before_holiday",
      "type": "RECORD"
    },
    {
      "fields": [
        {
          "description": "前日が祝日かどうか",
          "mode": "NULLABLE",
          "name": "flag",
          "type": "BOOLEAN"
        }
      ],
      "description": "翌日が祝日かどうかの情報",
      "mode": "NULLABLE",
      "name": "day_after_holiday",
      "type": "RECORD"
    }
]
```