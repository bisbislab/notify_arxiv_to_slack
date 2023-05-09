# notify_arxiv_to_slack

指定キーワードで arXiv の新着論文を探し、Slack に通知するプログラム

## 前提環境

- Ubuntu
- Docker
- ローカルで動かすプログラムなので、PCは常に起動させっぱなし

## 準備

### .env ファイルの作成

1. `.env.template` をコピーし、`.env` ファイルを作成する
2. `USERNAME` にユーザー名、`USER_UID` に uid、`USER_GID` に gid を記述する（id コマンドで確認できる）

### 翻訳用に GAS スクリプトを作成

1. Google Drive にスプレッドシートを新規作成する
2. 拡張機能 → Apps Script
3. gas.js の内容をコピペ
4. デプロイ → 新しいデプロイ → 種類の選択：ウェブアプリ、アクセスできるユーザー：全員 → デプロイ
5. URL をコピーし、`.env` ファイルの `GAS_ENDPOINT` にペースト

### Slack に通知を送るための Webhook URL の取得

※ 以下カスタムインテグレーションを使用した方法であるが、Slack的には既に非推奨で、Slack Appを作成する方法の方が良さそう

1. https://slack.com/services/new/incoming-webhook にアクセス
2. 複数のワークスペースにログインしている場合：右上から対象とするワークスペースを選択する
3. 送信先のチャンネルを選択し、「Incoming Webhook インテグレーションの追加」を押下
4. 生成された Webhook URL をコピーし、`.env` ファイルの `SLACK_WEBHOOK_URL` にペースト

### Slack への通知時刻と頻度の設定

`crontab`ファイルを編集する

### 論文の検索キーワードと最大取得件数の設定

`main.py`最下部の`main()`呼び出しの引数を変更する  
検索キーワードは、`%22`で囲むと空白を含む複数単語を1つのワードとして扱える  
例えば、`Contrastive`と`Learning`をそれぞれ検索するのではなく、`Contrastive Learning`というワードで検索したい場合に使用

## Docker コマンド

### build & run

```sh
docker build -t notify_arxiv_to_slack .
docker run --detach -v .:/workspace --name notify_arxiv_to_slack notify_arxiv_to_slack
```

### 停止・削除

```sh
docker stop notify_arxiv_to_slack
docker rm notify_arxiv_to_slack
```
