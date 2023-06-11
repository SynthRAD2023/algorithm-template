from typing import Dict

import SimpleITK as sitk
# import torch
import numpy as np

from base_algorithm import BaseSynthradAlgorithm


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
        assert list(input_dict.keys()) == ["image", "mask", "region"]

        # You may use the region information to generate the synthetic CT image if needed 
        region = input_dict["region"]
        print("Scan region: ", region)
        mr_sitk = input_dict["image"]
        mask_sitk = input_dict["mask"]

        # convert sitk images to np arrays
        mask_np = sitk.GetArrayFromImage(mask_sitk).astype("float32")
        mr_np = sitk.GetArrayFromImage(mr_sitk).astype("float32")



        # NOTE: To test using pytorch, uncomment the following lines and comment the lines below

        ## check if GPU is available
        # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # print("Using device: ", device)

        ## convert np arrays to tensors
        # mr_tensor = torch.tensor(mr_np, device=device)
        # mask_tensor = torch.tensor(mask_np, device=device)

        ## sCT generation placeholder (set values inside mask to 0)
        # mr_tensor[mask_tensor == 1] = 0
        # mr_tensor[mask_tensor == 0] = -1000

        ## convert tensor back to np array
        # sCT = mr_tensor.cpu().numpy()

        
        # NOTE: Comment the following lines if using pytorch
        sCT = np.zeros(mr_np.shape)
        sCT[mask_np == 1] = 0
        sCT[mask_np == 0] = -1000


        sCT_sitk = sitk.GetImageFromArray(sCT)
        sCT_sitk.CopyInformation(mr_sitk)

        return sCT_sitk


if __name__ == "__main__":
    # Run the algorithm on the default input and output paths specified in BaseSynthradAlgorithm.
    SynthradAlgorithm().process()
