"""Training script."""

from pathlib import Path
import sys

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm

sys.path.append(str(Path(__file__).parents[2]))
from dataset.object_detection_dataset import TextDetectionCocoDataset
from rcnn.rcnn_model import RCNN_Detector
from rcnn.rcnn_utils import draw_bounding_boxes_cv2
from utils.torch_utils.torch_metrics import (
    calculate_iou, calculate_prediction_count_diff)
from utils.torch_utils.torch_functions import image_tensor_to_numpy


def main():
    # Get dataset parameters
    anns_pth = DSET_DIR / 'parsed_cocotext.json'
    img_dir = DSET_DIR / 'images'
    name2index = {'pad': -1, 'legible': 0, 'illegible': 1}
    index2name = {-1: 'pad', 0: 'legible', 1: 'illegible'}
    n_cls = len(name2index) - 1
    crop_size = 448
    bbox_min_visibility = 0.1
    bbox_min_area = 30

    # Get model parameters
    input_size = (448, 448)
    roi_size = (2, 2)
    backbone_model = 'resnet50'
    conf_thresh = 0.8
    iou_thresh = 0.1

    # Get training parameters
    lr = 0.0001
    b_size = 8
    weight_decay = 1e-3
    device = 'cuda'
    continue_training = True
    end_ep = 56

    # Prepare some stuff
    device = torch.device(device=device)
    work_dir = Path('work_dir') / 'train_1'
    work_dir.mkdir(parents=True, exist_ok=True)
    if continue_training:
        checkpoint = torch.load(work_dir / 'last_checkpoint.pt')
        model_params = checkpoint['model']
        optim_params = checkpoint['optimizer']
        start_ep = checkpoint['epoch'] + 1
    else:
        model_params = None
        optim_params = None
        start_ep = 0

    # Get tensorboard
    log_writer = SummaryWriter(str(work_dir / 'tensorboard'), )

    # Get transforms
    mean = torch.tensor([0.46201408, 0.44023338, 0.40830722])
    std = torch.tensor([0.2513935, 0.24573067, 0.24901628])
    transform = A.Compose(
        [
            A.HorizontalFlip(),
            A.VerticalFlip(),
            A.RandomResizedCrop(crop_size, crop_size),
            A.RandomBrightnessContrast(),
            A.Normalize(mean=mean, std=std),
            ToTensorV2()
        ],
        bbox_params=A.BboxParams(
            format='pascal_voc', min_area=bbox_min_area,
            min_visibility=bbox_min_visibility, label_fields=['classes'])
    )

    # Get dataset and loader
    train_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type='train',
        name2index=name2index, transforms=transform)
    val_dset = TextDetectionCocoDataset(
        annotation_path=anns_pth, img_dir=img_dir, dset_type='val',
        name2index=name2index, transforms=transform)
    
    train_loader = DataLoader(
        train_dset, batch_size=b_size, shuffle=True)
    val_loader = DataLoader(
        val_dset, batch_size=b_size)

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
    best_loss = None
    for ep in range(start_ep, end_ep):
        train_losses = []
        val_losses = []
        iou_values = []
        n_pred_diff_values = []

        # Train pass
        model.train()
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

            train_losses.append(loss.item())

        # Validation pass
        desc = f'Val epoch {ep}'
        model.eval()
        with torch.no_grad():
            save_examples = True  # Save one batch of examples on validation
            for batch in tqdm(val_loader, desc=desc):
                images, gt_boxes, gt_classes = batch
                images = images.to(device=device)
                gt_boxes = gt_boxes.to(device=device)
                gt_classes = gt_classes.to(device=device)

                # Do forward pass to get loss
                proposals, classes, loss = model(images, gt_boxes, gt_classes)

                # Do inference pass to get some output examples
                bboxes, classes = model.inference(
                    images, conf_thresh, iou_thresh)

                # Calculate and save metrics
                val_losses.append(loss.item())
                iou_values.append(calculate_iou(gt_boxes, bboxes))
                n_pred_diff_values.append(
                    calculate_prediction_count_diff(gt_boxes, bboxes))
                
                # Save one batch of predictions
                if save_examples:
                    for i in range(b_size):
                        save_image = (
                            images[i] * std.view((3, 1, 1)).to(device=device) +
                            mean.view((3, 1, 1)).to(device=device))
                        save_image = image_tensor_to_numpy(save_image)
                        save_image = draw_bounding_boxes_cv2(
                            save_image, gt_boxes[i],
                            gt_classes[i].to(dtype=torch.int16),
                            index2name, color=(0, 255, 0))
                        labels = torch.argmax(classes[i], dim=1)
                        save_image = draw_bounding_boxes_cv2(
                            save_image, bboxes[i], labels,
                            index2name, color=(255, 255, 0))
                        
                        log_writer.add_image(
                            f'example_{i}', save_image,
                            ep, dataformats='HWC')
                    save_examples = False

        # Logging
        train_losses = sum(train_losses) / len(train_losses)
        val_losses = sum(val_losses) / len(val_losses)
        iou_values = sum(iou_values) / len(iou_values)
        n_pred_diff_values = sum(n_pred_diff_values) / len(n_pred_diff_values)
        print(f'Epoch: {ep} '
              f'train_loss: {train_losses} '
              f'val_loss: {val_losses} '
              f'IoU_metric: {iou_values.item()} '
              f'Predict_cnt_metric: {n_pred_diff_values.item()}')

        log_writer.add_scalar('Train_loss', train_losses, ep)
        log_writer.add_scalar('Validation_loss', val_losses, ep)
        log_writer.add_scalar('IoU_metric', iou_values, ep)
        log_writer.add_scalar('Predictions_count_diff', n_pred_diff_values, ep)

        # Saving
        if best_loss is None or best_loss > val_losses[-1]:
            best_loss = val_losses[-1]
            torch.save(
                model.state_dict(),
                work_dir / 'best_model.pt')

        torch.save(
            {
                'model': model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'epoch': ep + 1
            },
            work_dir / 'last_checkpoint.pt')

    log_writer.close()


if __name__ == '__main__':
    DSET_DIR = Path(__file__).parent / 'data'
    main()
