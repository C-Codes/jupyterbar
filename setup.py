from setuptools import setup

APP = ['jupyterbar/jupyterbar.py']
DATA_FILES = [
    'Resources/jupyter-logo-bw.png',
    'Resources/jupyter-logo.png',
    'Resources/jupyter-bar-bw.png',
    'Resources/jupyter-bar.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile':'Resources/jupyter-logo.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'], #, 'appdirs'
 }

setup(
    name='jupyterbar',
    version='0.1',
    description='A little statusbar for http://jupyter.org (http://ipython.org/) on OS X written in Python.',
    license='MIT',
    author='Christoph Russ',
    author_email='chruss@gmx.de',
    url='https://github.com/C-Codes/jupyterbar',
    download_url='',
    packages=['jupyterbar'],
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps'],
 )