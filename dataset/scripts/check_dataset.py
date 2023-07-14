"""Script to check some samples from dataset."""

from pathlib import Path
import sys

import torchvision.transforms as transforms
import torch
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).parents[2]))
from rcnn.rcnn_utils import draw_bounding_boxes
from dataset.object_detection_dataset import TextDetectionCocoDataset
from utils.image_utils import display_image
from dataset.transforms import Resize, ToTensor, Normalize, to_numpy


def main():
    anns_pth = DSET_DIR / 'parsed_cocotext.json'
    img_dir = DSET_DIR / 'images'
    name2index = {'pad': -1, 'legible': 0, 'illegible': 1}
    index2name = {-1: 'pad', 0: 'legible', 1: 'illegible'}  # noqa

    mean = torch.tensor([0.46614146, 0.44434145, 0.41298008])
    std = torch.tensor([0.25185052, 0.24620004, 0.24949865])
    transf = transforms.Compose([
        ToTensor(),
        Resize(448),
        Normalize(mean=mean, std=std)
    ])

    dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type=DATASET,
        name2index=name2index, transforms=None)

    # Show original
    img, bboxes, classes = dset[SAMPLE_IDX]
    print(img.shape, img.min(), img.max())
    _, axes = plt.subplots(1, 2)
    ax = display_image(img, axes[0])
    # draw_bounding_boxes(ax, bboxes, classes, index2name)
    draw_bounding_boxes(ax, bboxes)

    # Do transform
    img, bboxes, classes = transf((img, bboxes, classes))
    print(img.shape, img.min(), img.max())

    # Translate float tensor to uint array
    img = to_numpy(((img * std[:, None, None] + mean[:, None, None]) * 255)
                   .to(dtype=torch.uint8))
    print(img.shape, img.min(), img.max())
    
    # Show after transf
    ax = display_image(img, axes[1])
    classes = classes.to(dtype=torch.int16)
    # draw_bounding_boxes(ax, bboxes, classes, index2name)
    draw_bounding_boxes(ax, bboxes)
    plt.show()


if __name__ == '__main__':
    DSET_DIR = Path(__file__).parents[2] / 'data'
    DATASET = 'test'
    SAMPLE_IDX = 1037
    main()
