"""ICDAR 2003 dataset classes."""


from pathlib import Path
import sys
from typing import List, Union
import xml.etree.ElementTree as ET

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.datasets.base_dataset import (
    BaseAnnotation, BaseSample, BaseDataset)


class ICDAR2003_annotation(BaseAnnotation):

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


class ICDAR2003_sample(BaseSample):
    def __init__(
        self, img_pth: Path, img_annots: List[ICDAR2003_annotation]
    ) -> None:
        super().__init__(img_pth, img_annots)


class ICDAR2003_dataset(BaseDataset):
    def __init__(self, dset_folder: Union[Path, str]) -> None:
        super().__init__()

        if isinstance(dset_folder, str):
            dset_folder = Path(dset_folder)

        train_dir = dset_folder / 'SceneTrialTrain'
        test_dir = dset_folder / 'SceneTrialTest'
        sample_dir = dset_folder / 'SceneTrialSample'

        sample_set = self.read_set(sample_dir)
        self._train_set = self.read_set(train_dir) + sample_set
        self._test_set = self.read_set(test_dir)
        self._val_set = []

    def read_set(self, set_dir: Path) -> List[ICDAR2003_sample]:
        """Read a directory with a set, generate a list of samples.

        Parameters
        ----------
        set_dir : Path
            The set directory path.

        Returns
        -------
        List[ICDAR2003_sample]
            The list of set's samples.
        """
        tree = ET.parse(set_dir / 'words.xml')
        root = tree.getroot()

        samples: List[ICDAR2003_sample] = []
        for image_annots in root:
            img_pth = set_dir / image_annots[0].text
            bboxes = image_annots[2]

            annots: List[ICDAR2003_annotation] = []
            for bbox in bboxes:
                x = int(bbox.attrib['x'].split('.')[0])
                y = int(bbox.attrib['y'].split('.')[0])
                w = int(bbox.attrib['width'].split('.')[0])
                h = int(bbox.attrib['height'].split('.')[0])
                word = bbox[0].text
                annots.append(ICDAR2003_annotation(x, y, w, h, word))

            samples.append(ICDAR2003_sample(img_pth, annots))
        return samples
