# imagenet-dataset-downloader
Tool for downloading imagenet images into training and validation sets.

Started this 'cause I couldn't find a tool that worked and organized images the way I needed them for use in the fast.ai course. Got the basics working, then found that imagenet was basically dead and the new version of fast.ai handled splitting up the dataset itself.

planned command line usage: `imagenet-dataset-downloader.py wnid -n 100 --valid 0.2 -d /path/to/dir --humanreadable -f`
`-n` - number of images per class
`--valid` - percentage held out for validation
`-d` - directory dir, which will contain train/wnid1 train/wnid2 valid/wnid1 valid/wnid2
`--humanreadable` - replace wnids with the corresponding human-readable name
`-f` - draw from the full subtree
