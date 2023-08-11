"""A module that contains a base dataset, sample and annotation classes."""


from pathlib import Path
import sys
from typing import List

from numpy.typing import ArrayLike

sys.path.append(str(Path(__file__).parents[3]))
from utils.image_utils import read_image
from rcnn.rcnn_utils import draw_bounding_boxes_cv2


class BaseAnnotation:
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        language: str = 'unlabeled',
        word: str = ''
    ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.language = language
        self.word = word


class BaseSample:
    def __init__(
        self, img_pth: Path, img_annots: List[BaseAnnotation]
    ) -> None:
        self.img_pth = img_pth
        self.img_annots = img_annots

    def get_image(self) -> ArrayLike:
        return read_image(self.img_pth)
    
    def get_image_with_bboxes(self) -> ArrayLike:
        img = self.get_image()
        bboxes = list(map(lambda anns: (anns.x1, anns.y1, anns.x2, anns.y2),
                          self.img_annots))
        labels = list(map(lambda anns: anns.language, self.img_annots))
        return draw_bounding_boxes_cv2(img, bboxes, labels)


class BaseDataset:
    def __init__(self) -> None:
        self.train_set: List[BaseSample]
        self.val_set: List[BaseSample]
        self.test_set: List[BaseSample]
