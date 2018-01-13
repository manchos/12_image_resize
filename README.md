# Image Resizer

Saves the image with the new dimensions in specified path

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

# Using

Run the script
```#!bash
$ python image_resize.py IMAGE_PATH


optional arguments:
  -h, --help            show this help message and exit
  -img_path IMG_PATH    set path to image file to resize
  -width WIDTH          set image width (integer)
  -height HEIGHT        set image height (integer)
  -scale SCALE          set image scale (fractional number > 0)
  -output OUTPUT_PATH   set image path to save (default directory of IMAGE_PATH )

```

and save image with new size in output directory
default file name obtain from IMAGE_PATH like this:
FILE_NAME__WIDTHxHEIGHT.FILE_EXTENSION
