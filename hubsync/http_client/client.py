'''
http_client
'''

import urllib
import urllib2
import json

user_agent = 'Stark SyncClient(Python2.7)'
content_type_form = "application/x-www-form-urlencoded"
content_type_json = "application/json"

def do_get(url, query_parameters = {}):
    if query_parameters:
        query_string = urllib.urlencode(query_parameters)
        url = '%s?%s' % (url, query_string)
    req = urllib2.Request(url = url)
    res = urllib2.urlopen(req)
    res = res.read()
    return res

def do_delete(url):
    req = urllib2.Request(url)
    req.get_method = lambda: "DELETE"
    res = urllib2.urlopen(req)
    res = res.read()
    return res

def do_post_with_form(url, values={}):
    values  = urllib.urlencode(values)
    return do_req(method="POST", url=url, values=values, content_type=content_type_form)

def do_post_with_json(url, values={}):
    values = json.dumps(values)
    return do_req(method="POST", url=url, values=values, content_type=content_type_json)

def do_put_with_form(url, values={}):
    values  = urllib.urlencode(values)
    return do_req(method="PUT", url=url, values=values, content_type=content_type_form)

def do_put_with_json(url, values={}):
    values = json.dumps(values)
    return do_req(method="PUT", url=url, values=values, content_type=content_type_json)

def do_req(method, url, values, content_type=content_type_form):
    header_dict = {'User-Agent': user_agent, "Content-Type": content_type}
    req = urllib2.Request(url=url, data=values, headers=header_dict)
    req.get_method = lambda: method
    res = urllib2.urlopen(req)
    res = res.read()
    return res
