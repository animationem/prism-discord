import os
import json

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class DiscordConfig:
    def __init__(self, core):
        self.core = core

    @err_catcher(name=__name__)
    def getStudioConfig(self):
        studio_path = os.getenv("PRISM_STUDIO_PATH")
        if studio_path:
            return os.path.join(studio_path, "configs", "discord.json")

        elif self.core.getPlugin("Studio") is None:
            project_config = os.path.dirname(self.core.prismIni)

            return os.path.join(project_config, "pipeline.json")

        else:
            studio_plugin = self.core.getPlugin("Studio")
            studio_path = studio_plugin.getStudioPath()

            return os.path.join(studio_path, "configs", "discord.json")

    @err_catcher(name=__name__)
    def getUserConfig(self):
        return self.core.getConfigPath("user")

    @err_catcher(name=__name__)
    def loadConfig(self, mode):
        try:
            if mode == "user":
                config = self.getUserConfig()
                with open(config, "r") as f:
                    return json.load(f)
            else:
                config = self.getStudioConfig()

            config_dir = os.path.dirname(config)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                with open(config, "w") as f:
                    json.dump({"discord": {"token": ""}}, f, indent=4)

            with open(config, "r") as f:
                return json.load(f)

        except Exception:
            import traceback
            error_message = traceback.format_exc()
            self.core.popup(f"Cannot load the configuration file: {error_message}")

    @err_catcher(name=__name__)
    def saveConfigSetting(self, setting, mode):
        try: 
            if mode == "user":
                config = self.getUserConfig()
            else:
                config = self.getStudioConfig()

            with open(config, "w") as f:
                json.dump(setting, f, indent=4)
        except:
            self.core.popup(f"Cannot save {setting} to the configuration file")

    @err_catcher(name=__name__)
    def checkDiscordOptionsInConfig(self, config):
        discord_defaults = {
            "token": "",
            "notifications": {
            "method": "",
            "user_pool": ""
            },
            "server": {
            "status": "",
            "machine": "",
            "guild_name": ""
            }
        }

        if "discord" not in config:
            config["discord"] = discord_defaults
        else:
            for key, value in discord_defaults.items():
                if key not in config["discord"]:
                    config["discord"][key] = value
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in config["discord"][key]:
                            config["discord"][key][sub_key] = sub_value

        # Save updated config
        self.saveConfigSetting(config, "studio")
