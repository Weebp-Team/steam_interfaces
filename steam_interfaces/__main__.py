"""
:authors: Tarodictrl
:license: MIT License, see LICENSE file
:copyright: (c) 2022 Tarodictrl
"""
import requests
from typing import List, Union


class _SteamAPI(object):
    """Class for interacting with the Steam API."""
    def __init__(self, key: Union[str, None]) -> None:
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
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise ValueError("Invalid API key or access denied!")

    def _post(self, interface: str, method: str, version: int, params: dict) -> dict:
        """
        Send a POST request to the Steam API.

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
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise ValueError("Invalid API key")


class IBroadcastService(_SteamAPI):
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

        return self._post("IBroadcastService", "PostGameDataFrame", 1, params)


class ICheatReportingService(_SteamAPI):
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
        :param app_data: (Optional) App specific data about the type of cheating set by developer.
        (ex 1 = Aimbot, 2 = Wallhack, 3 = Griefing)
        :type app_data: int
        :param heuristic: (Optional) Extra information about the source of the cheating - was it a heuristic.
        :type heuristic: bool
        :param detection: (Optional) Extra information about the source of the cheating - was it a heuristic.
        :type detection: bool
        :param player_report: (Optional) Extra information about the source of the cheating - was it a player report.
        :type player_report: bool
        :param no_report_id: (Optional) Don't return reportid.
        This should only be passed if you don't intend to issue a ban based on this report.
        :type no_report_id: bool
        :param game_mode: (Optional) Extra information about state of game - was it a specific
        type of game play or game mode. (0 = generic).
        :type game_mode: int
        :param suspicion_start_time: (Optional) Extra information indicating how far back the game thinks
        is interesting for this user. Unix epoch time (time since Jan 1st, 1970).
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

        return self._post("ICheatReportingService", "ReportPlayerCheating", 1, params)

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
        :param duration: 	Ban duration requested in seconds.
        (duration 0 will issue infinite - less than a year is a suspension and not visible on profile)
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

        return self._post("ICheatReportingService", "RequestPlayerGameBan", 1, params)

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
        return self._post("ICheatReportingService", "RemovePlayerGameBan", 1, params)

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

        return self._post("ICheatReportingService", "ReportCheatData", 1, params)

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

        return self._post("ICheatReportingService", "RequestVacStatusForUser", 1, params)


class ISteamUser(_SteamAPI):
    """Used to access information and interact with users."""
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


class IDOTAChat_570(_SteamAPI):
    """Dota 2 Match chat API."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_channel_members(self,
                            channel_type: int,
                            channel_name: int
                            ) -> dict:
        """
        Get channel members.

        :param channel_type: Channel type
        :type channel_type: int
        :param channel_name: Channel name
        :type channel_name: int
        :return: Steam API response
        """

        params = {
            "channel_type": channel_type,
            "channel_name": channel_name
        }

        return self._get("IDOTAChat_570", "GetChannelMembers", 1, params)


class IDOTA2MatchStats_570(_SteamAPI):
    """Dota 2 Match Stats API."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_realtime_stats(self,
                           server_steam_id: int,
                           ) -> dict:
        """
        Get match stats.

        :param server_steam_id: Server Steam ID
        :type server_steam_id: int
        :return: Steam API response
        """

        params = {
            "server_steam_id": server_steam_id
        }

        return self._get("IDOTA2MatchStats_570", "GetMatchStats", 1, params)


class IDOTA2Fantasy_570(_SteamAPI):
    """Dota 2 fantasy API."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_fantasy_player_raw_stats(self,
                                     account_id: int,
                                     leagueid: int,
                                     StartTime: int,
                                     EndTime: int,
                                     ) -> dict:
        """
        Get fantasy player raw stats.

        :param account_id: Account ID
        :type account_id: int
        :param leagueid: League ID
        :type leagueid: int
        :param StartTime: Start time
        :type StartTime: int
        :param EndTime: End time
        :type EndTime: int
        :return: Steam API response
        """

        params = {
            "account_id": account_id,
            "leagueid": leagueid,
            "StartTime": StartTime,
            "EndTime": EndTime
        }

        return self._get("IDOTA2Fantasy_570", "GetFantasyPlayerRawStats", 1, params)

    def get_player_info(self,
                        account_id: int,
                        ) -> dict:
        """
        Get player info.

        :param account_id: Account ID
        :type account_id: int
        :return: Steam API response
        """

        params = {
            "account_id": account_id
        }

        return self._get("IDOTA2Fantasy_570", "GetPlayerInfo", 1, params)

    def get_player_infos(self,
                         account_ids: Union[List[int], int],
                         ) -> dict:
        """
        Get player infos.

        :param account_ids: Account IDs
        :type account_ids: Union[List[int], int]
        :return: Steam API response
        """

        if isinstance(account_ids, int):
            account_ids = [account_ids]
        account_ids = ",".join([str(account_id) for account_id in account_ids])

        params = {
            "account_ids": account_ids
        }

        return self._get("IDOTA2Fantasy_570", "GetPlayerInfos", 1, params)


class IDOTA2StreamSystem_205790(_SteamAPI):
    """Dota 2 Stream System API."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_broadcaster_info(self,
                             broadcaster_steam_id: int,
                             league_id: int = None
                             ) -> dict:

        """
        Get broadcaster info.

        :param broadcaster_steam_id: Broadcaster Steam ID
        :type broadcaster_steam_id: int
        :param league_id: League ID
        :type league_id: int
        :return: Steam API response
        """

        params = {
            "broadcaster_steam_id": broadcaster_steam_id,
            "league_id": league_id
        }

        return self._get("IDOTA2StreamSystem_205790", "GetBroadcasterInfo", 1, params)


class IPlayerService(_SteamAPI):
    """Provides additional methods for interacting with Steam Users."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_recently_played_games(self,
                                  steamid: int,
                                  count: int = 0
                                  ) -> dict:
        """
        Get recently played games.

        :param steamid: Steam ID
        :type steamid: int
        :param count: Number of games to return
        :type count: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "count": count
        }

        return self._get("IPlayerService", "GetRecentlyPlayedGames", 1, params)

    def get_owned_games(self,
                        steamid: int,
                        include_appinfo: int = 0,
                        include_played_free_games: int = 0,
                        appids_filter: Union[List[int], int] = None
                        ) -> dict:
        """
        Get owned games.

        :param steamid: Steam ID
        :type steamid: int
        :param include_appinfo: Include app info
        :type include_appinfo: int
        :param include_played_free_games: Include played free games
        :type include_played_free_games: int
        :param appids_filter: App IDs filter
        :type appids_filter: Union[List[int], int]
        :return: Steam API response
        """

        if isinstance(appids_filter, int):
            appids_filter = [appids_filter]
        if appids_filter:
            appids_filter = ",".join([str(appid) for appid in appids_filter])

        params = {
            "steamid": steamid,
            "include_appinfo": include_appinfo,
            "include_played_free_games": include_played_free_games,
            "appids_filter": appids_filter
        }

        return self._get("IPlayerService", "GetOwnedGames", 1, params)

    def get_steam_level(self,
                        steamid: int,
                        ) -> dict:
        """
        Get Steam level.

        :param steamid: Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid
        }

        return self._get("IPlayerService", "GetSteamLevel", 1, params)

    def get_badges(self,
                   steamid: int,
                   ) -> dict:
        """
        Get badges.

        :param steamid: Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid
        }

        return self._get("IPlayerService", "GetBadges", 1, params)

    def get_community_badge_progress(self,
                                     steamid: int,
                                     badgeid: int,
                                     ) -> dict:
        """
        Get community badge progress.

        :param steamid: Steam ID
        :type steamid: int
        :param badgeid: Badge ID
        :type badgeid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid,
            "badgeid": badgeid
        }

        return self._get("IPlayerService", "GetCommunityBadgeProgress", 1, params)


class ISteamApps(_SteamAPI):
    """Used to access data about applications on Steam."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_app_betas(self,
                      appid: int) -> dict:
        """
        Gets all the beta branches for the specified application.

        :param appid: Application ID
        :type appid: int
        :return: Steam API response
        """

        params = {
            "appid": appid
        }

        return self._get("ISteamApps", "GetAppBeta", 1, params)

    def get_app_builds(self,
                       appid: int,
                       count: int = 10,
                       ) -> dict:
        """
        Gets an applications build history.

        :param appid: Application ID
        :type appid: int
        :param count: Number of builds to return
        :type count: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "count": count
        }

        return self._get("ISteamApps", "GetAppBuilds", 1, params)

    def get_app_depot_versions(self,
                               appid: int,
                               ) -> dict:
        """
        Gets an applications depot versions.

        :param appid: Application ID
        :type appid: int
        :return: Steam API response
        """

        params = {
            "appid": appid
        }

        return self._get("ISteamApps", "GetAppDepotVersions", 1, params)

    def get_app_list(self) -> dict:
        """
        Gets a list of all applications.

        :return: Steam API response
        """

        return self._get("ISteamApps", "GetAppList", 1, {})

    def get_partner_app_list_for_web_API_Key(self,
                                             type_filter: str = None,
                                             ) -> dict:
        """
        Get a list of appIDs associated with a WebAPI key.

        :param type_filter: Type filter
        :type type_filter: str
        :return: Steam API response
        """

        params = {
            "type_filter": type_filter
        }

        return self._get("ISteamApps", "GetPartnerAppListForWebAPIKey", 1, params)

    def get_players_banned(self,
                           appid: int) -> dict:
        """
        Gets a list of banned players.

        :param appid: Application ID
        :type appid: int
        :return: Steam API response
        """

        params = {
            "appid": appid
        }

        return self._get("ISteamApps", "GetPlayersBanned", 1, params)

    def get_server_list(self,
                        filter: str = None,
                        limit: int = None,
                        ) -> dict:
        """
        Gets a list of servers.

        :param filter: Query filter string
        :type filter: str
        :param limit: Limit number of servers in the response
        :type limit: int
        :return: Steam API response
        """

        params = {
            "filter": filter,
            "limit": limit
        }

        return self._get("ISteamApps", "GetServersAtAddress", 1, params)

    def get_servers_at_address(self,
                               addr: str,
                               ) -> dict:
        """
        Gets a list of servers at an address.

        :param addr: Address
        :type addr: str
        :return: Steam API response
        """

        params = {
            "addr": addr
        }

        return self._get("ISteamApps", "GetServersAtAddress", 1, params)

    def set_app_build_live(self,
                           appid: int,
                           buildid: int,
                           betakey: str,
                           description: str = None
                           ) -> dict:
        """
        Sets an applications build as live.

        :param appid: Application ID
        :type appid: int
        :param buildid: Build ID
        :type buildid: int
        :param betakey: beta key, required. Use public for default branch
        :type betakey: str
        :param description: optional description for this build
        :type description: str
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "buildid": buildid,
            "betakey": betakey,
            "description": description
        }

        return self._post("ISteamApps", "SetAppBuildLive", 1, params)

    def up_to_date_check(self,
                         appid: int,
                         version: int,
                         ) -> dict:
        """
        Checks if an application is up-to-date.

        :param appid: Application ID
        :type appid: int
        :param version: The installed version of the game
        :type version: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "version": version
        }

        return self._get("ISteamApps", "UpToDateCheck", 1, params)


class ISteamNews(_SteamAPI):
    """Provides access to the Steam News functionality. """
    def __init__(self, key: str):
            super().__init__(key)

    def get_news_for_app(self,
                        appid: int,
                        count: int = 20,
                        maxlength: int = None,
                        enddate: int = None,
                        feeds: str = None,
                        ) -> dict:
        """
        Gets news for an application.

        :param appid: Application ID
        :type appid: int
        :param count: Number of news items to return
        :type count: int
        :param maxlength: Maximum length of the news item
        :type maxlength: int
        :param enddate: Unix timestamp of the last news item to return
        :type enddate: int
        :param feeds: Comma separated list of feed names to return news for
        :type feeds: str
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "count": count,
            "maxlength": maxlength,
            "enddate": enddate,
            "feeds": feeds
        }

        return self._get("ISteamNews", "GetNewsForApp", 2, params)

    def get_news_from_app_authed(self,
                                 appid: int,
                                 maxlength: int = 0,
                                 enddate: int = None,
                                 count: int = 20,
                                 feeds: str = None,
                                 ) -> dict:
        """
        Get the news for the specified app.
        Publisher only version that can return info for unreleased games.

        :param appid: Application ID
        :type appid: int
        :param maxlength: Maximum length of the news item
        :type maxlength: int
        :param enddate: Unix timestamp of the last news item to return
        :type enddate: int
        :param count: Number of news items to return
        :type count: int
        :param feeds: Comma separated list of feed names to return news for
        :type feeds: str
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "maxlength": maxlength,
            "enddate": enddate,
            "count": count,
            "feeds": feeds
        }

        return self._get("ISteamNews", "GetNewsForApp", 2, params)


class IWorkshopService(_SteamAPI):
    """Additional Steam Workshop service methods for publishers."""
    def __init__(self, key: str):
        super().__init__(key)

    def set_item_payment_rules(self,
                               appid: int,
                               gameitemid: int,
                               associated_workshop_files: dict,
                               partner_accounts: dict,
                               make_workshop_files_subscribable: bool,
                               validate_only: bool = False
                               ) -> dict:
        """
        Sets the payment rules for a specific item.

        :param appid: Application ID
        :type appid: int
        :param gameitemid: Game item ID
        :type gameitemid: int
        :param associated_workshop_files: Dict of associated workshop files
        :type associated_workshop_files: dict
        :param partner_accounts: Dict of partner accounts
        :type partner_accounts: dict
        :param make_workshop_files_subscribable: Allow users to subscribe to the workshop items?
        :type make_workshop_files_subscribable: bool
        :param validate_only: Only validates the rules and does not persist them.
        :type validate_only: bool
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "gameitemid": gameitemid,
            "associated_workshop_files": associated_workshop_files,
            "partner_accounts": partner_accounts,
            "make_workshop_files_subscribable": make_workshop_files_subscribable,
            "validate_only": validate_only
        }

        return self._post("IWorkshopService", "SetItemPaymentRules", 1, params)

    def get_finalized_contributors(self,
                                   appid: int,
                                   gameitemid: int,
                                   ) -> dict:
        """
        Get a list of contributors for a specific app/workshop item combination.

        :param appid: Application ID
        :type appid: int
        :param gameitemid: Game item ID
        :type gameitemid: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "gameitemid": gameitemid
        }

        return self._get("IWorkshopService", "GetFinalizedContributors", 1, params)

    def get_item_daily_revenue(self,
                               item_id: int,
                               date_start: int,
                               date_end: int,
                               ) -> dict:
        """
        Gets the daily revenue for a specific item.

        :param item_id: Item ID
        :type item_id: int
        :param date_start: Start date
        :type date_start: int
        :param date_end: End date
        :type date_end: int
        :return: Steam API response
        """

        params = {
            "item_id": item_id,
            "date_start": date_start,
            "date_end": date_end
        }

        return self._get("IWorkshopService", "GetItemDailyRevenue", 1, params)

    def populate_item_descriptions(self,
                                   appid: int,
                                   languages: list,
                                   ) -> dict:
        """
        Populate block of item descriptions.

        :param appid: Application ID
        :type appid: int
        :param languages: List of languages
        :type languages: list
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "languages": languages
        }

        return self._post("IWorkshopService", "PopulateItemDescriptions", 1, params)


class ISteamGameServerStats(_SteamAPI):
    """Interface to get and interact with game server stats."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_game_server_player_stats_for_game(self,
                                              gameid: int,
                                              appid: int,
                                              rangestart: int,
                                              rangeend: int,
                                              maxresults: int = 1000,
                                              ) -> dict:
        """
        Gets the game server player stats for a specific game.

        :param gameid: Game ID
        :type gameid: int
        :param appid: Application ID
        :type appid: int
        :param rangestart: Start of the range
        :type rangestart: int
        :param rangeend: End of the range
        :type rangeend: int
        :param maxresults: Maximum results to return
        :type maxresults: int
        :return: Steam API response
        """

        params = {
            "gameid": gameid,
            "appid": appid,
            "rangestart": rangestart,
            "rangeend": rangeend,
            "maxresults": maxresults
        }

        return self._get("ISteamGameServerStats", "GetGameServerPlayerStatsForGame", 1, params)


class ISteamWebAPIUtil(_SteamAPI):
    def __init__(self):
        super().__init__(None)

    def get_server_info(self):
        """ Gets the server info. """
        return self._get("ISteamWebAPIUtil", "GetServerInfo", 1, {})

    def get_supported_API_list(self):
        """ Returns a list of all supported API methods. """
        return self._get("ISteamWebAPIUtil", "GetSupportedAPIList", 1, {})


class IEconMarketService(_SteamAPI):
    def __init__(self, key: str):
        super().__init__(key)

    def get_market_eligibility(self,
                               steamid: int) -> dict:
        """
        Checks whether an account is allowed to use the market.

        :param steamid: Steam ID
        :type steamid: int
        :return: Steam API response
        """

        params = {
            "steamid": steamid
        }

        return self._get("IEconMarketService", "GetMarketEligibility", 1, params)

    def cancel_app_listings_for_user(self,
                                     appid: int,
                                     steamid: int,
                                     synchronous: bool
                                     ) -> dict:
        """
        Cancels all of a user's listings for a specific app ID.

        :param appid: Application ID
        :type appid: int
        :param steamid: The SteamID of the user whose listings should be canceled
        :type steamid: int
        :param synchronous: Whether to wait until all listings have been canceled before returning the response.
        :type synchronous: bool
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "steamid": steamid,
            "synchronous": synchronous
        }

        return self._post("IEconMarketService", "CancelAppListingsForUser", 1, params)

    def get_asset_ID(self,
                     appid: int,
                     listingid: int,
                     ) -> dict:
        """
        Returns the asset ID of the item sold in a listing.

        :param appid: Application ID
        :type appid: int
        :param listingid: Listing ID
        :type listingid: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "listingid": listingid
        }

        return self._get("IEconMarketService", "GetAssetID", 1, params)

    def get_popular(self,
                    language: str,
                    start: int,
                    filter_appid: int,
                    ecurrency: int,
                    rows: int = None,
                    ) -> dict:
        """
        Gets the most popular items.

        :param language: The language to use in item descriptions
        :type language: str
        :param start: Number of rows per page
        :type start: int
        :param filter_appid: If present, the app ID to limit results to
        :type filter_appid: int
        :param ecurrency: If present, prices returned will be represented in this currency
        :type ecurrency: int
        :param rows: Rows to return
        :type rows: int
        :return: Steam API response
        """

        params = {
            "language": language,
            "start": start,
            "filter_appid": filter_appid,
            "ecurrency": ecurrency,
            "rows": rows
        }

        return self._get("IEconMarketService", "GetPopular", 1, params)


class ILobbyMatchmakingService(_SteamAPI):
    """Provides access to the Steam Lobby methods."""
    def __init__(self, key: str):
        super().__init__(key)

    def create_lobby(self,
                     appid: int,
                     max_members: int,
                     lobby_type: int,
                     steamid_invited_members: list,
                     lobby_name: str = None,
                     input_json: str = None,
                     lobby_metadata: dict = None,
                     ) -> dict:
        """
        Creates a new lobby.

        :param appid: Application ID
        :type appid: int
        :param max_members: Maximum members
        :type max_members: int
        :param lobby_type: Lobby type
        :type lobby_type: int
        :param steamid_invited_members: List of Steam IDs to invite
        :type steamid_invited_members: list
        :param lobby_name: Lobby name
        :type lobby_name: str
        :param input_json: JSON input
        :type input_json: str
        :param lobby_metadata: Lobby metadata
        :type lobby_metadata: dict
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "max_members": max_members,
            "lobby_type": lobby_type,
            "steamid_invited_members": steamid_invited_members,
            "lobby_name": lobby_name,
            "input_json": input_json,
            "lobby_metadata": lobby_metadata
        }

        return self._post("ILobbyMatchmakingService", "CreateLobby", 1, params)

    def remove_user_from_lobby(self,
                               appid: int,
                               steamid_to_remove: int,
                               steamid_lobby: int,
                               input_json: dict = None,
                               ) -> dict:
        """
        Removes a user from a lobby.

        :param appid: Application ID
        :type appid: int
        :param steamid_to_remove: Steam ID to remove
        :type steamid_to_remove: int
        :param steamid_lobby: Steam ID of the lobby
        :type steamid_lobby: int
        :param input_json: JSON input
        :type input_json: dict
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "steamid_to_remove": steamid_to_remove,
            "steamid_lobby": steamid_lobby,
            "input_json": input_json
        }

        return self._post("ILobbyMatchmakingService", "RemoveUserFromLobby", 1, params)

    def get_lobby_data(self,
                       appid: int,
                       steamid_lobby: int,
                       ):
        """
        Gets the lobby data.

        :param appid: Application ID
        :type appid: int
        :param steamid_lobby: Steam ID of the lobby
        :type steamid_lobby: int
        :return: Steam API response
        """

        params = {
            "appid": appid,
            "steamid_lobby": steamid_lobby
        }

        return self._get("ILobbyMatchmakingService", "GetLobbyData", 1, params)


class ISiteLicenseService(_SteamAPI):
    """
    Provides access to services related
    to operating sites which are part of the
    Steam PC Café program.
    """
    def __init__(self, key: str):
        super().__init__(key)

    def get_current_client_connections(self,
                                    siteid: int = 0,
                                    ):
        """
        See current activity at one or more sites.

        :param siteid: Site ID to see; zero for all sites
        :type siteid: int
        :return: Steam API response
        """

        params = {
            "siteid": siteid
        }

        return self._get("ISiteLicenseService", "GetCurrentClientConnections", 1, params)

    def get_total_playtime(self,
                         start_time: str,
                         end_time: str,
                         siteid: int = 0):
        """
        Get total playtime amounts for all games over a period of time; for one or all sites.

        :param start_time: Report activity starting on or after this time. RFC 3339 UTC format.
        :type start_time: str
        :param end_time: Report activity starting before this time. RFC 3339 UTC format.
        :type end_time: str
        :param siteid: Site ID to see; zero for all sites
        :type siteid: int
        :return: Steam API response
        """

        param = {
            "start_time": start_time,
            "end_time": end_time,
            "siteid": siteid
        }

        return self._get("ISiteLicenseService", "GetTotalPlaytime", 1, param)


class ISteamCommunity(_SteamAPI):
    """Provides restricted access to Steam Community features."""
    def __init__(self, key: str):
        super().__init__(key)

    def report_abuse(self,
                     steamidActor: int,
                     steamidTarget: int,
                     appid: int,
                     abuseType: int,
                     contentType: int,
                     description: str,
                     gid: int = None,
                     ) -> dict:
        """
        Allows publishers to report users who are behaving badly on their community hub.

        :param steamidActor: SteamID of user doing the reporting
        :type steamidActor: int
        :param steamidTarget: Steam ID of the user being reported
        :type steamidTarget: int
        :param appid: Application ID of the hub being reported
        :type appid: int
        :param abuseType: Type of abuse being reported
        :type abuseType: int
        :param contentType: Type of content being reported
        :type contentType: int
        :param description: Description of the abuse
        :type description: str
        :param gid: Group ID of the hub being reported
        :type gid: int
        :return: Steam API response
        """

        params = {
            "steamidActor": steamidActor,
            "steamidTarget": steamidTarget,
            "appid": appid,
            "abuseType": abuseType,
            "contentType": contentType,
            "description": description,
            "gid": gid
        }

        return self._post("ISteamCommunity", "ReportAbuse", 1, params)


class IDOTA2Match_570(_SteamAPI):
    """Provides access to Dota 2 match data."""
    def __init__(self, key: str):
        super().__init__(key)

    def get_live_league_games(self,
                              league_id: int = None,
                              match_id: int = None,
                              dpc: bool = False,
                              ) -> dict:
        """
        Returns a list of live league games.

        :param league_id: Only show matches of the specified league id
        :type league_id: int
        :param match_id: Only show matches of the specified match id
        :type match_id: int
        :param dpc: Only show matches that are part of the DPC
        :type dpc: bool
        :return: Steam API response
        """

        params = {
            "league_id": league_id,
            "match_id": match_id,
            "dpc": dpc
        }

        return self._get("IDOTA2Match_570", "GetLiveLeagueGames", 1, params)

    def get_match_details(self,
                          match_id: int,
                          include_persona_names: bool = False,
                          ) -> dict:
        """
        Returns match details.

        :param match_id: Match ID
        :type match_id: int
        :param include_persona_names: Include persona names as part of the response
        :type include_persona_names: bool
        :return: Steam API response
        """

        params = {
            "match_id": match_id,
            "include_persona_names": include_persona_names
        }

        return self._get("IDOTA2Match_570", "GetMatchDetails", 1, params)

    def get_match_history(self,
                          hero_id: int = None,
                          game_mode: int = None,
                          skill: int = None,
                          min_players: int = None,
                          account_id: int = None,
                          league_id: int = None,
                          start_at_match_id: int = None,
                          matches_requested: int = None,
                          ) -> dict:
        """
        Returns match history.

        :param hero_id: Only show matches with this hero ID
        :type hero_id: int
        :param game_mode: Only show matches with this game mode
        :type game_mode: int
        :param skill: Only show matches with this skill bracket
        :type skill: int
        :param min_players: Only show matches with this many players
        :type min_players: int
        :param account_id: Only show matches with this account ID
        :type account_id: int
        :param league_id: Only show matches with this league ID
        :type league_id: int
        :param start_at_match_id: Only show matches after this match ID
        :type start_at_match_id: int
        :param matches_requested: Only show this many matches
        :type matches_requested: int
        :return: Steam API response
        """

        params = {
            "hero_id": hero_id,
            "game_mode": game_mode,
            "skill": skill,
            "min_players": min_players,
            "account_id": account_id,
            "league_id": league_id,
            "start_at_match_id": start_at_match_id,
            "matches_requested": matches_requested,
        }

        return self._get("IDOTA2Match_570", "GetMatchHistory", 1, params)

    def get_match_history_by_sequence_num(self,
                                          start_at_match_seq_num: int,
                                          matches_requested: int = None,
                                          ) -> dict:
        """
        Returns match history.

        :param start_at_match_seq_num: Start at this match sequence number
        :type start_at_match_seq_num: int
        :param matches_requested: Only show this many matches
        :type matches_requested: int
        :return: Steam API response
        """

        params = {
            "start_at_match_seq_num": start_at_match_seq_num,
            "matches_requested": matches_requested,
        }

        return self._get("IDOTA2Match_570", "GetMatchHistoryBySequenceNum", 1, params)

    def get_team_info_by_team_ID(self,
                                 start_at_team_id: int,
                                 teams_requested: int = None,
                                 ) -> dict:
        """
        Returns team info.

        :param start_at_team_id: Start at this team ID
        :type start_at_team_id: int
        :param teams_requested: Only show this many teams
        :type teams_requested: int
        :return: Steam API response
        """

        params = {
            "start_at_team_id": start_at_team_id,
            "teams_requested": teams_requested,
        }

        return self._get("IDOTA2Match_570", "GetTeamInfoByTeamID", 1, params)

    def get_top_live_event_game(self,
                                partner: int
                                ) -> dict:
        """
        Returns top live event game.

        :param partner: Which partner's games to use.
        :type partner: int
        :return: Steam API response
        """

        params = {
            "partner": partner
        }

        return self._get("IDOTA2Match_570", "GetTopLiveEventGame", 1, params)

    def get_top_live_game(self,
                          partner: int
                          ) -> dict:
        """
        Returns top live game.

        :param partner: Which partner's games to use.
        :type partner: int
        :return: Steam API response
        """

        params = {
            "partner": partner
        }

        return self._get("IDOTA2Match_570", "GetTopLiveGame", 1, params)

    def get_top_weekend_tourney_games(self,
                                      partner: int,
                                      home_division: int = None
                                      ) -> dict:
        """
        Returns top weekend tourney games.

        :param partner: Which partner's games to use.
        :type partner: int
        :param home_division: Which division to use.
        :type home_division: int
        :return: Steam API response
        """

        params = {
            "partner": partner,
            "home_division": home_division
        }

        return self._get("IDOTA2Match_570", "GetTopWeekendTourneyGames", 1, params)

    def get_tournament_player_stats(self,
                                    account_id: str,
                                    league_id: str = None,
                                    hero_id: str = None,
                                    time_frame: str = None,
                                    match_id: int = None,
                                    phase_id: int = None,
                                    ) -> dict:
        """
        Returns tournament player stats.

        :param account_id: Account ID
        :type account_id: str
        :param league_id: League ID
        :type league_id: str
        :param hero_id: Hero ID
        :type hero_id: str
        :param time_frame: Time frame
        :type time_frame: str
        :param match_id: Match ID
        :type match_id: int
        :param phase_id: Phase ID
        :type phase_id: int
        :return: Steam API response
        """

        params = {
            "account_id": account_id,
            "league_id": league_id,
            "hero_id": hero_id,
            "time_frame": time_frame,
            "match_id": match_id,
            "phase_id": phase_id,
        }

        return self._get("IDOTA2Match_570", "GetTournamentPlayerStats", 2, params)
