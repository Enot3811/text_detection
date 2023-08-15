"""ICDAR 2003 dataset classes."""


from pathlib import Path
import sys
from typing import List, Union
import xml.etree.ElementTree as ET

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.datasets.base_dataset import (
    BaseAnnotation, BaseSample, BaseDataset)


class NEOCR_annotation(BaseAnnotation):
    def __init__(
        self, x1: int, y1: int, x2: int, y2: int, language: str, word: str
    ) -> None:
        super().__init__(x1, y1, x2, y2, language, word)


class NEOCR_sample(BaseSample):
    def __init__(
        self, img_pth: Path, img_annots: List[NEOCR_annotation]
    ) -> None:
        super().__init__(img_pth, img_annots)


class NEOCR_dataset(BaseDataset):
    def __init__(self, dset_folder: Union[Path, str]) -> None:
        super().__init__()

        if isinstance(dset_folder, str):
            dset_folder = Path(dset_folder)

        annots_dir = dset_folder / 'Annotations'
        img_dir = dset_folder / 'Images'
        annots_files = annots_dir.glob('*.xml')

        self._train_set: List[NEOCR_sample] = [
            self.read_annotation_file(annots_file, img_dir)
            for annots_file in annots_files]
        self._val_set = []
        self._test_set = []

    def read_annotation_file(
        self, annot_pth: Path, img_dir: Path
    ) -> NEOCR_sample:
        """Read an annotation file of NEOCR dataset.

        Make an sample's annotation based on the read file.

        Parameters
        ----------
        annot_pth : Path
            A path to the file.
        img_dir : Path
            A path to an image directory.

        Returns
        -------
        NEOCR_sample
            The read sample annotation.
        """
        tree = ET.parse(annot_pth)
        root = tree.getroot()

        img_pth = img_dir / root[0].text
        
        annots: List[NEOCR_annotation] = []
        for image_annot in root.findall('object'):
            word = image_annot[0].text
            language = image_annot[7][1].text
            bbox = image_annot[9]

            x1 = int(bbox[1][0].text)
            y1 = int(bbox[1][1].text)
            x2 = int(bbox[3][0].text)
            y2 = int(bbox[3][1].text)

            annots.append(NEOCR_annotation(x1, y1, x2, y2, language, word))
        return NEOCR_sample(img_pth, annots)
