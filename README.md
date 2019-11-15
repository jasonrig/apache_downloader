# Apache Downloader

I needed a script to download and verify Apache projects automatically from an appropriate mirror.
I wrote this script to help me run automated builds that depend on Apache projects without hard-coding URLs and 
protects me from forgetting to verify their hashes.

## Installation
```shell script
pip install -U git+https://github.com/jasonrig/apache_downloader.git
```

## Usage
```
$ apache-dl 
usage: apache-dl [-h] [--destination DESTINATION] project_path
```

Example:
```
$ apache-dl /nifi/nifi-registry/nifi-registry-0.5.0/nifi-registry-0.5.0-bin.tar.gz
INFO:root:Downloading Apache project /nifi/nifi-registry/nifi-registry-0.5.0/nifi-registry-0.5.0-bin.tar.gz to destination ./nifi-registry-0.5.0-bin.tar.gz
INFO:root:File size: 72.5 MB
Downloading ◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉ 100% Done.
```

The Apache project path can be found on the respective project page. For example, the [Apache nifi
download page](https://nifi.apache.org/download.html) has a binary download link of 
`https://www.apache.org/dyn/closer.lua?path=/nifi/1.10.0/nifi-1.10.0-bin.tar.gz`.
The project path is therefore `/nifi/1.10.0/nifi-1.10.0-bin.tar.gz`.