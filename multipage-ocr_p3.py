#!/usr/bin/env python3
""" 
    Multi-page PDF --> Tesseract OCR --> Text
    William Wu <w@qed.ai>
    2013-03-08 
"""
# Updated to run with Python 3.6 by Ian Watt (@watty62 2018-05-30)

import argparse
import os
import random
import string
import sys
import tempfile
from pathlib import Path

from PyPDF2 import PdfFileReader


def main():
    parser = argparse.ArgumentParser(
        description="Execute tesseract OCR on a multi-page PDF."
    )
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help="Input PDF to perform OCR on",
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help="optional name for output file; if not supplied, output is [input_basename]_ocr.txt",
    )
    parser.add_argument(
        '-d',
        '--density',
        type=int,
        default=300,
        help="DPI density to supply to ImageMagick convert; defaults to 300.",
    )
    parser.add_argument(
        '-b',
        '--depth',
        type=int,
        default=8,
        help="Bit depth; defaults to 8.",
    )
    parser.add_argument(
        '-f',
        '--imageformat',
        type=str,
        default='jpg',
        help="image format (e.g., jpg, png, tif); defaults to jpg.",
    )
    parser.add_argument(
        '-p',
        '--psm',
        type=int,
        default=3,
        help="Set tesseract's layout analysis mode, see man tesseract for more details; defaults to 3.",
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        default=True,
        help="Make tesseract quiet 0 or 1; defaults to True.",
    )

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        sys.exit('ERROR: Input file \'%s\' was not found!' % input_file)

    if not input_file.suffix == ".pdf":
        sys.exit('ERROR: Input file should be a PDF.')

    dirname = input_file.parent.as_posix()
    base, ext = input_file.stem, input_file.suffix

    # Specify output file
    if args.output is None:
        if dirname == '':
            output_file = base + "_ocr.txt"
        else:
            output_file = dirname + "/" + base + "_ocr.txt"

    # Get number of pages
    with open(input_file, "rb") as fp:
        num_pages = PdfFileReader(fp).getNumPages()
        print ("Number of pages: %d" % num_pages)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # iterate through pages
        for i in range(0, num_pages):
            # Convert PDF to image format
            cmd = "convert -density {} -depth {} ".format(args.density, args.depth) + "{}[{}] -background white {}/{}.{}".format(args.input, i, tmp_dir, i, args.imageformat)
            print ("Convert PDF to image: " + cmd)
            os.system(cmd)

            # execute OCR
            cmd = "tesseract --psm %d %s/%d.%s %s/%d" % (args.psm, tmp_dir, i, args.imageformat, tmp_dir, i)
            if args.quiet: 
                    cmd = cmd + " quiet"
            print ("OCR on image: " + cmd)
            os.system(cmd)

            # concatenate results and delete them
            text_files = " ".join([tmp_dir + "/" + str(x) + ".txt" for x in range(0, num_pages)])
            cmd = "cat %s > %s" % (text_files, output_file)
            print("Concatenate OCR outputs: " + cmd)
            os.system(cmd)


if __name__ == "__main__":
    main()
