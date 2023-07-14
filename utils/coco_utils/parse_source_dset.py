"""Script that parse coco2014 images and cocotext.v2.json.

1) Get only images that have annotations
2) Split images into train and val sets as noted in json file
3) Copy selected images to new sets directories
(images are renamed as "{img_id}.jpg"
4) Convert bounding boxes from xywh format to xyxy.
"""


from pathlib import Path
import json
import shutil

from torchvision.ops import box_convert
from torch import tensor

from tqdm import tqdm


def main():
    json_path = DSET_PATH / 'cocotext.v2.json'
    img_dir = DSET_PATH / 'images'

    with open(json_path) as f:
        json_dset = f.read()
    dset = json.loads(json_dset)

    imgs_data = dset['imgs']
    anns_data = dset['anns']
    img_to_anns = dset['imgToAnns']

    # Discard images that has no any annotations
    img_to_anns = dict(filter(lambda item: len(img_to_anns[item[0]]) != 0,
                              img_to_anns.items()))
    imgs_data = dict(filter(lambda item: item[0] in img_to_anns,
                            imgs_data.items()))

    # Split images into train and val
    train_imgs = {img_id: imgs_data[img_id]
                  for img_id in imgs_data
                  if imgs_data[img_id]['set'] == 'train'}
    val_imgs = {img_id: imgs_data[img_id]
                for img_id in imgs_data
                if imgs_data[img_id]['set'] == 'val'}

    # Copy selected images to another directory
    train_dest_dir = img_dir / 'train'
    val_dest_dir = img_dir / 'val'
    train_dest_dir.mkdir(exist_ok=True)
    val_dest_dir.mkdir(exist_ok=True)

    desc = 'Copy selected train images'
    for img_id, img_info in tqdm(train_imgs.items(), desc=desc):
        src_name = img_info['file_name']
        src_dir = src_name[5:-17]
        src_pth = img_dir / src_dir / src_name
        dst_name = f'{img_id}.jpg'
        dst_pth = train_dest_dir / dst_name
        train_imgs[img_id]['file_name'] = dst_name
        shutil.copyfile(src_pth, dst_pth)

    desc = 'Copy selected val images'
    for img_id, img_info in tqdm(val_imgs.items(), desc=desc):
        src_name = img_info['file_name']
        src_dir = src_name[5:-17]
        src_pth = img_dir / src_dir / src_name
        dst_name = f'{img_id}.jpg'
        dst_pth = val_dest_dir / dst_name
        val_imgs[img_id]['file_name'] = dst_name
        shutil.copyfile(src_pth, dst_pth)

    # Parse annotations bboxes
    desc = 'Parse annotations'
    for ann_id in tqdm(anns_data, desc=desc):
        bbox = tensor(anns_data[ann_id]['bbox'])
        bbox[bbox < 0.0] = 0.0
        bbox = box_convert(bbox, 'xywh', 'xyxy')
        anns_data[ann_id]['bbox'] = bbox.tolist()

    # Save parsed json data
    json_dict = {
        'imgs': imgs_data,
        'imgToAnns': img_to_anns,
        'anns': anns_data
    }

    json_str = json.dumps(json_dict, indent=4)
    with open(DSET_PATH / 'parsed_cocotext.json', 'w') as f:
        f.write(json_str)


if __name__ == '__main__':
    DSET_PATH = Path(__file__).parents[2] / 'data'
    main()
