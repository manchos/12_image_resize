from PIL import Image
import os
import argparse
import logging


logging.basicConfig(level=logging.CRITICAL)


def get_new_image_name(width, height, filename):
    filename_without_ext, file_extension = os.path.splitext(filename)
    return '{}__{}x{}{}'.format(filename_without_ext, width,
                                height, file_extension)


def check_file_extension(file_path, img_formats_set):
    file_extension = os.path.splitext(file_path)[1]
    return file_extension in img_formats_set


def apply_aspect_ratio_to_height_dialog():
    enter_height = input('The height does not match to the aspect ratio.'
                         'To enter this value? (yes, no)')
    if enter_height in ('', 'yes'):
        return False
    elif enter_height == 'no':
        return True


def validate_size(size):
    if int(size) > 0:
        return int(size)
    else:
        raise argparse.ArgumentTypeError(
            'The size may be integer number and > 0!')


def validate_scale(scale):
    if float(scale) > 0:
        return float(scale)
    else:
        raise argparse.ArgumentTypeError(
            'The scale may be fractional number and > 0!')


def check_output_path(output_path, img_formats_set):
    dir, file_name = os.path.split(output_path)
    if dir and not os.path.isdir(dir) or (
                file_name and
                not check_file_extension(file_name, img_formats_set)):
        return False
    return True


def get_new_image_size(image, width, height, scale, aspect_ratio=True):
    if scale is not None:
        return image.size[0], image.size[1], scale
    scale = 1
    if width is None:
        width = int(round(image.size[0] / image.size[1] * height))
    aspect_ratio_height = int(round(image.size[1] / image.size[0] * width))
    if height is None:
        height = aspect_ratio_height
    else:
        height = (aspect_ratio_height
                  if (height != aspect_ratio_height and
                      apply_condition(aspect_ratio))
                  else height)
    return width, height, scale


def apply_condition(condition):
    return condition() if callable(condition) else condition


def check_valid_args(args):
    if (not os.path.isfile(args.img_path) or
        not check_file_extension(args.img_path, img_formats_set=img_formats) or
            not check_output_path(
                args.output_path,
                img_formats_set=img_formats
            )):
        print('Check the file path and file extension. '
              'Use files with the file extension:{}'.
              format(', '.join(img_formats)))
    elif not any((args.scale, args.width, args.height)):
        print('For image resize you must enter values '
              '(-scale or -width or -height)')
    elif args.scale is not None and (args.height or args.width):
        print('The scale x{} was defined!.\
              \n Resize with the width and height is not possible!'.
              format(args.scale))
    else:
        return True


def parse_args():
    parser = argparse.ArgumentParser(
        description=('save image with new size in output directory default '
                     'file name obtain from IMAGE_PATH like this: '
                     'FILE_NAME__WIDTHxHEIGHT.FILE_EXTENSION'))
    parser.add_argument('img_path', help='set path to image file to resize')
    parser.add_argument('-width', '--width', default=None,
                        type=validate_size, dest="width",
                        help='set image width (integer>0)')
    parser.add_argument('-height', '--height', default=None,
                        type=validate_size, dest="height",
                        help='set image height (integer>0)')
    parser.add_argument('-scale', '--scale', default=None,
                        type=validate_scale, dest="scale",
                        help='set image scale (fractional number > 0)')
    parser.add_argument('-output', '--output', default='', dest="output_path",
                        help='set image path to save')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    img_formats = {'.jpg', '.jpeg', '.png'}

    if check_valid_args(args):
        image = Image.open(args.img_path)
        apply_aspect_ratio = apply_aspect_ratio_to_height_dialog
        width, height, scale = get_new_image_size(
            image,
            args.width,
            args.height,
            args.scale,
            apply_aspect_ratio,
        )

        if os.path.isfile(args.output_path):
            output_path = args.output_path
        else:
            new_image_name = get_new_image_name(
                width,
                height,
                os.path.basename(image.filename)
            )
            output_dir = (os.path.dirname(image.filename)
                          if not args.output_path else args.output_path)
            output_path = os.path.join(output_dir, new_image_name)

        try:
            new_image = image.resize((int(round(width * scale)),
                                      int(round(height * scale))))
            new_image.save(output_path)
        except (IOError, ValueError, KeyError) as exc:
            print('{} File {} could not be written.'.
                  format(exc, args.output_path))
        else:
            print('file save in {} '.format(output_path))
