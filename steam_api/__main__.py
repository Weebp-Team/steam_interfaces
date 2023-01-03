"""
:authors: Tarodictrl
:license: MIT License, see LICENSE file
:copyright: (c) 2022 Tarodictrl
"""
import requests
from typing import List, Union


class SteamAPI(object):
    """Class for interacting with the Steam API."""
    # TODO: Make validation for the API key.

    def __init__(self, key: str) -> None:
        """
        :param key: Steam API key
        :type key: str
        """
        self._key = key

    def _get(self, interface: str, method: str, version: int, params: dict) -> dict:
        """
        Send a GET request to the Steam API.
        :param interface: Steam API interface
        :type interface: str
        :param method: Steam API method
        :type method: str
        :param version: Steam API version
        :type version: int
        :param params: Steam API parameters
        :type params: dict
        :return: Steam API response
        :rtype: dict
        """
        url = f"https://api.steampowered.com/{interface}/{method}/v{version}/"
        params["key"] = self._key
        response = requests.get(url, params=params)
        return response.json()


class IBroadcastService(SteamAPI):
    """Provides access to Steam broadcasts."""

    def __init__(self, key: str) -> None:
        super().__init__(key)

    def post_game_data_frame(self, app_id: int,
                             steam_id: int,
                             broadcast_id: int,
                             frame_data: str) -> dict:
        """
        Add a game meta data frame to broadcast.
        :param app_id: Application ID
        :type app_id: int
        :param steam_id: Steam ID
        :type steam_id: int
        :param broadcast_id: Broadcast ID
        :type broadcast_id: int
        :param frame_data: Frame data
        :type frame_data: str
        :return: Steam API response
        """
        params = {
            "appid": app_id,
            "steamid": steam_id,
            "broadcastid": broadcast_id,
            "framedata": frame_data
        }

        return self._get("IBroadcastService", "PostGameDataFrame", 1, params)


class ICheatReportingService(SteamAPI):
    """This service allows your game to report cheats and cheaters
    to the VAC system and provides the toolset behind the Game Bans system."""
    # TODO: Add more methods.
    def __init__(self, key: str) -> None:
        super().__init__(key)

    def report_player_cheating(self,
                               steam_id: int,
                               appid: int,
                               steam_id_reporter: int,
                               app_data: int,
                               heuristic: bool = None,
                               detection: bool = None,
                               player_report: bool = None,
                               no_report_id: bool = None,
                               game_mode: int = None,
                               suspicion_start_time: int = None,
                               severity: int = None,
                               ) -> dict:
        """
        Report a player for cheating.
        :param steam_id: Steam ID
        :type steam_id: int
        :param appid: Application ID
        :type appid: int
        :param steam_id_reporter: (Optional) The Steam ID of the user or game server who is reporting the cheating.
        :type steam_id_reporter: int
        :param app_data: (Optional) App specific data about the type of cheating set by developer. (ex 1 = Aimbot, 2 = Wallhack, 3 = Griefing)
        :type app_data: int
        :param heuristic: (Optional) Extra information about the source of the cheating - was it a heuristic.
        :type heuristic: bool
        :param detection: (Optional) Extra information about the source of the cheating - was it a heuristic.
        :type detection: bool
        :param player_report: (Optional) Extra information about the source of the cheating - was it a player report.
        :type player_report: bool
        :param no_report_id: (Optional) Don't return reportid. This should only be passed if you don't intend to issue a ban based on this report.
        :type no_report_id: bool
        :param game_mode: (Optional) Extra information about state of game - was it a specific type of game play or game mode. (0 = generic).
        :type game_mode: int
        :param suspicion_start_time: (Optional) Extra information indicating how far back the game thinks is interesting for this user. Unix epoch time (time since Jan 1st, 1970).
        :type suspicion_start_time: int
        :param severity: (Optional) Level of severity of bad action being reported. Scale set by developer.
        :type severity: int
        :return: Steam API response
        """
        params = {
            "steamid": steam_id,
            "appid": appid,
            "steamidreporter": steam_id_reporter,
            "ap_data": app_data,
            "heuristic": heuristic,
            "detection": detection,
            "playerreport": player_report,
            "noreportid": no_report_id,
            "gamemode": game_mode,
            "suspicionstarttime": suspicion_start_time,
            "severity": severity
        }

        return self._get("ICheatReportingService", "ReportPlayerCheating", 1, params)

    def request_player_game_ban(self,
                                steamid: int,
                                appid: int,
                                reportid: int,
                                cheatdescription: str,
                                duration: int,
                                delayban: bool,
                                flags: int
                                ) -> dict:
        """
        Requests a game ban on a specific player.
        :param steamid: Steam ID
        :type steamid: int
        :param appid: The appid of the game.
        :type appid: int
        :param reportid: The reportid originally used to report cheating.
        :type reportid: int
        :param cheatdescription: Text describing cheating infraction.
        :type cheatdescription: str
        :param duration: 	Ban duration requested in seconds. (duration 0 will issue infinite - less than a year is a suspension and not visible on profile)
        :type duration: int
        :param delayban: Delay the ban according to default ban delay rules.
        :type delayban: bool
        :param flags: Additional information about the ban request. (Unused)
        :type flags: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "appid": appid,
            "reportid": reportid,
            "cheatdescription": cheatdescription,
            "duration": duration,
            "delayban": delayban,
            "flags": flags
        }

        return self._get("ICheatReportingService", "RequestPlayerGameBan", 1, params)


class ISteamUser(SteamAPI):
    """Used to access information and interact with users."""

    # TODO: Add more methods.
    def __init__(self, key: str) -> None:
        super().__init__(key)

    def get_player_summaries(self, steam_ids: Union[List[int], int]) -> dict:
        """
        Get player summaries.
        :param steam_ids: Steam ID
        :type steam_ids: Union[List[int], int]
        :return: Steam API response
        """
        if isinstance(steam_ids, int):
            steam_ids = [steam_ids]
        steam_ids = ",".join([str(steam_id) for steam_id in steam_ids])
        params = {
            "steamids": steam_ids
        }
        return self._get("ISteamUser", "GetPlayerSummaries", 2, params)
