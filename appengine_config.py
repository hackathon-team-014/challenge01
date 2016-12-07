from google.appengine.ext import vendor
import os
import sys

on_appengine = os.environ.get('SERVER_SOFTWARE','').startswith('Development')
if on_appengine and os.name == 'nt':
    sys.platform = 'Not Windows'

#if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
#    sys.path.insert(0, 'lib.zip')
#else:
#    if os.name == 'nt':
#        os.name = None
#        sys.platform = 'Not Windows'

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
