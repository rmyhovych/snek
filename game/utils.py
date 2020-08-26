import os
import torch

OUT_DIR = "./out"


def save_model(model):
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    torch.save(model, os.path.join(OUT_DIR, "model"))


def load_model():
    return torch.load(os.path.join(OUT_DIR, "model"))
