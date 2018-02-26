from conans import ConanFile, CMake, tools


class OpencvConan(ConanFile):
    name = "opencv"
    version = "2.4.13"
    license = "Multi"
    url = "http://opencv.org"
    description = "Open source computer vision libs."
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("wget https://github.com/opencv/opencv/archive/2.4.13.5.zip")
        self.run("unzip 2.4.13.5.zip")

    def build(self):
        cmake = CMake(self)
        #cmake.definitions["CONAN_CMAKE_FIND_ROOT_PATH"] = "../cmake/build"
        cmake.verbose = True
        cmake.configure(source_folder="opencv-2.4.13.5")
        cmake.build()

	
    def package(self):
        self.run("ls lib")

    def package_info(self):
        self.cpp_info.libs = ["ceres"]
