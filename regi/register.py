import argparse
import logging
import math
import sys

import cv2


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i1', '--input1', type=str, required=True,
        help='path to the first image')
    ap.add_argument('-i2', '--input2', type=str, required=True,
        help='path to the second image')
    return ap.parse_args()

def log():
    logging.basicConfig(filename='register.log')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)


def tofloat(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return im.astype('float64')

def register(fn1, fn2):
    im1 = cv2.imread(fn1)
    im2 = cv2.imread(fn2)

    # Create a Hanning window.
    print(im1.shape)
    im1_flt = tofloat(im1)
    im2_flt = tofloat(im2)
    hann = cv2.createHanningWindow(im1.shape[:2], cv2.CV_64F)

    # Find the shift using.
    shift = cv2.phaseCorrelate(im1_flt, im2_flt)
    print('shift: ', shift)
    radius = math.sqrt(shift.x * shift.x + shift.y*shift.y)

    if radius > 5:
        center = (im1.cols >> 1, im1.rows >> 1)
        cv2.circle(im1, center, int(radius), (0,255,0), 3)

    cv2.imshow('result', im1)
    cv2.waitKey(0)

    # Convert both images to float images.
    
    

def main():
    args = cli()

    register(args.input1, args.input2)

if __name__ == '__main__':
    log()
    main()