from conans import ConanFile, AutoToolsBuildEnvironment, tools


class CmakeConan(ConanFile):
    name = "cmake"
    version = "3.10.2"
    license = "BSD-3-Clause"
    url = "https://cmake.org"
    description = "Make is an open-source, cross-platform family of tools designed to build, test and package software."

    def source(self):
        self.run("wget https://cmake.org/files/v3.10/cmake-3.10.2.tar.gz")
        self.run("tar -xf cmake-3.10.2.tar.gz")

    def build(self):
      env_build = AutoToolsBuildEnvironment(self)
      env_build.configure(configure_dir="cmake-3.10.2",args=[ '--prefix=`pwd`/build' ])
      env_build.make()

    def package(self):
        self.copy("*.h", dst="include", src="cmake-3.10.2/include")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cmake"]
