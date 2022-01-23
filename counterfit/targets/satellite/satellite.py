import numpy as np
import torchvision.models as models
from torchvision import transforms
from torch import nn
import torch
from torch.nn import functional as F
import PIL

from counterfit.core.targets import Target


class SatelliteImagesTarget(Target):
    """ Image recognition model that leverages pretrained ResNet-50 with a tuned fully-connected layer 
     to distinguish only classes: "airplane" and "stadium"
   """
    target_data_type = "image"
    target_name = "satellite"
    target_endpoint = f"satellite-image-params-airplane-stadium.h5"
    target_input_shape = (3, 256, 256)  # [Channels, Height, Width]
    target_output_classes = ["airplane", "stadium"]
    sample_input_path = f"satellite_images_airplane_stadium_196608.npz"
    target_classifier = "BlackBox"

    X = []  # we'll populate this in the constructor

    def load(self):
        self.data = np.load(self.fullpath(
            self.sample_input_path), allow_pickle=True)
        self.X = self.data["X"].astype(np.float32) / 255.  # map this to [0,1]
        # Loading the pretrained resnet50 model and ready for evaluations/inference
        self.model = self._load_model()

    def get_device(self):
        return 'cpu'

    def _load_model(self):
        device = self.get_device()
        model = models.resnet50(pretrained=False).to(device)
        # A sequential container where modules will be added in the order passed to the constructor.
        # defining model using `torch.nn` package by providing number of input dimensions, hidden units, and number of outputs(`classes`)
        model.fc = nn.Sequential(
            nn.Linear(2048, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 2)).to(device)
        model.load_state_dict(torch.load(self.fullpath(self.target_endpoint)))
        model.eval()
        return model

    def _apply_transformation_on_input_batch(self, x_batch):
        # Apply transformations on the data to make it suitable for predictions
        # the target model wants stack of PIL Image type for prediction
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
        transformer = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            normalize])
        x_transformed_batch = torch.stack([transformer(PIL.Image.fromarray(
            x.transpose(1, 2, 0), 'RGB')).to(self.get_device()) for x in x_batch])
        return x_transformed_batch

    def predict(self, x_batch):
        # This function takes `x_batch` as a numpy array of shape (batch, channels, H, W); apply transformations suitable for the model, and returns probability score
        # since this is an image, let's convert to uint8
        x_batch = (np.array(x_batch)*255).astype(np.uint8)  # quantize (as if saved to disk), and map to 255
        x_transformed_batch = self._apply_transformation_on_input_batch(
            x_batch)
        logps = self.model(x_transformed_batch)
        pred_probs = F.softmax(logps, dim=1).detach().numpy()
        # soften with a temperature that promotes uncertainty
        softening_temperature = 0.75
        aug_probs = pred_probs + softening_temperature
        aug_probs /= aug_probs.sum(axis=1, keepdims=True)  # renormalize rowsum to == 1
        return aug_probs.tolist()  # return a list of class probabilities
        