from pathlib import Path

import SimpleITK as sitk

# rtss files may not be neccessary for the algorithm submission as participants don't have access to them
# for the training phase. The mask however, should be accessible to the algorithm as participants may use them
# as a part of their algorithm
folder_structure = {
    "folders": ["1BAxxx", "1PAxxx", "2BAxxx", "2PAxxx"],
    "extension": ".nii.gz",
}


def main(args):
    args.target_dir.mkdir(parents=True, exist_ok=True)

    folders = folder_structure["folders"]
    ext = folder_structure["extension"]

    for folder_stem in folders:
        folder = args.target_dir / folder_stem
        folder.mkdir(parents=True, exist_ok=True)

        # Write dummy image

        if folder_stem.startswith("1"):
            identifier = "mr"
        elif folder_stem.startswith("2"):
            identifier = "cbct"
        else:
            raise ValueError(f"Unknown folder stem {folder_stem}")

        sitk.WriteImage(
            sitk.Image(100, 100, 100, sitk.sitkInt16),
            folder / f"{identifier}{ext}",
        )

        # Write dummy mask
        sitk.WriteImage(
            sitk.Image(100, 100, 100, sitk.sitkUInt8),
            folder / f"mask{ext}",
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
