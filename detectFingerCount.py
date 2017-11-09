import skimage.exposure
import skimage.filters
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import skimage.morphology
import sklearn.cluster
from time import sleep


def thresholdHSV(hsvImage, low, high):
    hueImage = hsvImage[:, :, 0]
    satImage = hsvImage[:, :, 1]
    valImage = hsvImage[:, :, 2]

    hueMask = (hueImage >= low[0]) & (hueImage <= high[0])
    satMask = (satImage >= low[1]) & (satImage <= high[1])
    valMask = (valImage >= low[2]) & (valImage <= high[2])

    return hueMask & satMask & valMask

def kmeans(image, k, isVector=False):
    # Flatten the image so that all of the values are in an array
    # If the image is a vector, then do not combine the last dimension
    flattenedImage = image.reshape(-1, image.shape[-1] if isVector else 1)

    centroids, labels, inertia = sklearn.cluster.k_means(flattenedImage, k)

    return centroids, labels.reshape(image.shape[:-1] if isVector else image.shape), inertia

def detectFingerCount(image, colorProfile):
    # Convert to float
    image = skimage.exposure.rescale_intensity(image.astype(float))

    # Smooth image to remove noise
    image = skimage.filters.gaussian(image, sigma=3, multichannel=True)

    # Due to rounding errors, rescale intensity again so that the range is [0.0, 1.0]
    image = skimage.exposure.rescale_intensity(image)

    # Apply adaptive histogram equalization
    image = skimage.exposure.equalize_adapthist(image)

    # Convert to HSV
    imageHSV = skimage.color.rgb2hsv(image)

    # Create an image mask that is all zeros
    imageMask = np.zeros(imageHSV.shape[:-1], dtype=bool)

    # Apply HSV threshold for each patch from color profile and OR it with the imageMask
    for patch in colorProfile:
        imageMask = imageMask | thresholdHSV(imageHSV, patch[0, :], patch[1, :])

    # # Show HSV image and final mask
    # plt.figure(1)
    # plt.title('Original Image')
    # plt.imshow(imageHSV)
    # plt.draw()
    #
    # plt.figure(2)
    # plt.title('Mask Image')
    # plt.imshow(imageMask)
    # plt.draw()
    #
    # plt.show()
    # plt.waitforbuttonpress()

    # Apply binary closing to fill in any small parts of the hand
    imageMask2 = skimage.morphology.binary_closing(imageMask, skimage.morphology.disk(10))

    # Then apply a binary opening to disconnect any small pieces from the hand.
    # This will make it a separate object that will be handled later.
    imageMask3 = skimage.morphology.binary_opening(imageMask2, skimage.morphology.disk(10))

    # Fill any holes in the image
    imageMask4 = scipy.ndimage.morphology.binary_fill_holes(imageMask3)

    # Finally remove any small objects in the image.
    # TODO: Would be better to select the object with the LARGEST area since this will likely be the hand
    imageMask5 = skimage.morphology.remove_small_objects(imageMask4, 5000)

    # Plot the filtering results
    plt.figure(1)
    plt.subplot(2, 3, 1)
    plt.title('Mask Image 1')
    plt.imshow(imageMask, cmap="gray")

    plt.subplot(2, 3, 2)
    plt.title('Mask Image 2')
    plt.imshow(imageMask2, cmap="gray")

    plt.subplot(2, 3, 3)
    plt.title('Mask Image 3')
    plt.imshow(imageMask3, cmap="gray")

    plt.subplot(2, 3, 4)
    plt.title('Mask Image 4')
    plt.imshow(imageMask4, cmap="gray")

    plt.subplot(2, 3, 5)
    plt.title('Mask Image 5')
    plt.imshow(imageMask5, cmap="gray")
    plt.tight_layout()

    plt.draw()
    plt.show()
    plt.waitforbuttonpress()

    return 1
