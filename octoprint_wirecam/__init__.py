# coding=utf-8
from __future__ import absolute_import
import flask
import octoprint.plugin
import serial

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class WirecamPlugin(octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.BlueprintPlugin,
    octoprint.plugin.AssetPlugin):

    def on_after_startup(self):
        self._logger.info("Hello World!")
        self.serial = serial.Serial ("/dev/ttyS0", 9600)

    def get_update_information(self):
        return {}

    def get_assets(self):
     return dict(
         js=["js/wirecam.js"]
     )

    @octoprint.plugin.BlueprintPlugin.route("/home", methods=["GET"])
    def home(self):
        self.serial.write(b'HOME')
        return 'Homed'

    @octoprint.plugin.BlueprintPlugin.route("/move", methods=["GET"])
    def move(self):
        x = flask.request.values['x']
        y = flask.request.values['y']
        z = flask.request.values['z']
        self.serial.write(str.encode('C' + x + ',' + y + ',' + z))
        return 'Moved'




# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Wirecam Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = WirecamPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
