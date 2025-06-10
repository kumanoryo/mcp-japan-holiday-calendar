# mcp-japan-holiday-calendar

日本の休日・祝日情報を提供するMCPサーバー

## Claude Code での接続方法

### Docker使用（推奨）
Claude Code CLIで以下のコマンドを実行：

```bash
claude mcp add-json '{
  "mcpServers": {
    "mcp-japan-holiday-calendar": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/kumanoryo/mcp-japan-holiday-calendar:latest"]
    }
  }
}'
```

### ローカル環境（Python直接実行）
Claude Code CLIで以下のコマンドを実行：

```bash
claude mcp add-json '{
  "mcpServers": {
    "mcp-japan-holiday-calendar": {
      "command": "python",
      "args": ["-m", "holiday-calendar.main"],
      "cwd": "/path/to/mcp-japan-holiday-calendar"
    }
  }
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
