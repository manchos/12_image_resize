from PIL import Image
import os
import argparse
import logging
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


def set_file_path(image, new_file_path=''):
    if new_file_path:
        if os.path.exist(image.filename):
            return new_file_path
        else:
            logging.error('Path: {} does not exist.\nThe file path will set in {}'.format(new_file_path, image.filename))
    else:
        file_path = os.path.dirname(image.filename)
        return file_path


def scale_image_size(image, new_scale):
    return int(round(image.size[0] * new_scale)), int(round(image.size[1] * new_scale))


def set_height(image, new_width):
    aspect_ratio = image.size[1] / image.size[0]
    return int(round(aspect_ratio * new_width))


def height_matches_aspect_ratio(image, new_width, new_height):
    aspect_ratio = image.size[1] / image.size[0]
    if new_height != int(round(aspect_ratio * new_width)):
        return False
    else:
        return True


def check_input_height(image, new_width, new_height):
    if not height_matches_aspect_ratio(image, new_width, new_height):
        enter_height = input('The height does not match to the aspect ratio. To enter this value? (yes, no)')
        if enter_height in ('', 'yes'):
            enter_height = True
        elif enter_height == 'no':
            enter_height = False
        print(enter_height)


def set_cli_argument_parse(image, new_image):
    '''
width - ширина результирующей картинки, height - её высота, scale - во сколько раз увеличить изображение
(может быть меньше 1), output - куда класть результирующий файл.
    '''
    parser = argparse.ArgumentParser(description="Displays information about 20 random curses from coursera.org")
    parser.add_argument('-f', '--filepath', default='courses_info.xlsx', dest="filepath",
                        help='set path to image file to save')
    parser = argparse.ArgumentParser(description="Displays information about 20 random curses from coursera.org")
    parser.add_argument("-cachetime", "--cache_time", default=2400, type=int,
                        dest="cache_time", help="Set cache time interval")
    parser.add_argument('-clearcache', '--clear_cache', action='store_true', help='Clear cache file')

    return parser.parse_args()



def set_file_name(image):
     return '{}__{}x{}.jpg'.format(os.path.basename('.'.join(image.filename.split('.')[:-1])),
                                   image.size[0], image.size[1])


if __name__ == '__main__':

    resize_image()
