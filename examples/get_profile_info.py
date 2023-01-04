from steam_interfaces import ISteamUser
import os

key = os.getenv("STEAM_API_KEY")

user = ISteamUser(key)
info = user.get_player_summaries(76561198248393810)

print(info)