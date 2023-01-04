# steam_interfaces
![PyPI](https://img.shields.io/pypi/v/steam_interfaces?color=orange) ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Weebp-Team/steam_interfaces?color=blueviolet) ![License](https://img.shields.io/pypi/l/steam_interfaces?color=blueviolet) ![Forks](https://img.shields.io/github/forks/Weebp-team/steam_interfaces?style=social)

Python library for working with the Steam API.

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

## Dependencies

[requests](https://pypi.org/project/requests/)

## Contributing

Bug reports and/or pull requests are welcome

## License

[MIT](https://choosealicense.com/licenses/mit/)