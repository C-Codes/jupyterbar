#!/usr/bin/env python

from __future__ import print_function

import os, sys
import time, datetime
import rumps
import webbrowser

from jupyter import Jupyter

class JupyterStatusBarApp(rumps.App):
    #def __init__(self):
    #    super(JupyterStatusBarApp, self).__init__("jupyter")
    #    self.title="jupyter"
    #    self.icon="jupyter-logo.png"
    #    self.menu = ["Active", "Preferences", "Status"]

    def __init__(self):
        self.jp_handler = Jupyter()
        super(JupyterStatusBarApp, self).__init__("iPy", quit_button=None) #jupyter

    @rumps.clicked("Open Notebooks")
    def onoff(self, sender):
        #sender.state = not sender.state
        #since we are only running on OS X anyways ...
        safari = webbrowser.get('safari')
        safari.open("http://localhost:8888")

    #@rumps.clicked("Active")
    #def onoff(self, sender):
    #    sender.state = not sender.state

    @rumps.clicked("Set Notebook dir")
    def prefs(self, _):
        #rumps.alert("No preferences available!")
        window = rumps.Window(message='Set notebook-dir', title='JupiterBar Preferences',
                              default_text=self.jp_handler.get_notebook_dir(),
                              ok=None, cancel=None, dimensions=(220, 24))

        response = window.run()
        if (not response.clicked is 1):
            return

        notebook_path = str(response.text)
        self.jp_handler.set_notebook_dir(notebook_path)

    @rumps.clicked("Set $PATH")
    def prefs(self, _):
        #rumps.alert("No preferences available!")
        window = rumps.Window(message='Set $PATH ennvironment variable', title='JupiterBar Preferences',
                              default_text=self.jp_handler.get_path(),
                              ok=None, cancel=None, dimensions=(220, 24))

        response = window.run()
        if (not response.clicked is 1):
            return

        path = str(response.text)
        self.jp_handler.set_path(path)

    @rumps.clicked("Set $PYTHONPATH")
    def prefs(self, _):
        #rumps.alert("No preferences available!")
        window = rumps.Window(message='Set $PYTHONPATH ennvironment variable', title='JupiterBar Preferences',
                              default_text=self.jp_handler.get_pythonpath(),
                              ok=None, cancel=None, dimensions=(220, 24))

        response = window.run()
        if (not response.clicked is 1):
            return

        python_path = str(response.text)
        self.jp_handler.set_pythonpath(python_path)
        
    @rumps.clicked("Reset Settings")
    def prefs(self, _):
        settings_file_path = self.jp_handler.reset_settings()
        time_st = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') #'%Y-%m-%d %H:%M:%S'
        rumps.notification("jupyter "+str(time_st), "Settings file has been reset.", str(settings_file_path))

    @rumps.clicked("Status")
    def status(self, _):
        '''
        Checking status of jupyter / ipython
        '''
        status,msg = self.jp_handler.get_status()
        time_st = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') #'%Y-%m-%d %H:%M:%S'
        rumps.notification("jupyter "+str(time_st), "Status: "+str(status), str(msg))

    @rumps.clicked("Restart")
    def prefs(self, _):
        #rumps.alert("Warning: All notebooks will be shut down!")

        self.jp_handler.restart()

    @rumps.clicked("Shut down")
    def prefs(self, _):
        #rumps.alert("Warning: All notebooks will be shut down!")

        self.jp_handler.shut_down()

    @rumps.clicked('Quit')
    def clean_quit_application(self, _):
        self.jp_handler.shut_down()
        rumps.quit_application()


def main(argv):

    #jp_bar = JupyterStatusBarApp("jupyter")
    #jp_bar = JupyterStatusBarApp("iPy")
    jp_bar = JupyterStatusBarApp()

    icon_bar = "jupyter-logo-bw.png"

    if os.path.isfile(icon_bar):
        jp_bar.icon=icon_bar
        jp_bar.template = True

    jp_bar.run()


if __name__ == "__main__":
    main(sys.argv[1:])

