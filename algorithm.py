import os
import scipy.misc
from detectFingerCount import *


def runAlgorithm(dir):
    # Loop through each file in directory
    for name in os.listdir(dir):
        # Get full path of filename
        fullPath = os.path.join(dir, name)

        # Skip if not a file
        if not os.path.isfile(fullPath):
            continue

        # Skip any patch files that were added for getting HSV range to extract
        # Get what the actual finger count should be
        if name.startswith('patch'):
            continue
        elif name.startswith('zero'):
            actualFingerCount = 0
        elif name.startswith('one'):
            actualFingerCount = 1
        elif name.startswith('two'):
            actualFingerCount = 2
        elif name.startswith('three'):
            actualFingerCount = 3
        elif name.startswith('four'):
            actualFingerCount = 4
        elif name.startswith('five'):
            actualFingerCount = 5

        image = scipy.misc.imread(fullPath)
        predictedFingerCount = detectFingerCount(image)

        # TODO Check if we got it right. Also, store statistics and analyze how we did
        print('Should be: %i    Got: %i' % (actualFingerCount, predictedFingerCount))