'''
registry
'''
import urllib
import urllib2
import json
import base64

def get_catalog_token():
    scope = "registry:catalog:*"
    return get_token(scope)

def get_repository_token(repository_fullname):
    scope =  "repository:%s:*" % repository_fullname
    return get_token(scope)

def get_token(scope):
    url="https://authgate-dev.cloudappl.com/v2/token"
    query_parameters = {}
    query_parameters["service"] = "token-service"
    query_parameters["scope"] = scope
    
    if query_parameters:
        query_string = urllib.urlencode(query_parameters)
        url = '%s?%s' % (url, query_string)
    print(url)
    req = urllib2.Request(url = url)
    req.add_header("Authorization", "Basic "+base64.standard_b64encode("%s:%s" %("admin", "keadmin")))
    res = urllib2.urlopen(req)
    res = res.read()
    return res

if __name__ == "__main__":
    print get_catalog_token()