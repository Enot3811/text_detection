"""Module with utilities related to numpy."""


from typing import List, Tuple

import numpy as np
from numpy.typing import ArrayLike
from torch import Tensor


def tensor_to_numpy(
    data: Tensor, permute_channel_dim: bool = True
) -> ArrayLike:
    """Convert tensor to numpy array.

    If needed do permute for channel dimension: `(c, h, w)` -> `(h, w, c)`.

    Parameters
    ----------
    data : Tensor
        The input tensor to convert.
    permute_channel_dim : bool, optional
        Whether to permute channel dimension.

    Returns
    -------
    ArrayLike
        Converted tensor.
    """
    data = data.detach().cpu()
    if permute_channel_dim:
        data = data.permute(1, 2, 0)
    return data.numpy()


def rotate_rectangle(
    points: List[Tuple[int, int]], angle: float, radians: bool = True
) -> List[Tuple[int, int]]:
    """Rotate points of rectangle by given angle.

    Parameters
    ----------
    points : List[Tuple[int, int]]
        Points of rectangle. There must be 2 or 4.
    angle : float
        Angle to rotate.
    radians : bool, optional
        Whether angle given in radians. Otherwise in degrees. By default equals
        `True` (radians).

    Returns
    -------
    List[Tuple[int, int]]
        List of rotated rectangle points.
    """
    if not radians:
        angle = np.deg2rad(angle)
    c_x, c_y = np.mean(points, axis=0)

    points = [
        (
            int(c_x + np.cos(angle) * (px - c_x) - np.sin(angle) * (py - c_y)),
            int(c_y + np.sin(angle) * (px - c_x) + np.cos(angle) * (py - c_y)))
        for px, py in points]
    return points
