"""A union text dataset classes.

This class is used as a unique text dataset that unions the other datasets.
"""


from pathlib import Path
import sys
from typing import List

from numpy.typing import NDArray

sys.path.append(str(Path(__file__).parents[3]))
from utils.image_utils import read_image
from rcnn.rcnn_utils import draw_bounding_boxes_cv2
from utils.data_utils.datasets import BaseAnnotation, BaseSample, BaseDataset


class UnionTextSample(BaseSample):
    def __init__(
        self, img_pth: Path, img_annots: List[BaseAnnotation], orig_dset_name: str, img_name: str
    ) -> None:
        self._img_pth = img_pth
        self._img_annots = img_annots

    def get_image(self) -> NDArray:
        """Get source image of this sample.

        Returns
        -------
        NDArray
            The source image of this sample.
        """
        return read_image(self._img_pth)
    
    def get_image_with_bboxes(self) -> NDArray:
        """Get this sample's image with showed bounding boxes.

        Returns
        -------
        NDArray
            The image with bounding boxes.
        """
        img = self.get_image()
        bboxes = list(map(lambda anns: (anns.x1, anns.y1, anns.x2, anns.y2),
                          self._img_annots))
        labels = list(map(lambda anns: anns.language, self._img_annots))
        return draw_bounding_boxes_cv2(img, bboxes, labels)
    
    def get_annotations(self) -> List[BaseAnnotation]:
        """Get annotations of this sample.

        Returns
        -------
        List[BaseAnnotation]
            The annotations of this sample.
        """
        return self._img_annots


class BaseDataset:
    def __init__(self) -> None:
        self._train_set: List[BaseSample]
        self._val_set: List[BaseSample]
        self._test_set: List[BaseSample]

    def __getitem__(self, set_name: str) -> List[BaseSample]:
        if set_name == 'train':
            return self._train_set
        elif set_name == 'val':
            return self._val_set
        elif set_name == 'test':
            return self._test_set
        else:
            raise KeyError('Available sets: "train", "val", "test".')
