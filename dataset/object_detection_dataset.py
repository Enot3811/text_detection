"""A module that contains TextDetectionCocoDataset class."""


from pathlib import Path
from typing import Dict, List, Union, Callable, Any
import json

import torch
from torch.utils.data import Dataset

from utils.image_utils import read_image


class TextDetectionCocoDataset(Dataset):
    """Coco text detection dataset class.

    Without transforms each sample is a tuple that contains
    image uint8 ndarray with shape `(H, W, C)`,
    ground truth bounding boxes list with shape `(n_obj, 4)`,
    corresponding ground truth classes list with shape `(n_obj,)`.
    """
    def __init__(
        self,
        annotation_path: Union[str, Path],
        img_dir: Union[str, Path],
        dset_type: str,
        name2index: Dict[str, int],
        transforms: Callable = None
    ):
        if dset_type not in {'train', 'val', 'test'}:
            raise ValueError(
                'Wrong set type received.'
                'dset_type must be on of ("train", "val", "test")')

        with open(annotation_path) as f:
            json_dset = f.read()
        dset_anns = json.loads(json_dset)

        # Get images annotations for defined set
        imgs_info = dict(filter(
            lambda img_item: img_item[1]['set'] == dset_type,
            dset_anns['imgs'].items()))
        imgs_to_anns = dset_anns['imgToAnns']
        anns = dset_anns['anns']

        # Collect paths, bboxes and corresponding classes
        dset_bboxes = []
        dset_classes = []
        self.img_pths = []
        for img_id, img_info in imgs_info.items():

            self.img_pths.append(
                Path(img_dir) / dset_type / img_info['file_name'])
            
            anns_ids = list(map(str, imgs_to_anns[img_id]))
            
            sample_bboxes: List[List[float]] = []
            sample_classes: List[int] = []
            for ann_id in anns_ids:
                sample_bboxes.append(anns[ann_id]['bbox'])
                sample_classes.append(name2index[anns[ann_id]['legibility']])

            dset_bboxes.append(sample_bboxes)
            dset_classes.append(sample_classes)
        self.bboxes = dset_bboxes
        self.classes = dset_classes

        self.transforms = transforms

        # Calculate n_max_obj for padding
        self.n_max_obj = 0
        for img_anns_ids in imgs_to_anns.values():
            if self.n_max_obj < len(img_anns_ids):
                self.n_max_obj = len(img_anns_ids)

    def __len__(self):
        return len(self.img_pths)

    def __getitem__(
        self, idx: int
    ) -> Any:
        """Return sample by index.

        Parameters
        ----------
        idx : int
            Index of the sample.

        Returns
        -------
        Any
            By default sample is a tuple that contains
            image ndarray with shape `(h, w, c)`,
            bounding boxes list with shape `(n_obj, 4)`
            and classes list with shape `(n_obj,)`.
        """
        image = read_image(self.img_pths[idx])  # ndarray
        bboxes = self.bboxes[idx]  # list[list[float]]
        classes = self.classes[idx]  # list[float]

        if self.transforms:
            transformed = self.transforms(
                image=image, bboxes=bboxes, classes=classes)
            image = transformed['image']  # tensor
            bboxes = transformed['bboxes']  # list[list[float]]
            classes = transformed['classes']  # list[float]

            # Pad values bboxes and classes after transforms
            n_pad = self.n_max_obj - len(bboxes)
            bboxes = torch.vstack(  # tensor
                (torch.tensor(bboxes, dtype=torch.float32).view(size=(-1, 4)),
                 torch.ones(n_pad, 4, dtype=torch.float32) * -1.0))
            classes = torch.hstack(  # tensor
                (torch.tensor(classes, dtype=torch.float32),
                 torch.ones(n_pad, dtype=torch.float32) * -1.0))
        return (image, bboxes, classes)
