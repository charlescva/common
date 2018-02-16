from conans import ConanFile, CMake, tools


class GflagsConan(ConanFile):
    name = "gflags"
    version = "2.2.1"
    license = "BSD-3-Clause"
    url = "https://github.com/gflags/gflags"
    description = "A C++ library that implements command-line flag processing."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/gflags/gflags.git")
        self.run("cd gflags && git checkout tags/v2.2.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
	#tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
	# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)	
	# conan_basic_setup()''')

    def build(self):
	self.run("export PATH=$PATH:$PWD/../cmake/build/bin")
        cmake = CMake(self)
	
	# Not working?
	#cmake.definitions["CONAN_CMAKE_FIND_ROOT_PATH"] = "../cmake/build"
	
	cmake.verbose = True
        cmake.configure(source_folder="gflags")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["gflags"]
