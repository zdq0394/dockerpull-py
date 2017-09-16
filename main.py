'''
pull
'''

from optparse import OptionParser
import lib.docker_hub as docker_hub

def main():
    parser = OptionParser()
    parser.add_option("-i", "--info", action="store_true", dest="info")
    parser.add_option("-t", "--tag", action="store_true", dest="tag")
    parser.add_option("-p", "--pull", action="store_true", dest="pull")
    parser.add_option("-s", "--inspect", action="store_true", dest="inspect")
    (options, args) = parser.parse_args()
    get_meta = options.info
    get_tags = options.tag
    pull_image = options.pull
    if pull_image:
        inspect_image = options.inspect

    repos = docker_hub.get_all_repos()
    print len(repos)
    for repo in repos:
        if get_meta:
            docker_hub.get_meta_of(repo)
        if get_tags:
            docker_hub.get_tags_of(repo)

    print repos[1]["name"]

if __name__ == "__main__":
    main()

    
