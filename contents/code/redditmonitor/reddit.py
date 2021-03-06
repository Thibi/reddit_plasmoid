# -*- coding: utf-8 -*-
# Reddit.py, a python lib capable of telling determining if you have a new reddit message.

# Copyright (C) 2009 Phillip (Philluminati) Taylor <Phillip.Taylor@bcs.org.uk>
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

import cookielib, urllib, urllib2

# Turns out simplejson is included in Python 2.6 and up as json.
try:
    import json as simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError('No module named json or simplejson')


REDDIT_USER_AGENT = { 'User-agent': 'Reddit Plasmoid' }
    # Was: Mozilla/4.0 (compatible; MSIE5.5; Windows NT
REDDIT_LOGIN_URL = 'http://www.reddit.com/api/login'
REDDIT_INBOX_PAGE = 'http://www.reddit.com/message/inbox/.json'
REDDIT_PROFILE_PAGE = 'http://www.reddit.com/user/%s/about.json'


class RedditInvalidUsernamePasswordException(Exception):
    pass

class RedditNotLoggedInException(Exception):
    pass

class RedditBadJSONException(Exception):
    pass


class Reddit(object):
    
    user = None
    
    def __init__(self):
        cookie_jar = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        urllib2.install_opener(opener)
        
    def login(self, user, passwd):
        self.user = user
        
        params = urllib.urlencode({
            'id' : '#login_login-main',
            'op' : 'login-main',
            'passwd' : passwd,
            'user' : user
        })
        
        req = urllib2.Request(REDDIT_LOGIN_URL, params, REDDIT_USER_AGENT)
        retval = urllib2.urlopen(req).read()
        
        if retval.find('invalid password') != -1:
            self.logged_in = False
            raise RedditInvalidUsernamePasswordException('Log in failed. Please ensure that your username and password are correct.')
        else:
            self.logged_in = True
        
    def get_karma(self, user=None):
        if not user and not self.logged_in:
            raise RedditNotLoggedInException('You must either specify a username or log in to get karma values.')
        
        if not user :
            user = self.user
        
        req = urllib2.Request(REDDIT_PROFILE_PAGE % user, None, REDDIT_USER_AGENT)
        json_data = urllib2.urlopen(req).read()            
        
        try:
            profile = simplejson.loads(json_data)
            return (profile['data']['link_karma'], profile['data']['comment_karma'])
        
        except (KeyError, ValueError):
            raise RedditBadJSONException('The JSON returned from reddit is incomplete. Perhpas the connection was interupted or reddit is down.')

    def get_new_mail(self):
        if not self.logged_in:
            raise RedditNotLoggedInException('You must be logged in to check for new messages.')
        
        url = '%s?mark=false' % REDDIT_INBOX_PAGE
        
        req = urllib2.Request(url, None, REDDIT_USER_AGENT)
        json_data = urllib2.urlopen(req).read()
        
        try:
            inbox = simplejson.loads(json_data)
            msgs = inbox['data']['children']
            return [msg['data'] for msg in msgs if msg['data']['new'] == True]
        
        except (KeyError, ValueError):
            raise RedditBadJSONException('The JSON returned from reddit is incomplete. Perhpas the connection was interupted or reddit is down.')
    
    def mark_messages_as_read(self):
        if not self.logged_in:
            raise RedditNotLoggedInException('You must be logged in to check for new messages.')
        
        req = urllib2.Request(REDDIT_INBOX_PAGE, None, REDDIT_USER_AGENT)
        urllib2.urlopen(req).read()
