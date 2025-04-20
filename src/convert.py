import os
import shutil
import yaml

def convert_cvat_to_yolov12(input_dir, output_dir):
    """
    Convert a CVAT-formatted dataset to YOLOv11/12 style using os.path

    - input_dir: str path to the CVAT dataset (with nested split folders under images/ and labels/)
    - output_dir: str path to write the new dataset (will contain 'train', 'val', 'test' subfolders with 'images' and 'labels')
    """
    # Map CVAT splits to YOLO splits
    split_map = {
        'Test': 'test',
        'Train': 'train',
        'Validation': 'val',
    }

    # Clean output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Process each split
    for src_split, dst_split in split_map.items():
        # Source directories (may contain nested subfolders)
        src_images_root = os.path.join(input_dir, 'images', src_split)
        src_labels_root = os.path.join(input_dir, 'labels', src_split)

        # Destination directories
        dst_images = os.path.join(output_dir, dst_split, 'images')
        dst_labels = os.path.join(output_dir, dst_split, 'labels')
        os.makedirs(dst_images, exist_ok=True)
        os.makedirs(dst_labels, exist_ok=True)

        # Recursively copy all image files
        if os.path.exists(src_images_root):
            for root, _, files in os.walk(src_images_root):
                for fname in files:
                    src_file = os.path.join(root, fname)
                    dst_file = os.path.join(dst_images, fname)
                    shutil.copy(src_file, dst_file)

        # Recursively copy all label files
        if os.path.exists(src_labels_root):
            for root, _, files in os.walk(src_labels_root):
                for fname in files:
                    src_file = os.path.join(root, fname)
                    dst_file = os.path.join(dst_labels, fname)
                    shutil.copy(src_file, dst_file)

    # Remove old split text files if they exist
    for txt in ['Test.txt', 'Train.txt', 'Validation.txt']:
        fpath = os.path.join(input_dir, txt)
        if os.path.exists(fpath):
            os.remove(fpath)

    # Read original YAML to preserve class names and nc
    orig_yaml = os.path.join(input_dir, 'data.yaml')
    if os.path.exists(orig_yaml):
        with open(orig_yaml, 'r') as f:
            orig_cfg = yaml.safe_load(f)
        names = orig_cfg.get('names', {})
    else:
        # Fallback if missing
        names = {0: 'pole'}

    nc = len(names)

    # Write new YAML config
    config = {
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'nc': nc,
        'names': names,
        'path': '.'
    }
    out_yaml = os.path.join(output_dir, 'data.yaml')
    with open(out_yaml, 'w') as f:
        yaml.dump(config, f, sort_keys=False)


def main():
    # Determine project root two levels up from this file
    this_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(this_file))
    input_dir = os.path.join(project_root, 'data', 'Roadpoles-iPhone-v2')
    output_dir = os.path.join(project_root, 'results', 'datasets')

    convert_cvat_to_yolov12(input_dir, output_dir)
    print(f"Converted dataset saved to {output_dir}")


if __name__ == '__main__':
    main()
