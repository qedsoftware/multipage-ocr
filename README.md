Multipage-OCR
===============

Description
---------------

This is a simple python script that executes tesseract OCR on a multi-page PDF. 

Each page of the PDF is converted into an image, each image is converted to text, and all text files are concatenated to produce the final output.

The script allows you to specify ImageMagick parameters in the image conversion, along with some tesseract parameters for the OCR.

William Wu (william.wu@themathpath.com), 2013 March 9 

Python 3
---------
The original script has been updated on 2018 May 20 by [Ian Watt](http://github.com/watty62) to work with Python 3.6+ on Mac OSX.  The new version is [multipage-ocr_p3.py](multipage-ocr_p3.py) 

If you experience errors at line 121 - convert PDF to image format - you can cure it by running "brew install imagemagick" as I did.  See the most popular answer to this [StackOverflow question](https://stackoverflow.com/questions/28627473/error-for-convert-command-in-command-line) which fixed the error.  

Python 2
---------
The [original script](multipage-ocr.py) created by William Wu is unchanged. 

Demo
---------------

$ python multipage_ocr.py -i input.pdf 

	Number of pages: 3
	/tmp/ocr_44XR0WPHN6
	Convert PDF to image: convert -density 300 -depth 8 input.pdf[0] -background white /tmp/ocr_44XR0WPHN6/0.jpg
	OCR on image: tesseract -psm 3 /tmp/ocr_44XR0WPHN6/0.jpg /tmp/ocr_44XR0WPHN6/0 quiet
	Convert PDF to image: convert -density 300 -depth 8 input.pdf[1] -background white /tmp/ocr_44XR0WPHN6/1.jpg
	OCR on image: tesseract -psm 3 /tmp/ocr_44XR0WPHN6/1.jpg /tmp/ocr_44XR0WPHN6/1 quiet
	Convert PDF to image: convert -density 300 -depth 8 input.pdf[2] -background white /tmp/ocr_44XR0WPHN6/2.jpg
	OCR on image: tesseract -psm 3 /tmp/ocr_44XR0WPHN6/2.jpg /tmp/ocr_44XR0WPHN6/2 quiet
	Concatenate OCR outputs: cat /tmp/ocr_44XR0WPHN6/0.txt /tmp/ocr_44XR0WPHN6/1.txt /tmp/ocr_44XR0WPHN6/2.txt > input_ocr.txt
	Cleanup temporary files: rm -r /tmp/ocr_44XR0WPHN6


Requirements
---------------
System requirements: tesseract, pypdf

To install tesseract on Mac OS X:

	$ brew install tesseract

To install pypdf:

	$ pip install pypdf

To install imagemagick 

    $ brew install imagemagick
