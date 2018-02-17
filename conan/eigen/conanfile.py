from conans import ConanFile, CMake, tools


class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.4"
    license = "MPL-2"
    url = "http://eigen.tuxfamily.org"
    description = "A C++ template library for linear algebra: matrices, vectors, numerical solvers and related algorithms."

    def source(self):
        self.run("wget http://bitbucket.org/eigen/eigen/get/3.3.4.tar.gz")
        self.run("tar -xf *.tar.gz")

    def build(self):
        self.run("echo Nothing to do")

    def package(self):
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
