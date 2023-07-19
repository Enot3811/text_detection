"""Script to check some samples from dataset."""

from pathlib import Path
import sys

import torch
from torch.utils.data import DataLoader  # noqa
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).parents[2]))
from rcnn.rcnn_utils import draw_bounding_boxes
from dataset.object_detection_dataset import TextDetectionCocoDataset
from utils.image_utils import display_image
from utils.numpy_utils import tensor_to_numpy


def main():
    anns_pth = DSET_DIR / 'parsed_cocotext.json'
    img_dir = DSET_DIR / 'images'
    name2index = {'pad': -1, 'legible': 0, 'illegible': 1}
    index2name = {-1: 'pad', 0: 'legible', 1: 'illegible'}  # noqa
    b_size = 2  # noqa

    mean = torch.tensor([0.46201408, 0.44023338, 0.40830722])
    std = torch.tensor([0.2513935, 0.24573067, 0.24901628])
    transform = A.Compose(
        [
            A.HorizontalFlip(),
            A.VerticalFlip(),
            A.RandomResizedCrop(448, 448),
            A.RandomBrightnessContrast(),
            A.Normalize(mean=mean, std=std),
            ToTensorV2()
        ],
        bbox_params=A.BboxParams(
            format='pascal_voc', min_area=30,
            min_visibility=0.1, label_fields=['classes'])
    )

    orig_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type=DATASET,
        name2index=name2index, transforms=None)
    transf_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type=DATASET,
        name2index=name2index, transforms=transform)
    # loader = DataLoader(dset, batch_size=b_size)

    for i in range(len(orig_dset)):
        # Show original
        img, bboxes, classes = orig_dset[i]
        print(img.shape, img.min(), img.max())
        _, axes = plt.subplots(1, 2, figsize=(16, 16))
        ax = display_image(img, axes[0])
        # draw_bounding_boxes(ax, bboxes, classes, index2name)
        draw_bounding_boxes(ax, bboxes)

        # Get transformed
        img, bboxes, classes = transf_dset[i]
        print(img.shape, img.min().item(), img.max().item())

        # Translate float tensor to uint array
        img = tensor_to_numpy(
            ((img * std[:, None, None] + mean[:, None, None]) * 255)
            .to(dtype=torch.uint8))
        print(img.shape, img.min(), img.max())
        
        # Show after transf
        ax = display_image(img, axes[1])
        # draw_bounding_boxes(ax, bboxes, classes, index2name)
        draw_bounding_boxes(ax, bboxes)
        plt.show()


if __name__ == '__main__':
    DSET_DIR = Path(__file__).parents[2] / 'data'
    DATASET = 'train'
    main()
