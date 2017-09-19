'''
pull
'''

from optparse import OptionParser
import lib.hub as docker_hub
import json
import os

OUT_FILE_FULL = "out/repos_full.txt"
OUT_FILE_LIST = "out/repos_list.txt"

def store(obj, file):
    f = open(file, 'a')
    f.write(json.dumps(obj, indent=4))
    f.flush()
    f.close()

def sync_dockerhub(options, args):
    get_meta = options.info
    get_tags = options.tag
    pull_image = options.pull
    save = options.save
    repos = docker_hub.get_all_repos()
    print len(repos)
    for repo in repos:
        if get_meta:
            docker_hub.get_meta_of(repo)
        if get_tags:
            docker_hub.get_tags_of(repo)
    if save:
        store(repos, OUT_FILE_LIST)
    #pull image and inspect it
    for repo in repos:
        if pull_image:
            docker_hub.pull_images_of(repo)
        if save:
            store(repo, OUT_FILE_FULL)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--info", action="store_true", dest="info")
    parser.add_option("-t", "--tag", action="store_true", dest="tag")
    parser.add_option("-p", "--pull", action="store_true", dest="pull")
    parser.add_option("-s", "--save", action="store_true", dest="save")
    (options, args) = parser.parse_args()

    # sync from docker hub
    sync_dockerhub(options, args)

    
