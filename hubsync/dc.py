'''
image pull/push
'''
import docker
docker_client = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
def login(username, password):
    docker_client.login(username, password)

def pull_image(repo, tag="latest", registry_server=None, namespace=None):
    repo_name = "%s" % repo
    if namespace:
        repo_name = "%s/%s" %(namespace, repo_name)
    if registry_server:
        repo_name = "%s/%s" %(registry_server, repo_name)
    image_name = "%s:%s" % (repo_name, tag)
    print "Pull image: %s" % image_name
    image = None
    try:
        docker_client.pull(repo_name, tag)
        image = docker_client.inspect_image(image_name)
    except Exception, e:
        print e
    return image

def push_image(registry, namespace, repo, tag="latest", source_r=None, source_ns=None):
    try:
        repository = "%s/%s/%s" % (registry, namespace, repo)
        local_image_name = "%s:%s" % (repo, tag)
        if source_ns:
            local_image_name = "%s/%s" % (source_ns, local_image_name)
        if source_r:
            local_image_name = "%s/%s" % (source_r, local_image_name)
        
        docker_client.tag(local_image_name, repository, tag)
        print "Push image %s:%s" % (repository, tag)
        docker_client.push(repository, tag)
        print "Delete image %s:%s" % (repository, tag)
        docker_client.remove_image("%s:%s" % (repository, tag))
        print "Delete image %s" % local_image_name
        docker_client.remove_image("%s" % local_image_name)
    except Exception, e:
        print e

def sync_image_r2r(repo_name, tag_name, source_r, source_ns, target_r, target_ns):
    source_repo = "%s/%s/%s" % (source_r, source_ns, repo_name)
    docker_client.pull(source_repo, tag_name)
    target_repo = "%s/%s/%s" % (target_r, target_ns, repo_name)
    docker_client.tag("%s:%s" %(source_repo, tag_name), target_repo, tag_name)
    docker_client.push(target_repo, tag_name)

def local_exists_image(repo_name, tag):
    try:
        docker_client.get_image("%s:%s" % (repo_name, tag))
    except docker.errors.NotFound, e:
        print e
        return False
    else:
        return True