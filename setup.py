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
VERSION='0.1'

setup(
    name='jupyterbar',
    version=VERSION,
    description='A little statusbar for http://jupyter.org (http://ipython.org/) on OS X written in Python.',
    license='MIT',
    author='Christoph Russ',
    author_email='chruss@gmx.de',
    url='https://github.com/C-Codes/jupyterbar',
    download_url='https://github.com/C-Codes/jupyterbar/tarball/v'+VERSION,
    packages=['jupyterbar'],
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps', 'appdirs', 'dicttoxml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Framework :: IPython',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
 )