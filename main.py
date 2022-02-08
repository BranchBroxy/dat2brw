import numpy as np
import h5py  # hdf5
from read_dat import read_dat
from bwr import create_bwr


# Type in these two commands:
# conda env create -f environment.yml
# conda activate mat2brw



def convert(path_dat, file_name):
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
    # data_raw = (data_raw * 10) # TODO: float64 to uint16 noch nicht geklärt
    # data_raw = data_raw + 2000

    """
    function [m]=digital2analog_sh(M,raw)
    Bit=raw.BitDepth;
    MxV=raw.MaxVolt;
    SIV=raw.SignalInversion;
    m = single(M);
    m=SIV*(m-(2^Bit)/2)*(MxV*2/2^Bit);
end
    """

    Bit = 12
    MxV = data_raw.max()
    SIV = 1
    # m = single(M);
    # m = SIV * (m - (2 ^ Bit) / 2) * (MxV * 2 / 2 ^ Bit)

    brw_data = data_raw/(SIV*(2*MxV/2**Bit))+(2**Bit)/2
    data_raw = brw_data


    brw_array = np.zeros(shape=(data_raw.shape[0], 4096), dtype="uint16")
    x = 0
    y = 0
    brw_array[x:x + data_raw.shape[0], y:y + data_raw.shape[1]] = data_raw
    # brw_length = data_raw.shape[0] * 4096
    brw_array = np.where(brw_array==0, 2000, brw_array)
    hop = 0
    alte_pos = 0

    for erstezeile in range(6):
        neue_pos = 1757 + erstezeile
        temp = np.copy(brw_array[:, alte_pos])
        brw_array[:, alte_pos] = brw_array[:, neue_pos]
        brw_array[:, neue_pos] = temp
        alte_pos = alte_pos + 1

    for zeilen in range(6):
        for spalten in range(8):
            # alte_pos = spalten + zeilen * 8
            neue_pos = 1820 + spalten + hop
            temp = np.copy(brw_array[:, alte_pos])
            brw_array[:, alte_pos] = brw_array[:, neue_pos]
            brw_array[:, neue_pos] = temp
            alte_pos = alte_pos + 1
        hop = hop + 64

    for letztezeile in range(6):
        neue_pos = 2205 + letztezeile
        temp = np.copy(brw_array[:, alte_pos])
        brw_array[:, alte_pos] = brw_array[:, neue_pos]
        brw_array[:, neue_pos] = temp
        alte_pos = alte_pos + 1


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

    create_bwr(file_name, Raw, Layout, MeaType, NCols, NRows, ROIs, SysChs, Chs, FwVersion, HwVersion, System, BitDepth,
               MaxVolt, MinVolt, NRecFrames, SamplingRate, SignalInversion, ExpMarkers, ExpNotes)
    print("Conversion successful")


if __name__ == '__main__':
    print("Starting")
    convert("/mnt/HDD/FauBox/Uni/Master/PyCharm/mat2brw_v1/Messung02.11.2020_10-59-15 GUT.dat", "/mnt/HDD/VirtualBox/Windows 10/shared/dat2brw_V9.brw")
    print("Finished")

