import os
from pathlib import Path

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class SettingsUI:
    def __init__(self, core):
        super().__init__()
        self.core = core

    @err_catcher(__name__)
    def createDiscordStudioSettingsUI(self, origin, settings):
        if not hasattr(origin, "w_discordStudioTab"):
            origin.w_discordStudioTab = QWidget()
            lo_discord = QVBoxLayout(origin.w_discordStudioTab)

            self.createDiscordTokenSettingsMenu(lo_discord, origin)

            origin.addTab(origin.w_discordStudioTab, "Discord")

    @err_catcher(__name__)
    def createDiscordProjectSettingsUI(self, origin, settings):
        if not hasattr(origin, "w_discordProjectTab"):
            origin.w_discordProjectTab = QWidget()
            lo_discord = QVBoxLayout(origin.w_discordProjectTab)

            self.createDiscordTokenSettingsMenu(lo_discord, origin)

            origin.addTab(origin.w_discordProjectTab, "Discord")

    @err_catcher(__name__)
    def createDiscordTokenSettingsMenu(self, lo_discord, origin):
        l_discord_logo = self.grabDiscordLogo()

        le_discord_token = QLineEdit()
        le_discord_token.setPlaceholderText("Enter your Discord API Token")
        le_discord_token.setEchoMode(QLineEdit.Password)
        le_discord_token.setReadOnly(True)
        le_discord_token.setFocusPolicy(Qt.NoFocus)
        le_discord_token.setContextMenuPolicy(Qt.NoContextMenu)
        origin.le_discord_token = le_discord_token

        b_discord_token = QPushButton("Input Token")
        origin.b_discord_token = b_discord_token

        lo_discord.addStretch()
        lo_discord.addWidget(l_discord_logo)
        lo_discord.setAlignment(l_discord_logo, Qt.AlignBottom)

        lo_discord.addWidget(origin.le_discord_token)
        lo_discord.setAlignment(origin.le_discord_token, Qt.AlignBottom)

        lo_discord.addWidget(origin.b_discord_token)
        lo_discord.setAlignment(origin.b_discord_token, Qt.AlignBottom | Qt.AlignCenter)

        lo_discord.addStretch()

    @err_catcher(__name__)
    def grabDiscordLogo(self):
        l_discord = QLabel()

        plugin_directory = Path(__file__).resolve().parents[2]
        i_discord = os.path.join(plugin_directory, "Resources", "discord-logo-blue.svg")

        pixmap = QPixmap(i_discord)

        scale = 0.5
        l_discord.setPixmap(pixmap)
        l_discord.setScaledContents(True)
        l_discord.setFixedSize(pixmap.width() * scale, pixmap.height() * scale)
        l_discord.setContentsMargins(0, 0, 0, 0)

        return l_discord
