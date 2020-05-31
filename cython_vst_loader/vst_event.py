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
    _NOTE_ON: str = 'note_on'
    _NOTE_OFF: str = 'note_off'

    def __init__(self, delta_frames: int):
        super().__init__()
        self.delta_frames = delta_frames
        self.type: int = VstEventTypes.kVstMidiType
        self.flags = 0
        self.note_length: Optional[int] = None
        self.note_offset: Optional[int] = None
        self.midi_data: bytearray = bytearray([0, 0, 0, 0])
        self.detune: int = 0
        self.note_off_velocity: int = 0
        self.reserved1: int = 0
        self.reserved2: int = 0

    @classmethod
    def _midi_note_as_bytes(cls, note: int, velocity: int = 100, kind: str = 'note_on', channel: int = 1) -> bytes:
        """
        borrowed from here:
        https://github.com/simlmx/pyvst/blob/ded9ff373f37d1cbe8948ccb053ff4849f45f4cb/pyvst/midi.py#L11

        :param note:
        :param velocity:
        :param kind:
        :param channel: Midi channel (those are 1-indexed)
        """
        if kind == cls._NOTE_ON:
            kind_byte = b'\x90'[0]
        elif kind == cls._NOTE_OFF:
            kind_byte = b'\x80'[0]
        else:
            raise NotImplementedError('MIDI type {} not supported yet'.format(kind))

        def _check_channel_valid(channel_to_check):
            if not (1 <= channel_to_check <= 16):
                raise ValueError('Invalid channel "{}". Must be in the [1, 16] range.'
                                 .format(channel_to_check))

        _check_channel_valid(channel)

        return bytes([
            (channel - 1) | kind_byte,
            note,
            velocity
        ])


class VstNoteOnMidiEvent(VstMidiEvent):
    def __init__(self, delta_frames: int, note: int, velocity: int, channel: int):
        super().__init__(delta_frames)
        self.midi_data = self._midi_note_as_bytes(note, velocity, self._NOTE_ON, channel)


class VstNoteOffMidiEvent(VstMidiEvent):
    def __init__(self, delta_frames: int, note: int, channel: int):
        super().__init__(delta_frames)
        self.midi_data = self._midi_note_as_bytes(note, 0, self._NOTE_OFF, channel)
