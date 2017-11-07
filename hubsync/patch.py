'''
patch
'''
from hubsync import hms_client
from hubsync import dc

def patch(image_list, source_r, source_ns, target_r, target_ns, hmsclient):
    for image in image_list:
        image_tag = image.split(":")
        repo_name = image_tag[0]
        tag = "latest"
        if len(image_tag) == 2:
            tag = image_tag[1]
        image = dc.pull_image(repo_name, tag, source_r, source_ns)
        dc.push_image(target_r, target_ns, repo_name, tag, source_r, source_ns)
        image_obj = hms_client.Image.from_image(target_ns, repo_name, tag, image)
        hmsclient.update_image(image_obj)
