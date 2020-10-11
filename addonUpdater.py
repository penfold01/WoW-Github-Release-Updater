import csv, json, requests
from urllib.parse import urljoin

def getLatestVersion(owner, repo, current):
    url = 'https://api.github.com/repos/{}/{}/releases/latest'.format(owner, repo)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        return False
    resp = r.json()
    if resp['tag_name'] != current:
        print('Fetching {} version {} from {}'.format(repo, resp['tag_name'], resp['zipball_url']))
        return True
    return False
    

def main():
    with open('addonList.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(getLatestVersion(row[0], row[1], row[2]))

if __name__ == "__main__":
    main()