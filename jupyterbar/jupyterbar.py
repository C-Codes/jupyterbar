#!/usr/bin/env python

import sys
import rumps

class JupyterStatusBarApp(rumps.App):
    #def __init__(self):
    #    super(JupyterStatusBarApp, self).__init__("jupyter")
    #    self.title="jupyter"
    #    self.icon="jupyter-logo.png"
    #    self.menu = ["Active", "Preferences", "Status"]

    @rumps.clicked("Active")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("No preferences available!")

    @rumps.clicked("Status")
    def status(self, _):
        rumps.notification("jupyter", "Status Notification", "Nothing to say")

def main(argv):
    jp_app = JupyterStatusBarApp("jupyter")

    jp_app.icon="jupyter-logo-bw.png"

    jp_app.run()


if __name__ == "__main__":
    main(sys.argv[1:])

