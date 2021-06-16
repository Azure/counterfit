import numpy as np
import torchvision.models as models
from torchvision import transforms
from torch import nn
import torch
from torch.nn import functional as F
from PIL import Image

from counterfit.core import config
from counterfit.core.state import ArtTarget


class SatelliteImagesTarget(ArtTarget):
    """ Image recognition model that leverages pretrained ResNet-50 with a tuned fully-connected layer 
     to distinguish only classes: "airplane" and "stadium"
   """
    model_name = "satelliteimages"
    model_data_type = "image"
    model_location = "local"
    model_endpoint = f"{config.targets_path}/{model_name}/satellite-image-params-airplane-stadium.h5"
    model_input_shape = (3, 256, 256) #[Channels, Height, Width]
    channels_first = True
    model_output_classes = ["airplane", "stadium"]  # the ART integration allows arbitrary labels
    sample_input_path = f"{config.targets_path}/{model_name}/satellite_images_airplane_stadium_196608.npz"
    clip_values = (0.0, 255.0)

    X = []  # we'll populate this in the constructor

    def __init__(self):
        self.data = np.load(self.sample_input_path, allow_pickle=True)
        self.X = self.data["X"]
        self.model = self._load_model()  # Loading the pretrained resnet50 model and ready for evaluations/inference
        
    def get_device(self):
        is_cuda = torch.cuda.is_available()
        # If we have a GPU available, we'll set our device to GPU.
        device = None
        if is_cuda:
            device = 'cuda'
        else:
            device = 'cpu'
        return device
            
    def _load_model(self):
        device = self.get_device()
        model = models.resnet50(pretrained=False).to(device)
        # A sequential container where modules will be added in the order passed to the constructor.
        # defining model using `torch.nn` package by providing number of input dimensions, hidden units, and number of outputs(`classes`) 
        model.fc = nn.Sequential(
                nn.Linear(2048, 128),
                nn.ReLU(inplace=True),
                nn.Linear(128, 2)).to(device)
        model.load_state_dict(torch.load(self.model_endpoint))
        model.eval()
        return model
    
    def _apply_transformation_on_input_batch(self, x_batch):
        # Apply transformations on the data to make it suitable for predictions
        # the target model wants stack of PIL Image type for prediction 
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        transformer = transforms.Compose([
                transforms.Resize((224,224)),
                transforms.ToTensor(),
                normalize])
        x_transformed_batch = torch.stack([transformer(Image.fromarray(x.transpose(1, 2, 0), 'RGB')).to(self.get_device()) for x in x_batch])
        return x_transformed_batch

    def __call__(self, x_batch):
        # This function takes `x_batch` as a numpy array of shape (batch, channels, H, W); apply transformations suitable for the model, and returns probability score
        x_transformed_batch = self._apply_transformation_on_input_batch(x_batch)
        logps = self.model(x_transformed_batch)
        pred_probs = F.softmax(logps, dim=1)
        return pred_probs.tolist()  # return a list of class probabilities
