from config_manager.config_manager import ConfigManager
from requester.requester import Requester

config = ConfigManager()
requester = Requester(config)

print(requester.get_comsumption_history("2024-06-30T22:00:00Z", "2024-07-30T22:00:00Z", raw=False))
