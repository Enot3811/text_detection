"""Module with custom transforms and wrappers over torchvision.transforms."""

from typing import Union, Tuple, List

import numpy as np
from numpy.typing import ArrayLike
import torch
from torch import FloatTensor, Tensor
import torchvision.transforms as transforms


class Resize:
    """Wrapper over torchvision.transforms.Resize.

    Get a FloatTensor with image with shape `(c, h, w)`,
    bounding boxes FloatTensor with shape `(n_max_obj, 4)`,
    classes FloatTensor with shape `(n_max_obj,)`
    and resize image to defined size
    with corresponding scaling of bounding boxes.
    """

    def __init__(self, size: Union[Tuple[int, int], int]) -> None:
        if isinstance(size, int):
            self.size = (size, size)
        elif isinstance(size, tuple):
            self.size = size
        else:
            raise TypeError('Size must be int or tuple.')
        self.resize = transforms.Resize(self.size, antialias=True)
        
    def __call__(
        self,
        sample: Tuple[FloatTensor, FloatTensor, FloatTensor]
    ) -> Tuple[FloatTensor, FloatTensor, FloatTensor]:
        img, bboxes, classes = sample

        orig_h, orig_w = img.shape[1:]
        img = self.resize(img)

        new_h, new_w = self.size
        scale_h = new_h / orig_h
        scale_w = new_w / orig_w

        bboxes[:, [0, 2]] *= scale_w
        bboxes[:, [1, 3]] *= scale_h

        return (img, bboxes, classes)
    

class ToTensor:
    """Custom torchvision converting to tensor.
    
    Get a uint8 ndarray with image with shape `(h, w, c)`,
    bounding boxes FloatTensor with shape `(n_max_obj, 4)`,
    classes FloatTensor with shape `(n_max_obj,)`
    and convert image to tensor type with permutation of channel dimension and
    a translation in the range from 0 to 1.
    """
    def __call__(
        self, sample: Tuple[ArrayLike, FloatTensor, FloatTensor]
    ) -> Tuple[FloatTensor, FloatTensor, FloatTensor]:
        img, bboxes, classes = sample
        img = np.transpose(img, (2, 0, 1))
        img = torch.tensor(img, dtype=torch.float32) / 255
        return (img, bboxes, classes)
    

class Normalize:
    """Wrapper over torchvision.transforms.Normalize.
    
    Get a FloatTensor with image with shape `(c, h, w)`,
    bounding boxes FloatTensor with shape `(n_max_obj, 4)`,
    classes FloatTensor with shape `(n_max_obj,)`
    and normalize image according to given mean and std values.
    """
    def __init__(
        self,
        mean: Union[FloatTensor, List[float]],
        std: Union[FloatTensor, List[float]],
        inplace: bool = True
    ) -> None:
        self.norm = transforms.Normalize(mean, std, inplace)

    def __call__(
        self,
        sample: Tuple[FloatTensor, FloatTensor, FloatTensor]
    ) -> Tuple[FloatTensor, FloatTensor, FloatTensor]:
        img, bboxes, classes = sample
        self.norm(img)
        return (img, bboxes, classes)


def to_numpy(data: Tensor, permute_channel_dim: bool = True) -> ArrayLike:
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
