# ICheatReportingService

## Description
This service allows your game to report cheats and cheaters
to the VAC system and provides the toolset behind the Game Bans system.

## ReportPlayerCheating
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

## RequestPlayerGameBan
Requests a game ban on a specific player.

This is designed to be used after the incidents from ReportPlayerCheating have been reviewed and cheating has been confirmed.

```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
steamid = 76561198000000000
appid = 570
report_id = 1
cheatdescription = "Cheating"
duration = 0
delayban = False
flags = 0

report_service = ICheatReportingService(key)
report_service.request_player_game_ban(steamid, appid, report_id, cheatdescription, duration, delayban, flags)
```

## RemovePlayerGameBan
Remove a game ban on a player.

This is used if a Game ban is determined to be a false positive.

```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
steamid = 76561198000000000
appid = 570

report_service = ICheatReportingService(key)
report_service.remove_player_game_ban(steamid, appid)
```

## ReportCheatData
Reports cheat data. Only use on test account that is running the game but not in a multiplayer session.

This is for reporting specific cheats to the VAC system. This is done by running the cheat and the game and then calling this webapi.

```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
steamid = 76561198000000000
appid = 570
pathandfilename = "C:\\Users\\user\\Desktop\\report.txt"
webcheaturl = "https://www.cheat.com"
time_now = 1672936365
time_started = 0
time_stopped = 0
cheatname = "Cheat Name"
game_process_id = 0
cheat_process_id = 0
cheat_param_1 = 0
cheat_param_2 = 0

report_service = ICheatReportingService(key)
report_service.report_cheat_data(steamid, 
                                 appid, 
                                 pathandfilename, 
                                 webcheaturl, 
                                 time_now, 
                                 time_started, 
                                 time_stopped, 
                                 cheatname, 
                                 game_process_id, 
                                 cheat_process_id, 
                                 cheat_param_1, 
                                 cheat_param_2)
```

## GetCheatingReports
Get a list of cheating reports submitted for this app.

Used to gather the cheating reports so that they may be reviewed and a determination made.

NOTE: This call requires a publisher API key to use this method. As such this API MUST be called from a secure server, and can never be used directly by clients!

```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
appid = 570
timeend = 1672936365
timestart = 1672936265
reportadmin = 76561198000000000
includereports = True
includebans = True
steamid = 76561198000000000
report_service = ICheatReportingService(key)
report_service.get_cheating_reports(appid, 
                                    timeend, 
                                    timestart, 
                                    reportadmin, 
                                    includereports, 
                                    includebans, 
                                    steamid)
```

## RequestVacStatusForUser
Checks a user's VAC ban status and verifies a user's VAC session status. If verification fails, then do not let the user matchmake into a secure game.

This is used before a user enters matchmaking or joins a game. If the player is blocking VAC in some way and VAC can not scan the computer for cheats, it will report success = true and session_verified = false. Checking this webapi will allow you to prevent the user from matchmaking or joining a server and then just getting kicked by VAC a short time later ( with a k_EAuthSessionResponseVACCheckTimedOut result from an authentication callback ). The VAC system may not always have had time to fully determine if the clients system is cooperating, and if so it will report success = false. It is also possible for the players system to pass the initial check but then fail to respond later, in that case verification will succeed, but a k_EAuthSessionResponseVACCheckTimedOut may follow later.

```python
from steam_interfaces import ICheatReportingService
import os

key = os.getenv('STEAM_API_KEY')
steamid = 76561198000000000
appid = 570
session_id = 0

report_service = ICheatReportingService(key)
report_service.request_vac_status_for_user(steamid, appid, session_id)
```