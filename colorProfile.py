from lxml import etree
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
import skimage.exposure
import skimage.filters
import skimage.color
import constants
from detectFingerCount import grayColorCorrection

import os

def getColorProfile(path, type='minmax'):
    profilePath = os.path.join(path, 'profile.xml')

    # Load data from XML
    config = etree.parse(profilePath)
    root = config.getroot()

    imageFilename = root.find('image').text

    patchesXML = root.find('patches')
    patches = list()
    for patchXML in patchesXML:
        x, y = int(patchXML.attrib['x']), int(patchXML.attrib['y'])
        w, h = int(patchXML.attrib['w']), int(patchXML.attrib['h'])

        patches.append((x, y, w, h))

    # Load image
    image = scipy.misc.imread(os.path.join(path, imageFilename))

    # Convert to float
    image = skimage.exposure.rescale_intensity(image.astype(float))

    # Smooth image to remove noise
    image = skimage.filters.gaussian(image, sigma=3, multichannel=True)

    # Due to rounding errors, rescale intensity again so that the range is [0.0, 1.0]
    image = skimage.exposure.rescale_intensity(image)

    # # Apply gray world color correction algorithm
    # image = grayColorCorrection(image)

    # Apply adaptive histogram equalization
    image = skimage.exposure.equalize_adapthist(image)

    # Convert to HSV
    imageHSV = skimage.color.rgb2hsv(image)

    profile = list()
    for patch in patches:
        x1, y1 = patch[1], patch[0]
        x2, y2 = x1 + patch[3], y1 + patch[2]

        patchImage = imageHSV[x1:x2, y1:y2, :]

        # Get min/max values from the patch in each band (H, S, V)
        if type == 'minmax':
            min = patchImage.min(axis=(0, 1))
            max = patchImage.max(axis=(0, 1))
        elif type == 'median':
            min = np.median(patchImage, axis=(0, 1))
            max = min
        elif type == 'average':
            min = np.average(patchImage, axis=(0, 1))
            max = min
        else:
            print('Invalid type given')
            return profile

        min = min * (1 - constants.patchTolerance)
        max = max * (1 + constants.patchTolerance)

        profile.append(np.vstack((min, max)))

        # # Show the patch to determine if it looks like skin
        # plt.figure(1)
        # plt.clf()
        # plt.imshow(image[x1:x2, y1:y2, :])
        # plt.draw()
        # plt.show()
        # plt.waitforbuttonpress()
        # print('Min: %s Max %s' % (min, max))

    return profile