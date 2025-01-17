import os

from pathlib import Path
from pprint import pprint

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from util.settings_ui import SettingsUI

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

# Bring it back


class Prism_Discord_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.settings_ui = SettingsUI(self.core)

        if self.isStudioLoaded() is not None:
            self.core.registerCallback(
                "studioSettings_loadSettings",
                self.studioSettings_loadSettings,
                plugin=self,
            )
        else:
            self.core.registerCallback(
                "onPluginsLoaded", self.onPluginsLoaded, plugin=self
            )

    @err_catcher(name=__name__)
    def onPluginsLoaded(self):
        if self.isStudioLoaded() is not None:
            self.core.registerCallback(
                "studioSettings_loadSettings",
                self.studioSettings_loadSettings,
                plugin=self,
            )
        else:
            self.core.registerCallback(
                "projectSettings_loadUI", self.projectSettings_loadUI, plugin=self
            )

    @err_catcher(name=__name__)
    def projectSettings_loadUI(self, origin):
        self.settings_ui.createDiscordProjectSettingsUI(origin, settings=None)

    # Check if the studio plugin is loaded
    @err_catcher(name=__name__)
    def isStudioLoaded(self):
        return self.core.getPlugin("Studio")
