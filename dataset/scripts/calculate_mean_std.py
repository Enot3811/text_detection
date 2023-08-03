"""Script to calculate dataset channel wise std and mean values."""

from pathlib import Path
import sys

import torch
from torchvision.transforms.functional import to_tensor
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[2]))
from dataset.object_detection_dataset import TextDetectionCocoDataset


def main():
    anns_pth = DSET_DIR / 'parsed_cocotext.json'
    img_dir = DSET_DIR / 'images'
    name2index = {'pad': -1, 'legible': 0, 'illegible': 1}

    total_mean = torch.zeros(3, dtype=torch.float32)
    total_std = torch.zeros(3, dtype=torch.float32)
    for dset_type in {'train', 'val', 'test'}:
        dset = TextDetectionCocoDataset(
            annotation_path=anns_pth, img_dir=img_dir, dset_type=dset_type,
            name2index=name2index)
        
        set_mean = torch.zeros(3, dtype=torch.float32)
        set_std = torch.zeros(3, dtype=torch.float32)

        desc = 'Calculate mean and std'
        for sample in tqdm(dset, desc=desc):
            img = sample[0]
            img = to_tensor(img)
            set_mean += img.mean((1, 2))
            set_std += img.std((1, 2))

        set_std /= len(dset)
        set_mean /= len(dset)
        print(f'"{dset_type}": mean = {set_mean.numpy()}, '
              f'std = {set_std.numpy()}')

        total_mean += set_mean
        total_std += set_std
    total_std /= 3
    total_mean /= 3
    print(f'Total: mean = {total_mean.numpy()}, std = {total_std.numpy()}')


if __name__ == '__main__':
    # "train": mean = [0.46201408 0.44023338 0.40830722],
    # std = [0.2513935  0.24573067 0.24901628]
    # Total: mean = [0.46614146 0.44434145 0.41298008],
    # std = [0.25185052 0.24620004 0.24949865]
    DSET_DIR = Path(__file__).parents[2] / 'data'
    main()
