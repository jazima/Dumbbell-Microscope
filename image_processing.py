from typing import Sequence
import numpy as np
import cv2

Image = np.ndarray

def normed_var(images: np.ndarray) -> np.ndarray:
    """Normed variance calculation.
    
    :param images: An (N, H, W) ndarray of greyscale images.
    :returns: A (N,) ndarray of the calculated metric.
    """
    mu = images.mean(axis=(1,2))
    v = images.var(axis=(1,2)) / mu
    return v

algorithms = {
    "normed_var" = normed_var
}

def analyze_z_stack(images, algorithm="normed_var") -> Tuple[int, np.ndarray, np.ndarray]:
    """Analyze a stack of images at varying level of focus to determine most in focus image.
    
    :param images: A sequence of images of the same microscope field taken at varying levels of focus.
    :returns: The first int is the index of the most in focus array.
    The first ndarray is the list of ranks, with the lowest ranked index representing the most in focus image.
    The second ndarray represents the raw metric calculated per image
    """
    
    N = len(images)
    H, W = images[0].shape
    
    images = np.array(
        cv2.cvtcolor(image, cv2.COLOR_RGB2GRAY) for image in images
    ).reshape(N, H, W)
    
    metric = algorithms[algorithm](images)
    
    order = metric.argsort()
    ranks = order.argsort()
    ranks = ranks.max() - ranks
    
    return np.argmin(ranks), ranks, metric
