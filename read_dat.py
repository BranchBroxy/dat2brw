import numpy as np
import pandas as pd

def read_dat(path):
    # f = open(path)
    i = pd.read_csv(path, sep="\s+", encoding="cp1252", nrows=0)
    meta = list(i.columns.values)
    data = pd.read_csv(path, sep="\s+", encoding="cp1252", skiprows=3)
    return data, meta
