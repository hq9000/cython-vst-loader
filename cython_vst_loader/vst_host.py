from cython_vst_loader.dto.vst_time_info import VstTimeInfo
from cython_vst_loader.exceptions import CythonVstLoaderException
from cython_vst_loader.vst_constants import AudioMasterOpcodes, VstProcessLevels


class VstHost:
    VST_VERSION: int = 2400

    def __init__(self, sample_rate: int, buffer_size: int):
        self._sample_rate: int = sample_rate
        self._block_size: int = buffer_size
        self._bpm: float = 120.0
        self._sample_position: int = 0

    @property
    def bpm(self) -> float:
        return self._bpm

    @bpm.setter
    def bpm(self, new_pbm: float):
        self._bpm = new_pbm

    @property
    def sample_position(self) -> int:
        return self._sample_position

    @sample_position.setter
    def sample_position(self, new_sample_position: int):
        self._sample_position = new_sample_position

    # turn into props
    def get_sample_rate(self) -> int:
        return self._sample_rate

    def get_block_size(self) -> int:
        return self._block_size

    # noinspection PyUnusedLocal
    def host_callback(self, plugin_instance_pointer: int, opcode: int, index: int, value: float, ptr: int, opt: float):

        # print('python called host_callback with plugin instance ' + str(plugin_instance_pointer) + ' opcode: ' + str(
        #    opcode) + " value: " + str(value))

        res = None
        if opcode == AudioMasterOpcodes.audioMasterVersion:
            res = (self.VST_VERSION, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetBlockSize:
            res = (self._block_size, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetSampleRate:
            res = (self._sample_rate, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetProductString:
            res = (0, b"CythonVstLoader")
        elif opcode == AudioMasterOpcodes.audioMasterWantMidi:
            res = (False, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetTime:
            res = (0, self.generate_time_info())
        elif opcode == AudioMasterOpcodes.audioMasterGetCurrentProcessLevel:
            res = (VstProcessLevels.kVstProcessLevelUnknown, None)
        elif opcode == AudioMasterOpcodes.audioMasterIOChanged:
            res = (0, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetVendorString:
            res = (0, b"cython vst loader")
        elif opcode == AudioMasterOpcodes.audioMasterGetVendorVersion:
            res = (1, None)
        elif opcode == AudioMasterOpcodes.audioMasterSizeWindow:
            res = (0, None)
        else:
            raise CythonVstLoaderException(f"plugin-to-host opcode {str(opcode)} is not supported")

        return res

    def generate_time_info(self) -> VstTimeInfo:
        res = VstTimeInfo(
            sample_pos=self.sample_position,
            sample_rate=self._sample_rate,
            cycle_start_pos=0,
            cycle_end_pos=10
        )

        return res
