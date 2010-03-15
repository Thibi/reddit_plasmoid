# -*- coding: utf-8 -*-

# Copyright (C) 2010  Thibi <thibitian@gmail.com>
#
# Repurposed from gmail-plasmoid 0.7.13
# Copyright (C) 2009  Mark McCans <mjmccans@gmail.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import *
from PyKDE4 import plasmascript
from PyKDE4.kio import *
from PyKDE4.solid import *
from reddit import *

import sys, os, subprocess, threading, ConfigParser

class redditplasmoid(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
    
    def init(self):
        self.OldRect = None
        self.setHasConfigurationInterface(True)
        #self.setAspectRatioMode(Plasma.ConstrainedSquare)
        self.setAspectRatioMode(Plasma.Square)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        #self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        #self.setBackgroundHints(Plasma.Applet.NoBackground)
        #self.setBackgroundHints(Plasma.Applet.StandardBackground)
        self.setBackgroundHints(Plasma.Applet.TranslucentBackground)
        self.layout = QGraphicsLinearLayout(self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setOrientation(Qt.Horizontal)
        self.icon = Plasma.IconWidget()
        self.layout.addItem(self.icon)
        #self.resize(128,128)
	
	# File versions
        vers = {}
        
        # Setup configuration
        self.settings = {}
        gc = self.config()
        
        # Setup translations
        kdehome = unicode(KGlobal.dirs().localkdedir())
        self.installTranslation(vers, unicode(KGlobal.locale().language()), kdehome)
        KGlobal.locale().insertCatalog("reddit_plasmoid")
        
        # Create notifyrc file if required
        if not os.path.exists(kdehome+"share/apps/reddit_plasmoid/reddit_plasmoid.notifyrc"):
            if os.path.exists(kdehome+"share/apps"):
                self.createNotifyrc(kdehome, vers)
        else:
            # Update if the version string does not match
            ver = self.fixType(gc.readEntry("reddit_plasmoid.notifyrc", "0"))
            if ver <> vers["reddit_plasmoid.notifyrc"]:
                print "Update .notifyrc file..."
                self.createNotifyrc(kdehome, vers)
                
        # Install icon into system
        ver = self.fixType(gc.readEntry("reddit_plasmoid-128.png", "0"))
        if ver <> vers["reddit_plasmoid-128.png"]:
            out = commands.getstatusoutput("xdg-icon-resource install --size 128 " + unicode(self.package().path()) + "contents/icons/reddit_plasmoid-128.png reddit_plasmoid")        
            if out[0] == 0:
                print "reddit_plasmoid icon installed"
                gc.writeEntry("reddit_plasmoid-128.png", vers["reddit_plasmoid-128.png"])
            else:
                print "Error installing reddit_plasmoid icon:", out
        
        # General settings
        self.settings["pollinterval"] = int(self.fixType(gc.readEntry("pollinterval", "5")))
        self.settings["command"] = self.fixType(gc.readEntry("command", "kfmclient exec"))
        self.settings["textfont"] = self.fixType(gc.readEntry("textfont", ""))
        self.settings["textsize"] = int(self.fixType(gc.readEntry("textsize", "60")))
        self.settings["textcolor"] = self.fixType(gc.readEntry("textcolor", "blue"))
        self.settings["icon"] = self.fixType(gc.readEntry("icon", self.package().path() + "contents/icons/reddit_plasmoid.svg"))
        self.settings["iconnone"] = self.fixType(gc.readEntry("iconnone", self.package().path() + "contents/icons/reddit_plasmoid-gray.svg"))
    
    # KDE Wallet
    def walletOpened(self, status):
        print "Wallet opened"
        if status:
            # Get passwords from wallet
            self.wallet.setFolder("reddit_plasmoid")
            for i in range(0, len(self.settings["accounts"])):
                passwd = QString()
                # FIXME: readPassword call changed in KDE 4.4
                try:
                    # New KDE 4.4 version
                    passwd = self.wallet.readPassword(self.settings["accounts"][i].username)[1]
                except:
                    self.wallet.readPassword(self.settings["accounts"][i].username, passwd)
                    print "wallet.readPassword error:", sys.exc_info()[0]
                self.settings["accounts"][i].setPasswd(unicode(passwd))
                self.settings["accountlist"][i]["passwd"] = unicode(passwd)
            
            # Now start checking for emails
            self.checkMail()
            #self.timer.start(self.settings["pollinterval"] * 60000)