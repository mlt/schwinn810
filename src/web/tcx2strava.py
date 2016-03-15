#!/usr/bin/env python
# Create ~/.schwinn810.yaml with the following 3 lines
# garmin:
#   username: your_garmin_connect_user_name
#   password: your_password
# mmf:
#   username: your_mmf_user_name
#   password: your_password

import argparse
#from antd import connect        # requires python-poster
#from mmf import MMF
#from yaml import load, dump
import os, logging, re
import thread
import BaseHTTPServer
from stravalib.client import Client


class StravaCallbackServer(BaseHTTPServer.HTTPServer):
    def set_onetimecode(self, code):
      self.onetimecode = code

    def get_onetimecode(self):
      return self.onetimecode 
    
      

class StravaCallbackReceiver(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
      print self.path
      
      #regex = re.compile('\/authorized?code=(\w+)')
      m = re.match('\/authorized\?[\w%&=\-]*code=(\w+)',  self.path)
      if(m):
        self.server.set_onetimecode(str(m.group(1)))
        print "match! " + self.server.get_onetimecode()
      else:
        self.server.set_onetimecode("")
        print "no match " + self.path



def main():
    logging.basicConfig(level=logging.DEBUG)

    localwebserverport = 8282
    clientid=10615

    client = Client()
    authorize_url = client.authorization_url(client_id=clientid, redirect_uri='http://localhost:'+str(localwebserverport)+'/authorized')
    # Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
    # .....

    print( "opening " + authorize_url)

    os.system("xdg-open '" + authorize_url + "'")
    

    server_address = ('localhost', localwebserverport)
    httpd = StravaCallbackServer(server_address, StravaCallbackReceiver)
    print("waiting for user...")
    httpd.handle_request()

    # Extract the code from your webapp response
    code = httpd.get_onetimecode()
    access_token = client.exchange_code_for_token(client_id=clientid, client_secret='0d95d8ab7a142820140dada94268e663d66a7b77', code=code)
    
    # Now store that access token somewhere (a database?)
    client.access_token = access_token
    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))

    return
    parser = argparse.ArgumentParser(description='Uploads TCX to the Internets')
    parser.add_argument(nargs='+', dest='tcx', help='TCX files to upload')
    args = parser.parse_args()

    stream = file(os.path.expanduser('~/.schwinn810.yaml'), 'r')
    cfg = load(stream)

    # join

if __name__ =='__main__':
    main()
