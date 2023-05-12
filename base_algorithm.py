import json
import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (Any, Callable, Dict, Iterable, List, Optional, Pattern,
                    Set, Tuple, Union)

import numpy as np
import SimpleITK
from evalutils.exceptions import FileLoaderError
from evalutils.io import FileLoader, ImageLoader, SimpleITKLoader
from evalutils.validators import (UniqueImagesValidator,
                                  UniquePathIndicesValidator)
from pandas import DataFrame

logger = logging.getLogger(__name__)

# Check if .env file exists and load it
if Path(".env").exists():
    from dotenv import dotenv_values

    config = dotenv_values(".env")

    TASK_TYPE = config["TASK_TYPE"]
    INPUT_FOLDER = config["INPUT_FOLDER"]

    print("########## ENVIRONMENT VARIABLES ##########")
    print(f"TASK_TYPE: {TASK_TYPE}")
    print(f"INPUT_FOLDER: {INPUT_FOLDER}")
else:
    TASK_TYPE = "mri"
    INPUT_FOLDER = "/input"

if INPUT_FOLDER == "/input":
    OUTPUT_FOLDER = "/output"
else:
    OUTPUT_FOLDER = "./output"

DEFAULT_IMAGE_PATH = Path(f"{INPUT_FOLDER}/images/{TASK_TYPE}")
DEFAULT_MASK_PATH = Path(f"{INPUT_FOLDER}/images/body")
DEFAULT_OUTPUT_PATH = Path(f"{OUTPUT_FOLDER}/images/synthetic-ct")
DEFAULT_OUTPUT_FILE = Path(f"{OUTPUT_FOLDER}/results.json")


class BaseSynthradAlgorithm(ABC):
    def __init__(
        self,
        input_path: Path = DEFAULT_IMAGE_PATH,
        mask_path: Path = DEFAULT_MASK_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
        output_file: Path = DEFAULT_OUTPUT_FILE,
        validators: Optional[Dict[str, callable]] = None,
        file_loader: FileLoader = SimpleITKLoader(),
    ):
        """
         Parameters
         ----------

         input_path
             The path in the container where the input images will be loaded from.
             from. Default: `/input/images/mri/`
         mask_path
             The path in the container where the input masks will be loaded from.
             Default: `/input/images/body/`
         output_path
             The path in the container where the output images will be written.
             Default: `/output/images/synthetic-ct/`

         output_file
             The path to the location where the results will be written.
             Default: `/output/results.json`
         file_loader
             The loaders that will be used to get all files.
             Default: `evalutils.io.SimpleITKLoader` for `image` and `mask`
        validators
             A dictionary containing the validators that will be used on the
             loaded data per file_loader key. Default:
             `evalutils.validators.UniqueImagesValidator` for `input_image`
        """

        self._index_keys = ["image", "mask"]
        self.input_path = input_path
        self.mask_path = mask_path
        self.output_path = output_path
        self.output_file = output_file
        self._file_loader = file_loader

        # TODO: Add validators
        # self.validators = [
        #     UniquePathIndicesValidator(),
        #     UniqueImagesValidator(),
        # ]

        self.cases = {}
        self._case_results = []

    def load(self):
        self.images = self._load_cases(
            folder=self.input_path, file_loader=self._file_loader
        )

        self.masks = self._load_cases(
            folder=self.mask_path, file_loader=self._file_loader
        )

    def _load_cases(
        self,
        folder: Path,
        file_loader: ImageLoader,
    ) -> DataFrame:
        cases = []

        for fp in sorted(folder.glob("*")):
            try:
                new_cases = file_loader.load(fname=fp)
            except FileLoaderError:
                logger.warning(f"Could not load {fp.name} using {file_loader}.")
            else:
                cases.extend(new_cases)

        if len(cases) == 0:
            raise FileLoaderError(
                f"Could not load any files in {folder} with " f"{file_loader}."
            )

        return cases

    def validate(self):
        """TODO: Validates each dataframe for each fileloader separately"""
        pass

    def _validate_data_frame(self, df: DataFrame):
        "TODO: Validate the dataframe for a specific fileloader"
        pass

    def process_cases(self):
        self._case_results = []

        for idx, case in enumerate(zip(self.images, self.masks)):
            self._case_results.append(self.process_case(idx=idx, case=case))

    def process_case(self, idx: int, case: List[DataFrame]) -> Dict:
        images, images_file_paths = {}, {}

        images["image"], images_file_paths["image"] = self._load_input_image(case[0])
        images["mask"], images_file_paths["mask"] = self._load_input_image(case[1])

        # Predict and generate output
        out = self.predict(input_dict=images)

        # Write resulting segmentation to output location
        out_path = self.output_path / images_file_paths["image"].name
        if not self.output_path.exists():
            self.output_path.mkdir(parents=True, exist_ok=True)

        SimpleITK.WriteImage(out, str(out_path), True)

        # Write segmentation file path to result.json for this case
        return {
            "outputs": [dict(type="metaio_image", filename=str(out_path))],
            "inputs": [
                dict(type="metaio_image", filename=str(fn))
                for fn in images_file_paths.values()
            ],
            "error_messages": [],
        }

    def _load_input_image(self, image) -> Tuple[SimpleITK.Image, Path]:
        input_image_file_path = image["path"]
        input_image_file_loader = self._file_loader

        if not isinstance(input_image_file_loader, ImageLoader):
            raise RuntimeError("The used FileLoader was not of subclass ImageLoader")

        # Load the image
        input_image = input_image_file_loader.load_image(input_image_file_path)

        # Check that it is the expected image
        if input_image_file_loader.hash_image(input_image) != image["hash"]:
            raise RuntimeError("Image hashes do not match")
        return input_image, input_image_file_path

    @abstractmethod
    def predict(self, *, input_dict: Dict[str, SimpleITK.Image]) -> SimpleITK.Image:
        pass

    def save(self):
        with open(str(self.output_file), "w") as f:
            json.dump(self._case_results, f)

    def process(self):
        self.load()
        self.validate()
        self.process_cases()
        self.save()
