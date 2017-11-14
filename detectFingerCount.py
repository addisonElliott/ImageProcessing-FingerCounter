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

    # Due to rounding errors, rescale intensity again so that the range is [0.0, 1.0]
    image = skimage.exposure.rescale_intensity(image)

    # Convert to YCbCr
    imageYCbCr = skimage.color.rgb2ycbcr(image)

    # Create an image mask that is all zeros
    imageMask = np.zeros(imageYCbCr.shape[:-1], dtype=bool)

    # imageMask = thresholdHSV(imageYCbCr, np.array([70, 50, 140]), np.array([183, 255, 180]))
    imageMask = thresholdYCbcr(imageYCbCr, np.array([0, 77, 145]), np.array([255, 255, 180]))

    # plt.figure(1)
    # plt.figure(2)
    #
    # # Apply HSV threshold for each patch from color profile and OR it with the imageMask
    # for patch in colorProfile:
    #     mask = thresholdHSV(imageYCbCr, patch[0, :], patch[1, :])
    #     imageMask = imageMask | mask
    #
    #     print('Min/Max: %s %s' % (patch[0, :], patch[1, :]))
    #
    #     # plt.figure()
    #     # plt.imshow(mask, cmap="gray")
    #     # plt.draw()

    # Show HSV image and final mask
    plt.figure(1)
    plt.clf()
    plt.title('Original Image')
    plt.imshow(image)
    plt.draw()

    plt.figure(2)
    plt.clf()
    plt.title('Original YCbCr Image')
    plt.imshow(imageYCbCr)
    plt.draw()

    plt.figure(3)
    plt.clf()
    plt.title('Y Image')
    plt.imshow(imageYCbCr[:, :, 0], cmap="gray")
    plt.draw()

    plt.figure(4)
    plt.clf()
    plt.title('Cb Image')
    plt.imshow(imageYCbCr[:, :, 1], cmap="gray")
    # print(imageYCbCr[:, :, 1].min())
    # print(imageYCbCr[:, :, 1].max())
    plt.draw()

    plt.figure(5)
    plt.clf()
    plt.title('Cr Image')
    plt.imshow(imageYCbCr[:, :, 2], cmap="gray")
    print(imageYCbCr[:, :, 2].min())
    print(imageYCbCr[:, :, 2].max())
    plt.draw()

    plt.figure(6)
    plt.clf()
    plt.title('Mask Image')
    plt.imshow(imageMask, cmap="gray")
    plt.draw()

    plt.show()
    plt.waitforbuttonpress()

    # Then apply a binary opening to disconnect any small pieces from the hand.
    # This will make it a separate object that will be handled later.
    imageMask2 = skimage.morphology.binary_opening(imageMask, skimage.morphology.disk(5))

    # Apply binary closing to fill in any small parts of the hand
    imageMask3 = skimage.morphology.binary_closing(imageMask2, skimage.morphology.disk(3))

    # Fill any holes in the image
    imageMask4 = scipy.ndimage.morphology.binary_fill_holes(imageMask3)

    # Finally remove any small objects in the image.
    # Label the objects of the image mask. Get the area for each of the labels
    imageMaskLabel = skimage.morphology.label(imageMask4)
    imageMaskProps = skimage.measure.regionprops(imageMaskLabel)

    # Sort objects based on area descending, first largest object should be the hand
    sortedAreaIndices = sorted(range(len(imageMaskProps)), key=lambda x: imageMaskProps[x].area, reverse=True)

    # Mask is the object with largest area
    imageMask5 = (imageMaskLabel == sortedAreaIndices[0] + 1)

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
    # plt.subplot(2, 3, 5)
    # plt.title('Mask Image 5')
    # plt.imshow(imageMask5, cmap="gray")
    # plt.tight_layout()
    #
    # plt.draw()
    # plt.show()
    # plt.waitforbuttonpress()

    # Retrieve contours of image mask to get outline of hand. Combine the contours into one list in case there
    # are multiple objects
    image, contours, hierarchy = cv2.findContours(imageMask5.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = np.vstack(contours)

    # Calculate convex hull of the combined contours and retrieve convexity defects
    # Convexity defects are points that deviate from the convex hull and by how much
    convexHull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, convexHull)

    # Label the objects of the image mask. Get the area for the hand mask
    imageMaskProps = skimage.measure.regionprops(imageMask5.astype(np.uint8))
    imageMaskProps = imageMaskProps[0]

    largestDimension = max(imageMaskProps.bbox[2] - imageMaskProps.bbox[0],
                           imageMaskProps.bbox[3] - imageMaskProps.bbox[1])
    dimensionThreshold = 0.2 * largestDimension

    # plt.figure(1)
    # plt.clf()
    # plt.imshow(imageMask5, cmap="gray")
    # plt.plot(contours[:, 0, 0], contours[:, 0, 1], '-g', linewidth=2)
    #
    # for i in range(defects.shape[0]):
    #     # (S)tart index, (e)nd index, (f)arthest point, (d)istance
    #     s, e, f, d = defects[i, 0]
    #     d = np.math.sqrt(d)
    #
    #     if d > dimensionThreshold:
    #         start = contours[s][0]
    #         end = contours[e][0]
    #         far = contours[f][0]
    #         plt.plot(far[0], far[1], 'b^')
    #         print(d)
    #
    # plt.draw()
    # plt.show()
    # plt.waitforbuttonpress()

    return 1
