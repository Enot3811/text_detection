"""ICDAR 2003 dataset classes."""


from pathlib import Path
import sys
from typing import List, Union
import xml.etree.ElementTree as ET

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.datasets.base_dataset import (
    BaseAnnotation, BaseSample, BaseDataset)


class SVT_annotation(BaseAnnotation):

    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        w: Union[int, float],
        h: Union[int, float],
        word: str
    ) -> None:
        x1 = int(x)
        y1 = int(y)
        x2 = x1 + int(w)
        y2 = y1 + int(h)
        language = 'english'
        super().__init__(x1, y1, x2, y2, language, word)


class SVT_sample(BaseSample):
    def __init__(
        self, img_pth: Path, img_annots: List[SVT_annotation]
    ) -> None:
        super().__init__(img_pth, img_annots)


class SVT_dataset(BaseDataset):
    def __init__(self, dset_folder: Union[Path, str]) -> None:
        super().__init__()

        if isinstance(dset_folder, str):
            dset_folder = Path(dset_folder)

        train_annots = dset_folder / 'train.xml'
        test_annots = dset_folder / 'test.xml'

        self._train_set = self.read_set(train_annots, dset_folder)
        self._test_set = self.read_set(test_annots, dset_folder)
        self._val_set = []

    def read_set(
        self, set_annots: Path, dset_folder: Path
    ) -> List[SVT_sample]:
        """Read an annotations file of a set, generate a list of samples.

        Parameters
        ----------
        set_annots : Path
            The set directory path.
        dset_folder : Path
            A dataset folder path.

        Returns
        -------
        List[SVT_sample]
            The list of set's samples.
        """
        tree = ET.parse(set_annots)
        root = tree.getroot()

        samples: List[SVT_sample] = []
        for image_annots in root:
            img_pth = dset_folder / image_annots[0].text
            bboxes = image_annots[4]

            annots: List[SVT_annotation] = []
            for bbox in bboxes:
                x = int(bbox.attrib['x'])
                y = int(bbox.attrib['y'])
                w = int(bbox.attrib['width'])
                h = int(bbox.attrib['height'])
                word = bbox[0].text
                annots.append(SVT_annotation(x, y, w, h, word))

            samples.append(SVT_sample(img_pth, annots))
        return samples
