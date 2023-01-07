# ISteamCommunity

## Description
Provides restricted access to Steam Community features.

## ReportAbuse
Report a player for cheating.
```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
appid = 570
app_data = 1
steam_id_reporter = 76561198000000000
steam_id = 76561198000000001
report_service = ICheatReportingService(key)

report_service.report_player_cheating(steam_id, appid, steam_id_reporter, app_data)
```