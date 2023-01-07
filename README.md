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
- [IBroadcastService](docs/IBroadcastService.md)
- [ICheatReportingService](docs/ICheatReportingService.md)
- [IDOTA2Fantasy_570](docs/IDOTA2Fantasy_570.md)
- [IDOTA2MatchStats_570](docs/IDOTA2MatchStats_570.md)
- [IDOTA2Match_570](docs/IDOTA2Match_570.md)
- [IDOTA2StreamSystem_205790](docs/IDOTA2StreamSystem_205790.md)
- [IDOTAChat_570](docs/IDOTAChat_570.md)
- [IEconMarketService](docs/IEconMarketService.md)
- [ILobbyMatchmakingService](docs/ILobbyMatchmakingService.md)
- [IPlayerService](docs/IPlayerService.md)
- [ISiteLicenseService](docs/ISiteLicenseService.md)
- [ISteamApps](docs/ISteamApps.md)
- [ISteamCommunity](docs/ISteamCommunity.md)
- [ISteamGameServerStats](docs/ISteamGameServerStats.md)
- [ISteamNews](docs/ISteamNews.md)
- [ISteamUser](docs/ISteamUser.md)
- [ISteamWebAPIUtil](docs/ISteamWebAPIUtil.md)
- [IWorkshopService](docs/IWorkshopService.md)

## Dependencies

[requests](https://pypi.org/project/requests/)

## Contributing

Bug reports and/or pull requests are welcome

## License

[MIT](https://choosealicense.com/licenses/mit/)