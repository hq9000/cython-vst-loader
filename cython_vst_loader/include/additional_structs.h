
struct VstEvents16
{
//-------------------------------------------------------------------------------------------------------
	VstInt32 numEvents;		///< number of Events in array
	VstIntPtr reserved;		///< zero (Reserved for future use)
	VstEvent* events[1024];	///< event pointer array, variable size
//-------------------------------------------------------------------------------------------------------
};


struct VstEvents1024
{
//-------------------------------------------------------------------------------------------------------
	VstInt32 numEvents;		///< number of Events in array
	VstIntPtr reserved;		///< zero (Reserved for future use)
	VstEvent* events[1024];	///< event pointer array, variable size
//-------------------------------------------------------------------------------------------------------
};