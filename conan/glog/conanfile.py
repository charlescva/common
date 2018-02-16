from conans import ConanFile, tools, AutoToolsBuildEnvironment
import platform

class GlogConan(ConanFile):
    name = "glog"
    version = "0.3.5"
    license = "BSD"
    url = "https://github.com/google/glog"
    description = "a C++ implementation of the Google logging module."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
#    generators = "qmake"

   

    def source(self):
        self.run("git clone https://github.com/google/glog")
        self.run("cd glog && git checkout tags/v0.3.5")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("glog/configure", "1.14", "1.15")
    
    # The libraries libglog depends on.
    #COMMON_LIBS = $(PTHREAD_LIBS) $(GFLAGS_LIBS) $(UNWIND_LIBS)
    def build(self):
        glog_build = AutoToolsBuildEnvironment(self)
        #glog_build.libs.append("pthread")

        with tools.environment_append(glog_build.vars):
            self.run("autoreconf -fi ./glog")
            self.run("./glog/configure --prefix=`pwd`/build")
            self.run("make -j2 && make install")

    def package(self):
        # headers
        self.copy("*.h", dst="include", src="build/include", keep_path=True)
        # libs
        libdir = "build/lib"
        self.copy("*.so", dst="lib", src=libdir, keep_path=False)
        self.copy("*.a", dst="lib", src=libdir, keep_path=False)
    
    def package_info(self):
        self.cpp_info.libs = ["glog"]
