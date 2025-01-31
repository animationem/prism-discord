# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.

import os
import requests
import json


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from integration.discord_config import DiscordConfig

from PrismUtils.Decorators import err_catcher_plugin as err_catcher



class Prism_Discord_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.discord_config = DiscordConfig(self.core)
        self.token = self.getToken()
        self.project = self.getProject()
        self.guild_id = self.getGuildID(self.token)
        self.channel_id = self.getChannelID( self.token, self.guild_id)

        self.core.registerCallback(
            "mediaPlayerContextMenuRequested",
            self.mediaPlayerContextMenuRequested,
            plugin=self,
        )
        
    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True

    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):
        discord_action = QAction("Publish to Discord", origin)

        self.content = origin.seq[0]
        self.identifier = origin.origin.getCurrentIdentifier()["identifier"]
        self.sequence = None
        self.shot = None
        self.version = None

        iconPath = os.path.join(
            self.pluginDirectory, "Resources", "discord-mark-blue.svg"
        )
        icon = self.core.media.getColoredIcon(iconPath)

        discord_action.triggered.connect(lambda: self.publishToDiscord(self.content))
        menu.insertAction(menu.actions()[-1], discord_action)
        discord_action.setIcon(icon)

    @err_catcher(name=__name__)
    def publishToDiscord(self, content):
        
        print("Publishing to Discord")
        self.sendMessage(self.token, self.channel_id, content)


    def getToken(self):
        config = self.discord_config.loadConfig("studio")
        token = config["discord"]["token"]
        return token

    def getProject(self):
        project = self.core.getConfig("globals", "project_name", configPath=self.core.prismIni)
        return project
            
    #-----------------Get Guild ID -----------------

    def getGuildID(self, token):
        url = "https://discord.com/api/v10/users/@me/guilds"
        headers = {"Authorization": f"Bot {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        for d in data:
            if d["name"] == "Prism for Discordo":
                guild_id = d["id"]

        return guild_id

    #-----------------Get Channel ID -----------------
    def getChannelID(self, token, guild_id):
        url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
        headers = {"Authorization": f"Bot {token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        for d in data:
            if d.get("name") == "Text Channels":
                t_id = d["id"]
                
            if d.get("name") == "test" and d.get("parent_id") == t_id:
                channel_id = d["id"]
        
        return channel_id

        
    #-----------------Send Message -----------------
    def sendMessage(self, token, channel_id, content):
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {"Authorization": f"Bot {token}"}
        #headers = {"Authorization": f"Bot {token}", 'Content-Type': 'application/json'}

        # Prep File
    
        files = {'file': (os.path.basename(content), open(content, 'rb'))}

        #project = self.core.getConfig("globals", "project_name", configPath=self.core.prismIni)

        # Prep payload with an embed
        payload = {
            "content": "hey",
            "embeds": [
                {
                    "title": "PLEASE WORK",  # Use the project name as the title
                    "video": {
                        "url": f"attachment://{os.path.basename(content)}"  # Use the file as the image
                    },
                    "description": "This is a test message",
                    "color": 16711680,
                }
            ]
        }

        response = requests.post(url, headers=headers, files=files, data={"payload_json": json.dumps(payload)})

        # Print the response
        print(response.status_code)
        print(response.json())

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Message sent successfully to Discord!")
        else:
            print("Failed to send message to Discord.")