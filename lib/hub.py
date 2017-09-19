'''
pull
'''
import json
import urllib2
from lib.registry import DC


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


def get_paged_repo(page_size,page_index, total_repos):
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
    total = get_paged_repo(page_size, page_index, repos)
    print "Total repos:%s" % total
    page_index_total = (total-1)/page_size + 1
    page_index += 1
    while page_index <= page_index_total:
        get_paged_repo(page_size, page_index, repos)
        page_index += 1
    return repos


def get_tags_of(repo):
    print "Get tags of repo: %s" % repo["name"]
    url = DOCKER_HUB_REPO_TAGS % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["tags"] = result

def get_meta_of(repo):
    print "Get meta of repo: %s" % repo["name"]
    url = DOCKER_STORE_REPO_INFO % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["meta"] = result

def pull_images_of(repo):
    print "Pull images of repo: %s" % repo["name"]
    images = {}
    for tag in repo["tags"]:
        image = pull_image(repo["name"], tag["name"])
        images[tag["name"]] = image
    repo["images"] = images
    # clean local images
    for tag in repo["tags"]:
        image_name = "%s:%s" % (repo["name"], tag["name"])
        DC.remove_image(image_name, force=True)

def pull_image(repo, tag="latest"):
    image_name = "%s:%s" % (repo, tag)
    print "Pull image: %s" % image_name
    image = None
    try:
        DC.pull(repo, tag)
        image = DC.inspect_image(image_name)
    except Exception, e:
        print e
    return image
