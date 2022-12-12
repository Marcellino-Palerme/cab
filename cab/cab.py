#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The ``cab`` module
    ==================

    The module can read a barcode in image.

    Notes
    -----
    Before use the module it has to define a 'cab' logging
"""

import csv
import logging

import cv2
from pyzbar.pyzbar import decode

try:
    import Image
except ImportError:
    from PIL import Image

__all__ = ['read_barcode', 'valid_barcode']


class OutMaxBarcode(Exception):
    """Raised when we find too much barcode"""
    pass

def read_barcode(i_image_path, nb_bc):
    """!@brief
        Read barcode in image

        @param i_image_path (str) path of image
        
        @param nb_bc: (int) maximum number of barcode can find in image 

        @return (list) A list of data of differents barcodes
    """
    logging.debug("IN")

    # Read image in grayscale
    img = cv2.imread(i_image_path,0)

    # Verify  the reading of image is a success
    if img is None:
        raise IOError

    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1,2))
    # Apply CLAHE on image
    cl1 = clahe.apply(img)
    temp = cl1.copy()
    datas = []
    thresold = 1
    while(thresold<255 and len(datas) < nb_bc):
        #search barcode and decode
        results = decode(temp)

        # get value of barcode
        for result in results :
            logging.debug("barcode found")
            logging.debug(result.data)
            if str(result.data, 'utf-8') not in datas:
                datas.append(str(result.data, 'utf-8'))

        # 
        temp = cl1.copy()
        temp[temp<=thresold] = 0
        temp[temp>thresold] = 255
        thresold += 5

    # Verify if there are too much barcode
    if  len(datas) > nb_bc :
        raise OutMaxBarcode

    logging.debug("OUT")
    return datas


def valid_barcode (valid_file, found_cabs):
    """!@brief
        Verify if barcode(s) are in validation file. 
        Order barcode(s)
    """
    logging.debug("IN")
    Index = []
    # read line by line validation file
    with open(valid_file, "r") as file:
        read_valid = csv.reader(file)
        # Verify if all barcodes are in same line
        for valid_tab in read_valid:
            # Verify we have the same number of barcode
            if len(found_cabs) != len(valid_tab):
                continue
            for found_cab in found_cabs:
                if found_cab in valid_tab:
                    # get position of barcode in the line
                    Index.append(valid_tab.index(found_cab))
                else:
                    Index = []
                    break
            # get out of search when we found the line contain all barcodes
            if len(Index) == len(found_cabs):
                break

    # not find the line
    if len(Index) == 0:
        return Index

    Ordered_cabs =found_cabs.copy()
    # order the barcode like in validation file 
    for i, val in enumerate(Index): 
        Ordered_cabs[val] = found_cabs[i] 

    logging.debug("OUT")
    return Ordered_cabs
