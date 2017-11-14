import os

import numpy as np
from lxml import etree


def getColorProfile(path, type='minmax'):
    profilePath = os.path.join(path, 'profile.xml')

    # Load data from XML
    config = etree.parse(profilePath)
    root = config.getroot()

    tag = root.find('ycbcr')
    profile = np.array([[int(tag.attrib['minY']), int(tag.attrib['minCb']), int(tag.attrib['minCr'])],
                        [int(tag.attrib['maxY']), int(tag.attrib['maxCb']), int(tag.attrib['maxCr'])]])

    return profile
