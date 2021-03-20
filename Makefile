all: build/vstsdk

build/vstsdk: build/vstsdk.zip
    # fix for linux, linux expects .zip
	unzip build/vstsdk -d build
	mv "build/VST3 SDK" build/vstsdk

build/vstsdk.zip:
    # "inspired" by https://github.com/teragonaudio/MrsWatson/blob/master/vendor/CMakeLists.txt#L379
	mkdir -p build
	curl http://www.steinberg.net/sdk_downloads/vstsdk366_27_06_2016_build_61.zip -o build/vstsdk.zip