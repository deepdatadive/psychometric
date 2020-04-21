from uuid import uuid4
import json
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder

from collections import OrderedDict
import os

def change_status(new_status, hub_id, incident_id, user, secret):

    status_ids = {
        'Uploaded': 1627,
        'Processing': 1637,
        'Ready For Coding': 1638,
        'Coded': 1628,
        'Finished': 1629,
    }
    new_status = status_ids[new_status]
    auth = HTTPBasicAuth(
        username=user, password=secret
    )
    base_url = 'https://core.caveon.com'
    # get one incident
    one_incident = base_url + f'/api/hubs/{ hub_id }/incidents/{ incident_id }?include=data'
    response = requests.get(one_incident, auth=auth)

    data = {
        'partial_data': True,
        'status_id': 1628,
        'data': response.json()["data"]
    }

    data['status_id'] = new_status
    response = requests.put(one_incident, json=data, auth=auth)
    return 'status_changed'


def upload_file_to_core(filename, file_type, incident_id, hub_id, file_to_upload_path, user, secret):

    base_url = 'https://core.caveon.com/api/hubs/' + str(hub_id)
    post_url = base_url + '/files'
    file_size = os.path.getsize(file_to_upload_path)
    file_to_upload = open(file_to_upload_path,'rb').read()
    # step 1: post to core to get the signed post url


    post_data = {
    'step': 'sign_post',
    'replace': False,
    'mongo_id': str(uuid4()), # uuid4(): create a random uuid which is an unique id.
    'name': filename,
    'type': file_type,
    'size': file_size,
    'incident_id': incident_id,
    }

    print(post_data['mongo_id'])
    post_response = requests.post(post_url, data=json.dumps(post_data), auth=HTTPBasicAuth(user, secret)) # using the headers to classify different data.
    post_response_json = json.loads(post_response.text, object_pairs_hook=OrderedDict)
    print(post_response_json)

    payload = post_response_json['fields']
    payload['file'] = file_to_upload
    # step 2: post file to amazon
    s3_url = post_response_json['url']
    m = MultipartEncoder(fields=payload)
    s3_post = requests.post(s3_url, data=m, headers={'x-amz-server-side-encryption': 'AES256', 'Content-Type': m.content_type})
    print('status_code', s3_post.text)
    # step 3: post again to core when the upload is successful
    post_data['step'] = 'add_file'
    post_again = requests.post(post_url, data=json.dumps(post_data), auth=HTTPBasicAuth(user, secret))
    post_again_response = json.loads(post_again.text, object_pairs_hook=OrderedDict)
    print(post_again_response)
    return 'Complete'
