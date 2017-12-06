from PIL import Image
import os
import argparse
import logging
from collections import namedtuple
logging.basicConfig(level=logging.INFO)




def resize_image(img_path='unsplash_01.jpg', new_img_path = 'unsplash_02.jpg', width=300, height=220):
    image = Image.open(img_path)
    if width and height:
        image.resize((width, height))
    elif width:
        height = int(aspect_ratio * width)
        if old_width > old_height:
            image.thumbnail((width, width))
        else:
            image.resize((width, height))

    print(image.size)
    print('{}__{}x{}.jpg'.format(os.path.basename('.'.join(img_path.split('.')[:-1])), width, height))
    # image.save('{}__{}x{}.jpg'.format(os.path.split(img_path)[1], width, height))


def set_new_file_path(image, new_image, new_file_path=''):
    if new_file_path != image:
        if os.path.exist(new_file_path):
            if os.path.isfile(new_file_path):
                return new_file_path
            else:
                file_name = set_default_file_name(image, new_image)
                return os.path.join(new_file_path, file_name)
        else:
            logging.error('Path: {} does not exist.\nThe file path will set in {}'.format(new_file_path, image.filename))
    else:
        new_file_path = os.path.dirname(image.filename)
        return os.path.join(new_file_path, set_default_file_name(image, new_image))


def set_default_file_name(image, new_image):
    width, height = new_image.size
    file_extension = os.path.split(image.filename)[1].split('.')[-1]
    return '{}__{}x{}.{}'.format(os.path.basename('.'.join(image.filename.split('.')[:-1])),
                                 width, height, file_extension)


def check_file_extension(file_path, file_extension_tuple = ('jpg', 'png')):
    file_extension = os.path.split(file_path)[1].split('.')[-1]
    return file_extension in file_extension_tuple


def set_default_path(file_path):
    if os.path.isfile(file_path):
        return os.path.split(file_path)[0]


def check_scale(scale):
    if type(scale) is float and scale > 0:
        return True
    else:
        return False


def scale_image_size(image, new_scale):
    return int(round(image.size[0] * new_scale)), int(round(image.size[1] * new_scale))


def get_valid_height(image, new_width):
    aspect_ratio = image.size[1] / image.size[0]
    return int(round(aspect_ratio * new_width))


def height_yes_no_dialog():
    enter_height = input('The height does not match to the aspect ratio. To enter this value? (yes, no)')
    if enter_height in ('', 'yes'):
        return True
    elif enter_height == 'no':
        return False


def height_matches_aspect_ratio(image, new_width, new_height):
    aspect_ratio = image.size[1] / image.size[0]
    if new_height != int(round(aspect_ratio * new_width)):
        return False
    else:
        return True


def set_cli_argument_parse():
    parser = argparse.ArgumentParser(description="Displays information about 20 random curses from coursera.org")
    parser.add_argument('img_path', help='set path to image file to resize')
    parser.add_argument('-width', '--width', default=0, type=int, dest="width", help='set image width')
    parser.add_argument('-scale', '--scale', default=1, dest="scale", help='set image height')
    parser.add_argument('-height', '--height', default=0, type=int, dest="height", help='set image height')
    parser.add_argument('-output', '--output', default='', dest="output_path", help='set image path to save')


    # parser = argparse.ArgumentParser(description="Displays information about 20 random curses from coursera.org")
    # parser.add_argument("-cachetime", "--cache_time", default=2400, type=int,
    #                     dest="cache_time", help="Set cache time interval")
    # parser.add_argument('-clearcache', '--clear_cache', action='store_true', help='Clear cache file')

    return parser.parse_args()


def validate_cli_arguments(arguments):
    # validate_arguments = {}

    # if check_path(arguments.img_path):
    pass


def set_image_with_new_size(image, scale, width, height, default_width='200'):
    if (width, height) == (0, 0):
        width = default_width
        logging.info('Set the default value of image width {}px'.format(default_width))

    if scale == 1:
        if 0 in (width, height):
            if height != 0:
                width = int(round(height * (image.size[0] / image.size[1])))
            else:
                height = get_valid_height(image, width)
        else:
            if not height_matches_aspect_ratio(image, width, height) and not height_yes_no_dialog():
                height = get_valid_height(image, width)

        new_image = image.resize((width, height))
    else:
        if height or width:
            logging.error('The scale x{} was defined!.\n Resize is not possible!'.format(scale))
            raise Exception("Resize is not possible!")
        else:
            if check_scale(scale):
                new_image = image.resize((width*scale, height*scale))
            else:
                logging.error('The scale x{} is wrong!.\n Resize is not possible!'.format(scale))
                raise Exception("Resize is not possible!")
    return new_image

def set_ouput_path(image, output_path):

    pass


if __name__ == '__main__':
    cli_args = set_cli_argument_parse()
    # image_info_class = namedtuple('ImgClass', ['image', 'aspect_ratio', 'filepath', 'filename', 'filetype'])

    print(check_file_extension(cli_args.img_path))

    if os.path.isfile(cli_args.img_path) and check_file_extension(cli_args.img_path, ('jpg', 'png')):

        image = Image.open(cli_args.img_path)

        new_image = set_image_with_new_size(image, cli_args.scale, cli_args.width, cli_args.height)

        print(new_image.size)

        print(set_default_file_name(image, new_image))
    else:
        logging.error('Check the file path: {}. Program work with jpg and png format'.format(cli_args.img_path))


    set_new_file_path(image, new_image, new_file_path='')

    print(cli_args)
    # resize_image()
