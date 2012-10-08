# -*- coding: utf-8 -*-
import httplib2
import base64
import json
from sys import stdout



class Api(object):
    """
        Class is responsible for working with API
    """
    host = 'https://api-lon-p.elastichosts.com'
    uuid = 'f51cc9fe-27e2-4a47-a9ea-e30d7cc9c15a'
    api_key = 'DVEyGRVJAK66UndxAQDzpcudwCkCCDMFH5Rbk5GR'
    debug = 0


    def __init__(self):
        """
            Init object. Creates auth and headers and sets debug level
        """
        httplib2.debuglevel = self.debug
        self.auth = base64.encodestring( self.uuid + ':' + self.api_key).replace("\n", '')
        self.headers = {
            'Authorization' : 'Basic ' + self.auth,
            'Accept': 'application/json',
        }

    def _normalize_url(self, url):
        """
            stripes url and adds '/' to the start of url
        """
        return '/%s' % url.strip('/')


    def get_url(self, url):
        """
            Returns API data. Uses get method
        """
        h = httplib2.Http()
        resp, content = h.request(self.host + self._normalize_url(url), 'GET', headers = self.headers)
        if resp.status == 200:
            content =json.loads(content)
        return content



if __name__ == '__main__':
    api = Api()
    for server in api.get_url('/servers/info'):
        stdout.write('%s: ' % server['name'])
        for i, drive in filter(lambda x: x[0].startswith('ide:'), server.items()):
            drive_info = api.get_url('/drives/' + drive + '/info')
            stdout.write('%s ' % drive_info['name'])
        stdout.write("\n")

