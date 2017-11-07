'''
Synchronzier
'''
import json
import os
from hubsync import hub
from hubsync import hms_client
from hubsync import project
from hubsync.registry import registry
import urllib
import urllib2

def ignore_tag(tag_name, tag_list):
    if not tag_list:
        return False
    for tag in tag_list:
        if tag_name.find(tag) != -1:
            return True
    return False

class Synchronizer(object):
    CanPush = True
    CanUpdateHms = True
    def __init__(self, config, args, options):
        self.config = config
        self.args = args
        self.options = options
        self.repos = [] 
        
        self.hms_server = config.get("hms", "server")
        self.update_hms = config.getboolean("hms", "update")
        
        self.source_registry = config.get("registry", "source_server")
        self.source_namespace = config.get("registry", "source_namespace")
        
        self.registry = config.get("registry", "server")
        self.namespace = config.get("registry","hub_namespace")
        
        self.pull = config.getboolean("default","pull")
        self.pics_path = config.get("default","pics_path")
        self.file_path = config.get("default","file_path")
        self.logo_pic = config.getboolean("default", "logo_pic")
        
        ignored_repos = config.get("default", "ignored_repos")
        if ignored_repos:
            self.ignored_repos = ignored_repos.split(",")
        else:
            self.ignored_repos = []
        
        chosen_repos = config.get("default", "chosen_repos")
        if chosen_repos:
            self.chosen_repos = chosen_repos.split(",")
        else:
            self.chosen_repos = []

        ignored_tags = config.get("default", "ignored_tags")
        if ignored_tags:
            self.ignored_tags = ignored_tags.split(",")
        else:
            self.ignored_tags = []

        self.roundtimes = config.getint("default", "round")
        self.images_per_round = config.getint("default", "images_per_round")

    def sync(self):
        self.get_all_repos()
        print "Total offical repos %s" % str(len(self.repos))
        self.filter_repos()
        self.print_statistics()
        self.store_pics()
        if self.CanUpdateHms and self.update_hms:
            self.sync_to_hms()
        if self.CanPush and self.pull:
            self.sync_to_registry() 
    
    def filter_repos(self):
        filterred_repos = [r for r in self.repos \
           if ((not self.chosen_repos) or (self.chosen_repos and r["name"] in self.chosen_repos)) and \
             (r["name"] not in self.ignored_repos)
           ]
        self.repos = filterred_repos
        for repo in self.repos:
            if repo:
                new_tags = []
                for tag in repo["tags"]:
                    tag_name = tag["name"]
                    if not ignore_tag(tag_name, self.ignored_tags):
                        new_tags.append(tag)

                repo["tags"] = new_tags

                if self.roundtimes > 0:
                    repo["tags"] = new_tags[(self.roundtimes-1)*self.images_per_round:self.roundtimes*self.images_per_round]

                print("Round time %d will process %d images of repo %s: %s\n" %
                        (self.roundtimes, self.images_per_round, repo["name"], repo["tags"]))

    def get_all_repos(self):
        pass
    
    def sync_to_hms(self):
        if not self.repos:
            return
        c = hms_client.HmsClient(self.hms_server)
        for repo in self.repos:
            if not repo:
                continue
            repo_obj = hms_client.Repo.from_repo(self.namespace, repo)
            c.add_repo(repo_obj)
            for tag in repo["tags"]:
                image_obj = hms_client.Image.from_image(self.namespace, repo["name"], tag["name"], [])
                c.add_image(image_obj)

    
    def sync_to_registry(self):
        if not self.repos:
            return
        c = hms_client.HmsClient(self.hms_server)
        for repo in self.repos:
            hub.pull_images_of(repo, self.registry, self.namespace, True,  self.update_hms, c, self.source_registry, self.source_namespace)

    def print_statistics(self):
        general_info = {}
        repo_count = len(self.repos)
        image_count = 0
        repos_details = {}
        for repo in self.repos:
            repos_details[repo["name"]] = len(repo["tags"])
            image_count += len(repo["tags"])
    
        general_info["repos_count"] = repo_count
        general_info["image_count"] = image_count
        general_info["repos_details"] = repos_details

        self.general_info = general_info

        hub.store_json_file(self.general_info, os.path.join(project.PROJECT_DIR, self.file_path, "general_info.json"))
        hub.store_json_file(self.repos, os.path.join(project.PROJECT_DIR, self.file_path, "repo_meta.json"))

    def store_pics(self):
        if not self.repos:
            return
        for repo in self.repos:
            if not repo:
                continue
            if self.logo_pic:
                hub.download_logo_pic(repo,  os.path.join(project.PROJECT_DIR, self.pics_path))


class HubOnlineSync(Synchronizer):

    def get_all_repos(self):
        repos = hub.get_all_repos()
        for repo in repos:
            hub.get_meta_of(repo)
        for repo in repos:
            hub.get_tags_of(repo)
        self.repos = repos


class LocalFileReposHmsSync(Synchronizer): 
    def get_all_repos(self):
        local_repos_file = self.config.get("local","repos_file")
        local_repos_file = os.path.join(project.PROJECT_DIR, local_repos_file)
        repos = []
        with open(local_repos_file) as repo_data:
            repos = json.load(repo_data)
        self.repos = repos

class R2RSynchonizer(Synchronizer):
    
    def get_all_repos(self):
        local_repos_file = self.config.get("local","repos_file")
        local_repos_file = os.path.join(project.PROJECT_DIR, local_repos_file)
        repos = []
        with open(local_repos_file) as repo_data:
            repos = json.load(repo_data)
        self.repos = repos

class R2HmsDBSynchronizer(Synchronizer):

    def get_all_repos(self):
        self.repos = registry.get_all_repos_with_tags()
        


