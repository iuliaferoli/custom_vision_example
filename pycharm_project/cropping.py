import cv2
import urllib
import numpy as np

# example img_url = 'https://batchscoring.blob.core.windows.net/customvisiontesting/A3_West/Transport damage/A3_West_9122421.jpg'
# example coord = [0.402596354, 0.442837417, 0.166825891, 0.477024257]
# example buffer = 10

# img_url is the url of the image in the blob storage, the coordinates are the detection results for the coil, buffer is how much we want to "zoom-out" around our coordinates
# get the image coordinates (with buffer) and the image file from the url and crop (to send to classification)
def crop_img(img_url, coord, buffer):
    img_url = urllib.parse.quote(img_url, safe="/:")
    resp = urllib.request.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if type(coord) == list:
        x1 = int(coord[0] * image.shape[1])
        y1 = int(coord[1] * image.shape[0])
        x2 = x1 + int(coord[2] * image.shape[1])
        y2 = y1 + int(coord[3] * image.shape[0])
    else:
        x1 = int(coord.left * image.shape[1])
        y1 = int(coord.top * image.shape[0])
        x2 = x1 + int(coord.width * image.shape[1])
        y2 = y1 + int(coord.height * image.shape[0])

    if x1 - buffer >= 0:
        x1 -= buffer
    if y1 - buffer >= 0:
        y1 -= buffer
    if x2 + buffer <= image.shape[1]:
        x2 += buffer
    if y2 + buffer <= image.shape[0]:
        y2 += buffer

    cropped_image = image[y1:y2, x1:x2]
    new_coord = [x1/image.shape[1], y1/image.shape[0], (x2-x1)/image.shape[1], (y2-y1)/image.shape[0]]

    return [cropped_image, new_coord]


def process_image(img_url, coord, buffer):
    img_url = urllib.parse.quote(img_url, safe="/:")
    resp = urllib.request.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    x1, y1, x2, y2 = coord[0], coord[1], coord[2], coord[3]

    if x1 - buffer >= 0:
        x1 -= buffer
    if y1 - buffer >= 0:
        y1 -= buffer
    if x2 + buffer <= image.shape[1]:
        x2 += buffer
    if y2 + buffer <= image.shape[0]:
        y2 += buffer

    new_coord = [x1 / image.shape[1], y1 / image.shape[0], (x2 - x1) / image.shape[1], (y2 - y1) / image.shape[0]]
    return [image, new_coord]

"""
cv2.imshow('image', cropped_image)
cv2.waitKey(0)
"""