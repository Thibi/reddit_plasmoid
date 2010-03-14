What is it?
-----------
It is a Python and QT4 Plasmoid that's designed to notify you of new messages 
on reddit.  It was forked off of Reddit Monitor GIT on 13 March 2010.

Contributors to "Reddit Monitor":
--------------------------------
[Phillip (Philluminati) Taylor](http://github.com/PhillipTaylor)  
[David Keogh](http://github.com/davekeogh)  
[Chromakode](http://github.com/chromakode)

Contributors to this Plasmoid fork:
----------------------------------
[Thibi](http://github.com/Thibi)

Build Dependencies
------------------

    python-dev                  2.x
    python-gtk2-dev             2.12


Dependencies
------------

    python                      2.x
    python-gtk2                 2.12        
    python-simplejson           ?           Included as part of Python 2.6
    

Optional Dependencies
---------------------

    python-gnome2-extras        2.19.1      More featureful tray icon
    python-notify               0.1.x       Display pop-up notifications
    gnome-keyring               2.x         Save username & password
    xdg-utils                   1.0.x       Open the prefered web browser


I'm unsure about the exact minimum versions of most of the dependencies. If you
are unable to run Reddit Monitor for whatever reason, let me know so that I can
look in to it.


How to get it?
--------------

The latest stable version of Reddit Monitor can always be found here:
    
[http://github.com/davekeogh/reddit_monitor/downloads](http://github.com/davekeogh/reddit_monitor/downloads)

The development version can be checked out with this command:
    
    git clone git://github.com/davekeogh/reddit_monitor.git


Installation
------------

Ubuntu users can do the following:

    tar xzf reddit_monitor-0.1.0.tar.gz
    cd reddit_monitor-0.1.0
    python setup.py build
    sudo python setup.py install --install-layout=deb --prefix=/usr



Everyone else, something similar to the following should work for you:

    tar xzf reddit_monitor-0.1.0.tar.gz
    cd reddit_monitor-0.1.0
    python setup.py build
    python setup.py install


How to report bugs?
-------------------

You can add bug reports, patches, or feature requests to the issue tracker:

[http://github.com/davekeogh/reddit_monitor/issues](http://github.com/davekeogh/reddit_monitor/issues)

