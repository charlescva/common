from conans import ConanFile, CMake, tools

'''
 Eigen consists only of header files, hence there is nothing to compile
before you can use it. Moreover, these header files do not depend on your
platform, they are the same for everybody.
'''


class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.4"
    license = "MPL-2"
    url = "http://eigen.tuxfamily.org"
    description = "A C++ template library for linear algebra: matrices, vectors, numerical solvers and related algorithms."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "-DCMAKE_INSTALL_PREFIX": "`pwd`/packges"}
    default_options = "shared=False"
    generators = "cmake"


    def source(self):
        self.run("wget http://bitbucket.org/eigen/eigen/get/3.3.4.tar.gz")
        self.run("tar -xf *.tar.gz")

    def build(self):
        cmake = CMake(self)
	build_dir = "`pwd`/build"
	cmake.configure(source_folder="eigen-eigen-5a0156e40feb", defs=self.options)
	self.run("make -j8 check")

    def package(self):
	self.run("echo Prefix targetted conan package path.")

    def package_info(self):
        self.cpp_info.libs = ["eigen"]
