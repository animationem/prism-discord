import os

from pathlib import Path
from pprint import pprint

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from integration.discord_config import DiscordConfig
from util.settings_ui import SettingsUI
from util.dialogs import InputDialog

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Discord_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.discord_config = DiscordConfig(self.core)
        self.settings_ui = SettingsUI(self.core)

        self.core.registerCallback(
            "projectSettings_loadUI",
            self.projectSettings_loadUI,
            plugin=self,
        )

    @err_catcher(name=__name__)
    def onPluginsLoaded(self):
        if self.isStudioLoaded() is not None:
            self.core.registerCallback(
                "projectSettings_loadUI",
                self.projectSettings_loadUI,
                plugin=self,
            )
        else:
            self.core.registerCallback(
                "projectSettings_loadUI", self.projectSettings_loadUI, plugin=self
            )

    @err_catcher(name=__name__)
    def projectSettings_loadUI(self, origin):
        self.settings_ui.createDiscordProjectSettingsUI(origin, settings=None)
        self.setStudioOptions(origin)
        self.connectEvents(origin)

    @err_catcher(name=__name__)
    def setStudioOptions(self, origin):
        try:
            self.checkToken(origin)

            self.addNotificationMethods(origin)
            self.checkNotificationMethod(origin)
            self.addNotificationsUserPools(origin)
            self.checkNotificationsUserPool(origin)

            self.checkGuildName(origin)

        except Exception as e:
            self.core.popup(str(e))

    @err_catcher(name=__name__)
    def connectEvents(self, origin):
        origin.b_discord_token.clicked.connect(lambda: self.inputBotToken(origin))
        origin.cb_notify_method.currentIndexChanged.connect(
            lambda: self.saveNotificationMethod(origin)
        )
        origin.cb_notify_user_pool.currentIndexChanged.connect(
            lambda: self.saveNotificationsUserPool(origin)
        )
        origin.b_save_server_name.clicked.connect(lambda: self.saveGuildName(origin))

    @err_catcher(name=__name__)
    def inputBotToken(self, origin):
        dialog = InputDialog(title="Enter your Discord Bot Token")
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            token = dialog.get_input()

            config = self.discord_config.loadConfig("studio")
            self.discord_config.checkDiscordOptionsInConfig(config)

            config["discord"]["token"] = token
            origin.le_discord_token.setText(token)

            self.discord_config.saveConfigSetting(config, mode="studio")

    @err_catcher(name=__name__)
    def checkToken(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        if "token" not in config["discord"]:
            config["discord"]["token"] = ""
            origin.le_discord_token.setPlaceholderText("Enter your Discord Bot Token")

        token = config["discord"]["token"]
        origin.le_discord_token.setText(token)

    @err_catcher(name=__name__)
    def addNotificationMethods(self, origin):
        methods = ["", "Discord", "Prism Studio"]

        origin.cb_notify_method.addItems(methods)

    @err_catcher(name=__name__)
    def checkNotificationMethod(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        method = config["discord"]["notifications"].get("method", "")

        origin.cb_notify_method.setCurrentText(method)

    @err_catcher(name=__name__)
    def saveNotificationMethod(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        method = origin.cb_notify_method.currentText()

        config["discord"]["notifications"]["method"] = method
        self.discord_config.saveConfigSetting(config, mode="studio")

    @err_catcher(name=__name__)
    def addNotificationsUserPools(self, origin):
        user_pool = ["", "Discord", "Prism Studio"]

        origin.cb_notify_user_pool.addItems(user_pool)

    @err_catcher(name=__name__)
    def checkNotificationsUserPool(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        user_pool = config["discord"]["notifications"].get("user_pool", "")

        origin.cb_notify_user_pool.setCurrentText(user_pool)

    @err_catcher(name=__name__)
    def saveNotificationsUserPool(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        user_pool = origin.cb_notify_user_pool.currentText()

        config["discord"]["notifications"]["user_pool"] = user_pool
        self.discord_config.saveConfigSetting(config, mode="studio")

    @err_catcher(name=__name__)
    def checkGuildName(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        if "guild_name" not in config["discord"]["server"]:
            config["discord"]["server"]["guild_name"] = ""
            origin.le_discord_server.setPlaceholderText(
                "Enter your Discord Server Name"
            )

        guild_name = config["discord"]["server"].get("guild_name", "")
        origin.le_discord_server.setText(guild_name)

    @err_catcher(name=__name__)
    def saveGuildName(self, origin):
        config = self.discord_config.loadConfig("studio")
        self.discord_config.checkDiscordOptionsInConfig(config)

        guild_name = origin.le_discord_server.text()

        config["discord"]["server"]["guild_name"] = guild_name
        self.discord_config.saveConfigSetting(config, mode="studio")

    # Check if the studio plugin is loaded
    @err_catcher(name=__name__)
    def isStudioLoaded(self):
        return self.core.getPlugin("Studio")
