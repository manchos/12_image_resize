from PIL import Image
import os
import argparse
import logging


logging.basicConfig(level=logging.CRITICAL)


def get_default_file_name(image, new_image):
    width, height = new_image.size
    file_extension = image.format.lower()
    filename = os.path.basename(image.filename)
    return '{}__{}x{}.{}'.format(os.path.splitext(filename)[0], width, height, file_extension)


def check_file_extension(file_path, img_formats_tuple):
    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1]
    return file_extension in img_formats_tuple


def apply_aspect_ratio_to_height_dialog():
    enter_height = input('The height does not match to the aspect ratio. '
                         'To enter this value? (yes, no)')
    if enter_height in ('', 'yes'):
        return False
    elif enter_height == 'no':
        return True


def get_valid_size(size):
    if int(size) > 0:
        return int(size)
    else:
        raise argparse.ArgumentTypeError('The size may be integer number and > 0!')


def get_valid_scale(scale):
    if float(scale) > 0:
        return float(scale)
    else:
        raise argparse.ArgumentTypeError('The scale may be fractional number and > 0!')


def get_valid_image_size(image, width, height, apply_aspect_ratio=True, default_width=200):
    aspect_ratio = image.size[1] / image.size[0]
    if (width, height) == (0, 0):
        width = default_width
        height = int(round(aspect_ratio * width))
        logging.info('Set the default width of image to {}px'.format(default_width))
    elif width:
        height = int(round(aspect_ratio * width))
    elif height:
        width = int(round(height * image.size[0] / image.size[1]))
    else:
        width, height = resize_width_and_height(image, width, height,
                                                apply_aspect_ratio=apply_aspect_ratio)
    return width, height


def resize_width_and_height(image, width, height, apply_aspect_ratio=True):
    aspect_ratio_height = int(round(image.size[1] / image.size[0] * width))
    if height != aspect_ratio_height:
        if callable(apply_aspect_ratio):
            apply_aspect_ratio = apply_aspect_ratio()
        if apply_aspect_ratio:
            height = aspect_ratio_height
    return width, height

def resize_image(image, scale, width, height, apply_aspect_ratio=True, default_width=200):
    if scale == 1:
        width, height = get_valid_image_size(
            image, width, height, apply_aspect_ratio, default_width
        )
    else:
        width, height = image.size
    return image.resize((int(round(width*scale)), int(round(height * scale))))


def set_valid_ouput_path(image, new_image, output_path, img_formats):
    if output_path:
        if os.path.isdir(output_path):
            new_image_name = get_default_file_name(image, new_image)
            return os.path.join(output_path, new_image_name)
        else:
            if (os.path.split(output_path)[0] == os.path.split(image.filename)[0] or
                    os.path.isdir(os.path.split(output_path)[0])):
                if check_file_extension(output_path, img_formats):
                    return output_path
                else:
                    logging.error('Program work with {} format'.format(*img_formats))
                    return None
    else:
        return os.path.join(os.path.dirname(image.filename),
                            get_default_file_name(image, new_image))


def parse_args():
    parser = argparse.ArgumentParser(
        description='save image with new size in output directory default file name obtain '
                    'from IMAGE_PATH like this: FILE_NAME__WIDTHxHEIGHT.FILE_EXTENSION')
    parser.add_argument('img_path', help='set path to image file to resize')
    parser.add_argument('-width', '--width', default=0, type=get_valid_size, dest="width",
                        help='set image width (integer>0)')
    parser.add_argument('-height', '--height', default=0, type=get_valid_size, dest="height",
                        help='set image height (integer>0)')
    parser.add_argument('-scale', '--scale', default=1, type=get_valid_scale, dest="scale",
                        help='set image scale (fractional number > 0)')
    parser.add_argument(
        '-output', '--output', default='', dest="output_path", help='set image path to save')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    img_formats = ('.jpg', '.jpeg', '.png')

    scale, width, height, img_path = args.scale, args.width, args.height, args.img_path

    if (not os.path.isfile(args.img_path) or
            not check_file_extension(args.img_path, img_formats_tuple=img_formats)):
        print('Check the file path and file extension. Use files with the file extension:{}'.
              format(', '.join(img_formats)))
    else:
        image = Image.open(args.img_path)
        scale, width, height = args.scale, args.width, args.height
        if scale != 1 and (height or width):
            print('The scale x{} was defined!.\n Resize with the width and height is not possible!'
                  .format(scale))
        else:
            new_image = resize_image(
                image, scale, width, height,
                apply_aspect_ratio=apply_aspect_ratio_to_height_dialog,
                default_width=200
            )
            try:
                output_path = set_valid_ouput_path(
                    image, new_image, args.output_path,
                    img_formats=img_formats
                )
                new_image.save(output_path)
            except (IOError, ValueError, KeyError) as exc:
                print('{} File {} could not be written.'.format(exc, args.output_path))
            else:
                print('file save in {} '.format(output_path))
