News-Ingestor is an service to fetch news articles from an api news source


# Goals

1. Fetch news articles from APIs 
2. Standardize and clean news sources 
3. Store in database or export as JSON for other services


# Data Sources

1. General News: NewsAPI, RSS Feeds, Reddit/Twitter
2. Finance: Finnhub, Alpha Vantage, Yahoo Finance API


# Data Scheme

schema: 
{
    source,
    asset,
    timestamp,
    headline,
    content,
    url,
    category: optional,
    tags: optional
}


