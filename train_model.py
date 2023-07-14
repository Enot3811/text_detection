"""Training script."""

from pathlib import Path
import sys

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[2]))
from dataset.object_detection_dataset import TextDetectionCocoDataset
from dataset.transforms import Resize, ToTensor, Normalize
from rcnn.rcnn_model import RCNN_Detector


def main():
    # Get dataset parameters
    anns_pth = DSET_DIR / 'parsed_cocotext.json'
    img_dir = DSET_DIR / 'images'
    name2index = {'pad': -1, 'legible': 0, 'illegible': 1}
    n_cls = len(name2index) - 1

    # Get model parameters
    input_size = (448, 448)
    roi_size = (2, 2)
    backbone_model = 'resnet50'

    # Get training parameters
    lr = 0.001
    epochs = 35
    b_size = 8
    n_workers = 8
    device = 'cuda'
    device = torch.device(device=device)

    # Get transforms
    mean = torch.tensor([0.46201408, 0.44023338, 0.40830722])
    std = torch.tensor([0.2513935, 0.24573067, 0.24901628])
    transf = transforms.Compose([
        ToTensor(),
        Resize(input_size),
        Normalize(mean=mean, std=std)
    ])

    # Get dataset and loader
    train_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type='train',
        name2index=name2index, transforms=transf)
    val_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type='val',
        name2index=name2index, transforms=transf)
    
    train_loader = DataLoader(
        train_dset, batch_size=b_size, num_workers=n_workers, shuffle=True)
    val_loader = DataLoader(
        val_dset, batch_size=b_size, num_workers=n_workers)

    # Get the model
    model = RCNN_Detector(input_size=input_size,
                          n_cls=n_cls,
                          roi_size=roi_size,
                          backbone_model=backbone_model)
    model.to(device=device)
    
    # Get an optimizer
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Do training
    model.train()
    loss_log = []
    best_loss = None
    for ep in range(epochs):

        # Train
        ep_losses = []
        desc = f'Epoch {ep}'
        for batch in tqdm(val_loader, desc=desc):
            images, gt_boxes, gt_classes = batch
            images = images.to(device=device)
            gt_boxes = gt_boxes.to(device=device)
            gt_classes = gt_classes.to(device=device)

            proposals, classes, loss = model(images, gt_boxes, gt_classes)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            ep_losses.append(loss.item())
        loss_log.append(torch.mean(torch.tensor(ep_losses)))
        print(f'Epoch: {ep} loss: {loss_log[-1]}')

        if best_loss is None or best_loss > loss_log[-1]:
            best_loss = loss_log[-1]
            torch.save(model.state_dict(), 'best_model.pt')

        with open('train_log.txt', 'a') as f:
            f.write(f'Epoch: {ep} loss: {loss_log[-1]}\n')

        # Validation
        # TODO сделать валидацию


if __name__ == '__main__':
    DSET_DIR = Path(__file__).parent / 'data'
    main()
