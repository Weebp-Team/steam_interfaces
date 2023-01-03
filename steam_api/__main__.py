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
        # TODO: Make validation.
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
        :param steam_id_reporter: (Optional) The Steam ID of the user or game server who
        is reporting the cheating.
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

    def remove_player_game_ban(self,
                               steamid: int,
                               appid: int) -> dict:
        """
        Remove a game ban on a player.

        :param steamid: Steam ID
        :type steamid: int
        :param appid: The appid of the game.
        :type appid: int
        """

        params = {
            "steamid": steamid,
            "appid": appid
        }
        return self._get("ICheatReportingService", "RemovePlayerGameBan", 1, params)

    def get_cheating_reports(self,
                             appid: int,
                             timeend: int,
                             timebegin: int,
                             reportidmin: int,
                             includereports: bool,
                             includebans: bool,
                             steamid: int) -> dict:
        """
        Get a list of cheating reports submitted for this app.

        :param appid: The appid of the game.
        :type appid: int
        :param timeend: The end of the time range to search for reports. (Unix epoch time)
        :type timeend: int
        :param timebegin: The start of the time range to search for reports. (Unix epoch time)
        :type timebegin: int
        :param reportidmin: The minimum reportid to return.
        :type reportidmin: int
        :param includereports: Include reports in the response.
        :type includereports: bool
        :param includebans: Include bans in the response.
        :type includebans: bool
        :param steamid: (Optional) Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "timeend": timeend,
            "timebegin": timebegin,
            "reportidmin": reportidmin,
            "includereports": includereports,
            "includebans": includebans,
            "steamid": steamid
        }

        return self._get("ICheatReportingService", "GetCheatingReports", 1, params)

    def report_cheat_data(self,
                          steamid: int,
                          appid: int,
                          pathandfilename: str,
                          webcheaturl: str,
                          time_now: int,
                          time_started: int,
                          time_stopped: int,
                          cheatname: str,
                          game_process_id: int,
                          cheat_process_id: int,
                          cheat_param_1: int,
                          cheat_param_2: int) -> dict:
        """
        Reports cheat data.
        Only use on test account that is running the game but not in a multiplayer session.

        :param steamid: Steam ID
        :type steamid: int
        :param appid: The appid of the game.
        :type appid: int
        :param pathandfilename: Path and filename of the cheat.
        :type pathandfilename: str
        :param webcheaturl: URL of the cheat.
        :type webcheaturl: str
        :param time_now: The current time. (Unix epoch time)
        :type time_now: int
        :param time_started: The time the cheat started. (Unix epoch time)
        :type time_started: int
        :param time_stopped: The time the cheat stopped. (Unix epoch time)
        :type time_stopped: int
        :param cheatname: Descriptive name for the cheat.
        :type cheatname: str
        :param game_process_id: Process ID of the running game.
        :type game_process_id: int
        :param cheat_process_id: Process ID of the cheat process that ran.
        :type cheat_process_id: int
        :param cheat_param_1: Extra cheat data.
        :type cheat_param_1: int
        :param cheat_param_2: Extra cheat data.
        :type cheat_param_2: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "appid": appid,
            "pathandfilename": pathandfilename,
            "webcheaturl": webcheaturl,
            "time_now": time_now,
            "time_started": time_started,
            "time_stopped": time_stopped,
            "cheatname": cheatname,
            "game_process_id": game_process_id,
            "cheat_process_id": cheat_process_id,
            "cheat_param_1": cheat_param_1,
            "cheat_param_2": cheat_param_2
        }

        return self._get("ICheatReportingService", "ReportCheatData", 1, params)

    def request_vac_status_for_user(self,
                                    steamid: int,
                                    appid: int,
                                    session_id: int = None) -> dict:
        """
        Checks a user's VAC ban status and verifies a user's VAC session status.

        :param steamid: Steam ID
        :type steamid: int
        :param appid: The appid of the game.
        :type appid: int
        :param session_id: (Optional) Session ID
        :type session_id: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "appid": appid,
            "session_id": session_id
        }

        return self._get("ICheatReportingService", "RequestVacStatusForUser", 1, params)


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

    def check_app_ownership(self, steam_id: int, app_id: int) -> dict:
        """
        Check if a user owns a specific app.

        :param steam_id: Steam ID
        :type steam_id: int
        :param app_id: App ID
        :type app_id: int
        :return: Steam API response
        """

        params = {
            "steamid": steam_id,
            "appid": app_id
        }

        return self._get("ISteamUser", "CheckAppOwnership", 2, params)

    def get_app_price_info(self,
                           steamid: int,
                           appids: Union[List[int], int],
                           ) -> dict:
        """
        Get app price info.

        :param steamid: Steam ID
        :type steamid: int
        :param appids: App ID
        :type appids: Union[List[int], int]
        :return: Steam API response
        """

        if isinstance(appids, int):
            appids = [appids]
        appids = ",".join([str(appid) for appid in appids])

        params = {
            "steamid": steamid,
            "appids": appids
        }

        return self._get("ISteamUser", "GetAppPriceInfo", 1, params)

    def get_deleted_steam_ids(self,
                              rowversion: int,
                              ) -> dict:
        """
        You can use GetDeletedSteamIDs to retrieve a list of deleted accounts
        that owned your game(s) before deletion.

        :param rowversion: Row version
        :type rowversion: int
        :return: Steam API response
        """

        params = {
            "rowversion": rowversion
        }

        return self._get("ISteamUser", "GetDeletedSteamIDs", 1, params)

    def get_friends_list(self,
                         steamid: int,
                         relationship: str = None,
                         ) -> dict:
        """
        Get friends list.

        :param steamid: Steam ID
        :type steamid: int
        :param relationship: Relationship
        :type relationship: str
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "relationship": relationship
        }

        return self._get("ISteamUser", "GetFriendList", 1, params)

    def get_player_bans(self,
                        steam_ids: Union[List[int], int],
                        ) -> dict:
        """
        Get player bans.

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

        return self._get("ISteamUser", "GetPlayerBans", 1, params)

    def get_publisher_app_ownership(self,
                                    steamid: int) -> dict:
        """
        Get publisher app ownership.
        This method has previous versions which are no longer officially supported.
        They will continue to be usable, but it's highly recommended that you use the latest version.

        :param steamid: Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid
        }

        return self._get("ISteamUser", "GetPublisherAppOwnership", 3, params)

    def get_publisher_app_ownership_changes(self,
                                            packagerowversion: str,
                                            cdkeyrowversion: str) -> dict:
        """
        This method can be used to determine what SteamIDs have ownership changes
        starting from a particular package or key row version number.
        From the list of SteamIDs returned, a call to GetPublisherAppOwnership can then
        return the associated ownership data for the applications in the group associated with the key passed in.
        A partner may wish to track this data in conjunction with linked Steam Accounts
        to better understand the state of product ownership on Steam.

        :param packagerowversion: The unsigned 64-bit row version to read package changes from.
        The row version of data read up to will be returned for use in future calls.
        :type packagerowversion: str
        :param cdkeyrowversion: The unsigned 64-bit row version to read CD Key changes from.
        The row version of data read up to will be returned for use in future calls.
        :type cdkeyrowversion: str
        """

        params = {
            "packagerowversion": packagerowversion,
            "cdkeyrowversion": cdkeyrowversion
        }

        return self._get("ISteamUser", "GetPublisherAppOwnershipChanges", 1, params)

    def get_user_group_list(self,
                            steamid: int) -> dict:
        """
        Get user group list.

        :param steamid: Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid
        }

        return self._get("ISteamUser", "GetUserGroupList", 1, params)

    def resolve_vanity_url(self,
                           vanityurl: str,
                           url_type: int = 1) -> dict:
        """
        Resolve vanity URL.

        :param vanityurl: The vanity URL to get a SteamID for
        :type vanityurl: str
        :param url_type: The type of vanity URL. 1 (default): Individual profile, 2: Group, 3: Official game group
        :type url_type: int
        :return: Steam API response
        """

        params = {
            "vanityurl": vanityurl,
            "url_type": url_type
        }

        return self._get("ISteamUser", "ResolveVanityURL", 1, params)