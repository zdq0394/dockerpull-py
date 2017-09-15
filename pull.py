import json
import urllib2
from optparse import OptionParser  

Docker_Hub_Repo_List = "https://index.docker.io/v1/search?q=library&n=%s&page=%s"
Docker_Hub_Repo = "https://index.docker.io/v1/repositories/library/%s/tags"
Docker_Store_Repo_Info = "https://store.docker.com/api/content/v1/products/images/%s"


def get_from_url(url):
    print url
    html = "{}"
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print(e)
    else:
        html = response.read()
    return html

def get_paged_repo(page_size,page_index, total_repos):
    print("Get page %s and %s records eacho page" % (page_index, page_size))
    url = Docker_Hub_Repo_List % (page_size, page_index)
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
    total = get_paged_repo(page_size,page_index,repos)
    print("Total repos:%s" % total)
    page_index_total = (total-1)/page_size + 1
    page_index += 1
    while page_index<=page_index_total:
        get_paged_repo(page_size,page_index,repos)
        page_index += 1
    return repos

def get_tags_of(repo):
    print("Get tags of repo: %s" % repo["name"])
    url = Docker_Hub_Repo % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["tags"] = result

def get_meta_of(repo):
    print("Get meta of repo: %s" % repo["name"])
    url = Docker_Store_Repo_Info % repo["name"]
    html = get_from_url(url)
    result = json.loads(html)
    repo["meta"] = result


def main():
    (options, args) = parser.parse_args()
    get_meta = options.info
    get_tags = options.tag
    pull_image = options.pull
    if pull_image:
        inspect_image = options.inspect

    repos = get_all_repos()
    print len(repos)
    for repo in repos:
        if get_meta:
            get_meta_of(repo)
        if get_tags:
            get_tags_of(repo)

    print(repos[1]["name"])


#####
parser = OptionParser()
parser.add_option("-i", "--info", action="store_true", dest="info")
parser.add_option("-t", "--tag", action="store_true", dest="tag")
parser.add_option("-p", "--pull", action="store_true", dest="pull")
parser.add_option("-s", "--inspect", action="store_true", dest="inspect")


if __name__ == "__main__":
    main()

    
