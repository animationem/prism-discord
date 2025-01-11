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
            self.createNotificationSettingsMenu(lo_discord, origin)
            self.createServerSettingsMenu(lo_discord, origin)

            origin.addTab(origin.w_discordProjectTab, "Discord")

    @err_catcher(__name__)
    def createDiscordTokenSettingsMenu(self, lo_discord, origin):
        l_discord_logo = self.grabDiscordLogo()

        le_discord_token = QLineEdit()
        le_discord_token.setPlaceholderText("Enter your Discord Bot Token")
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

    @err_catcher(__name__)
    def createNotificationSettingsMenu(self, lo_discord, origin):
        gb_notifications = QGroupBox()
        gb_notifications.setTitle("Notifications")
        gb_notifications.setContentsMargins(0, 30, 0, 0)
        lo_notifications = QVBoxLayout()
        gb_notifications.setLayout(lo_notifications)

        lo_notify_method = QHBoxLayout()
        l_notify_method = QLabel("Notification Method:")
        cb_notify_method = QComboBox()
        origin.cb_notify_method = cb_notify_method

        l_notify_method_help = self.grabHelpIcon()
        l_notify_method_help.setToolTip("""<p style='line-height:1;'>
                                        <span style='color:DodgerBlue;'><b>Direct</b></span>: Notify the selected user by Direct message<br>
                                        <br>
                                        <span style='color:Tomato;'><b>Channel</b></span>: Notify selected user in the Discord Channel<br>
                                        <br>
                                        <span style='color:MediumSeaGreen;'><b>Ephemeral Direct</b></span>: Notify the selected user in an ephemeral Direct message<br>
                                        <br>
                                        <span style='color:MediumSlateBlue;'><b>Ephemeral Channel</b></span>: Notify selected user in an ephemeral Channel message<br>
                                        </p>""")

        lo_notify_method.addWidget(l_notify_method)
        lo_notify_method.addWidget(origin.cb_notify_method)
        lo_notify_method.addWidget(l_notify_method_help)
        lo_notify_method.addStretch()
        lo_notifications.addLayout(lo_notify_method)

        lo_discord.addWidget(gb_notifications)
        lo_discord.setAlignment(gb_notifications, Qt.AlignTop)

    @err_catcher(__name__)
    def createServerSettingsMenu(self, lo_discord, origin):
        gb_server = QGroupBox()
        gb_server.setTitle("Server")
        gb_server.setContentsMargins(0, 30, 0, 0)
        lo_server = QVBoxLayout()
        gb_server.setLayout(lo_server)

        lo_status = QHBoxLayout()
        l_server_status = QLabel("Status:")
        l_server_status_value = QLabel("Offline")
        fo_server_status_value = l_server_status_value.font()
        fo_server_status_value.setItalic(True)
        l_server_status_value.setFont(fo_server_status_value)
        origin.l_server_status_value = l_server_status_value

        lo_status.addWidget(l_server_status)
        lo_status.addWidget(origin.l_server_status_value)
        lo_status.addStretch()

        b_server_button = QPushButton("Start Server")
        origin.b_server_button = b_server_button
        lo_status.addWidget(origin.b_server_button)

        b_reset_button = QPushButton("Reset Server Status")
        origin.b_reset_button = b_reset_button
        lo_status.addWidget(origin.b_reset_button)

        lo_machine = QHBoxLayout()
        l_machine = QLabel("Machine:")
        l_machine_value = QLabel()

        lo_machine.addWidget(l_machine)
        lo_machine.addWidget(l_machine_value)

        lo_discord_server_name = QHBoxLayout()
        le_discord_server = QLineEdit()
        le_discord_server.setPlaceholderText("Enter your Discord Server Name")
        l_discord_server_help = self.grabHelpIcon()
        l_discord_server_help.setToolTip("""<p style='line-height:1;'>
                                Enter your Discord Server Name<br><br>
                                
                                Note: Because the app can theoretically be installed on multiple servers, you need to specify which server you are trying to connect to.
                                </p>""")
        lo_discord_server_name.addWidget(le_discord_server)
        lo_discord_server_name.addWidget(l_discord_server_help)

        lo_save_server = QHBoxLayout()
        lo_save_server.addStretch()
        b_save_server_name = QPushButton("Save")
        lo_save_server.addWidget(b_save_server_name)
        lo_save_server.addStretch()

        lo_server.addLayout(lo_status)
        lo_server.addLayout(lo_machine)
        lo_server.addLayout(lo_discord_server_name)
        lo_server.addLayout(lo_save_server)

        lo_discord.addWidget(gb_server)
        lo_discord.setAlignment(gb_server, Qt.AlignTop)
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

    @err_catcher(__name__)
    def grabHelpIcon(self):
        l_help = QLabel()
        help_icon = os.path.join(
            self.core.prismLibs, "Scripts", "UserInterfacesPrism", "help.png"
        )

        pixmap = QPixmap(help_icon)

        l_help.setPixmap(pixmap)

        return l_help
