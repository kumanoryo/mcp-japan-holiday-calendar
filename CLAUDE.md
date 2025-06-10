日本の休日・祝日情報を扱うMCP Serverを構築したい。

data/calendar.holidayから休日カレンダー情報を取得する。
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