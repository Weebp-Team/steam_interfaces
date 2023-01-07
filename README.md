# steam-interfaces
![PyPI](https://img.shields.io/pypi/v/steam_interfaces?color=orange) ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Weebp-Team/steam_interfaces?color=blueviolet) ![License](https://img.shields.io/pypi/l/steam_interfaces?color=blueviolet) ![Forks](https://img.shields.io/github/forks/Weebp-team/steam_interfaces?style=social)

Python library for working with the Steam API.

**API Documentation:** 
- https://partner.steamgames.com/doc/webapi
- https://steamapi.xpaw.me

## Installation

```sh
pip install steam_interfaces 
```

## Usage
How get player info:
```python
from steam_interfaces import ISteamUser
import os

key = os.getenv('STEAM_API_KEY')

steam_user = ISteamUser(key)
user_info = steam_user.get_player_summaries(76561198248393810)
``` 

## Supported interfaces
- [IBroadcastService](https://partner.steamgames.com/doc/webapi/IBroadcastService)
- [ICheatReportingService](https://partner.steamgames.com/doc/webapi/ICheatReportingService)
- [IDOTA2Fantasy_570](https://steamapi.xpaw.me/#IDOTA2Fantasy_570)
- [IDOTA2MatchStats_570](https://steamapi.xpaw.me/#IDOTA2MatchStats_570)
- [IDOTA2Match_570](https://steamapi.xpaw.me/#IDOTA2Match_570)
- [IDOTA2StreamSystem_205790](https://steamapi.xpaw.me/#IDOTA2StreamSystem_205790)
- [IDOTAChat_570](https://steamapi.xpaw.me/#IDOTA2Match_570)
- [IEconMarketService](https://partner.steamgames.com/doc/webapi/IEconMarketService)
- [ILobbyMatchmakingService](https://partner.steamgames.com/doc/webapi/ILobbyMatchmakingService)
- [IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService)
- [ISiteLicenseService](https://partner.steamgames.com/doc/webapi/ISiteLicenseService)
- [ISteamApps](https://partner.steamgames.com/doc/webapi/ISteamApps)
- [ISteamCommunity](https://partner.steamgames.com/doc/webapi/ISteamCommunity)
- [ISteamGameServerStats](https://partner.steamgames.com/doc/webapi/ISteamGameServerStats)
- [ISteamNews](https://partner.steamgames.com/doc/webapi/ISteamNews)
- [ISteamUser](https://partner.steamgames.com/doc/webapi/ISteamUser)
- [ISteamWebAPIUtil](https://partner.steamgames.com/doc/webapi/ISteamWebAPIUtil)
- [IWorkshopService](https://partner.steamgames.com/doc/webapi/IWorkshopService)

## Dependencies

[requests](https://pypi.org/project/requests/)

## Contributing

Bug reports and/or pull requests are welcome

## License

[MIT](https://choosealicense.com/licenses/mit/)