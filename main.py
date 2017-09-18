'''
pull
'''

from optparse import OptionParser
import lib.hub as docker_hub
import json

def store(obj, file):
    f = open("out/%s" % file, 'w')
    f.write(json.dumps(obj, indent=4))
    f.flush()
    f.close()

def sync_dockerhub(options, args):
    get_meta = options.info
    get_tags = options.tag
    pull_image = options.pull
    save = options.save
    if pull_image:
        inspect_image = options.inspect

    repos = docker_hub.get_all_repos()
    print len(repos)
    store(repos, "repos_list.txt")
    for repo in repos:
        if get_meta:
            docker_hub.get_meta_of(repo)
        if get_tags:
            docker_hub.get_tags_of(repo)

    if save:
        store(repos, "repos_full.txt")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--info", action="store_true", dest="info")
    parser.add_option("-t", "--tag", action="store_true", dest="tag")
    parser.add_option("-p", "--pull", action="store_true", dest="pull")
    parser.add_option("-s", "--inspect", action="store_true", dest="inspect")
    parser.add_option("-S", "--save", action="store_true", dest="save")
    (options, args) = parser.parse_args()

    # sync from docker hub
    sync_dockerhub(options, args)

    
