#!/usr/bin/env python

from __future__ import print_function

import os, signal
import subprocess

import appdirs
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom

import dicttoxml

class Jupyter:
    def __init__(self, notebook=True, notebook_dir="", path="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/sbin", pythonpath="/usr/local/lib/python2.7/site-packages:/Library/Python/2.7/site-packages"):
        #settings
        self._notebook = notebook
        self._notebook_dir = notebook_dir
        self._path = path
        self._pythonpath = pythonpath

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

    def set_path(self, path_var):
        self._path = path_var
        self.save_settings()

    def get_path(self):
        return self._path

    def set_pythonpath(self, pythonpath_var):
        self._path = pythonpath_var
        self.save_settings()

    def get_pythonpath(self):
        return self._pythonpath

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
        #print("notebook-dir: " + self._notebook_dir)

        usr_cfg_file = self.get_settings_file()

        settings_dict = dict()
        settings_dict["notebook"] = self._notebook
        settings_dict["notebook_dir"] = self._notebook_dir
        settings_dict["path"] = self._path
        settings_dict["pythonpath"] = self._pythonpath

        #print(settings_dict)

        settings_xml = dicttoxml.dicttoxml(settings_dict)

        settings_dom = minidom.parseString(settings_xml)
        #print(settings_dom.toprettyxml())

        with open(usr_cfg_file, 'w') as f:
            f.write(settings_dom.toprettyxml())

        return usr_cfg_file

    def reset_settings(self):
        self._notebook = True
        self._notebook_dir = ""
        self._path = "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/sbin"
        self._pythonpath = "/usr/local/lib/python2.7/site-packages:/Library/Python/2.7/site-packages"

        return self.save_settings()

    def load_settings(self):
        '''
        Loading settings from user config dir
        '''
        usr_cfg_file = self.get_settings_file()

        if os.path.isfile( usr_cfg_file ):
            # load pre-existing settings
            tree = ElementTree.parse(usr_cfg_file)
            root = tree.getroot()

            if root.find('notebook') is not None:
                self._notebook = bool(root.find('notebook').text)
            if root.find('notebook_dir') is not None:
                self._notebook_dir = str(root.find('notebook_dir').text)
            if root.find('path') is not None:
                self._path = str(root.find('path').text)
            if root.find('pythonpath') is not None:
                self._pythonpath = str(root.find('pythonpath').text)

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

        ipython_env = os.environ.copy()
        ipython_env['PATH'] = "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/sbin"
        ipython_env['PYTHONPATH'] = "/usr/local/lib/python2.7/site-packages:"+ipython_env['HOME']+"/Library/Python/2.7/lib/python/site-packages"

        #print(launch_cmd)
        #test_cmd = ['echo', '$PATH']
        #test_cmd = ['set']

        try:
            # without the shell environment, somehow the process doesn't exit clean
            #subprocess.Popen(' '.join(test_cmd), shell=True, executable="/bin/bash", env=ipython_env)
            self.jp_app = subprocess.Popen(' '.join(launch_cmd), shell=True, executable="/bin/bash", env=ipython_env) #, preexec_fn=os.setsid
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
            #os.killpg(self.jp_app.pid, signal.SIGTERM)
            self.jp_app.terminate()
            self.jp_app.wait()

        self.jp_app = None