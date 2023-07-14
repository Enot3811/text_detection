"""Script tht create test set for coco text dataset.

Test samples are got from val set according to defined percent.
Selected images are moved to test set directory
and their set in json are changed to 'test'.
"""


from pathlib import Path
import json
import shutil

from tqdm import tqdm


def main():
    json_path = DSET_PATH / 'parsed_cocotext.json'
    img_dir = DSET_PATH / 'images'

    with open(json_path) as f:
        json_dset = f.read()
    dset = json.loads(json_dset)

    imgs_data = dset['imgs']

    # Get val images
    val_imgs = [(img_id, img_info)
                for img_id, img_info in imgs_data.items()
                if img_info['set'] == 'val']
    
    # Split val into val and test according to percent
    n_test_img = int(len(val_imgs) * TEST_PERCENT)
    test_imgs = dict(val_imgs[-n_test_img::1])
    val_imgs = dict(val_imgs[:-n_test_img:1])
    
    # Change set in json for test images
    for img_id in test_imgs:
        dset['imgs'][img_id]['set'] = 'test'

    # Move selected images to another directory
    src_dir = img_dir / 'val'
    dst_dir = img_dir / 'test'
    dst_dir.mkdir(exist_ok=True)

    desc = 'Move selected test images'
    for img_info in tqdm(test_imgs.values(), desc=desc):
        img_name = img_info['file_name']
        src_pth = src_dir / img_name
        dst_pth = dst_dir / img_name
        shutil.move(src_pth, dst_pth)

    # Save changed json
    json_str = json.dumps(dset, indent=4)
    with open(DSET_PATH / 'parsed_cocotext.json', 'w') as f:
        f.write(json_str)


if __name__ == '__main__':
    DSET_PATH = Path(__file__).parents[2] / 'data'
    TEST_PERCENT = 0.25
    main()
