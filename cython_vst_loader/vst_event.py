from typing import Optional

from cython_vst_loader.vst_constants import VstEventTypes


class VstEvent:
    def __init__(self):
        self.type: Optional[int] = None
        self.byte_size: Optional[int] = None
        self.delta_frames: Optional[int] = None
        self.flags: Optional[int] = None
        self.data: Optional[bytes] = None

    def is_midi(self) -> bool:
        return self.type == VstEventTypes.kVstMidiType


class VstMidiEvent(VstEvent):
    def __init__(self):
        super().__init__()
        self.type: int = VstEventTypes.kVstMidiType
        self.note_length: Optional[int] = None
        self.note_offset: Optional[int] = None
        self.midi_data: bytearray = bytearray([0, 0, 0, 0])
        self.detune: bytearray = bytearray([0])
        self.note_off_velocity: bytearray = bytearray([0])
        self.reserved1: bytearray = bytearray([0])
        self.reserved2: bytearray = bytearray([0])
