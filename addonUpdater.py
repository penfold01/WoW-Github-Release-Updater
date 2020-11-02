import requests, dirsync
import csv, json, configparser
from urllib.parse import urljoin
from pathlib import Path
from zipfile import ZipFile
from shutil import rmtree
from os.path import isdir

dlPath = Path.cwd() / 'addons'

def getLatestVersion(owner, repo, current):
    updatedVersion = -1
    url = 'https://api.github.com/repos/{}/{}/releases/latest'.format(owner, repo)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print('Version check for {} failed.'.format(repo))
        return -1
    resp = r.json()
    if resp['tag_name'] != current:
        updatedVersion = resp['tag_name']
        print("Found new version {}".format(updatedVersion))
        for assetItem in resp['assets']:
            if assetItem['content_type'] == 'application/zip':
                print('Update {} to version {} from {}? \033[92mY/\033[91mN\033[0m'.format(repo, updatedVersion, assetItem['browser_download_url']))
                yn = str(input()).lower()
                if yn != 'y':
                    continue
                filename = "{}-{}".format(repo, Path(assetItem['browser_download_url']).name)
                result = downloadURL(assetItem['browser_download_url'], filename)
                if result == True:
                    print("Download success.")
                    unzipFile(filename)
                else:
                    print("Download failed.")
    return updatedVersion

def downloadURL(url, filename):
    r = requests.get(url, allow_redirects=True)
    if r.status_code != requests.codes.ok:
        print("Wrong status.")
        return False
    filePath = dlPath / filename
    with open(filePath, 'wb') as f:
        f.write(r.content)
    return True

def unzipFile(filename):
    with ZipFile(dlPath / filename, 'r') as f:
        f.extractall(dlPath / 'unzipped')
    return True

def updateFiles(sourceDir, destDir):
    if isdir(sourceDir) and isdir(destDir):
        print("Copying to Addon directory...")
        dirsync.sync(sourceDir, destDir, action='sync')
        rmtree(sourceDir, ignore_errors=True)

def main():
    cfg = configparser.ConfigParser()
    cfg.read('default.cfg')
    if 'default' not in cfg:
        print('Malformed config file. Missing "[default]" section.')
        return
    if 'InstallPath' not in cfg['default']:
        print('Malformed config file. Missing WoW "InstallPath".')
        return
    installPath = Path(cfg['default']['InstallPath']) / '_retail_' / 'Interface' / 'AddOns'
    entries = []
    updatedEntries = []
    updated = False
    with open('addonList.csv', mode='r', newline='') as f:
        reader = csv.reader(f)
        entries = [row for row in reader]
        updatedEntries = []
        updated = False
        for row in entries:
            print("Checking {}".format(row[1]))
            latest = getLatestVersion(row[0], row[1], row[2])
            if latest != -1:
                row[2] = latest
                updated = True
            updatedEntries.append(row)
    if updated:
        with open('addonList.csv', mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updatedEntries)
        updateFiles(dlPath / 'unzipped', installPath)

if __name__ == "__main__":
    main()