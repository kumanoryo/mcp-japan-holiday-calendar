# トラブルシューティング

## GitHub Actions エラー

### スケジュールワークフローエラー
**症状**: スケジュールワークフローで「Check if base image has been updated」がエラー  
**エラー内容**: `date: invalid date` エラーでジョブが終了  
**解決済み**: 2025-06-11に修正済み。複雑な日時解析を削除して安全な24時間経過チェックに変更。

**修正内容**:
- `docker buildx imagetools inspect`の複雑な出力による`date`コマンドエラーを解決
- Manifest.Created形式の解析を削除
- 毎日のリビルドスケジュールを確実に実行するように簡素化

### ワークフロー手動実行
```bash
gh workflow run "Scheduled Base Image Update Check"
```

## MCPサーバー接続エラー

### Claude CodeでMCPサーバーが認識されない
**症状**: MCPサーバーが利用できない、ツールが表示されない  
**解決策**: 
1. `.mcp.json`があることを確認
   ```bash
   ls -la .mcp.json
   ```
2. プロジェクト選択をリセット
   ```bash
   claude mcp reset-project-choices
   ```
3. Claude Codeを再起動

### MCPサーバーが起動しない
**症状**: Dockerコンテナが起動しない  
**解決策**:
1. Dockerイメージの存在確認
   ```bash
   docker images | grep mcp-japan-holiday
   ```
2. ローカルビルド
   ```bash
   docker build -t mcp-japan-holiday .
   ```
3. 手動実行テスト
   ```bash
   docker run -i --rm mcp-japan-holiday
   ```

## Dockerビルドエラー

### ローカルでDockerビルドが失敗
**症状**: `docker build`コマンドでエラー  
**解決策**: 
1. Dockerが起動していることを確認
   ```bash
   docker --version
   docker info
   ```
2. キャッシュをクリア
   ```bash
   docker system prune
   ```
3. 最新のベースイメージを取得
   ```bash
   docker pull python:3.11-slim
   ```

### マルチプラットフォームビルドエラー
**症状**: `linux/arm64`プラットフォームでビルドエラー  
**解決策**:
1. BuildKitを有効化
   ```bash
   export DOCKER_BUILDKIT=1
   ```
2. Buildxセットアップ
   ```bash
   docker buildx create --use
   docker buildx inspect --bootstrap
   ```

## データファイルエラー

### 休日データの読み込みに失敗
**症状**: "休日データの読み込みに失敗しました" エラー  
**解決策**:
1. データファイルの存在確認
   ```bash
   ls -la data/calendar_holiday.json
   ```
2. ファイル権限確認
   ```bash
   chmod 644 data/calendar_holiday.json
   ```
3. JSONフォーマット検証
   ```bash
   head -5 data/calendar_holiday.json
   ```

### メモリ不足エラー
**症状**: 大容量データ読み込み時のメモリエラー  
**解決策**:
1. Dockerメモリ制限を増加
   ```bash
   docker run -m 1g -i --rm mcp-japan-holiday
   ```
2. システムメモリ使用量確認
   ```bash
   free -h
   ```

## パフォーマンス問題

### 検索が遅い
**症状**: 日付検索や月別検索に時間がかかる  
**確認事項**:
1. キャッシュが正常に動作しているか
2. インデックスが構築されているか
3. ログでパフォーマンス情報を確認

**期待値**:
- 日付検索: 0.001ms以下
- 月別検索: 0.023ms以下
- データ読み込み: 初回のみ約100ms

## ログ確認方法

### MCPサーバーログ
```bash
# Dockerログ確認
docker logs [container_id]

# リアルタイムログ
docker run -i --rm mcp-japan-holiday 2>&1 | tee mcp.log
```

### GitHub Actionsログ
```bash
# 最新の実行結果
gh run list --limit 5

# 詳細ログ
gh run view [run_id] --log-failed
```

## サポート・報告

問題が解決しない場合:
1. [GitHub Issues](https://github.com/kumanoryo/mcp-japan-holiday-calendar/issues)で報告
2. エラーログと実行環境を含めて報告
3. 再現手順を明記