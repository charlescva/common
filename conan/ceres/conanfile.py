from conans import ConanFile, CMake, tools


class CeresConan(ConanFile):
    name = "ceres"
    version = "1.13"
    license = "New BSD"
    url = "http://ceres-solver.org"
    description = "an open source C++ library for modeling and solving large, complicated optimization problems."
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("wget http://ceres-solver.org/ceres-solver-1.13.0.tar.gz")
        self.run("tar -xf ceres-solver-1.13.0.tar.gz")

    def build(self):
        cmake = CMake(self)
        #cmake.definitions["CONAN_CMAKE_FIND_ROOT_PATH"] = "../cmake/build"
        cmake.verbose = True
        cmake.configure(source_folder="ceres-solver-1.13.0")
        cmake.build()

	
    def package(self):
        self.run("ls lib")

    def package_info(self):
        self.cpp_info.libs = ["ceres"]
