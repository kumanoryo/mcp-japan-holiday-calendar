# mcp-japan-holiday-calendar

日本の休日・祝日情報を提供するMCPサーバー

## Claude Code での接続方法

### プロジェクトスコープ設定（最推奨）
このリポジトリには `.mcp.json` が含まれているため、プロジェクトをクローンして Claude Code を起動するだけで自動的に MCP サーバーが利用可能になります：

```bash
git clone https://github.com/kumanoryo/mcp-japan-holiday-calendar.git
cd mcp-japan-holiday-calendar
docker build -t mcp-japan-holiday .  # ローカルイメージをビルド
claude  # Claude Code を起動すると自動的に MCP サーバーが利用可能
```

> **注意**: `.mcp.json` はローカルビルドイメージ `mcp-japan-holiday` を参照します。事前に `docker build` でイメージを作成してください。

### Docker使用（個別設定）
Claude Code CLIで以下のコマンドを実行：

```bash
claude mcp add-json mcp-japan-holiday-calendar '{
  "command": "docker",
  "args": ["run", "--rm", "-i", "ghcr.io/kumanoryo/mcp-japan-holiday-calendar:latest"]
}'
```

### ローカル環境（Python直接実行）
Claude Code CLIで以下のコマンドを実行：

```bash
claude mcp add-json mcp-japan-holiday-calendar '{
  "command": "python",
  "args": ["-m", "holiday-calendar.main"],
  "cwd": "/path/to/mcp-japan-holiday-calendar"
}'
```

### 手動設定
以下の設定を `~/.claude/claude_desktop_config.json` に追加：

```json
{
  "mcpServers": {
    "mcp-japan-holiday-calendar": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/kumanoryo/mcp-japan-holiday-calendar:latest"]
    }
  }
}
```

## Cursor での接続方法

Cursor で MCP サーバーに接続するには、以下の設定を `cursor_settings.json` に追加してください：

```json
{
  "mcp": {
    "servers": {
      "mcp-japan-holiday-calendar": {
        "command": "python",
        "args": ["-m", "holiday-calendar.main"],
        "cwd": "/path/to/mcp-japan-holiday-calendar"
      }
    }
  }
}
```

## Docker Build

```bash
docker build -t mcp-japan-holiday-calendar .
```

## Docker Run

### ローカルビルド版
```bash
docker run -p 8080:8080 mcp-japan-holiday-calendar
```

### GitHub Container Registry版
```bash
docker run -p 8080:8080 ghcr.io/kumanoryo/mcp-japan-holiday-calendar:latest
```

## 利用可能な機能

MCPサーバーに接続すると、以下の機能がClaude Codeで利用可能になります：

### ツール一覧
- **`get_next_holiday()`**: 次の祝日を取得
- **`get_holiday_info(target_date)`**: 指定日の祝日情報を取得
- **`get_holidays_in_month(year, month)`**: 指定月の祝日一覧を取得
- **`get_business_days_count(year, month)`**: 指定月の営業日数を取得

### 使用例
Claude Codeで以下のような質問ができます：

```
次の祝日はいつですか？
2025年9月の祝日を教えてください
今月は何営業日ありますか？
2025年1月1日は祝日ですか？
```

### パフォーマンス
- **超高速検索**: 辞書インデックスによりO(1)検索を実現
- **大容量データ**: 26,298件の休日データを瞬時に検索
- **メモリ効率**: 起動時にデータをキャッシュして高速レスポンス
