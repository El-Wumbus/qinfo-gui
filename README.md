# qinfo-gui

A gui for [qinfo](https://github.com/el-wumbus/qinfo) using [qinfo-python](https://github.com/el-wumbus/qinfo-python) and [GTK 3.0](https://docs.gtk.org/gtk3/)

![qinfo version 0.0.1](https://i.imgur.com/OWM9O3K.png)

qinfo-gui has many of the features of qinfo but now automatically updates its information every 3 seconds. Slow operations, like getting package counts, aren't repeated and only happen on inital loading.  
qinfo-gui uses the same configuration file and (mostly) takes the same configuration options as qinfo.  
qinfo-gui is currently in **very early development**. Not too much time has been put into this application.

## Installation

```bash
pip install qinfo-gui
```

## Usage

```txt
$ qinfo-gui --help 
usage: qinfo-gui [-h] [-c [CONFIG]] [-s]

A gui for qinfo

options:
  -h, --help            show this help message and exit
  -c [CONFIG], --config [CONFIG]
                        Use this config file instead of the one at defualt location.
  -s, --hide_warnings   Hide non-critical warnings
```
