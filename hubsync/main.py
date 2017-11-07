'''
pull
'''
import sys
import os
hubsync_dir = os.path.abspath(os.path.dirname(__file__))
sync_dir = os.path.abspath(os.path.join(hubsync_dir, ".."))
sys.path.append(sync_dir)
from optparse import OptionParser
from configparser import ConfigParser
import shutil
from hubsync import hub
from hubsync import project
from hubsync import synchronizer

def init_project_constants():
    project.PROJECT_DIR = sync_dir

if __name__ == "__main__":
    # parse options and args
    option_parser = OptionParser()
    option_parser.add_option("-c", "--conf", metavar="conf", dest="conf", help="config file")
    (options, args) = option_parser.parse_args()
    if not options.conf:
        option_parser.print_help()
        sys.exit(-1)
    else:
        print "Config file:", options.conf
    
    # init project constants
    init_project_constants()
    print project.PROJECT_DIR
    # parse configs
    config = ConfigParser()
    config.read(options.conf)
    sections = config.sections()
    print "#########################################################"
    for sec in sections:
        sec_config = config.items(sec)
        print sec, ":", sec_config
    print "#########################################################"
    # init dirs
    pics_path = config.get("default","pics_path")
    pics_path = os.path.join(project.PROJECT_DIR, pics_path)
    print pics_path

    if not os.path.exists(pics_path):
        os.makedirs(pics_path, 0777)
    
    file_path = config.get("default","file_path")
    file_path = os.path.join(project.PROJECT_DIR, file_path)
    
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.makedirs(file_path, 0777)
    
    # sync from docker hub
    # hub.sync_dockerhub(config, args)

    sync = None
    mode = config.get("default", "mode")
    if mode == "hub":
        sync = synchronizer.HubOnlineSync(config, args, options)
    elif mode == "local":
        sync = synchronizer.LocalFileReposHmsSync(config, args, options)
    
    sync.sync()