# IDOTA2Fantasy_570

## Description
Provides access to the Dota 2 fantasy league API.

## GetFantasyPlayerRawStats
Get fantasy player raw stats.
```python
from steam_interfaces import IDOTA2Fantasy_570
import os

key = os.getenv('STEAM_API_KEY')
account_id = 76561198000000000
league_id = 1
StartTime = 1673093543
EndTime = 1673093643

fantasy_service = IDOTA2Fantasy_570(key)
fantasy_service.get_fantasy_player_raw_stats(account_id, 
                                             league_id, 
                                             StartTime, 
                                             EndTime)
```
