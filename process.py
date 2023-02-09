from typing import Dict

import SimpleITK

from base_algorithm import BaseSynthradAlgorithm


class SynthradAlgorithm(BaseSynthradAlgorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, input_dict: Dict[str, SimpleITK.Image]) -> SimpleITK.Image:
        # Segment all values greater than 2 in the input image
        assert list(input_dict.keys()) == ["image", "mask"]

        return SimpleITK.BinaryThreshold(
            image1=input_dict["image"], lowerThreshold=2, insideValue=1, outsideValue=0
        )


if __name__ == "__main__":
    SynthradAlgorithm().process()
