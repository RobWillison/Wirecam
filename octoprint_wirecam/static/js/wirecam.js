/*
 * View model for OctoPrint-Wirecam
 *
 * Author: You
 * License: AGPLv3
 */
$(function() {
    function WirecamViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        self.move = function() {
          $('#tab_plugin_wirecam button').prop('disabled', true);

          $.ajax({
                url: "./plugin/wirecam/move",
                type: "GET",
                data: {x: $('#tab_plugin_wirecam #x').val(), y: $('#tab_plugin_wirecam #y').val(), z: $('#tab_plugin_wirecam #z').val(), r: $('#tab_plugin_wirecam #r').val(), u: $('#tab_plugin_wirecam #u').val()},
                success: function (results) {
                  console.log(results)
                  $('#tab_plugin_wirecam button').prop('disabled', false);
                }
            });
        }

        self.home = function() {
          $('#tab_plugin_wirecam button').prop('disabled', true);

          $.ajax({
                url: "./plugin/wirecam/home",
                type: "GET",
                success: function (results) {
                  console.log(results)
                  $('#tab_plugin_wirecam button').prop('disabled', false);
                }
            });
        }

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: WirecamViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_wirecam, #tab_plugin_wirecam, ...
        elements: [ '#tab_plugin_wirecam' ]
    });
});
