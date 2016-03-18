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
import requests
import yaml


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
        htmlbody = '<body onload="window.close()"></body>'
      else:
        self.server.set_onetimecode("")
        print "no match " + self.path
        htmlbody = '<body><p>An Error occurred while requesting a strava access token</p></body>'

      self.wfile.write("<html><head><title>Access Token Request</title></head>")
      self.wfile.write(htmlbody)
      self.wfile.write("</html>")
      self.wfile.close()

def post_file_to_strava(client, filename):
    return requests.post("https://www.strava.com/api/v3/uploads", data={'data_type' : 'tcx'}, files={'file' : open(filename, 'rb')}, headers={'Authorization' : 'Bearer ' + client.access_token})

def read_strava_auth_file():
    try:
      with open(os.path.expanduser("~/.strava_auth.yaml"), 'r') as f:
        return yaml.load(f)
    except IOError:
        return {}

def write_strava_auth_file(creds):
    with open(os.path.expanduser("~/.strava_auth.yaml"), 'w') as f:
      f.write(yaml.dump(creds))
    
def write_access_token_to_strava_auth_file(email, token):
    creds = read_strava_auth_file()
    creds[email] = token
    write_strava_auth_file(creds)

def strava_authorize(client):
    localwebserverport = 8282
    clientid=10615

    authorize_url = client.authorization_url(client_id=clientid, redirect_uri='http://localhost:'+str(localwebserverport)+'/authorized', scope='write')
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
    client.access_token = access_token

    # Now store that access token somewhere (a database?)
    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))
   
    write_access_token_to_strava_auth_file(athlete.email, client.access_token)

    

def main():
    logging.basicConfig(level=logging.DEBUG)

    client = Client()

    creds = read_strava_auth_file()
    if args.login :
      login = args.login
    else:
      login = None
      if len(creds) > 0:
        print("found strava credentials for: " )
        n = 0
        for email in creds.keys():
          print(str(n) + " " + email)
          n += 1
   
        index_input = raw_input("enter the number corresponding to your email address.  Or just press enter to use your default browser to login\n")
        if re.match("\A\d+\Z", index_input):
          index = int(index_input)
          if index < len(creds):
            login = creds.keys()[index]
    
    if login and creds.has_key(login):
      client.access_token = creds[login]
    else:
      strava_authorize(client)

    for tcxfile in args.tcx:
      r = post_file_to_strava(client, tcxfile)
      if(r.status_code == 401):
        print("invalid auth token, rerequesting authorization")
        strava_authorize(client)
        r = post_file_to_strava(client, tcxfile)

      if(r.status_code != 200):
        print("error uploading file")
        print(str(r.text))


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Uploads TCX to the Internets')
    parser.add_argument(nargs='+', dest='tcx', help='TCX files to upload')
    parser.add_argument('--login', dest='login', help='email address to use as strava login')
    args = parser.parse_args()
    #print "these are the tcx " + str(args.tcx)
    main()
