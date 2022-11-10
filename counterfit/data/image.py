import numpy as np
from PIL.Image import Image

class ImageDataType():
    @staticmethod
    def is_channels_last(input_shape):
        if input_shape[-1] == 3:
            channels_last = True
        elif input_shape[-1] == 1:
            channels_last = True
        else:
            channels_last = False
        return channels_last

    @staticmethod
    def convert_to_uint8(array, factor=None):
        if not factor:
            return np.uint8(array)
        else:
            return np.uint8(array * factor)

    @staticmethod
    def get_channels(input_shape):
        if input_shape[-1] == 3 or input_shape[0] == 3:
            return "RGB"
        else:
            return "L"

    @staticmethod
    def transpose_array(array):
        return np.transpose(array)

    @staticmethod
    def convert_to_pil(array):
        pil_image = Image.fromarray(array)
        return pil_image

    @staticmethod
    def convert_to_array(image: Image):
        image_array = np.array(image)
        return image_array

    @staticmethod
    def grayscale_to_pil(array: np.ndarray) -> Image:
           pil_image = Image.fromarray((np.squeeze(array) * 255).astype(np.uint8))
           return pil_image