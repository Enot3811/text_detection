from pathlib import Path
import sys
from typing import Tuple, List, Union

sys.path.append(str(Path(__file__).parents[3]))
from utils.numpy_utils import rotate_rectangle
from utils.data_utils.datasets.base_dataset import (
    BaseAnnotation, BaseSample, BaseDataset)


class MSRA_TD500_annotation(BaseAnnotation):

    def __init__(
        self, annt_str: str
    ) -> None:
        idx, difficult, x, y, w, h, angle = annt_str.split()
        self.difficult = difficult == '1'
        self.idx = int(idx)
        
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        x1, y1, x2, y2 = self.normalize_bboxes(x, y, w, h, angle)
        super().__init__(x1, y1, x2, y2)
    
    def normalize_bboxes(
        self, x: int, y: int, w: int, h: int, angle: float
    ) -> Tuple[int, int, int, int]:
        """Rotate bbox and convert from xywh to xyxy.

        Parameters
        ----------
        x : int
            Left-up x coordinate.
        y : int
            Left-up y coordinate.
        w : int
            Width of bbox.
        h : int
            Height of bbox.
        angle : float
            Angle to rotate bbox.

        Returns
        -------
        Tuple[int, int, int, int]
            Xyxy bbox coordinates.
        """
        xlu = int(x)
        ylu = int(y)
        xrd = xlu + int(w)
        yrd = ylu + int(h)
        xld = xlu
        yld = yrd
        xru = xrd
        yru = ylu
        angle = float(angle)

        points = [(xlu, ylu), (xld, yld), (xrd, yrd), (xru, yru)]
        points = rotate_rectangle(points, angle)
        x1 = min(points, key=lambda point: point[0])[0]
        x2 = max(points, key=lambda point: point[0])[0]
        y1 = min(points, key=lambda point: point[1])[1]
        y2 = max(points, key=lambda point: point[1])[1]
        return x1, y1, x2, y2


class MSRA_TD500_sample(BaseSample):
    def __init__(
        self, img_pth: Path, img_annots: List[MSRA_TD500_annotation]
    ) -> None:
        super().__init__(img_pth, img_annots)


class MSRA_TD500_dataset(BaseDataset):
    def __init__(self, dset_folder: Union[Path, str]) -> None:
        super().__init__()

        if isinstance(dset_folder, str):
            dset_folder = Path(dset_folder)

        train_dir = dset_folder / 'train'
        test_dir = dset_folder / 'test'

        self._train_set = self.read_set(train_dir)
        self._test_set = self.read_set(test_dir)
        self._val_set = []

    def read_set(self, set_dir: Path) -> List[MSRA_TD500_sample]:
        """Read a directory with a set, generate a list of samples.

        Parameters
        ----------
        set_dir : Path
            The set directory path.

        Returns
        -------
        List[MSRA_TD500_sample]
            The list of set's samples.
        """
        annots_files = list(set_dir.glob('*.gt'))
        img_pths = list(set_dir.glob('*.JPG'))
        annots_files.sort()
        img_pths.sort()

        samples = []
        for annt_file, img_pth in zip(annots_files, img_pths):
            annots = self.read_annotation_file(annt_file)
            samples.append(MSRA_TD500_sample(img_pth, annots))
        return samples

    def read_annotation_file(
        self, annot_pth: Path
    ) -> List[MSRA_TD500_annotation]:
        """Read annotation file of MSRA TD500 dataset and get annotations list.

        Parameters
        ----------
        annot_pth : Path
            A path to file.

        Returns
        -------
        List[MSRA_TD500_annotation]
            The list of annotations.
        """
        with open(annot_pth, 'r') as f:
            lines = f.readlines()
        annots = []
        for annot_str in lines:
            annot = MSRA_TD500_annotation(annot_str)
            annots.append(annot)
        return annots
