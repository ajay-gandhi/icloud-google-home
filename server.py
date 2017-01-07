
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from pyicloud import PyiCloudService
from datetime import datetime, timedelta
from dateutil.parser import parse
import urlparse
import os

# Initialize iCloud
api = PyiCloudService('YOUR EMAIL', 'YOUR PASSWORD')
print "Logged in and ready"

############################## Datetime functions ##############################

# Ceiling a datetime to the next hour
def ceilTime(dt=None):
  return (dt + timedelta(hours=1)).replace(minute=0)

# Parses a date out of given text
# Returns the non-date portion of the string and a datetime object
def parse_date(text):
  d = datetime.now()

  # "today" "tomorrow" keywords
  today = text.rfind('today')
  tomor = text.rfind('tomorrow')

  if today >= 0 or tomor >= 0:
    rem_text = None

    if today >= 0:
      # today
      rem_text = text[0:today]
    else:
      # tomorrow
      d = datetime.now() + timedelta(days=1)
      rem_text = text[0:tomor]

    time = None
    if text.rfind('at') >= 0:
      # specific time
      time = parse(text[text.rfind('at'):])
      d = d.replace(hour=time.hour, minute=time.minute)
    else:
      # round time to next hour
      d = ceilTime(d);

    return rem_text.rstrip(), d

  else:
    # search for date/time delimiters
    on = text.rfind(' on ')
    at = text.rfind(' at ')

    if on >= 0:
      # provided date
      if at >= 0:
        # provided date and time
        return text[0:on].rstrip(), parse(text[on:])

      else:
        # provided just date
        d = parse(text[on:])
        n = datetime.now()
        return text[0:on].rstrip(), ceilTime(d.replace(hour=n.hour, minute=n.minute))

    elif at >= 0:
      # provided just time
      d = parse(text[at:])
      return text[0:at].rstrip(), datetime.now().replace(hour=d.hour, minute=d.minute)

    else:
      # no datetime information
      return text, None

################################# Server loop ##################################

PORT_NUMBER = 8000
if 'PORT' in os.environ:
  PORT_NUMBER = int(os.environ['PORT'])

class requestHandler(BaseHTTPRequestHandler):
  
  def do_GET(self):

    # Play sound on iPhone
    if self.path == '/findPhone':
      # Headers
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()

      self.wfile.write('')
      api.devices[0].play_sound()
      print 'Played sound'
      return

    else:
      url = self.path
      path = urlparse.urlparse(url).path
      queries = urlparse.parse_qs(urlparse.urlparse(url).query)
      if path == '/reminder':
        # Validated, make reminder
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write('')
        rem_title, d = parse_date(queries['message'][0])
        api.reminders.post(rem_title, description='', collection='Reminders', dueDate=d)
        print 'Set new reminder to ' + queries['message'][0]
        return

      else:
        print 'Invalid path: ' + self.path
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write('')
        return

try:
  server = HTTPServer(('', PORT_NUMBER), requestHandler)
  print 'Server started on port ' , PORT_NUMBER
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()
