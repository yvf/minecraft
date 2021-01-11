#!/usr/bin/env python3

import requests
import json
from pathlib import Path
import sys

print("welcome to upgrade")

print("error")

print("idk what im doing")

url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
resp = requests.get(url)
resp.raise_for_status()
latest_version = resp.json()['latest']['release']

print(f'minecraft latest version is {latest_version}')

version_json = None
for version in resp.json()['versions']:
    if version['id'] == latest_version and version['type'] == 'release':
        version_json = version['url']
        print(f'JSON URL for version {latest_version} is {version_json}')
        break

if version_json == None:
    raise RuntimeError('failed to find JSON URL for latest version')

resp = requests.get(version_json)
resp.raise_for_status()

server_url = resp.json()['downloads']['server']['url']
print(f"SHA1 of jar file: {resp.json()['downloads']['server']['sha1']}")

resp = requests.get(server_url)
resp.raise_for_status()

server_filename = f'/opt/minecraft/minecraft_server-{latest_version}.jar'

if Path(server_filename).exists():
    print(f'Minecraft server file version {latest_version} already downloaded.')
    sys.exit(0)

with open(server_filename, 'wb') as f:
    f.write(resp.content)

server_linkname = '/opt/minecraft/minecraft_server.jar'

link = Path(server_linkname)

link.unlink()

link.symlink_to(server_filename)

print('misson accomplished')
