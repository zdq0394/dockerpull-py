'''
hms_client
'''
from hubsync.http_client import client

class Repo(object):
    ''' Repo
	Namespace   string    `json:"namespace,omitempty"`
	Name        string    `json:"name,omitempty"`
    LogoUrl     string    `json:"logoUrl"`
	Summary     string    `json:"summary,omitempty"`
	Description string    `json:"description,omitempty"`
	Origin      string    `json:"origin,omitempty"`
	Labels      []string  `json:"labels,omitempty"`
	Tags        []string  `json:"tags,omitempty"`
	CodeSource  string    `json:"codeSource,omitempty"`
	IsPub       bool      `json:"isPub,omitempty"`
	IsCertified bool      `json:"isCertified,omitempty"`
	CreatedAt   time.Time `json:"createdAt,omitempty"`
	UpdatedAt   time.Time `json:"updatedAt,omitempty"`
	IsDeleted   bool      `json:"isDeleted,omitempty"`
	DeletedAt   time.Time `json:"deletedAt,omitempty"`
	Stars       uint32    `json:"stars,omitempty"`
	Pulls       uint32    `json:"pulls,omitempty"`
    '''
    def __init__(self, namespace, repo_name, origin, logo_url = "",
                 labels=None, is_pub=True, is_certified=False,
                 code_source=None, summary=None, description=None):
        self.namespace = namespace
        self.name = repo_name
        self.logoUrl = logo_url
        self.summary = summary
        self.description = description
        self.origin = origin
        self.labels = labels
        self.isPub = is_pub
        self.isCertified = is_certified
        self.codeSource = code_source
    
    @staticmethod
    def from_repo(namespace, repo):
        '''
        from_repo
        generate repo object from repo dict get from DockerHub
        '''
        meta = repo.get("meta")
        full_desc = ""
        logo_url = ""
        if meta:
            full_desc = repo["meta"]["full_description"]
            logo = meta.get("logo_url")
            if logo:
                large = logo.get("large")
                small = logo.get("small")
                logo_url = large or small

        return Repo(namespace=namespace, 
                repo_name=repo["name"], 
                origin="docker",
                labels=[],
                logo_url = logo_url,
                summary=repo["description"], 
                description=full_desc)


class Image(object):
    ''' Image
	Namespace string    `json:"namespace"`
	RepoName  string    `json:"repoName"`
	Tag       string    `json:"tag"`
	Hash      string    `json:"hash"`
	Size      int64     `json:"size"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
	IsDeleted bool      `json:"isDeleted"`
	DeletedAt time.Time `json:"deletedAt"`
    '''
    def __init__(self, namespace, repo_name, tag, hash_str, size):
        self.namespace = namespace
        self.repoName = repo_name
        self.tag = tag
        self.hash = hash_str
        self.size = size
    
    @staticmethod
    def from_image(namespace, repo_name, tag, image):
        hash_str = ""
        size = 0
        if image:
            hash_str = image["Id"][7:]
            size = image["Size"]
        return Image(namespace=namespace, 
                    repo_name=repo_name, 
                    tag=tag, 
                    hash_str=hash_str,
                    size=size)

class HmsClient(object):
    ''' HmsClient
    '''
    def __init__(self, hms_server):
        self.hms_server = hms_server

    def add_repo(self, repo):
        '''
        add_repo
        add repo metadata to hms
        '''
        print "Add repo %s" % repo.name
        url1 = "http://%s/v1/hms/namespaces/%s/repos" % (self.hms_server, repo.namespace)
        print url1
        try:
            client.do_put_with_json(url1, repo.__dict__)
        except Exception, e:
            print e


    def update_repo(self, repo):
        '''
        update_repo
        update repo metadata to hms
        '''
        print "Update repo %s" % repo.name
        url1 = "http://%s/v1/hms/namespaces/%s/repos/%s" % (self.hms_server, repo.namespace, repo.name)
        print url1
        try:
            client.do_post_with_json(url1, repo.__dict__)
        except Exception as e:
            print e


    def add_image(self, image):
        '''
        add_image
        add image metadata to hms
        '''
        print "Add image %s/%s:%s" % (image.namespace, image.repoName, image.tag)
        url1 = "http://%s/v1/hms/namespaces/%s/repos/%s/tags" % (self.hms_server, image.namespace, image.repoName)
        try:
            client.do_put_with_json(url1, image.__dict__)
        except Exception as e:
            print e


    def update_image(self, image):
        '''
        update_image
        update image metadata to hms
        '''
        print "Update image %s/%s:%s" % (image.namespace, image.repoName, image.tag)
        url1 = "http://%s/v1/hms/namespaces/%s/repos/%s/tags/%s" % (self.hms_server, image.namespace, image.repoName, image.tag)
        try:
            client.do_post_with_json(url1, image.__dict__)
        except Exception as e:
            print e

