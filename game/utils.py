import os
import torch

OUT_DIR = "./out"


def save_model(model, model_name="model"):
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    torch.save(model, os.path.join(OUT_DIR, model_name))


def load_model(name="model"):
    return torch.load(os.path.join(OUT_DIR, name))
