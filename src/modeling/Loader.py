import numpy as np
import pathlib as pl 
from tqdm import tqdm

def load_glove_model(path:pl.Path) -> dict:
    """
    Returns loaded GloVe model located in `path` as dictionary
    """
    print("Loading Glove Model")
    f = open(path,'r', encoding='utf8')
    gloveModel = {}
    for line in tqdm(f):
        splitLines = line.split()
        word = splitLines[0]
        wordEmbedding = np.array([float(value) for value in splitLines[1:]])
        gloveModel[word] = wordEmbedding
    print(len(gloveModel)," words loaded!")
    return gloveModel