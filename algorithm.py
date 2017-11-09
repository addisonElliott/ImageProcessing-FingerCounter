import os
import scipy.misc
from detectFingerCount import *
from colorProfile import *


def runAlgorithm(dir):
    # Loop through each file in directory
    for name in os.listdir(dir):
        fullPath = os.path.join(dir, name)

        # Skip if not a directory
        if not os.path.isdir(fullPath):
            continue

        colorProfile = getColorProfile(fullPath)

        for name2 in os.listdir(fullPath):
            fullPath2 = os.path.join(fullPath, name2)

            # Skip non-files and the profile.xml
            if not os.path.isfile(fullPath2) or name2.endswith('profile.xml'):
                continue

            # Get what the actual finger count should be
            if name2.startswith('zero'):
                actualFingerCount = 0
            elif name2.startswith('one'):
                actualFingerCount = 1
            elif name2.startswith('two'):
                actualFingerCount = 2
            elif name2.startswith('three'):
                actualFingerCount = 3
            elif name2.startswith('four'):
                actualFingerCount = 4
            elif name2.startswith('five'):
                actualFingerCount = 5
            else:
                print('Found filename that does not start with a valid number: %s' % (name2))
                continue

            image = scipy.misc.imread(fullPath2)
            predictedFingerCount = detectFingerCount(image, colorProfile)

            # TODO Check if we got it right. Also, store statistics and analyze how we did
            print('Should be: %i    Got: %i' % (actualFingerCount, predictedFingerCount))