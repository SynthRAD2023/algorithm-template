from pathlib import Path

import SimpleITK as sitk

# rtss files may not be neccessary for the algorithm submission as participants don't have access to them
# for the training phase. The mask however, should be accessible to the algorithm as participants may use them
# as a part of their algorithm
folder_structure = {
    "identifier": "1BAxxx",
    "folders": ["images", "masks"],
    "extension": ".nii.gz",
}


def main(args):
    args.target_dir.mkdir(parents=True, exist_ok=True)
    identifier = folder_structure["identifier"]
    ext = folder_structure["extension"]
    for folder_name in folder_structure["folders"]:
        if folder_name == "masks":
            out_type = sitk.sitkUInt8
        else:
            out_type = sitk.sitkInt16

        folder = args.target_dir / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        sitk.WriteImage(
            sitk.Image(100, 100, 100, out_type),
            folder / f"{identifier}{ext}",
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create dummy data for SynthRAD")
    parser.add_argument(
        "target_dir",
        type=Path,
        help="Target directory to create dummy folder structure",
    )
    args = parser.parse_args()
    main(args)
