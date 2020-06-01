from cython_vst_loader.vst_constants import AudioMasterOpcodes


class VstHost:
    VST_VERSION: int = 2400

    def __init__(self, sample_rate: int, buffer_size: int):
        self._sample_rate: int = sample_rate
        self._block_size: int = buffer_size
        self._bpm: float = 120.0

    @property
    def bpm(self) -> float:
        return self._bpm

    @bpm.setter
    def bpm(self, new_pbm: float):
        self._bpm = new_pbm

    # turn into props
    def get_sample_rate(self) -> int:
        return self._sample_rate

    def get_block_size(self) -> int:
        return self._block_size

    # noinspection PyUnusedLocal
    def host_callback(self, plugin_instance_pointer: int, opcode: int, index: int, value: float, ptr: int, opt: float):

        res = None
        if opcode == AudioMasterOpcodes.audioMasterVersion:
            res = (self.VST_VERSION, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetBlockSize:
            res = (self._block_size, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetSampleRate:
            res = (self._sample_rate, None)
        elif opcode == AudioMasterOpcodes.audioMasterGetProductString:
            res = (0, b"CythonVstLoader")

        return res
