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
        if mode == "user":
            config = self.getUserConfig()
            with open(config, "r") as f:
                return json.load(f)

        elif mode == "studio":
            config = self.getStudioConfig()
        else:
            self.core.popup("Cannot retrieve the configuration file")
            return

        try:
            if not os.path.exists(config):
                os.makedirs(os.path.dirname(config), exist_ok=True)
                with open(config, "w") as f:
                    json.dump({"discord": {"token": ""}}, f, indent=4)

            with open(config, "r") as f:
                return json.load(f)

        except:
            self.core.popup("Cannot load the configuration file")

    @err_catcher(name=__name__)
    def saveConfigSetting(self, setting, mode):
        if mode == "user":
            config = self.getUserConfig()
        elif mode == "studio":
            config = self.getStudioConfig()
        else:
            self.core.popup("Cannot retrieve the configuration file")
            return

        try:
            with open(config, "w") as f:
                json.dump(setting, f, indent=4)
        except:
            self.core.popup(f"Cannot save {setting} to the configuration file")

    @err_catcher(name=__name__)
    def checkDiscordOptionsInConfig(self, config):
        if "discord" not in config:
            config["discord"] = {}
        if "token" not in config["discord"]:
            config["discord"]["token"] = ""
        if "notifications" not in config["discord"]:
            config["discord"]["notifications"] = {}
        if "method" not in config["discord"]["notifications"]:
            config["discord"]["notifications"]["method"] = ""
        if "user_pool" not in config["discord"]["notifications"]:
            config["discord"]["notifications"]["user_pool"] = ""
        if "server" not in config["discord"]:
            config["discord"]["server"] = {}
        if "status" not in config["discord"]["server"]:
            config["discord"]["server"]["status"] = ""
        if "machine" not in config["discord"]["server"]:
            config["discord"]["server"]["machine"] = ""
        if "guild_name" not in config["discord"]["server"]:
            config["discord"]["server"]["guild_name"] = ""

        # Save updated config
        self.saveConfigSetting(config, "studio")
