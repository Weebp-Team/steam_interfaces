# IBroadcastService

## Description
Provides access to Steam broadcasts.

## PostGameDataFrame
Add a game meta data frame to broadcast.
```python
from steam_interfaces import IBroadcastService
import os

key = os.getenv('STEAM_API_KEY')
appid = 570
broadcast_id = 1234567890
steam_id = 76561198248393810
frame_data = 'frame_data'
broadcast_service = IBroadcastService(key)
broadcast_service.post_game_data_frame(appid, steam_id, broadcast_id,frame_data)
```