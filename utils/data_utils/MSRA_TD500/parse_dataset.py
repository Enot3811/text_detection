from pathlib import Path
import sys
from typing import Tuple, List

import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).parents[3]))
from image_utils import read_image
from numpy_utils import rotate_rectangle
from rcnn.rcnn_utils import draw_bounding_boxes_cv2


class MSRA_TD500_annotation:

    def __init__(
        self, difficult: str, x: str, y: str, w: str, h: str, angl: str
    ) -> None:
        difficult = difficult == '1'
        xlu = int(x)
        ylu = int(y)
        xrd = xlu + int(w)
        yrd = ylu + int(h)
        xld = xlu
        yld = yrd
        xru = xrd
        yru = ylu
        angl = float(angl)

        points = [(xlu, ylu), (xld, yld), (xrd, yrd), (xru, yru)]
        points = rotate_rectangle(points, angl)
        self.x1 = min(points, key=lambda point: point[0])[0]
        self.x2 = max(points, key=lambda point: point[0])[0]
        self.y1 = min(points, key=lambda point: point[1])[1]
        self.y2 = max(points, key=lambda point: point[1])[1]


def read_annotation(annt_pth: Path) -> List[MSRA_TD500_annotation]:
    with open(annt_pth, 'r') as f:
        lines = f.readlines()
    annots = []
    for annot_str in lines:
        idx, difficult, x, y, w, h, angl = annot_str.split()
        annot = MSRA_TD500_annotation(difficult, x, y, w, h, angl)
        annots.append(annot)
    return annots


def main():
    train_dir = DSET_FOLDER / 'train'
    test_dir = DSET_FOLDER / 'test'

    for set_dir in (train_dir, test_dir):
        annots_files = list(set_dir.glob('*.gt'))
        img_pths = list(set_dir.glob('*.JPG'))
        annots_files.sort()
        img_pths.sort()

        for i, (annt_file, img_pth) in enumerate(zip(annots_files, img_pths)):
            img = read_image(img_pth)
            annots = read_annotation(annt_file)
            
            for annot in annots:
                img = draw_bounding_boxes_cv2(
                    img, [[annot.x1, annot.y1, annot.x2, annot.y2]])

            # plt.imshow(img)
            # plt.show()




if __name__ == '__main__':
    DSET_FOLDER = Path(
        '/home/pc0/projects/text_detection/data/images/MSRA_TD500')
    main()
