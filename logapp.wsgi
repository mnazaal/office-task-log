#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/logapp/')

<VirtualHost *>
    SeverName localhost.com
    
    WSGIScriptAlias / /var/www/logapp/logapp.wsgi
</VirtualHost>
