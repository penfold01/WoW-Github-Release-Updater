# WoW Addon Updater

Updates WoW addons via Github releases.  This specifically checks for packaged .zip assets included with release.  The script downloads each updated release (after Y/N prompt), extracts the contents, and copies new files to WoW addon directory.

## Setup

This script expects a config file named "default.cfg" (in python ConfigParser INI format) and a list of addons in "addonList.csv". Examples of each of these files is given as "example-..."

#### default.cfg

Contains a default section with the InstallPath variable containing the base install directory for your WoW install.

#### addonList.csv

Each row is given in the format Repo-Owner,Repo-Name,Version-Number  
Owner and name info is in the repo URL. For example the URL for WeakAuras is https://github.com/WeakAuras/WeakAuras2, so the owner is WeakAuras and the Repo name is WeakAuras2.  For version number it checks for any version different to the existing, so for newly added entries the example gives 0 as the current version number.

## Running the script

The script is executed via command line.  
```bash
python addonUpdater.py
```
For each new release found the script will prompt Y/N for download.  This is due to WeakAuras including both Retail and Classic builds for each release.  
```
Update TellMeWhen to version 9.0.2 from https://github.com/ascott18/TellMeWhen/releases/download/9.0.2/TellMeWhen-9.0.2.zip? Y/N
```