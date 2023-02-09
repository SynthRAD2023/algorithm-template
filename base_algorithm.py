import json
import logging
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

execute_in_docker = True

DEFAULT_INPUT_PATH = Path("/input/") if execute_in_docker else Path("./test/")
DEFAULT_OUTPUT_PATH = Path("/output/") if execute_in_docker else Path("./output/")
DEFAULT_OUTPUT_FILE = (
    Path("/output/results.json") if execute_in_docker else Path("./output/results.json")
)


class BaseSynthradAlgorithm(ABC):
    def __init__(
        self,
        file_filters: Optional[Dict[str, Pattern[str]]] = None,
        file_loaders: Optional[Dict[str, FileLoader]] = None,
        input_path: Path = DEFAULT_INPUT_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
        output_file: Path = DEFAULT_OUTPUT_FILE,
        file_sorter_key: Optional[callable] = None,
        validators: Optional[Dict[str, callable]] = None,
    ):
        """
        Parameters
        ----------
        file_loaders
            The loaders that will be used to get all files.
            Default: `evalutils.io.SimpleITKLoader` for `input_image`
        file_filters
            Regular expressions for filtering certain FileLoaders.
            Default: no filtering.
        images_path
            The path in the container where the input images will be loaded from.
            from. Default: `/input/images`
        masks_path
            The path in the container where the input masks will be loaded from.
            Default: `/input/masks`
        output_path
            The path in the container where the output images will be written.
            Default: `/output/images`
        file_sorter_key
            A function that determines how files in the input_path are sorted.
            Default: `None` (alphanumerical)
        validators
            A dictionary containing the validators that will be used on the
            loaded data per file_loader key. Default:
            `evalutils.validators.UniqueImagesValidator` for `input_image`
        output_file
            The path to the location where the results will be written.
            Default: `/output/results.json`
        """

        self._index_keys = ["image", "mask"]
        self.input_path = input_path
        self.output_path = output_path
        self.output_file = output_file
        self._file_sorter_key = file_sorter_key

        self.validators = [
            UniquePathIndicesValidator(),
            UniqueImagesValidator(),
        ]

        self._file_loaders: Dict[str, FileLoader] = (
            dict(image=SimpleITKLoader(), mask=SimpleITKLoader())
            if file_loaders is None
            else file_loaders
        )

        self._file_filters: Dict[str, Optional[Pattern[str]]] = (
            # Patterns without mask are images and with mask are masks
            dict(image=re.compile(r"^((?!mask).)*$"), mask=re.compile(r".*mask.*"))
            if file_filters is None
            else file_filters
        )

        self.cases = {}
        self._case_results = []

    def load(self):
        for key, file_loader in self._file_loaders.items():
            filter = self._file_filters[key] if key in self._file_filters else None

            self.cases[key] = self._load_cases(
                folder=self.input_path,
                file_loader=file_loader,
                file_filter=filter,
            )

    def _load_cases(
        self,
        *,
        folder: Path,
        file_loader: ImageLoader,
        file_filter: Pattern[str] = None,
    ) -> DataFrame:
        cases = []
        for fp in sorted(folder.glob("**/*"), key=self._file_sorter_key):
            if fp.is_dir():
                continue
            if file_filter is None or file_filter.match(str(fp)):
                try:
                    new_cases = file_loader.load(fname=fp)
                except FileLoaderError:
                    logger.warning(f"Could not load {fp.name} using {file_loader}.")
                else:
                    cases.extend(new_cases)
            else:
                logger.info(
                    f"Skip loading {fp.name} because it doesn't match {file_filter}."
                )

        if len(cases) == 0:
            raise FileLoaderError(
                f"Could not load any files in {folder} with " f"{file_loader}."
            )

        return cases

    def validate(self):
        """Validates each dataframe for each fileloader separately"""
        pass

    def _validate_data_frame(self, *, df: DataFrame, file_loader_key: str):
        for validator in self._validators[file_loader_key]:
            validator.validate(df=df)

    def process_cases(self, file_loader_keys: list = None):
        if file_loader_keys is None:
            file_loader_keys = self._index_keys

        self._case_results = []
        case_mapping = [self.cases[key] for key in file_loader_keys]
        for idx, cases in enumerate(zip(*case_mapping)):
            self._case_results.append(
                self.process_case(idx=idx, cases=cases, keys=file_loader_keys)
            )

    def process_case(
        self, *, idx: int, cases: List[DataFrame], keys: List[str]
    ) -> Dict:
        images = {}
        images_file_paths = {}
        for case, key in zip(cases, keys):
            image, image_file_path = self._load_input_image(case=case, key=key)
            images[key] = image
            images_file_paths[key] = image_file_path

        # Predict and generate output
        out = self.predict(input_dict=images)

        # Write resulting segmentation to output location
        out_path = self.output_path / images_file_paths["image"].name
        if not self.output_path.exists():
            self.output_path.mkdir()

        SimpleITK.WriteImage(out, str(out_path), True)

        # Write segmentation file path to result.json for this case
        return {
            "outputs": [dict(type="metaio_image", filename=out_path.name)],
            "inputs": [
                dict(type="metaio_image", filename=fn.name)
                for fn in images_file_paths.values()
            ],
            "error_messages": [],
        }

    def _load_input_image(self, *, case, key) -> Tuple[SimpleITK.Image, Path]:
        input_image_file_path = case["path"]

        input_image_file_loader = self._file_loaders[key]
        if not isinstance(input_image_file_loader, ImageLoader):
            raise RuntimeError("The used FileLoader was not of subclass ImageLoader")

        # Load the image for this case
        input_image = input_image_file_loader.load_image(input_image_file_path)

        # Check that it is the expected image
        if input_image_file_loader.hash_image(input_image) != case["hash"]:
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
