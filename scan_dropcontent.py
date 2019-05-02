#!/usr/bin/env python3

from requests import get
import os,json

local_processed_file = 'processed_db.json'
content_url = 'https://raw.githubusercontent.com/datdat/dropcontent/master/getme.txt'
#content_url = 'https://raw.githubusercontent.com/datdat/dropcontent/master/getme.tx'

def load_local_file():
        try:
                if os.path.exists(local_processed_file):
                        with open(local_processed_file, 'r') as f:
                                json_data = json.load(f)
                                if 'data' in json_data:
                                        return(json_data['data'])
                else:
                        return []

        except Exception as e:
                raise("Problem reading or creating file:", e)   


def write_local_file(local_content):
        try:
                with open(local_processed_file, 'w+') as f:
                        json.dump({'data': local_content},f)
        except Exception as e:
                raise("Problem writing to file:", e)


def load_remote_list():
        try:
                r = get(content_url)
        except Exeception as e:
                print('Unable to fetch content, error:', e)
                exit(1)

        if r.status_code != 200:
                print('Problem, Got back non 200:\n', r.text) 
                exit(1)
        remote_list = []
        for line in r.text.splitlines():
                remote_list.append(line)
        return remote_list


local_content = load_local_file()
remote_list = load_remote_list()

print('local content is %s' % local_content)

if local_content == remote_list:
        print('No changes, nothing to do')
        exit()

for remote_item in remote_list:
        if not remote_item in local_content:
                print('adding remote item %s' % remote_item)
                local_content.append(remote_item)

print('Updating local database.')
write_local_file(local_content)
