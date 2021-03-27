from dataclasses import dataclass
from typing import Optional


@dataclass
class VstTimeInfo:
    """
    This class is a python representation of the following structs defined in aeffectx.h

    //-------------------------------------------------------------------------------------------------------
    // VstTimeInfo
    //-------------------------------------------------------------------------------------------------------
    //-------------------------------------------------------------------------------------------------------
    /** VstTimeInfo requested via #audioMasterGetTime.  @see AudioEffectX::getTimeInfo

    \note VstTimeInfo::samplePos :Current Position. It must always be valid, and should not cost a lot to ask for. The sample position is ahead of the time displayed to the user. In sequencer stop mode, its value does not change. A 32 bit integer is too small for sample positions, and it's a double to make it easier to convert between ppq and samples.
    \note VstTimeInfo::ppqPos : At tempo 120, 1 quarter makes 1/2 second, so 2.0 ppq translates to 48000 samples at 48kHz sample rate.
    25 ppq is one sixteenth note then. if you need something like 480ppq, you simply multiply ppq by that scaler.
    \note VstTimeInfo::barStartPos : Say we're at bars/beats readout 3.3.3. That's 2 bars + 2 q + 2 sixteenth, makes 2 * 4 + 2 + .25 = 10.25 ppq. at tempo 120, that's 10.25 * .5 = 5.125 seconds, times 48000 = 246000 samples (if my calculator servers me well :-).
    \note VstTimeInfo::samplesToNextClock : MIDI Clock Resolution (24 per Quarter Note), can be negative the distance to the next midi clock (24 ppq, pulses per quarter) in samples. unless samplePos falls precicely on a midi clock, this will either be negative such that the previous MIDI clock is addressed, or positive when referencing the following (future) MIDI clock.
    */
    //-------------------------------------------------------------------------------------------------------
    struct VstTimeInfo
    {
    //-------------------------------------------------------------------------------------------------------
        double samplePos;				///< current Position in audio samples (always valid)
        double sampleRate;				///< current Sample Rate in Herz (always valid)
        double nanoSeconds;				///< System Time in nanoseconds (10^-9 second)
        double ppqPos;					///< Musical Position, in Quarter Note (1.0 equals 1 Quarter Note)
        double tempo;					///< current Tempo in BPM (Beats Per Minute)
        double barStartPos;				///< last Bar Start Position, in Quarter Note
        double cycleStartPos;			///< Cycle Start (left locator), in Quarter Note
        double cycleEndPos;				///< Cycle End (right locator), in Quarter Note
        VstInt32 timeSigNumerator;		///< Time Signature Numerator (e.g. 3 for 3/4)
        VstInt32 timeSigDenominator;	///< Time Signature Denominator (e.g. 4 for 3/4)
        VstInt32 smpteOffset;			///< SMPTE offset (in SMPTE subframes (bits; 1/80 of a frame)). The current SMPTE position can be calculated using #samplePos, #sampleRate, and #smpteFrameRate.
        VstInt32 smpteFrameRate;		///< @see VstSmpteFrameRate
        VstInt32 samplesToNextClock;	///< MIDI Clock Resolution (24 Per Quarter Note), can be negative (nearest clock)
        VstInt32 flags;					///< @see VstTimeInfoFlags
    //-------------------------------------------------------------------------------------------------------
    };

    and also some data passed in flags

    enum VstTimeInfoFlags
    {
    //-------------------------------------------------------------------------------------------------------
        kVstTransportChanged     = 1,		///< indicates that play, cycle or record state has changed 1
        kVstTransportPlaying     = 1 << 1,	///< set if Host sequencer is currently playing 2
        kVstTransportCycleActive = 1 << 2,	///< set if Host sequencer is in cycle mode 4
        kVstTransportRecording   = 1 << 3,	///< set if Host sequencer is in record mode 8
        kVstAutomationWriting    = 1 << 6,	///< set if automation write mode active (record parameter changes) 16
        kVstAutomationReading    = 1 << 7,	///< set if automation read mode active (play parameter changes) 32

        kVstNanosValid           = 1 << 8,	///< VstTimeInfo::nanoSeconds valid 64
        kVstPpqPosValid          = 1 << 9,	///< VstTimeInfo::ppqPos valid 128
        kVstTempoValid           = 1 << 10,	///< VstTimeInfo::tempo valid 256
        kVstBarsValid            = 1 << 11,	///< VstTimeInfo::barStartPos valid 512
        kVstCyclePosValid        = 1 << 12,	///< VstTimeInfo::cycleStartPos and VstTimeInfo::cycleEndPos valid 1024
        kVstTimeSigValid         = 1 << 13,	///< VstTimeInfo::timeSigNumerator and VstTimeInfo::timeSigDenominator valid
        kVstSmpteValid           = 1 << 14,	///< VstTimeInfo::smpteOffset and VstTimeInfo::smpteFrameRate valid
        kVstClockValid           = 1 << 15	///< VstTimeInfo::samplesToNextClock valid
    //-------------------------------------------------------------------------------------------------------
    };

    """
    sample_pos: float  # always valid
    sample_rate: float  # always valid
    nano_seconds: Optional[float] = None
    ppq_pos: Optional[float] = None
    tempo: Optional[float] = None
    bar_start_pos: Optional[float] = None
    cycle_start_pos: Optional[float] = None
    cycle_end_pos: Optional[float] = None
    time_sig_numerator: Optional[int] = None
    time_sig_denominator: Optional[int] = None
    smpte_offset: Optional[int] = None
    smpte_frame_rate: Optional[int] = None
    samples_to_next_clock: Optional[int] = None

    transport_changed_flag: bool = False
    transport_playing_flag: bool = True
    transport_cycle_active_flag: bool = False
    transport_recording_flag: bool = False
    automation_writing_flag: bool = False
    automation_reading_flag: bool = False
