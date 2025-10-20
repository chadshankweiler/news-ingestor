import requests
import pandas as pd
from datetime import date, datetime, timedelta
import json
import os
import click

from dotenv import load_dotenv, find_dotenv

# Load .env
load_dotenv(find_dotenv(usecwd=True))

class News:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def getNews(
            self, 
            query: str = "Apple", 
            from_date: str | None = None, 
            to_date: str | None = None, 
            page: int = 1
        ):
        """ 
        Fetch news by NewsAPI and write to output.json

        Defaults:
          - query="Apple"
          - from_date = 7 days ago (YYYY-MM-DD)
          - to_date   = today (YYYY-MM-DD)
          - page=1, page_size=100, sort_by="publishedAt"
        """

        if from_date is None:
            from_date = (date.today() - timedelta(days=7)).isoformat()
        if to_date is None:
            to_date = date.today().isoformat()

        params = {
                "q": query,
                "from": from_date,
                "to": to_date,
                "sortBy": "publishedAt",
                "pageSize": 100,
                page: page,
                "apiKey": self.api_key 
            }

        url = ('https://newsapi.org/v2/everything?')

            


        try: 
            response = requests.get(url, params=params, timeout=30)
            data = response.json()

            with open('output.json', 'w', encoding='utf-8') as f: 
                json.dump(data, f, ensure_ascii=False, indent=4)

            return data 
        except IOError as e: 
            print(e)



## --- CLi Layer (click) --- #
@click.group()
@click.option(
        "--api",
        "--api-key",
        "api_key",
        envvar="NEWS_API_KEY",
        required=True,
        help="Your NewsAPI key (or set Env as NEWS_API_KEY)"
        )

@click.pass_context
def cli(ctx, api_key):
    ctx.obj = News(api_key)


# --- Subcommand: getNews() --- #

@cli.command("get-news")
@click.option("--query", "-q", default=None, help="Search Query (defaults to Apple)")
@click.option("--from", "from_date", default=None, help="Start date YYYY-MM-DD (defaults to 7 days ago).")
@click.option("--to", "to_date", default=None, help="End date YYYY-MM-DD (defaults to today).")
@click.option("--page", default=1, show_default=True, type=int, help="Page number.")
@click.option("--page-size", "page_size", default=100, show_default=True, type=int, help="Results per page.")
@click.option(
    "--sort-by",
    "sort_by",
    default="publishedAt",
    show_default=True,
    type=click.Choice(["relevancy", "popularity", "publishedAt"]),
    help="Sort order for NewsAPI results.",
)

@click.pass_obj
def getNewsCli(news: News, query, from_date, to_date, page, page_size, sort_by):
    data = news.getNews(
            query=query or "Apple",
            from_date=from_date,
            to_date=to_date,
            page=page,
            )
    click.echo(f"Wrote {len(data.get('articles', []))} articles to output.json")


if __name__ == "__main__":
    cli()

