'''
pull
'''
import docker

DOCKER_REGISTRY = "localhost:5000"
DOCKER_HUB_NAMESPACE = "library"

DC = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
