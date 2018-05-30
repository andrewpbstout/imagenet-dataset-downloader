#!/usr/bin/env python

import argparse


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('wnid', help='Imagenet wnid, example n03489162')
    p.add_argument('--nimages', '-n', type=int, default=20,
                   metavar='N_IMAGES',
                   help='Number of images per class to download')
    p.add_argument('--valid', type=float, default
    
    args = p.parse_args()
    main(wnid = args.wnid)