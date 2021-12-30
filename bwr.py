import h5py
import numpy as np
import os

def create_bwr(file_name, Raw, Layout, MeaType, NCols, NRows, ROIs, SysChs, Chs, FwVersion, HwVersion, System, BitDepth, MaxVolt, MinVolt, NRecFrames, SamplingRate, SignalInversion, ExpMarkers, ExpNotes):
    path = os.getcwd()
    path = path + "/Brw/empty.brw"
    file = h5py.File(path, 'r')
    with h5py.File(file_name, "w") as f:
        print("Start creating .bwr file")
        data_grp = f.create_group("3BData")
        rec_info_grp = f.create_group("3BRecInfo")
        user_info_grp = f.create_group("3BUserInfo")

        #########################################################
        #######################Attributes########################
        #########################################################
        print("Attributes")
        f.attrs["Version"] = file.attrs["Version"]
        f.attrs["Description"] = file.attrs["Description"]
        f.attrs["GUID"] = file.attrs["GUID"]

        # TODO: make own Version and Description

        #########################################################
        ####################3BData############################
        #########################################################
        print("3BData: Attributes")
        data_grp.attrs.create(name="Version", data=101, shape=None, dtype=np.int32)
        print("3BData")
        results_ch_events = data_grp.create_dataset("Raw", data=Raw)



        #########################################################
        ####################3BRecInfo############################
        #########################################################
        rec_info_grp.attrs.create(name="Version", data=100, shape=None, dtype=np.int32)
        print("3BRecInfo")
        rec_info_mea_chip = rec_info_grp.create_group("3BMeaChip")
        rec_info_mea_streams = rec_info_grp.create_group("3BMeaStreams")
        rec_info_mea_systems = rec_info_grp.create_group("3BMeaSystem")
        rec_info_rec_vars = rec_info_grp.create_group("3BRecVars")

        rec_info_mea_chip.attrs.create(name="Version", data=100, shape=None, dtype=np.int32)
        rec_info_mea_info_layout = rec_info_mea_chip.create_dataset("Layout", data=Layout, dtype='|u1')
        rec_info_mea_info_meatype = rec_info_mea_chip.create_dataset("MeaType", data=MeaType, dtype='i4')
        rec_info_mea_info_ncols = rec_info_mea_chip.create_dataset("NCols", data=NCols, dtype='u4')
        rec_info_mea_info_nrows = rec_info_mea_chip.create_dataset("NRows", data=NRows, dtype='u4')
        rec_info_mea_info_rois = rec_info_mea_chip.create_dataset("ROIs", data=ROIs)
        rec_info_mea_info_syschs = rec_info_mea_chip.create_dataset("SysChs", data=SysChs)

        rec_info_mea_streams.attrs.create(name="Version", data=100, shape=None, dtype=np.int32)
        rec_info_mea_streams_raw = rec_info_mea_streams.create_group("Raw")
        rec_info_mea_streams_raw_chs = rec_info_mea_streams_raw.create_dataset("Chs", data=Chs)

        rec_info_mea_systems.attrs.create(name="Version", data=100, shape=None, dtype=np.int32)
        rec_info_mea_systems_fwversion = rec_info_mea_systems.create_dataset("FwVersion", data=FwVersion)
        rec_info_mea_systems_hwversion = rec_info_mea_systems.create_dataset("HwVersion", data=HwVersion)
        rec_info_mea_systems_system = rec_info_mea_systems.create_dataset("System", data=System)

        rec_info_rec_vars.attrs.create(name="Version", data=100, shape=None, dtype=np.int32)
        rec_info_mea_vars_bitdepth = rec_info_rec_vars.create_dataset("BitDepth", data=BitDepth)
        rec_info_mea_vars_maxvolt = rec_info_rec_vars.create_dataset("MaxVolt", data=MaxVolt)
        rec_info_mea_vars_mivolt = rec_info_rec_vars.create_dataset("MinVolt", data=MinVolt)
        rec_info_mea_vars_nrecframes = rec_info_rec_vars.create_dataset("NRecFrames", data=NRecFrames)
        rec_info_mea_vars_samplingrate = rec_info_rec_vars.create_dataset("SamplingRate", data=SamplingRate, dtype='f8')
        rec_info_mea_vars_signalinversion = rec_info_rec_vars.create_dataset("SignalInversion", data=SignalInversion)


        #########################################################
        ####################3BUserInfo###########################
        #########################################################
        user_info_grp.attrs.create(name="Version", data=101, shape=None, dtype=np.int32)
        print("3BUserInfo")
        user_info_exp_markers = user_info_grp.create_dataset("ExpMarkers", data=ExpMarkers)
        user_info_exp_notes = user_info_grp.create_dataset("ExpNotes", data=ExpNotes)
        print("Finished creating .bwr file")

    #f.close()


class read_brw:
    def __init__(self, path):
        self.file = h5py.File(path, 'r')
        self.raw = self.file["3BData/Raw"]

        self.sf = self.file['3BRecInfo/3BRecVars/SamplingRate'][()][0]
        self.recLenght = self.file['3BRecInfo/3BRecVars/NRecFrames'][0] / self.sf