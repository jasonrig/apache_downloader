import hashlib
import logging
import os
import sys
from math import ceil
from os.path import basename, dirname, isdir, expanduser
from urllib.parse import urlunparse, urlencode

import humanize
import requests
from progress.bar import FillingCirclesBar
from progress.spinner import Spinner

DOWNLOAD_CHUNK_SIZE = 8192


def get_mirror_url(path):
    """
    Formats the download URL for the Apache project file path
    :param path: the download file path, e.g. /nifi/nifi-registry/nifi-registry-0.5.0/nifi-registry-0.5.0-bin.tar.gz
    :return: the direct download URL
    """
    return urlunparse(("https", "www.apache.org", "/dyn/mirrors/mirrors.cgi", "", urlencode({
        "action": "download",
        "filename": path
    }), ""))


def get_hash(path):
    """
    Get the hash value from the official apache.org website
    :param path: the download file path, e.g. /nifi/nifi-registry/nifi-registry-0.5.0/nifi-registry-0.5.0-bin.tar.gz
    :return: the sha512 hash
    """
    url = urlunparse(("https", "www.apache.org", "/dist/%s.sha512" % path.lstrip("/"), "", "", ""))
    hash = requests.get(url).text.strip()
    logging.debug("Expected hash is {hash}".format(hash=hash))
    return hash


def download_and_verify(path, destination=None):
    """
    Downloads the Apache file and verifies its hash
    :param path: the download file path, e.g. /nifi/nifi-registry/nifi-registry-0.5.0/nifi-registry-0.5.0-bin.tar.gz
    :param destination: the location to save the downloaded file or file object
    """
    destination = destination or "."
    if isinstance(destination, str):
        download_dir = dirname(destination)
        download_file = basename(destination) or basename(path)
        if isdir(download_file):
            download_dir = download_file
            download_file = basename(path)
        download_path = expanduser(os.path.join(download_dir, download_file))
        logging.info("Downloading Apache project {path} to destination {dest}".format(path=path, dest=download_path))
        assert not os.path.exists(download_path), "File already exists"
    else:
        download_path = destination
        logging.info("Downloading Apache project {path}".format(path=path))

    expected_hash = get_hash(path)

    with requests.get(get_mirror_url(path), stream=True) as r:
        r.raise_for_status()
        file_length = r.headers.get("content-length")
        if file_length:
            file_length = int(file_length)
            logging.info("File size: {size}".format(size=humanize.naturalsize(file_length)))
            progress_bar = FillingCirclesBar("Downloading", max=ceil(file_length / DOWNLOAD_CHUNK_SIZE))
        else:
            progress_bar = Spinner("Downloading")

        def save_to_file(_f):
            m = hashlib.sha512()
            for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    _f.write(chunk)
                    m.update(chunk)
                    progress_bar.next()
            assert m.hexdigest() == expected_hash, "Hash of downloaded file is invalid"

        if hasattr(download_path, "write"):
            save_to_file(download_path)
        else:
            with open(download_path, "wb") as f:
                save_to_file(f)
            assert os.path.exists(download_path), "File could not be downloaded."
    print("Done.", file=sys.stderr)
