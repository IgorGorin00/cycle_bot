import torch
from PIL import Image
import torchvision.transforms as tt
from utils import tensor2im
from model import ResnetGenerator
import os


def get_models(models_dir):

    model_files = [
        os.path.join(models_dir, 'model_cezanne.pth'),
        os.path.join(models_dir, 'model_monet.pth'),
        os.path.join(models_dir, 'model_vangogh.pth'),
        os.path.join(models_dir, 'model_ukiyoe.pth'),
    ]

    models = {}
    for fname in model_files:
        basename = os.path.basename(fname)
        model = ResnetGenerator()
        style_name = basename.split('.')[0]
        style_name = style_name.split('_')[1]
        model.load_networks(fname)
        models[style_name] = model
    return models


def get_visual(img_path, model):
    tsfms = tt.Compose([
        tt.Resize([256, 256], tt.InterpolationMode.BICUBIC),
        #    tt.RandomCrop(256),
        tt.ToTensor(),
        tt.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    img = Image.open(img_path)

    with torch.no_grad():
        res = model.forward(tsfms(img))
        res = tensor2im(res)

    return res
