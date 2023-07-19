"""Module with utilities related to numpy."""

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
    if permute_channel_dim:
        data = data.permute(1, 2, 0)
    return data.numpy()
