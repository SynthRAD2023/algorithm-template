from pathlib import Path

import SimpleITK as sitk

# rtss files may not be neccessary for the algorithm submission as participants don't have access to them
# for the training phase. The mask however, should be accessible to the algorithm as participants may use them
# as a part of their algorithm
folder_structure = {
    "identifier": "1BAxxx",
    "files": [
        "ct.nii.gz",
        "mask.nii.gz",
        #  {"rtss": ["Body.nrrd", "Brain.nrrd"]}
    ],
}


def main(args):
    args.target_dir.mkdir(parents=True, exist_ok=True)
    identifier = folder_structure["identifier"]
    for file in folder_structure["files"]:
        if isinstance(file, dict):
            for key, value in file.items():
                folder = args.target_dir / key
                folder.mkdir(parents=True, exist_ok=True)
                for file in value:
                    sitk.WriteImage(
                        sitk.Image(100, 100, 100, sitk.sitkUInt8),
                        folder / f"{identifier}_{file}",
                    )
        else:
            if "mask" in file:
                folder = args.target_dir / "mask"
                folder.mkdir(parents=True, exist_ok=True)
                sitk.WriteImage(
                    sitk.Image(100, 100, 100, sitk.sitkUInt8),
                    folder / f"{identifier}_{file}",
                )
            else:
                folder = args.target_dir / "images"
                folder.mkdir(parents=True, exist_ok=True)
                sitk.WriteImage(
                    sitk.Image(100, 100, 100, sitk.sitkInt16),
                    folder / f"{identifier}_{file}",
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
