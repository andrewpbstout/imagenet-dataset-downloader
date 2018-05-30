# imagenet-dataset-downloader
Tool for downloading imagenet images into training and validation sets.

planned command line usage: `imagenet-dataset-downloader.py wnid -n 100 --valid 0.2 -d /path/to/dir --humanreadable -f`
`-n` - number of images per class
`--valid` - percentage held out for validation
`-d` - directory dir, which will contain train/wnid1 train/wnid2 valid/wnid1 valid/wnid2
`--humanreadable` - replace wnids with the corresponding human-readable name
`-f` - draw from the full subtree