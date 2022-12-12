#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""!@brief
    The ``argument`` module
    =======================

    This module pool command line called
"""

from argparse import ArgumentParser, RawTextHelpFormatter

__all__ = ['arguments']


def arguments():
    """!@brief
        Take arguments for file when it call by command line

        @return Namespace with options
    """
    # Define all parameters

    parser = ArgumentParser(conflict_handler='resolve',
                            formatter_class=RawTextHelpFormatter)

    # use command line
    parser.add_argument("-l", "--commandline", dest="line", action="store_true",
                        default=False,
                        help="use command line")

    # Directory where are images with barcode
    parser.add_argument("-i", "--input", dest="input", type=str,
                        help="Directory where are images with barode")

    # Directory where are file to modified
    parser.add_argument("-o", "--output", dest="output", type=str,
                        help="Directory where we save results",)
    
    # Number maximum of barcode by image
    parser.add_argument("-n", dest="nb_bc", default=1, type=int,
                        help="Number maximum of barcode by image")
    
    # path of validation file
    parser.add_argument("-v", "--valid", dest="valid", type=str,
                        help="Path of validation file. Mandatory if n>1",)

    # Export csv
    parser.add_argument("-c", "--csv", dest="csv", action="store_true",
                        default=False,
                        help="Export results in csv file")

    # Copy and Rename images with barcode
    parser.add_argument("-b", dest="barcode", action="store_true",
                        default=False,
                        help="Copy and Rename images with barcode")

    # Copy and Rename images with barcode_namefile
    parser.add_argument("-p", "--prefix", dest="prefix", action="store_true",
                        default=False,
                        help="Copy and Rename images with barcode_namefile")

    # Copy and Rename images with namefile_barcode
    parser.add_argument("-s", "--suffix", dest="suffix", action="store_true",
                        default=False,
                        help="Copy and Rename images with namefile_barcode")

    # Allow not use validation file
    parser.add_argument("-f", "--force", dest="force", action="store_true",
                        default=False,
                        help="Allow not use validation file when n>1")

    # Take value of arguments
    args = parser.parse_args()
    
    # Verify parameters only in command line
    if not args.line : 
        return args

    # Verify if output directory define
    if not args.output:
        # output directory is same of input
        args.output = args.input

    # Verify we have validation file
    if not args.force and args.nb_bc > 1 and args.valid is None :
        parser.error("The validation file is mandatory or put flag -f")  

    # Verify at least one out flag
    if not(args.csv or args.barcode or args.prefix or args.suffix):
        parser.error("Miss output format")

    
    return args
