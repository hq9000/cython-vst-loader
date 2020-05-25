class AudioMasterOpcodes:
    # [index]: parameter index [opt]: parameter value  @see AudioEffect::setParameterAutomated
    audioMasterAutomate = 0
    # [return value]: Host VST version (for example 2400 for VST 2.4) @see AudioEffect::getMasterVersion
    audioMasterVersion = 1
    # [return value]: current unique identifier on shell plug-in  @see AudioEffect::getCurrentUniqueId
    audioMasterCurrentId = 2
    # no arguments  @see AudioEffect::masterIdle
    audioMasterIdle = 3

    # \deprecated deprecated in VST 2.4 r2
    # DECLARE_VST_DEPRECATED (audioMasterPinConnected)
    # \deprecated deprecated in VST 2.4
    audioMasterWantMidi = 6

    # [return value]: #VstTimeInfo* or null if not supported [value]:
    # request mask  @see VstTimeInfoFlags @see AudioEffectX::getTimeInfo
    audioMasterGetTime = 7
    # [ptr]: pointer to #VstEvents  @see VstEvents @see AudioEffectX::sendVstEventsToHost
    audioMasterProcessEvents = 8

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetTime),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterTempoAt),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetNumAutomatableParameters),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetParameterQuantization),

    # [return value]: 1 if supported  @see AudioEffectX::ioChanged
    audioMasterIOChanged = 13

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterNeedIdle),

    # [index]: new width [value]: new height [return value]: 1 if supported  @see AudioEffectX::sizeWindow
    audioMasterSizeWindow = 15
    # [return value]: current sample rate  @see AudioEffectX::updateSampleRate
    audioMasterGetSampleRate = 16
    # [return value]: current block size  @see AudioEffectX::updateBlockSize
    audioMasterGetBlockSize = 17
    # [return value]: input latency in audio samples  @see AudioEffectX::getInputLatency
    audioMasterGetInputLatency = 18
    # [return value]: output latency in audio samples  @see AudioEffectX::getOutputLatency
    audioMasterGetOutputLatency = 19

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetPreviousPlug),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetNextPlug),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterWillReplaceOrAccumulate),

    # [return value]: current process level  @see VstProcessLevels
    audioMasterGetCurrentProcessLevel = 23
    # [return value]: current automation state  @see VstAutomationStates
    audioMasterGetAutomationState = 24

    # [index]: numNewAudioFiles [value]: numAudioFiles [ptr]: #VstAudioFile*  @see AudioEffectX::offlineStart
    audioMasterOfflineStart = 25
    # [index]: bool readSource [value]: #VstOfflineOption* @see VstOfflineOption [ptr]: #VstOfflineTask*
    # @see VstOfflineTask @see AudioEffectX::offlineRead
    audioMasterOfflineRead = 26
    # @see audioMasterOfflineRead @see AudioEffectX::offlineRead
    audioMasterOfflineWrite = 27
    # @see AudioEffectX::offlineGetCurrentPass
    audioMasterOfflineGetCurrentPass = 28
    # @see AudioEffectX::offlineGetCurrentMetaPass
    audioMasterOfflineGetCurrentMetaPass = 29

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetOutputSampleRate),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetOutputSpeakerArrangement),

    # [ptr]: char buffer for vendor string, limited to #kVstMaxVendorStrLen  @see AudioEffectX::getHostVendorString
    audioMasterGetVendorString = 32
    # [ptr]: char buffer for vendor string, limited to #kVstMaxProductStrLen  @see AudioEffectX::getHostProductString
    audioMasterGetProductString = 33
    # [return value]: vendor-specific version  @see AudioEffectX::getHostVendorVersion
    audioMasterGetVendorVersion = 34
    # no definition, vendor specific handling  @see AudioEffectX::hostVendorSpecific
    audioMasterVendorSpecific = 35

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterSetIcon),

    # [ptr]: "can do" string [return value]: 1 for supported
    audioMasterCanDo = 37
    # [return value]: language code  @see VstHostLanguage
    audioMasterGetLanguage = 38

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterOpenWindow),
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterCloseWindow),

    # [return value]: FSSpec on MAC, else char*  @see AudioEffectX::getDirectory
    audioMasterGetDirectory = 41
    # no arguments
    audioMasterUpdateDisplay = 42
    # [index]: parameter index  @see AudioEffectX::beginEdit
    audioMasterBeginEdit = 43
    # [index]: parameter index  @see AudioEffectX::endEdit
    audioMasterEndEdit = 44
    # [ptr]: VstFileSelect* [return value]: 1 if supported  @see AudioEffectX::openFileSelector
    audioMasterOpenFileSelector = 45
    # [ptr]: VstFileSelect*  @see AudioEffectX::closeFileSelector
    audioMasterCloseFileSelector = 46

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterEditFile),

    # \deprecated deprecated in VST 2.4 [ptr]: char[2048] or sizeof (FSSpec) [return value]:
    # 1 if supported  @see AudioEffectX::getChunkFile
    # DECLARE_VST_DEPRECATED (audioMasterGetChunkFile),

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (audioMasterGetInputSpeakerArrangement)


class AEffectOpcodes:
    """
    https://github.com/simlmx/pyvst/blob/ded9ff373f37d1cbe8948ccb053ff4849f45f4cb/pyvst/vstwrap.py#L11
    in SDK it is declared as enum AEffectOpcodes
    with a comment "Basic dispatcher Opcodes (Host to Plug-in)"
    Apparently, a better name would be PluginToHostDispatcherOpcodes, but let's keep it
    like it is to keep it aligned with sdk
    """

    # no arguments  @see AudioEffect::open
    effOpen = 0
    # no arguments  @see AudioEffect::close
    effClose = 1

    # [value]: new program number  @see AudioEffect::setProgram
    effSetProgram = 2
    # [return value]: current program number  @see AudioEffect::getProgram
    effGetProgram = 3
    # [ptr]: char* with new program name, limited to #kVstMaxProgNameLen  @see AudioEffect::setProgramName
    effSetProgramName = 4
    # [ptr]: char buffer for current program name, limited to #kVstMaxProgNameLen  @see AudioEffect::getProgramName
    effGetProgramName = 5

    # [ptr]: char buffer for parameter label, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterLabel
    effGetParamLabel = 6
    # [ptr]: char buffer for parameter display, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterDisplay
    effGetParamDisplay = 7
    # [ptr]: char buffer for parameter name, limited to #kVstMaxParamStrLen  @see AudioEffect::getParameterName
    effGetParamName = 8
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effGetVu)

    # [opt]: new sample rate for audio processing  @see AudioEffect::setSampleRate
    effSetSampleRate = 10
    # [value]: new maximum block size for audio processing  @see AudioEffect::setBlockSize
    effSetBlockSize = 11
    # [value]: 0 means "turn off", 1 means "turn on"  @see AudioEffect::suspend @see AudioEffect::resume
    effMainsChanged = 12

    # [ptr]: #ERect** receiving pointer to editor size  @see ERect @see AEffEditor::getRect
    effEditGetRect = 13
    # [ptr]: system dependent Window pointer, e.g. HWND on Windows  @see AEffEditor::open
    effEditOpen = 14
    # no arguments @see AEffEditor::close
    effEditClose = 15

    # \deprecated deprecated in VST 2.4
    effEditDraw = 16
    # deprecated deprecated in VST 2.4
    effEditMouse = 17
    # deprecated deprecated in VST 2.4
    effEditKey = 18

    # no arguments @see AEffEditor::idle
    effEditIdle = 19

    # deprecated deprecated in VST 2.4
    effEditTop = 20
    # deprecated deprecated in VST 2.4
    effEditSleep = 21
    # deprecated deprecated in VST 2.4
    effIdentify = 22

    # [ptr]: void** for chunk data address [index]: 0 for bank, 1 for program  @see AudioEffect::getChunk
    effGetChunk = 23
    # [ptr]: chunk data [value]: byte size [index]: 0 for bank, 1 for program  @see AudioEffect::setChunk
    effSetChunk = 24

    # [ptr]: #VstEvents*  @see AudioEffectX::processEvents
    effProcessEvents = 25

    # [index]: parameter index [return value]: 1=true, 0=false  @see AudioEffectX::canParameterBeAutomated
    effCanBeAutomated = 26
    # [index]: parameter index [ptr]: parameter string
    # [return value]: true for success  @see AudioEffectX::string2parameter
    effString2Parameter = 27

    # \deprecated deprecated in VST 2.4
    effGetNumProgramCategories = 28

    # [index]: program index [ptr]: buffer for program name, limited to #kVstMaxProgNameLen
    # [return value]: true for success  @see AudioEffectX::getProgramNameIndexed
    effGetProgramNameIndexed = 29

    # \deprecated deprecated in VST 2.4
    effCopyProgram = 30
    # \deprecated deprecated in VST 2.4
    effConnectInput = 31
    # \deprecated deprecated in VST 2.4
    effConnectOutput = 32

    # [index]: input index [ptr]: #VstPinProperties*
    # [return value]: 1 if supported  @see AudioEffectX::getInputProperties
    effGetInputProperties = 33
    # [index]: output index [ptr]: #VstPinProperties*
    # [return value]: 1 if supported  @see AudioEffectX::getOutputProperties
    effGetOutputProperties = 34
    # [return value]: category  @see VstPlugCategory @see AudioEffectX::getPlugCategory
    effGetPlugCategory = 35

    # \deprecated deprecated in VST 2.4
    effGetCurrentPosition = 36
    # \deprecated deprecated in VST 2.4
    effGetDestinationBuffer = 37

    # [ptr]: #VstAudioFile array [value]: count [index]: start flag  @see AudioEffectX::offlineNotify
    effOfflineNotify = 38
    # [ptr]: #VstOfflineTask array [value]: count  @see AudioEffectX::offlinePrepare
    effOfflinePrepare = 39
    # [ptr]: #VstOfflineTask array [value]: count  @see AudioEffectX::offlineRun
    effOfflineRun = 40

    # [ptr]: #VstVariableIo*  @see AudioEffectX::processVariableIo
    effProcessVarIo = 41
    # [value]: input #VstSpeakerArrangement* [ptr]:
    # output #VstSpeakerArrangement*  @see AudioEffectX::setSpeakerArrangement
    effSetSpeakerArrangement = 42

    # \deprecated deprecated in VST 2.4
    effSetBlockSizeAndSampleRate = 43

    # [value]: 1 = bypass, 0 = no bypass  @see AudioEffectX::setBypass
    effSetBypass = 44
    # [ptr]: buffer for effect name limited to #kVstMaxEffectNameLen  @see AudioEffectX::getEffectName
    effGetEffectName = 45

    # \deprecated deprecated in VST 2.4
    effGetErrorText = 46

    # [ptr]: buffer for effect vendor string, limited to #kVstMaxVendorStrLen  @see AudioEffectX::getVendorString
    effGetVendorString = 47
    # [ptr]: buffer for effect vendor string, limited to #kVstMaxProductStrLen  @see AudioEffectX::getProductString
    effGetProductString = 48
    # [return value]: vendor-specific version  @see AudioEffectX::getVendorVersion
    effGetVendorVersion = 49
    # no definition, vendor specific handling  @see AudioEffectX::vendorSpecific
    effVendorSpecific = 50
    # [ptr]: "can do" string [return value]: 0: "don't know" -1: "no" 1: "yes"  @see AudioEffectX::canDo
    effCanDo = 51
    # [return value]: tail size (for example the reverb time of a reverb plug-in); 0 is default (return 1 for 'no tail')
    effGetTailSize = 52

    # \deprecated deprecated in VST 2.4
    effIdle = 53
    # \deprecated deprecated in VST 2.4
    effGetIcon = 54
    # \deprecated deprecated in VST 2.4
    effSetViewPosition = 55

    # [index]: parameter index [ptr]: #VstParameterProperties*
    # [return value]: 1 if supported  @see AudioEffectX::getParameterProperties
    effGetParameterProperties = 56

    # \deprecated deprecated in VST 2.4
    effKeysRequired = 57

    # [return value]: VST version  @see AudioEffectX::getVstVersion
    effGetVstVersion = 58

    # [value]: @see VstProcessPrecision  @see AudioEffectX::setProcessPrecision
    effSetProcessPrecision = 59
    # [return value]: number of used MIDI input channels (1-15)  @see AudioEffectX::getNumMidiInputChannels
    effGetNumMidiInputChannels = 60
    # [return value]: number of used MIDI output channels (1-15)  @see AudioEffectX::getNumMidiOutputChannels
    effGetNumMidiOutputChannels = 61


class VstStringConstants:
    # used for #effGetProgramName, #effSetProgramName, #effGetProgramNameIndexed
    kVstMaxProgNameLen = 24
    # used for #effGetParamLabel, #effGetParamDisplay, #effGetParamName
    kVstMaxParamStrLen = 8
    # used for #effGetVendorString, #audioMasterGetVendorString
    kVstMaxVendorStrLen = 64
    # used for #effGetProductString, #audioMasterGetProductString
    kVstMaxProductStrLen = 64
    # used for #effGetEffectName
    kVstMaxEffectNameLen = 32


class Vst2StringConstants:
    # used for #MidiProgramName, #MidiProgramCategory, #MidiKeyName, #VstSpeakerProperties, #VstPinProperties
    kVstMaxNameLen = 64
    # used for #VstParameterProperties->label, #VstPinProperties->label
    kVstMaxLabelLen = 64
    # used for #VstParameterProperties->shortLabel, #VstPinProperties->shortLabel
    kVstMaxShortLabelLen = 8
    # used for #VstParameterProperties->label
    kVstMaxCategLabelLen = 24
    # used for #VstAudioFile->name
    kVstMaxFileNameLen = 100


class VstEventTypes:
    kVstMidiType = 1  # < MIDI event  @see VstMidiEvent
    # kVstAudioType = 2,		#< \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstVideoType) = 3,		///< \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstParameterType) = 4,	///< \deprecated unused event type
    # DECLARE_VST_DEPRECATED (kVstTriggerType) = 5,	///< \deprecated unused event type
    kVstSysExType = 6  # < MIDI system exclusive  @see VstMidiSysexEvent


class VstAEffectFlags:
    # set if the plug-in provides a custom editor
    effFlagsHasEditor = 1 << 0
    # supports replacing process mode (which should the default mode in VST 2.4)
    effFlagsCanReplacing = 1 << 4
    # program data is handled in formatless chunks
    effFlagsProgramChunks = 1 << 5
    # plug-in is a synth (VSTi), Host may assign mixer channels for its outputs
    effFlagsIsSynth = 1 << 8
    # plug-in does not produce sound when input is all silence
    effFlagsNoSoundInStop = 1 << 9

    # plug-in supports double precision processing
    effFlagsCanDoubleReplacing = 1 << 12

    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsHasClip) = 1 << 1,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsHasVu)   = 1 << 2,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsCanMono) = 1 << 3,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsExtIsAsync)   = 1 << 10,
    # \deprecated deprecated in VST 2.4
    # DECLARE_VST_DEPRECATED (effFlagsExtHasBuffer) = 1 << 11
