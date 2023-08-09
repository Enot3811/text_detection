from pathlib import Path
import sys
from typing import Tuple, List, Union

from numpy.typing import ArrayLike

sys.path.append(str(Path(__file__).parents[3]))
from utils.image_utils import read_image
from utils.numpy_utils import rotate_rectangle
from rcnn.rcnn_utils import draw_bounding_boxes_cv2


class MSRA_TD500_annotation:

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
        self.x1, self.y1, self.x2, self.y2 = self.normalize_bboxes(
            x, y, w, h, angle)
    
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


class MSRA_TD500_example:
    def __init__(
        self, img_pth: Path, img_annots: List[MSRA_TD500_annotation]
    ) -> None:
        self.img_pth = img_pth
        self.img_annots = img_annots

    def get_image(self) -> ArrayLike:
        return read_image(self.img_pth)
    
    def get_image_with_bboxes(self) -> ArrayLike:
        img = read_image(self.img_pth)
        bboxes = list(map(lambda anns: (anns.x1, anns.y1, anns.x2, anns.y2)))
        return draw_bounding_boxes_cv2(img, bboxes)


class MSRA_TD500_dataset:
    def __init__(self, dset_folder: Union[Path, str]) -> None:
        if isinstance(dset_folder, str):
            dset_folder = Path(dset_folder)

        train_dir = dset_folder / 'train'
        test_dir = dset_folder / 'test'

        self.train_set = self.read_set(train_dir)
        self.test_set = self.read_set(test_dir)

    def read_set(self, set_dir: Path) -> List[MSRA_TD500_example]:
        """Read a directory with a set, generate a list of examples.

        Parameters
        ----------
        set_dir : Path
            The set directory path.

        Returns
        -------
        List[MSRA_TD500_example]
            The list of set's examples.
        """
        annots_files = list(set_dir.glob('*.gt'))
        img_pths = list(set_dir.glob('*.JPG'))
        annots_files.sort()
        img_pths.sort()

        examples = []
        for annt_file, img_pth in zip(annots_files, img_pths):
            annots = self.read_annotation_file(annt_file)
            examples.append(MSRA_TD500_example(img_pth, annots))
        return examples

    def read_annotation_file(
        self, annt_pth: Path
    ) -> List[MSRA_TD500_annotation]:
        """Read annotation file of MSRA TD500 dataset and get annotations list.

        Parameters
        ----------
        annt_pth : Path
            A path to file.

        Returns
        -------
        List[MSRA_TD500_annotation]
            The list of annotations.
        """
        with open(annt_pth, 'r') as f:
            lines = f.readlines()
        annots = []
        for annot_str in lines:
            annot = MSRA_TD500_annotation(annot_str)
            annots.append(annot)
        return annots
