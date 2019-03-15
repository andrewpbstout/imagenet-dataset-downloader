#!/usr/bin/env python

# TODO: find the proper way to acknowledge that this is based on https://github.com/itf/imagenet-download

import argparse
import urllib.request, urllib.error, urllib.parse
from socket import timeout as TimeoutError
from socket import error as SocketError
import time
import http.client
from ssl import CertificateError
import random

WN_FULL_SUBTREE_WNIDS_URL = 'http://image-net.org/api/text/wordnet.structure.hyponym?full=1&wnid='
WN_IMG_LIST_URL = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='
WN_WNID_TO_WORD_URL = 'http://www.image-net.org/api/text/wordnet.synset.getwords?wnid='

class DownloadError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message=""):
        self.message = message


def download(url, timeout=5, retry=3, sleep=0.8):
    """Downloads a file at given URL."""
    count = 0
    while True:
        try:
            f = urllib.request.urlopen(url, timeout=timeout)
            if f is None:
                raise DownloadError('Cannot open URL' + url)
            content = f.read()
            f.close()
            break
        except (urllib.error.HTTPError, http.client.HTTPException, CertificateError) as e:
            count += 1
            if count > retry:
                raise DownloadError()
        except (urllib.error.URLError, TimeoutError, SocketError, IOError) as e:
            count += 1
            if count > retry:
                raise DownloadError('failed to open ' + url + ' after ' + str(retry) + ' retries')
            time.sleep(sleep)
        #except (Error) as e:
        #    print('otherwise uncaught error: ' + e)
    return content

def get_url_request_list_function(request_url):
    def get_url_request_list(wnid, timeout=5, retry=3):
        url = request_url + wnid
        response = download(url, timeout, retry).decode()
        lst = str.split(response)
        return lst
    return get_url_request_list


get_full_subtree_wnid = get_url_request_list_function(WN_FULL_SUBTREE_WNIDS_URL)
get_image_urls = get_url_request_list_function(WN_IMG_LIST_URL)

def get_words_wnid(wnid, timeout=5, retry=3):
    url = WN_WNID_TO_WORD_URL + wnid
    response = download(url, timeout, retry).decode().strip()
    return response

def make_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    # TODO: raise error if directory already exists and isn't empty


# with new version of fastai, I don't need to split train/valid/test
def set_up_directories(rootdir, classname):
    """rootdir is the root directory,
    classname is the wnid or human-readable name,
    directories will be rootdir/train/classname and rootdir/valid/classname.
    Creates directories if they don't exist; 
    throws an error if classname directories exist and aren't empty."""
    # TODO: might be nice if train and valid weren't hard-coded

def set_up_directory_simple(rootdir, classname):
    """rootdir is the root directory,
    classname is the wnid or human-readable name,
    directory will be rootdir/classname
    Creates directories if they don't exist; 
    throws an error if classname directories exist and aren't empty."""
    dir_path = os.path.join(rootdir, classname)


def main(wnid,
        timeout,
        retry,
        human_readable):
    # get all subtree wnids
    # TODO: wrap this in a try/except with good error message
    subtree_wnids = get_full_subtree_wnid(wnid,timeout,retry)
    for i in range(1,len(subtree_wnids)):
        subtree_wnids[i] = subtree_wnids[i][1:] #removes dash
    print("subtree_wnids: ", subtree_wnids)
    # get image url list for all wnids
    all_urls = []
    for swnid in subtree_wnids:
        # TODO: wrap this in a try/except with a good error message
        wnid_urls = get_image_urls(swnid, timeout, retry)
        all_urls += wnid_urls
    print(len(all_urls), "image urls retrieved. Randomizing...")
    # randomize in some way
    # I have efficiency concerns about this, 
    # but incremental random sampling without replacement is complicated
    random.shuffle(all_urls)
    #print("all urls, suffled: ", all_urls)
    # compute number of images in training, validation, and testing
    # todo: multithread
    # check/set up directories
    if human_readable:
        dir_name = get_words_wnid(wnid, timeout, retry)
    else:
        dir_name = wnid
    print("dir_name: ", dir_name)
    #set_up_directory_simple(rootdir, classname)
    # for number of images in each:
        # get a url
        # attempt to download
        # check handle failures; retry or get another url if necessary
        # write to correct directory

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('wnid', help='Imagenet wnid, example n03489162')
    p.add_argument('--nimages', '-n', type=int, default=20,
                metavar='N_IMAGES',
                help='Number of images per class to download')
    p.add_argument('--valid', type=float, default=0.2,
                help='Percentage of images in validation set')
    p.add_argument('--timeout', '-t', type=float, default=15,
                help='Timeout per request in seconds')
    p.add_argument('--retry', '-r', type=int, default=3,
                help='Max count of retry for each request')
    p.add_argument('--humanreadable', '-H', action='store_true',
                   help='Makes the folders human readable')


    args = p.parse_args()
    main(wnid = args.wnid,
        timeout = args.timeout,
        retry = args.retry,
        human_readable = args.humanreadable)


