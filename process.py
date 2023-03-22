from typing import Dict
import SimpleITK
from base_algorithm import BaseSynthradAlgorithm

class SynthradAlgorithm(BaseSynthradAlgorithm):
    """
    This class implements a simple synthetic CT generation algorithm that segments all values greater than 2 in the input image.

    Author: Suraj Pai (b.pai@maastrichtuniversity.nl)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def predict(self, input_dict: Dict[str, SimpleITK.Image]) -> SimpleITK.Image:
        """
        Generates a synthetic CT image from the given input image and mask.

        Parameters
        ----------
        input_dict : Dict[str, SimpleITK.Image]
            A dictionary containing two keys: "image" and "mask". The value for each key is a SimpleITK.Image object representing the input image and mask respectively.

        Returns
        -------
        SimpleITK.Image
            The generated synthetic CT image.
        
        Raises
        ------
        AssertionError:
            If the keys of `input_dict` are not ["image", "mask"]
        """
        
        assert list(input_dict.keys()) == ["image", "mask"]
        
        return SimpleITK.BinaryThreshold(
            image1=input_dict["image"], lowerThreshold=2, insideValue=1, outsideValue=0
        )

if __name__ == "__main__":
    # Run the algorithm on the default input and output paths specified in BaseSynthradAlgorithm.
    SynthradAlgorithm().process()