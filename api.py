# -*- coding: utf-8 -*-
import httplib2
import base64
import json
from sys import stdout

class ApiException(Exception):
    def __init__(self, code=None, url=None, message=None):
        self.code, self.url, self.message = code, url, message

class Api(object):
    """
        Class is responsible for working with API
    """
    host = 'https://api-lon-p.elastichosts.com'
    uuid = 'f51cc9fe-27e2-4a47-a9ea-e30d7cc9c15a'
    api_key = 'DVEyGRVJAK66UndxAQDzpcudwCkCCDMFH5Rbk5GR'
    disable_ssl_certificate_validation = False
    debug = 0

    def __init__(self):
        """
            Init object. Creates auth and headers and sets debug level
        """
        httplib2.debuglevel = self.debug
        auth = base64.encodestring( self.uuid + ':' + self.api_key).replace("\n", '')
        self.headers = {
            'Authorization' : 'Basic ' + auth,
            'Accept': 'application/json',
        }
        self.h = httplib2.Http(disable_ssl_certificate_validation=self.disable_ssl_certificate_validation)

    def _normalize_url(self, url):
        """
            stripes url and adds '/' to the start of url
        """
        return '/%s' % url.strip('/')


    def get_url(self, url):
        """
            Returns API data. Uses get method
        """
        url = self.host + self._normalize_url(url)
        resp, content = self.h.request(url, 'GET', headers = self.headers)
        if resp.status == 200:
            content =json.loads(content)
        else:
            raise ApiException(code=resp.status, url=url, message=content)
        return content

if __name__ == '__main__':
    urls = {
        'servers_info':'/servers/info',
        'drives_info':'/drives/info',
        'drive_info':'/drives/%s/info',
    }

    api = Api()
    try:
        for server in api.get_url(urls['servers_info']):
            stdout.write('%s: ' % server['name'])
            for i, drive in filter(lambda x: x[0].startswith('ide:'), server.items()):
                drive_info = api.get_url(urls['drive_info'] %  drive)
                stdout.write('%s ' % drive_info['name'])
            stdout.write("\n")
    except ApiException, e:
        stdout.write('%s %s %s' %(e.code, e.message, e.url))