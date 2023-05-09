import logging
import os
from pathlib import Path

import arxiv
import requests
from dotenv import load_dotenv
from slack_sdk.webhook import WebhookClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("/workspace/main.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s : %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
)
logger.addHandler(handler)

load_dotenv()
GAS_ENDPOINT = os.getenv("GAS_ENDPOINT")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def main(query, max_fetch_num):
    webhook = WebhookClient(SLACK_WEBHOOK_URL)

    try:
        results = fetch_arxiv(query, max_fetch_num)
    except Exception as e:
        logger.error(e)
        webhook.send(text="arxiv接続エラー")
        exit()

    results = filter(results)
    contents = [parse(result) for result in results]
    blocks = format(contents)
    if blocks:
        logger.info("新着論文を{}件取得".format((len(blocks) + 1) // 2))
        webhook.send(text=f"arXiv: {query}", blocks=blocks)
    else:
        logger.info("新着論文なし")


def fetch_arxiv(query, max_fetch_num):
    search = arxiv.Search(
        query=query,
        max_results=max_fetch_num,
        sort_by=arxiv.SortCriterion.LastUpdatedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    return search.results()


def filter(results):
    path = Path("/workspace/send.log")
    if path.is_file():
        send_list = path.read_text().split("\n")
        send_list = [path for path in send_list if path != ""]
    else:
        send_list = []

    results = [result for result in results if result.entry_id not in send_list]

    send_list.extend([result.entry_id for result in results])
    send_list = send_list[-100:]
    path.write_text("\n".join(send_list))

    return results


def translate(text):
    params = {
        "text": text,
        "src": "en",
        "dest": "ja",
    }
    try:
        response = requests.get(GAS_ENDPOINT, params=params, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(e)
        return "翻訳失敗"


def parse(result):
    title = result.title
    title_ja = translate(result.title)
    summary = translate(result.summary.replace("\n", ""))
    url = result.entry_id
    return title, title_ja, summary, url


def format(contents):
    blocks = []
    for title, title_ja, summary, url in contents:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"【Title】\n{title}\n{title_ja}\n【Abstract】\n{summary}\n【URL】\n<{url}>\n",
                },
            },
        )
        blocks.append(
            {"type": "divider"},
        )
    return blocks[:-1]


if __name__ == "__main__":
    logger.info("開始")
    main(query="%22 Contrastive Learning %22", max_fetch_num=10)
    logger.info("終了")
