import numpy as np
import cv2
from PIL import Image
import base64
import io


def compare_images(template, testing, delta=0):
    '''
    @template: Template image
    @testing: Testing image (actual screenshot)
    @delta: Max percentage of difference in pixels
    '''
    if template is None or testing is None:
        raise ValueError("[ERROR] Could not read properly the images")

    if template.shape != testing.shape:
        raise ValueError("[ERROR] Images do not have the same shape")

    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    testing_gray = cv2.cvtColor(testing, cv2.COLOR_RGB2GRAY)

    xor = np.bitwise_xor(template_gray, testing_gray)
    ones = cv2.countNonZero(xor)
    pixels = template.shape[1] * template.shape[0]

    # If there is at least the same delta difference, the images are different
    result = (ones / pixels) > (delta / 100.0)

    return result


def paint_image_difference(image_template, image_testing):
    '''
    Return a numpy array with the mask of differences
    '''

    if image_template is None or image_testing is None:
        raise ValueError("[ERROR] Missed one of the images")

    if image_template.shape != image_testing.shape:
        raise ValueError("[ERROR] Images do not have the same shape")

    result = cv2.absdiff(image_testing, image_template)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    if cv2.countNonZero(gray) <= 0:
        return result

    ret, thresh = cv2.threshold(gray, 1, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    cv2.drawContours(result, cnts, -1, (0, 0, 255), 1)
    return result


def extract_roi(image, x, y, width, height):
    '''
    Extracts a region of interest from an image coded as numpy array
    @image: Numpy array
    @x: x-axis position
    @y: y-axis position
    @width: Width of the image beginning from @x
    @height: Height of the image beginning from @y
    '''
    return image[y:y+height, x:x+width]


def b64_to_cv2(image):
    '''
    Converts an image coded as base64 to numpy array
    '''
    imgdata = base64.b64decode(image)
    buffer = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(buffer), cv2.COLOR_BGR2RGB)

def b64_to_bytes(b64):
    '''
    converts a b64 string to bytes type
    '''

    return base64.b64decode(b64)
