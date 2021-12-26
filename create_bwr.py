import h5py
import numpy as np

def create_bwr(file_name, Raw, Layout, MeaType, NCols, NRows, ROIs, SysChs, Chs, FwVersion, HwVersion, System, BitDepth, MaxVolt, MinVolt, NRecFrames, SamplingRate, SignalInversion, ExpMarkers, ExpNotes):
    file = h5py.File("/mnt/HDD/VirtualBox/Windows 10/shared/1min 9000Hz.brw", 'r')
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
        # f.attrs["Version"] = 211
        # f.attrs["Description"] = b'BXR-File Level2 - 3Brain eXperiment Results file for high resolution MEA platform, HDF5-format - Created with BrainWave v.4.4.7998.22458 on date Wednesday, December 1, 2021'
        # f.attrs["GUID"] = b'982c7143-2982-4624-b8c3-4593b93fd330'

        # Description = 'BXR-File Level2 - 3Brain eXperiment Results file for high resolution MEA platform, HDF5-format - Created with BrainWave v.4.4.7998.22458 on date Wednesday, December 1, 2021'

        # f.attrs.create(name="Version", data=211, shape=None, dtype=np.int32)
        # TODO: Datatypes of Description and GUID are not right
        # f.attrs.create(name="Description", data=Description,shape=None, dtype=h5py.special_dtype(vlen=str))
        # f.attrs.create(name="GUID", data='982c7143-2982-4624-b8c3-4593b93fd330',shape=None, dtype=h5py.string_dtype('ascii'))

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
