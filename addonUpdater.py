import csv, json, requests
from urllib.parse import urljoin
from pathlib import Path
from zipfile import ZipFile

dlPath = Path.cwd() / 'addons'

def getLatestVersion(owner, repo, current):
    url = 'https://api.github.com/repos/{}/{}/releases/latest'.format(owner, repo)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print('Version check for {} failed.'.format(repo))
        return -1
    resp = r.json()
    if resp['tag_name'] != current:
        print("Found new version {}".format(resp['tag_name']))
        for assetItem in resp['assets']:
            if assetItem['content_type'] == 'application/zip':
                print('Update {} to version {} from {}? \033[92mY/\033[91mN\033[0m'.format(repo, resp['tag_name'], assetItem['browser_download_url']))
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
    return resp['tag_name']

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

def main():
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

if __name__ == "__main__":
    main()