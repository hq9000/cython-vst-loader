all: build/vstsdk

build/vstsdk: build/vstsdk.zip
	unzip build/vstsdk.zip -d build
	mv "build/VST3 SDK" build/vstsdk

build/vstsdk.zip:
    # "inspired" by https://github.com/teragonaudio/MrsWatson/blob/master/vendor/CMakeLists.txt#L379
	mkdir -p build
	curl https://www.steinberg.net/sdk_downloads/vstsdk366_27_06_2016_build_61.zip -o build/vstsdk.zip