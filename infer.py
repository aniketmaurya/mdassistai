from fastai.vision import *
import fastai
fastai.torch_core.defaults.device = 'cpu'
def infer(path):
    img = open_image(path)
    learn = load_learner('')
    return learn.predict(img)