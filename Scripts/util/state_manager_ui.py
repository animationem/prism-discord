import os
from pathlib import Path

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class StateManagerUI:
    def __init__(self, core):
        self.core = core

    # Create the Slack section of the State Manager UI
    @err_catcher(__name__)
    def createStateManagerSlackUI(self, state):
        state.cb_userPool = QComboBox()
        state.cb_userPool.setPlaceholderText("Select Artist")

        lo_discord_publish = QHBoxLayout()
        lo_discord_publish.setContentsMargins(10, 5, 0, 0)

        state.l_slackPublish = QLabel("Publish to Slack:")
        state.chb_discordPublish = QCheckBox()
        state.chb_discordPublish.setLayoutDirection(Qt.RightToLeft)

        lo_discord_notify = QHBoxLayout()
        lo_discord_notify.setContentsMargins(10, 5, 0, 0)

        state.l_discordNotify = QLabel("Notify Artist:")
        state.chb_discordNotify = QCheckBox()
        state.chb_discordNotify.setLayoutDirection(Qt.RightToLeft)

        lo_discord_publish.addWidget(state.l_slackPublish)
        lo_discord_publish.addWidget(state.chb_discordPublish)
        lo_discord_notify.addWidget(state.l_discordNotify)
        lo_discord_notify.addWidget(state.chb_discordNotify)
        lo_discord_notify.addWidget(state.cb_userPool)

        state.lo_discord_publish = lo_discord_publish
        state.lo_discord_notify = lo_discord_notify
        state.gb_discord.layout().addLayout(lo_discord_publish)
        state.gb_discord.layout().addLayout(lo_discord_notify)

    # Remove the Slack section of the State Manager UI
    @err_catcher(__name__)
    def removeCleanupLayout(self, layout, attribute_name, state):
        if hasattr(state, attribute_name):
            sub_layout = getattr(state, attribute_name)
            if sub_layout:
                for i in reversed(range(sub_layout.count())):
                    item = sub_layout.itemAt(i)
                    if item.widget():
                        widget = item.widget()
                        sub_layout.removeWidget(widget)
                        widget.deleteLater()

                layout.removeItem(sub_layout)
                sub_layout.deleteLater()

                delattr(state, attribute_name)

            for attr in [
                "chb_discordPublish",
                "l_discordPublish",
                "cb_userPool",
                "l_discordNotify",
                "chb_discordNotify",
            ]:
                if hasattr(state, attr):
                    delattr(state, attr)
