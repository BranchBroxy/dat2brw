import numpy as np
import h5py  # hdf5
import scipy.io
from read_brw import ReadBrw
from read_dat import read_dat
from create_bwr import create_bwr
from bwr_test import create_bwr_test

# pip install -r requirements.txt


def convert(path_dat, file_name):
    brw_data = ReadBrw("/mnt/HDD/VirtualBox/Windows 10/shared/1min 9000Hz.brw")

    V4 = np.dtype([('Row', '<i2'), ('Col', '<i2')])
    V16 = np.dtype([('Major', '<i4'), ('Minor', '<i4'), ('Build', '<i4'), ('Revision', '<i4')])
    V16_2 = np.dtype([('Title', h5py.special_dtype(vlen=str)), ('Value', h5py.special_dtype(vlen=str))])
    V24 = np.dtype([('StartFrame', '<i8'), ('EndFrame', '<i8'), ('FrameRate', '<f8')])
    V36 = np.dtype({'names': ['Name', 'Color', 'IsVisible', 'Intervals'],
                    'formats': [h5py.special_dtype(vlen=str),
                                [('KnownColor', '<i4'), ('Alpha', 'u1'), ('Red', 'u1'), ('Green', 'u1'),
                                 ('Blue', 'u1')], 'u1', h5py.special_dtype(vlen=V24)],
                    'offsets': [0, 8, 16, 20],
                    'itemsize': 36})

    V36_2 = np.dtype({'names': ['Type', 'MarkIn', 'MarkOut', 'Desc', 'Color'],
                      'formats': ['<i2', '<i8', '<i8', h5py.special_dtype(vlen=str),
                                 [('KnownColor', '<i4'), ('Alpha', 'u1'),
                                  ('Red', 'u1'), ('Green', 'u1'),
                                  ('Blue', 'u1')]],
                      'offsets': [0, 4, 12, 20, 28],
                      'itemsize': 36})

    data, meta = read_dat(path_dat)
    rec_dur = data.iloc[:, 0].max() # Recording Duration
    SaRa = meta[2] # Sample Rate
    data_raw = data.iloc[:, 1:].to_numpy()
    # data_raw = data_raw / data_raw.max()  # normalizes data in range 0 - 255
    data_raw = np.abs(data_raw * 1000) # TODO: float64 to uint16 noch nicht geklärt
    brw_array = np.zeros(shape=(data_raw.shape[0], 4096), dtype="uint16") # TODO: move to the middle 64:64
    x = 0
    y = 0 #TODO: change y to something else
    brw_array[x:x + data_raw.shape[0], y:y + data_raw.shape[1]] = data_raw
    # brw_length = data_raw.shape[0] * 4096

    hop = 0
    for zeilen in range(8):

        for spalten in range(8):
            alte_pos = spalten + zeilen * 8
            neue_pos = 1755 + spalten + hop
            temp = np.copy(brw_array[:, alte_pos])
            brw_array[:, alte_pos] = brw_array[:, neue_pos]
            brw_array[:, neue_pos] = temp
        hop = hop + 64


    brw_array_one_dim = brw_array.reshape(-1)
    Raw = brw_array_one_dim
    Layout = np.ones(shape=(64,64), dtype="uint8")
    MeaType = np.array([65536], dtype="int32")
    NCols = np.array([64], dtype="uint32")
    NRows = np.array([64], dtype="uint32")
    ROIs = np.empty(shape=(0,), dtype=V36)
    SysChs = np.ones(shape=(1,), dtype=V4)
    Chs = np.zeros(shape=(4096,), dtype=V4)
    for i in range(0, 64):
        for y in range(0, 64):
            Chs[y + (64 * i)][0] = i + 1
            Chs[y + (64 * i)][1] = y + 1
    FwVersion = np.array([(0, 0, 0, 0)], dtype=V16)
    HwVersion = np.array([(0, 0, -1, -1)], dtype=V16)
    System = np.array(([1]), dtype=np.int32)

    BitDepth = np.array([12], dtype=np.uint8)
    MaxVolt = np.array([data_raw.max()])
    MinVolt = np.array([data_raw.min()])
    NRecFrames_float = Raw.shape[0] / (NCols[0] * NRows[0])
    NRecFrames = np.ones(shape=(1,), dtype="i8")
    NRecFrames[0] = NRecFrames_float
    SamplingRate = np.ones(shape=(1,), dtype="f8")
    SamplingRate[0] = SaRa
    SignalInversion = np.array([1], dtype=np.float64)

    ExpMarkers = np.empty(shape=(0,), dtype=V36_2)
    ExpNotes = np.empty(shape=(0,), dtype=V16_2)
    ExpNotes = np.array(([(b'Remarks', b'')]), dtype=V16_2)

    z1 = np.array(brw_data.file["3BData/Raw"]).reshape((brw_data.file["3BRecInfo/3BRecVars/NRecFrames"][0], 4096))
    # brw_data.file["3BData/Raw"][1 * 4096]
    create_bwr(file_name, Raw, Layout, MeaType, NCols, NRows, ROIs, SysChs, Chs, FwVersion, HwVersion, System, BitDepth,
               MaxVolt, MinVolt, NRecFrames, SamplingRate, SignalInversion, ExpMarkers, ExpNotes)
    # current_length = data_raw_one_dim.shape[0]
    # add_length = brw_length - current_length
    # data_raw_one_dim_brw = np.lib.pad(data_raw_one_dim, ((0, add_length)), 'constant', constant_values=(0))
    print("Conversion successful")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting")
    brw_data = ReadBrw("/mnt/HDD/VirtualBox/Windows 10/shared/1min 9000Hz.brw") # 555622400
    convert("/mnt/HDD/FauBox/Uni/Master/PyCharm/mat2brw_v1/Messung02.11.2020_10-59-15 GUT.dat", "/mnt/HDD/VirtualBox/Windows 10/shared/dat2brw_V7.brw")
    # create_bwr_test()
    #brw_data_me = ReadBrw("/mnt/HDD/VirtualBox/Windows 10/shared/dat2brw.brw")
    print("Finished")

