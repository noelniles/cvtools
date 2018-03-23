from skimage.color import rgb2gray
from skimage.feature import corner_harris
from skimage.feature import corner_peaks
from skimage.feature import match_descriptors
from skimage.feature import BRIEF
from skimage.feature import CENSURE

def keypoints_censure(img):
    """Detect key points using CENSURE."""
    censure = CENSURE(mode='STAR')
    censure.detect(img)
    keypoints = censure.keypoints

    return keypoints

def keypoints_and_descriptors_brief(img):
    """Detect key point using BRIEF and return keypoints and descriptors.""" 
    gray = rgb2gray(img)
    extractor = BRIEF(patch_size=5)

    keypoints = corner_peaks(corner_harris(gray), min_distance=1)

    extractor.extract(gray, keypoints)
    keypoints = keypoints[extractor.mask]
    descriptors = extractor.descriptors

    return keypoints, descriptors

def get_matches(pts1, pts2):
    # Get the matches
    return match_descriptors(pts1, pts2, metric='hamming', cross_check=True)
