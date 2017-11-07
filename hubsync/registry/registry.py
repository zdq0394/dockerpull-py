'''
registry
'''
import urllib
import urllib2
import json
import base64
import token

RegistryEndpoint = "https://reg-dev.cloudappl.com"

def get_all_repos():
    t = token.get_catalog_token()
    token_json = json.loads(t)
    t_str = token_json["token"]
    url = "%s/v2/_catalog?n=1000000" % RegistryEndpoint
    print(url)
    req = urllib2.Request(url = url)
    req.add_header("Authorization", "Bearer "+t_str)
    res = urllib2.urlopen(req)
    res = res.read()
    return res

def get_all_tags_of_repo(full_reponame):
    t = token.get_repository_token(full_reponame)
    token_json = json.loads(t)
    t_str = token_json["token"]
    url="%s/v2/%s/tags/list" % (RegistryEndpoint, full_reponame)
    print(url)
    req = urllib2.Request(url = url)
    req.add_header("Authorization", "Bearer "+t_str)
    res = urllib2.urlopen(req)
    res = res.read()
    return res

def get_all_repos_with_tags():
    repos_str = get_all_repos()
    repos_json = json.loads(repos_str)
    repo_names = repos_json["repositories"]
    repos = []
    for repo_name in repo_names:
        try:
            tags_str = get_all_tags_of_repo(repo_name)
        except Exception,e:
            print(repo_name, e)
            continue
        
        tags_json = json.loads(tags_str)
        tags_list = []
        for tag_name in tags_json["tags"]:
            tag = {}
            tag["name"] = tag_name
            tags_list.append(tag)
        tags_json["tags"] = tags_list
        repos.append(tags_json)
    return repos


if __name__ == "__main__":
    res = get_all_tags_of_repo("wangzhijun2/testhook")
    print(res)