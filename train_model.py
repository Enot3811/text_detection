"""Training script."""

from pathlib import Path
import sys

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
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
    lr = 0.0001
    b_size = 8
    n_workers = 8
    weight_decay = 1e-3
    device = 'cuda'
    continue_training = True
    end_ep = 20

    # Prepare some stuff
    device = torch.device(device=device)
    work_dir = Path('work_dir') / 'train_1'
    work_dir.mkdir(parents=True, exist_ok=True)
    if continue_training:
        checkpoint = torch.load(work_dir / 'last_checkpoint.pt')
        model_params = checkpoint['model']
        optim_params = checkpoint['optimizer']
        start_ep = checkpoint['epoch']
    else:
        model_params = None
        optim_params = None
        start_ep = 0

    # Get tensorboard
    log_writer = SummaryWriter(str(work_dir / 'tensorboard'), )

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
    if model_params:
        model.load_state_dict(model_params)
    
    # Get an optimizer
    optimizer = optim.Adam(
        model.parameters(), lr=lr, weight_decay=weight_decay)
    if optim_params:
        optimizer.load_state_dict(optim_params)
    
    # Do training
    model.train()
    train_log = []
    val_log = []
    best_loss = None
    for ep in range(start_ep, end_ep):

        # Train pass
        ep_losses = []
        desc = f'Train epoch {ep}'
        for batch in tqdm(train_loader, desc=desc):
            images, gt_boxes, gt_classes = batch
            images = images.to(device=device)
            gt_boxes = gt_boxes.to(device=device)
            gt_classes = gt_classes.to(device=device)

            proposals, classes, loss = model(images, gt_boxes, gt_classes)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            ep_losses.append(loss.item())
        train_log.append(torch.mean(torch.tensor(ep_losses)))

        # Validation pass
        ep_losses.clear()
        desc = f'Val epoch {ep}'
        with torch.no_grad():
            for batch in tqdm(val_loader, desc=desc):
                images, gt_boxes, gt_classes = batch
                images = images.to(device=device)
                gt_boxes = gt_boxes.to(device=device)
                gt_classes = gt_classes.to(device=device)

                proposals, classes, loss = model(images, gt_boxes, gt_classes)

                ep_losses.append(loss.item())
            val_log.append(torch.mean(torch.tensor(ep_losses)))

        # Logging
        print(f'Epoch: {ep} '
              f'train_loss: {train_log[-1]} '
              f'val_loss: {val_log[-1]}')

        log_writer.add_scalar('Train_loss', train_log[-1], ep)
        log_writer.add_scalar('Validation_loss', val_log[-1], ep)

        # Saving
        if best_loss is None or best_loss > val_log[-1]:
            best_loss = val_log[-1]
            torch.save(
                model.state_dict(),
                work_dir / 'best_model.pt')

        torch.save(
            {
                'model': model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'epoch': ep
            },
            work_dir / 'last_checkpoint.pt')

    log_writer.close()


if __name__ == '__main__':
    DSET_DIR = Path(__file__).parent / 'data'
    main()
