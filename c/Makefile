all: build/libvst_loader.a

build/libvst_loader.a: build/vst_loader.o
	ar rcs build/libvst_loader.a  build/vst_loader.o	

build/vst_loader.o: vst_loader.c vst_loader.h   
	gcc -c -o $@ $< -I.

vendor/vstsdk: vendor/vstsdk.zip
	unzip vendor/vstsdk.zip -d vendor
	mv "vendor/VST3 SDK" vendor/vstsdk

vendor/vstsdk.zip:
    # "inspired" by https://github.com/teragonaudio/MrsWatson/blob/master/vendor/CMakeLists.txt#L379
	wget http://www.steinberg.net/sdk_downloads/vstsdk366_27_06_2016_build_61.zip -O vendor/vstsdk.zip