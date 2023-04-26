from typing import Dict

import SimpleITK as sitk

from base_algorithm import BaseSynthradAlgorithm


# Utility function to create a dummy masked image
def set_mask_value(image, mask, inside_value, outside_value):
    # Ensure the mask is binary
    binary_mask = sitk.BinaryThreshold(mask, 1, 255, 255, 0)

    # Create casted image with same origin, spacing, and direction as input image
    casted_image = sitk.Cast(image, binary_mask.GetPixelID())

    # Set values inside the mask
    inside_masked_image = sitk.Mask(casted_image, binary_mask, inside_value)

    # Invert the mask
    inverted_mask = sitk.InvertIntensity(binary_mask, maximum=255)

    # Set values outside the mask
    outside_masked_image = sitk.Mask(casted_image, inverted_mask, outside_value)

    # Combine both masked parts
    masked_image = inside_masked_image + outside_masked_image

    return masked_image


class SynthradAlgorithm(BaseSynthradAlgorithm):
    """
    This class implements a simple synthetic CT generation algorithm that segments all values greater than 2 in the input image.

    Author: Suraj Pai (b.pai@maastrichtuniversity.nl)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, input_dict: Dict[str, sitk.Image]) -> sitk.Image:
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
        return set_mask_value(input_dict["image"], input_dict["mask"], -50, -1024)


if __name__ == "__main__":
    # Run the algorithm on the default input and output paths specified in BaseSynthradAlgorithm.
    SynthradAlgorithm().process()
