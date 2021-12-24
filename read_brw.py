import h5py

class ReadBrw:
    def __init__(self, path):
        self.file = h5py.File(path, 'r')
        self.raw = self.file["3BData/Raw"]

        self.sf = self.file['3BRecInfo/3BRecVars/SamplingRate'][()][0]
        self.recLenght = self.file['3BRecInfo/3BRecVars/NRecFrames'][0] / self.sf