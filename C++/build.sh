if [ ! -d "3rdParty" ]; then
	unzip 3rdParty.zip
fi
if [ ! -d "build" ]; then
	mkdir build
fi
cd build
cmake -A x64 -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release --target install
cd ..