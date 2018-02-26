from conans import ConanFile, tools


class GflagsConan(ConanFile):
    name = "suitesparse"
    version = "5.1.0"
    license = "Multi"
    url = "http://faculty.cse.tamu.edu/davis/suitesparse.html"
    description = "SuiteSparse is a suite of sparse matrix algorithms."
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("wget http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-5.1.0.tar.gz")
        self.run("tar -xf SuiteSparse-5.1.0.tar.gz")

    def build(self):
        tools.replace_in_file("SuiteSparse/SuiteSparse_config/SuiteSparse_config.mk", "lib64", "lib/x86_64-linux-gnu")
        self.run("make -C SuiteSparse")
	
    def package(self):
        self.copy("*.so", dst="lib", src="SuiteSparse/lib")
        self.copy("*", dst="include", src="SuiteSparse/include")

    def package_info(self):
        self.cpp_info.libs = ["suitesparse"]
