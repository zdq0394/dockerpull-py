'''
pull
'''
import json
import urllib2
import os
import threading
from hubsync import dc
from hubsync import hms_client
from hubsync import stats


DOCKER_HUB_REPO_LIST = "https://index.docker.io/v1/search?q=library&n=%s&page=%s"
DOCKER_HUB_REPO_TAGS = "https://index.docker.io/v1/repositories/library/%s/tags"
DOCKER_STORE_REPO_INFO = "https://store.docker.com/api/content/v1/products/images/%s"

def get_from_url(url):
    print url
    html = "{}"
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e
    else:
        html = response.read()
    return html


def _get_paged_repo(page_size, page_index, total_repos):
    print "Get page %s and %s records eacho page" % (page_index, page_size)
    url = DOCKER_HUB_REPO_LIST % (page_size, page_index)
    html = get_from_url(url)
    result = json.loads(html)
    repos = result["results"]
    for repo in repos:
        if repo["is_official"]:
            total_repos.append(repo)
    return result["num_results"]


def get_all_repos():
    repos = []
    page_size = 100
    page_index = 1
    total = _get_paged_repo(page_size, page_index, repos)
    print "Total candidate repos:%s" % total
    page_index_total = (total-1)/page_size + 1
    page_index += 1
    while page_index <= page_index_total:
        _get_paged_repo(page_size, page_index, repos)
        page_index += 1
    return repos

@stats.fn_timer
def get_tags_of(repo):
    print "Get tags of repo: %s" % repo["name"]
    url = DOCKER_HUB_REPO_TAGS % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["tags"] = result

@stats.fn_timer
def get_meta_of(repo):
    print "Get meta of repo: %s" % repo["name"]
    url = DOCKER_STORE_REPO_INFO % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["meta"] = result

@stats.fn_timer
def download_logo_pic(repo, pics_path):
    try:
        repo_meta = repo["meta"]
        logo = repo_meta["logo_url"]
        if logo:
            large = logo.get("large")
            small = logo.get("small")
            logo_url = large or small
            logo_pic = get_from_url(logo_url)
            postfix = large.rsplit('.',1)[1]
            store_pic(logo_pic, pics_path+"/"+repo["name"]+"_"+"logo."+postfix)
    except Exception, e:
        print e
        

def _get_pic_url_in_desc(desc):
    if desc:
        start = desc.find("![logo]")
        if start != -1:
            desc = desc[start+8:]
            end = desc.find(".png")
            if end != -1:
                desc = desc[:end]
                if desc.endswith(".png") or desc.endswith(".svg"):
                    print desc
                    return desc
    return None

def download_desc_pic(repo, pics_path):
    try:
        repo_meta = repo["meta"]
        desc = repo_meta.get("full_description")
        if desc:
            pic_url = _get_pic_url_in_desc(desc)
            if pic_url and (desc.endswith(".png") or desc.endswith(".svg")):
                postfix = pic_url.rsplit('.',1)[1]
                large_pic = get_from_url(pic_url)
                store_pic(large_pic, pics_path+"/"+repo["name"]+"_"+"desc."+postfix)
    except Exception, e:
        print e

def pull_images_of(repo, registry, namespace, push=False, update=False, hmsclient=None, source_r=None, source_ns=None):
    print "Pull images of repo: %s" % repo["name"]
    images = {}
    for tag in repo["tags"]:
        image = dc.pull_image(repo["name"], tag["name"], source_r, source_ns)
        images[tag["name"]] = image
        if push:
            dc.push_image(registry, namespace, repo["name"], tag["name"], source_r, source_ns)
        if update:
            image_obj = hms_client.Image.from_image(namespace, repo["name"], tag["name"], image)
            hmsclient.add_image(image_obj)
    repo["images"] = images

def store_json_file(obj, filepath):
    """
    store obj to filepath in JSON format.
    """
    f_file = open(filepath, 'w')
    f_file.write(json.dumps(obj, indent=4))
    f_file.flush()
    f_file.close()

def store_pic(pic, filepath):
    """
    store pic object to filepath.
    """
    f_file = open(filepath, 'wb')
    f_file.write(pic)
    f_file.flush()
    f_file.close()

def update_meta_of(c, namespace, repo):
    if repo:
        repo_obj = hms_client.Repo.from_repo(namespace, repo)
        c.add_repo(repo_obj)
        for tag in repo["tags"]:
            image_obj = hms_client.Image.from_image(namespace, repo["name"], tag["name"], [])
            c.add_image(image_obj)
