# coding=utf-8
from __future__ import absolute_import
import flask
import octoprint.plugin
from octoprint.events import Events
import serial
import re
import math
from time import sleep

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
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SettingsPlugin):

    def on_after_startup(self):
        self._logger.info('Starting Wirecam')
        self._camera_coords = []
        self._logger.info('========================================================')
        self._logger.info('TEST - ' + self._settings.settings.getBaseFolder('uploads'))
        try:
            self.serial = serial.Serial("/dev/ttyACM0", 115200, timeout=30)
        except:
            self.serial = False

    def get_update_information(self):
        return {}

    def get_assets(self):
         return dict(
             js=["js/wirecam.js"]
         )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_settings_defaults(self):
        return dict(radius=7, start_height=5, end_height=12)

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            self.process_gcode(self._settings.settings.getBaseFolder('uploads') + '/' + payload['path'])

    def process_gcode(self, filename):
        gcode = open(filename, 'r').read()
        layer_height = float(re.search(r'layer_height = ([0-9.]+)', gcode).group(1))
        matches = re.findall(r'Z([0-9.-]+)', gcode)
        top_layer = max([float(m) for m in matches])
        layers = math.ceil(top_layer / layer_height)
        self._logger.info('The gcode has ' + str(layers) + ' layers')
        radius = int(self._settings.get(['radius']))

        self._logger.info('radius is set too ' + str(radius))

        camera_coords = []
        angle_step = 165 / layers

        start_height = float(self._settings.get(['start_height']))
        height_step = (float(self._settings.get(['end_height'])) - start_height) / layers
        self._logger.info('Height step is ' + str(height_step))
        for i in range(layers):
            angle = angle_step * i
            x = radius * math.sin(math.radians(angle + 90))
            y = - radius * math.cos(math.radians(90 - angle))
            # point camera to the center
            rotate_stepper = 1 - (angle / 180)

            z = height_step * i + start_height

            camera_coords.append([x,y,z, rotate_stepper, 1])

        self._logger.info(camera_coords)
        self._camera_coords = camera_coords

    @octoprint.plugin.BlueprintPlugin.route("/home", methods=["GET"])
    def home(self):
        self._logger.info('HOMING')
        self.homeCamera()
        return 'Homed'

    @octoprint.plugin.BlueprintPlugin.route("/move", methods=["GET"])
    def move(self):
        x = flask.request.values['x']
        y = flask.request.values['y']
        z = flask.request.values['z']
        r = flask.request.values['r']
        u = flask.request.values['u']
        self._logger.info('MOVING TO ' + x + ',' + y + ',' + z + ',' + r + ',' + u)
        self.moveCamera(x,y,z, r, u)

        return 'Moved'

    @octoprint.plugin.BlueprintPlugin.route("/next_position", methods=["GET"])
    def next_position(self):
        if len(self._camera_coords) > 0:
            x,y,z,r,u = self._camera_coords.pop(0)
            self._logger.info('MOVING TO ' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(r) + ',' + str(u))
            self.moveCamera(x,y,z,r,u)

        return 'Moved'

    def moveCamera(self, x, y, z,r,u):
        if not self.serial:
            return
        self.serial.reset_input_buffer()
        self.serial.write(str.encode('C' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(r) + ',' + str(u) + '\r\n'))
        self.serial.read_until(b'Done')

    def homeCamera(self):
        if not self.serial:
            return

        self.serial.reset_input_buffer()
        self.serial.write(b'Home\r\n')
        self.serial.read_until(b'Done')

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
