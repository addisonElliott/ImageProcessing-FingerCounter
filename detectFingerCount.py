import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
import skimage.color
import skimage.exposure
import skimage.filters
import skimage.measure
import skimage.morphology
import sklearn.cluster
import math
import constants


def thresholdYCbcr(ycbcrImage, low, high):
    yImage = ycbcrImage[:, :, 0]
    cbImage = ycbcrImage[:, :, 1]
    crImage = ycbcrImage[:, :, 2]

    yMask = (yImage >= low[0]) & (yImage <= high[0])
    cbMask = (cbImage >= low[1]) & (cbImage <= high[1])
    crMask = (crImage >= low[2]) & (crImage <= high[2])

    return yMask & cbMask & crMask


def kmeans(image, k, isVector=False):
    # Flatten the image so that all of the values are in an array
    # If the image is a vector, then do not combine the last dimension
    flattenedImage = image.reshape(-1, image.shape[-1] if isVector else 1)

    centroids, labels, inertia = sklearn.cluster.k_means(flattenedImage, k)

    return centroids, labels.reshape(image.shape[:-1] if isVector else image.shape), inertia


def detectFingerCount(image, colorProfile):
    # Convert to float
    image = skimage.exposure.rescale_intensity(image.astype(float))

    # Convert to YCbCr
    imageYCbCr = skimage.color.rgb2ycbcr(image)

    # Apply threshold based on color profile
    imageMask = thresholdYCbcr(imageYCbCr, colorProfile[0, :], colorProfile[1, :])

    # # Testing image mask
    # imageMask = thresholdYCbcr(imageYCbCr, np.array([120, 77, 140]), np.array([255, 127, 180]))

    # # Show YCbCr image and final mask
    # plt.figure(1)
    # plt.clf()
    # plt.title('Original Image')
    # plt.imshow(image)
    # plt.draw()
    #
    # plt.figure(2)
    # plt.clf()
    # plt.title('Original YCbCr Image')
    # plt.imshow(imageYCbCr)
    # plt.draw()
    #
    # plt.figure(3)
    # plt.clf()
    # plt.title('Y Image')
    # plt.imshow(imageYCbCr[:, :, 0], cmap="gray")
    # plt.draw()
    #
    # plt.figure(4)
    # plt.clf()
    # plt.title('Cb Image')
    # plt.imshow(imageYCbCr[:, :, 1], cmap="gray")
    # plt.draw()
    #
    # plt.figure(5)
    # plt.clf()
    # plt.title('Cr Image')
    # plt.imshow(imageYCbCr[:, :, 2], cmap="gray")
    # plt.draw()
    #
    # plt.figure(6)
    # plt.clf()
    # plt.title('Mask Image')
    # plt.imshow(imageMask, cmap="gray")
    # plt.draw()
    #
    # plt.show()
    # plt.waitforbuttonpress()

    # Erode the image to open up the gap between fingers (finger webbing)
    # In some cases, the gap may be merged together or close to it, so we want to open it
    imageMask2 = skimage.morphology.binary_erosion(imageMask, skimage.morphology.disk(5))

    # Fill any holes in the image
    imageMask3 = scipy.ndimage.morphology.binary_fill_holes(imageMask2)

    # Finally remove any small objects in the image.
    # Label the objects of the image mask. Get the area for each of the labels
    imageMaskLabel = skimage.morphology.label(imageMask3)
    imageMaskProps = skimage.measure.regionprops(imageMaskLabel)

    # Sort objects based on area descending, first largest object should be the hand
    sortedAreaIndices = sorted(range(len(imageMaskProps)), key=lambda x: imageMaskProps[x].area, reverse=True)

    # Mask is the object with largest area
    imageMask4 = (imageMaskLabel == sortedAreaIndices[0] + 1)

    # # Plot the filtering results
    # plt.figure(1)
    # plt.clf()
    # plt.subplot(2, 3, 1)
    # plt.title('Mask Image 1')
    # plt.imshow(imageMask, cmap="gray")
    #
    # plt.subplot(2, 3, 2)
    # plt.title('Mask Image 2')
    # plt.imshow(imageMask2, cmap="gray")
    #
    # plt.subplot(2, 3, 3)
    # plt.title('Mask Image 3')
    # plt.imshow(imageMask3, cmap="gray")
    #
    # plt.subplot(2, 3, 4)
    # plt.title('Mask Image 4')
    # plt.imshow(imageMask4, cmap="gray")
    #
    # plt.draw()
    # plt.show()
    # plt.waitforbuttonpress()

    # Retrieve contours of image mask to get outline of hand. Combine the contours into one list in case there
    # are multiple objects
    image, contours, hierarchy = cv2.findContours(imageMask4.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = np.vstack(contours)

    # Calculate convex hull of the combined contours and retrieve convexity defects
    # Convexity defects are points that deviate from the convex hull and by how much
    convexHull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, convexHull)

    # Label the objects of the image mask. Get the area for the hand mask
    imageMaskProps = skimage.measure.regionprops(imageMask4.astype(np.uint8))
    imageMaskProps = imageMaskProps[0]

    # plt.figure(1)
    # plt.clf()
    # plt.imshow(imageMask4, cmap="gray")
    # plt.plot(contours[:, 0, 0], contours[:, 0, 1], '-g', linewidth=2)

    fingerWebs = 0
    for i in range(defects.shape[0]):
        # (S)tart index, (e)nd index, (f)arthest point, (d)istance squared
        s, e, f, d = defects[i, 0]

        # For some reason, the contours are in a list of length 1. Remove list wrapper by getting first element
        start = contours[s][0]
        end = contours[e][0]
        far = contours[f][0]

        # Calculate each side of the triangle and use law of cosines to compute angle of defects
        a = np.linalg.norm(start - end)
        b = np.linalg.norm(start - far)
        c = np.linalg.norm(end - far)
        angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c))

        if angle < math.radians(constants.fingerAngleThreshold):
            # print('Angle: %f Dist: %f' % (angle, d))
            # plt.plot(far[0], far[1], 'b^')

            # Increment finger webs count which keeps track of how many finger webs were found
            fingerWebs = fingerWebs + 1

    # plt.draw()
    # plt.show()
    # plt.waitforbuttonpress()

    # Number of fingers up is webs plus one
    return min(fingerWebs + 1, 5)
