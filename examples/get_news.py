from steam_interfaces import ISteamNews
import os

key = os.getenv("STEAM_API_KEY")

news = ISteamNews(key)
info = news.get_news_for_app(570)

print(info)