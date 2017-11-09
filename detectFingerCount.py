import skimage.exposure
import skimage.filters
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import skimage.morphology
import sklearn.cluster


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

def segmentHand(image):
    i = 4

def detectFingerCount(image):
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

    segmentHand(imageHSV, 0.20, 7)

    # # Mask for hand is thresholded based on this range:
    # # Hue: 0 - 30 degrees or 300 to 360 degrees
    # # Sat: 10% - 40%
    # # Val: 20% - 90%
    # imageMask = thresholdHSV(imageHSV, np.array([0 / 360, 0.10, 0.20]), np.array([30 / 360, 0.40, 0.90]))
    # imageMask2 = thresholdHSV(imageHSV, np.array([300 / 360, 0.10, 0.20]), np.array([360 / 360, 0.40, 0.90]))
    # imageMask = imageMask | imageMask2
    #
    # # Plot results from segmentation
    # plt.subplot(2, 3, 1)
    # plt.title('Original Image')
    # plt.imshow(image, cmap="gray")
    #
    # plt.subplot(2, 3, 2)
    # plt.title('HSV Image')
    # plt.imshow(imageHSV)
    #
    # plt.subplot(2, 3, 3)
    # plt.title('Hue Band')
    # plt.imshow(imageHSV[:, :, 0], cmap="gray")
    #
    # plt.subplot(2, 3, 4)
    # plt.title('Sat Band')
    # plt.imshow(imageHSV[:, :, 1], cmap="gray")
    #
    # plt.subplot(2, 3, 5)
    # plt.title('Val Band')
    # plt.imshow(imageHSV[:, :, 2], cmap="gray")
    #
    # plt.subplot(2, 3, 6)
    # plt.title('Image Mask')
    # plt.imshow(imageMask, cmap="gray")
    # plt.tight_layout()
    #
    # # Apply binary closing to fill in any small parts of the hand
    # imageMask2 = skimage.morphology.binary_closing(imageMask, skimage.morphology.disk(10))
    #
    # # Then apply a binary opening to disconnect any small pieces from the hand. This will make it a separate object that will be handled later
    # imageMask3 = skimage.morphology.binary_opening(imageMask2, skimage.morphology.disk(10))
    #
    # # Fill any holes in the image
    # imageMask4 = scipy.ndimage.morphology.binary_fill_holes(imageMask3)
    #
    # # Finally remove any small objects in the image.
    # # TODO: Would be better to select the object with the LARGEST area since this will likely be the hand
    # imageMask5 = skimage.morphology.remove_small_objects(imageMask4, 5000)
    #
    # # Plot the filtering results
    # plt.figure()
    # plt.subplot(2, 2, 1)
    # plt.title('Mask Image 2')
    # plt.imshow(imageMask2, cmap="gray")
    #
    # plt.subplot(2, 2, 2)
    # plt.title('Mask Image 3')
    # plt.imshow(imageMask3, cmap="gray")
    #
    # plt.subplot(2, 2, 3)
    # plt.title('Mask Image 4')
    # plt.imshow(imageMask4, cmap="gray")
    #
    # plt.subplot(2, 2, 4)
    # plt.title('Mask Image 5')
    # plt.imshow(imageMask5, cmap="gray")
    # plt.tight_layout()
    #
    # plt.show()

    return 1
