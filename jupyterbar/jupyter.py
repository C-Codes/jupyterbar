#!/usr/bin/env python

from __future__ import print_function

import os
import subprocess

import appdirs
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom

import dicttoxml

class Jupyter:
    def __init__(self, notebook=True, notebook_dir=""):
        #settings
        self._notebook = notebook
        self._notebook_dir = notebook_dir

        #process handle
        self.jp_app = None

        #initialization
        self.load_settings()
        #launch
        self.launch(self._notebook, self._notebook_dir)

    def use_notebook(self):
        return self._notebook

    def set_notebook(self, notebook):
        self._notebook = notebook
        self.save_settings()

    def get_notebook_dir(self):
        return self._notebook_dir

    def set_notebook_dir(self, notebook_dir):
        if not os.path.isdir(notebook_dir):
            print("Warning: Notebook directory can not be found.")

        self._notebook_dir = notebook_dir
        self.save_settings()

    def get_settings_file(self):
        usr_cfg_dir = appdirs.user_config_dir(appname="jupyterbar", appauthor="ccodes")
        if not os.path.isdir(usr_cfg_dir):
            os.mkdir(usr_cfg_dir)

        usr_cfg_file = os.path.join(usr_cfg_dir, "ccodes.jupyterbar.xml")
        return usr_cfg_file

    def save_settings(self):
        '''
        Saving settings from user config dir
        '''
        #print("Writing settings file")

        usr_cfg_file = self.get_settings_file()

        settings_dict = dict()
        settings_dict["notebook"] = self._notebook
        settings_dict["notebook_dir"] = self._notebook_dir

        settings_xml = dicttoxml.dicttoxml(settings_dict)

        settings_dom = minidom.parseString(settings_xml)
        #print(settings_dom.toprettyxml())

        with open(usr_cfg_file, 'w') as f:
            f.write(settings_dom.toprettyxml())

    def load_settings(self):
        '''
        Loading settings from user config dir
        '''
        usr_cfg_file = self.get_settings_file()

        if os.path.isfile( usr_cfg_file ):
            # load pre-existing settings
            tree = ElementTree.parse(usr_cfg_file)
            root = tree.getroot()

            self._notebook = bool(root.find('notebook').text)
            self._notebook_dir = str(root.find('notebook_dir').text)

            #print(root.tag, root.attrib)
            #for child in root:
            #    print(child.tag, child.attrib, child.text)
        else:
            # storing default settings
            self.save_settings()

    def get_status(self):
        '''
        Return status message for display
        '''
        status = "unknown"
        msg = "jupyther (iPython) status could not be determined."

        if not self.jp_app is None:
            status = "running"
            pid = str(self.jp_app.pid)

            msg = "jupyther (iPython) is running on process-id: " + pid

        return status,msg


    def launch(self, notebook, notebook_dir):
        '''
        Launching jupyter with optional notebook[-dir] setting
        '''
        launch_cmd = ['ipython']
        self.set_notebook(notebook)
        self.set_notebook_dir(notebook_dir)

        if self.use_notebook():
            launch_cmd.append('notebook')

        # this is a user configured variable, this check also serves as a
        # security measure to not execute any unknown code input by the user
        if len(self.get_notebook_dir()) > 0:
            if os.path.isdir(self.get_notebook_dir()):
                launch_cmd.append('--notebook-dir='+self.get_notebook_dir())

        #print(launch_cmd)

        try:
            # without the shell environment, somehow the process doesn't exit clean
            self.jp_app = subprocess.Popen(' '.join(launch_cmd), shell=True)
        except:
            print("ERROR: Starting jupyter (iPython) failed. (Are you sure your environment is setup properly?)")

    def restart(self):
        '''
        Restart jupyter app
        '''
        self.shut_down()

        self.launch(self._notebook, self._notebook_dir)

    def shut_down(self):
        '''
        Shut down jupyter app
        '''
        print("Exiting jupyter (iPython)")

        if not self.jp_app is None:
            print("jupyter was defined")

            self.jp_app.terminate()
            self.jp_app.wait()

        self.jp_app = None