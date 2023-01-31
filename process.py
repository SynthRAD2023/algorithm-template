
import SimpleITK
import numpy as np

from evalutils import SegmentationAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)


class Synthrad_algorithm(SegmentationAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )

    def predict(self, *, input_image: SimpleITK.Image) -> SimpleITK.Image:
        # Segment all values greater than 2 in the input image
        return SimpleITK.BinaryThreshold(
            image1=input_image, lowerThreshold=2, insideValue=1, outsideValue=0
        )


if __name__ == "__main__":
    Synthrad_algorithm().process()
