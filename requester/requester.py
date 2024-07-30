import pandas as pd
import requests

from config_manager.config_manager import ConfigManager
from fluvius_token.fluvius_token import Token


class Requester:
    def __init__(self, config: ConfigManager):
        self.config = config
        fluviuslogin = config.get("fluvius", "fluviuslogin")
        fluviuspassword = config.get("fluvius", "fluviuspassword")
        browser = config.get("browser", "kind", fallback=None)

        # Use the token to make a request
        self.token = Token(fluviuslogin, fluviuspassword, browser)

    def get_comsumption_history(self, from_time, to_time, raw=True):
        fluviusEAN = self.config.get("fluvius", "fluviusEAN")
        # Define the URL
        url = f'https://mijn.fluvius.be/verbruik/api/consumption-histories/{fluviusEAN}?historyFrom={from_time}&historyUntil={to_time}&granularity=3&asServiceProvider=false'

        # Make the GET request
        response = requests.get(url, headers={
            'Authorization': self.token.access_token,
        })
        if response.ok:
            if raw:
                # return the response
                return response.json()
            else:
                json = response.json()
                return [pd.DataFrame(json_item["val"]) for json_item in json if "val" in json_item]
        return None
