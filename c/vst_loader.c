#include "aeffectx.h"
#include "dlfcn.h"
#include "stdio.h"
#include <stdlib.h>

#define GENERIC_ERROR_CODE 1

void error(char *message, int exitCode)
{
    printf("%s", message);
    exit(exitCode);
}

typedef VstIntPtr (*audioMasterCallback)(AEffect *effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void *ptr, float opt);
typedef VstIntPtr (*AEffectDispatcherProc)(AEffect *effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void *ptr, float opt);
// Plugin's entry point
typedef AEffect *(*vstPluginFuncPtr)(audioMasterCallback host);
// Plugin's dispatcher function
typedef VstIntPtr (*dispatcherFuncPtr)(AEffect *effect, VstInt32 opCode,
                                       VstInt32 index, VstInt32 value, void *ptr, float opt);
// Plugin's getParameter() method
typedef float (*getParameterFuncPtr)(AEffect *effect, VstInt32 index);
// Plugin's setParameter() method
typedef void (*setParameterFuncPtr)(AEffect *effect, VstInt32 index, float value);

// Plugin's process() method
typedef void (*processFuncPtr)(AEffect *effect, float **inputs,
                               float **outputs, VstInt32 sampleFrames);

AEffect *loadPlugin(audioMasterCallback hostCallback)
{
    AEffect *plugin = NULL;
    char *vstPath = "c:\\wherever\\the\\plugin\\is\\located.vst";

    void *handle = dlopen(vstPath, RTLD_LAZY);
    if (!handle)
    {
        error("unable to obtain library handle", GENERIC_ERROR_CODE);
    }

    vstPluginFuncPtr entryFunction = dlsym(handle, "VSTPluginMain");
    plugin = entryFunction(hostCallback);

    if (plugin->magic != kEffectMagic)
    {
        error("magic not found", 1);
    }

    return plugin;
}