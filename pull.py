import json
import urllib2
Docker_Hub_Repo_List = "https://index.docker.io/v1/search?q=library&n=%s&page=%s"
Docker_Hub_Repo = "https://index.docker.io/v1/repositories/library/%s/tags"


def parse_result(result):
    repoList = json.loads(result)
    print(repoList["num_results"])

def get_repo_list(page_size,page_index, total_repos):
    print("Get page %s and %s records eacho page" % (page_index, page_size))
    url = Docker_Hub_Repo_List % (page_size, page_index)
    print url
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print(e)
    else:
        html = response.read()
    result = json.loads(html)
    total_repos.extend(result["results"])
    return result["num_results"]

def get_all_repos():
    repos = []
    page_size = 100
    page_index = 1
    total = get_repo_list(page_size,page_index,repos)
    print("Total repos:%s" % total)
    page_index_total = (total-1)/page_size + 1
    page_index += 1
    while page_index<=page_index_total:
        get_repo_list(page_size,page_index,repos)
        page_index += 1
    return repos

def get_tags_of(repo):
    print("Process repo: %s" % repo["name"])
    url = Docker_Hub_Repo % repo["name"]
    print url
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print(e)
    else:
        html = response.read()
    result = json.loads(html)
    repo["tags"] = result

def 



def main():
    repos = get_all_repos()
    print len(repos)
    get_tags_of(repos[1])
    print(repos[1]["tags"])


if __name__ == "__main__":
    main()