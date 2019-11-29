import os, os.path

TRAINED_MODEL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "trained_model.h5")


def cracker(image_path):
    from tensorflow import keras
    import cv2
    import numpy as np
    import pandas as pd
    from PIL import Image
    import imutils
    from openpyxl import Workbook

    import re
    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, Activation
    from keras.utils import to_categorical
    from tensorflow.keras.callbacks import ModelCheckpoint

    # Create a pandas dataframe for 244x956 = 233265 pixels
    col = [x for x in range(233264)]

    road_pixels = pd.DataFrame(columns=col)

    z = 0
    image = cv2.imread(image_path)
    image = cv2.resize(image, (960, 540))
    r = (4, 122, 956, 244)
    img = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # get mean and standard deviation of pixel colour values
    means, stddevs = cv2.meanStdDev(imgHSV)

    # Set lowest value of colur
    lowerBound = means - stddevs
    # Set highest value of colur
    upperBound = means + stddevs

    # kernel of 5x5 matrix of ones
    kernelOpen = np.ones((5, 5))
    # kernel of 20x20 matrix of ones
    kernelClose = np.ones((20, 20))

    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    # Use maskClose
    maskFinal = maskClose
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(maskFinal, kernel, iterations=7)

    # get contours
    conts, h = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    hull = []

    # calculate hull for each contour
    for i in range(len(conts)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(conts[i], False))

    # create matrix with a shape of img.shape
    stencil = np.zeros(img.shape).astype(img.dtype)

    # set color black for areas outside hull
    color = [255, 255, 255]
    cv2.fillPoly(stencil, hull, color)
    result = cv2.bitwise_and(img, stencil)

    # convert the processed image into Grayscale
    resultGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    block_size = 293
    constant = 2
    # Threshold converted image
    th1 = cv2.adaptiveThreshold(resultGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size,
                                constant)
    th2 = cv2.adaptiveThreshold(resultGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size,
                                constant)

    # convert the numpy array of image pixel data to list
    row = th2.ravel()
    row_as_list = row.tolist()

    # convert the lists to pandas dataframe
    road_pixels.loc[z] = row_as_list

    z += 1

    road_pixels = road_pixels.reset_index(drop=True)

    # X_train
    predict = road_pixels.to_numpy().reshape(len(road_pixels), 956, 244, 1).astype('float32')
    predict /= 255

    model = keras.models.load_model(TRAINED_MODEL_PATH)

    # predict for train set
    predicted_categories = model.predict(predict)
    predicted_categories = np.argmax(np.round(predicted_categories), axis=1)

    # predictaed labels for train set
    print(predicted_categories)
    return predicted_categories[0]