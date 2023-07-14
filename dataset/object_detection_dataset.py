"""A module that contains TextDetectionCocoDataset class."""


from pathlib import Path
from typing import Dict, List, Union, Callable, Any
import json

import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence

from utils.image_utils import read_image


class TextDetectionCocoDataset(Dataset):
    """Coco text detection dataset class.

    Without transforms each sample is a tuple that contains
    image uint8 ndarray with shape `(H, W, C)`,
    ground truth bounding boxes FloatTensor with shape `(n_max_obj, 4)`,
    corresponding ground truth classes FloatTensor with shape `(n_max_obj,)`.
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

            dset_bboxes.append(torch.tensor(sample_bboxes))
            dset_classes.append(torch.tensor(sample_classes))

        # Pad bboxes and classes to n_max_obj
        self.bboxes = pad_sequence(
            dset_bboxes, batch_first=True, padding_value=-1)
        self.classes = pad_sequence(
            dset_classes, batch_first=True, padding_value=-1)

        self.transforms = transforms

    def __len__(self):
        return len(self.img_pths)

    def __getitem__(
        self, idx: int
    ) -> Any:
        """
        Return the sample by index.

        Parameters
        ----------
        idx : int
            Index of the sample.

        Returns
        -------
        Any
            By default sample is a tuple that contains
            image ndarray with shape `(h, w, c)`,
            bounding boxes tensor with shape `(n_max_obj, 4)`
            and classes tensor with shape `(n_max_obj,)`.
        """
        image = read_image(self.img_pths[idx])
        bboxes = self.bboxes[idx]
        classes = self.classes[idx]
        if self.transforms:
            image, bboxes, classes = self.transforms((image, bboxes, classes))
        return (image, bboxes, classes)
