import docker

DOCKER_REGISTRY = "localhost:5000"
DOCKER_HUB_NAMESPACE = "library"

DC = docker.Client(base_url='unix://var/run/docker.sock',version='1.12',timeout=10)

def image(name):
    return DC.images(name)

def push(image):
    DC.push(image)

def tag(image, repo_name, tag):
    DC.tag(image, repo_name, tag)