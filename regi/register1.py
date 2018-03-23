import argparse

import numpy as np
from skimage.color import rgb2gray
from skimage.feature import daisy
from skimage.feature import ORB, match_descriptors
from skimage.measure import ransac
from skimage import transform
from skimage.transform import PiecewiseAffineTransform
from skimage.transform import ProjectiveTransform
from skimage.transform import warp
from skimage import io
import matplotlib.pyplot as plt


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--reference', type=str, required=True)
    ap.add_argument('-s', '--sensed', type=str, required=True)
    return ap.parse_args()

def feature_registration(src, dst):
    """Register dst to src using feature detection."""
    # First convert both image to grayscale.
    src_gray = rgb2gray(src)
    dst_gray = rgb2gray(dst)

    # Scale down.
    src_scaled = transform.rescale(src_gray, 0.25)
    dst_scaled = transform.rescale(src_gray, 0.25)

    orb = ORB(n_keypoints=1000, fast_threshold=0.05)
    orb.detect_and_extract(src_scaled)
    src_keypoints = orb.keypoints
    src_descriptors = orb.descriptors

    orb.detect_and_extract(dst_scaled)
    dst_keypoints = orb.keypoints
    dst_descriptors = orb.descriptors

    matches = match_descriptors(src_descriptors, dst_descriptors, cross_check=True)

    src_points = src_keypoints[matches[:,0]][:, ::-1]
    dst_points = dst_keypoints[matches[:,0]][:, ::,-1]

    model, inlier = ransac(
        (src_points, dst_points), ProjectiveTransform, min_samples=4, residual_threshold=2)
    )

def main():
    args = cli()

    reference = io.imread(args.reference)
    sensed = io.imread(args.sensed)

    rows, cols = reference.shape
    ref_cols = np.linspace(0, cols, 20)
    ref_rows = np.linspace(0, rows, 10)
    ref_cols, ref_rows = np.meshgrid(ref_rows, ref_rows)
    src = np.dstack([ref_cols.flat, ref_rows.flat])[0]

    rows, cols = sensed.shape
    ref_cols = np.linspace(0, cols, 20)
    ref_rows = np.linspace(0, rows, 10)
    ref_cols, ref_rows = np.meshgrid(ref_rows, ref_rows)
    dst = np.dstack([ref_cols.flat, ref_rows.flat])[0]

    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)

    out = warp(sensed, tform)
    plt.subplot(211)
    plt.imshow(reference)

    plt.subplot(212)
    plt.imshow(out)

    plt.show()

if __name__ == '__main__':
    main()