#
# spec file for package python-numpy for Mer, based on OpenSuse version
#

%define modname numpy
Name:           python-%{modname}
Version:        1.9.3
Release:        0
URL:            http://sourceforge.net/projects/numpy
Summary:        NumPy array processing for numbers, strings, records and objects
License:        BSD-3-Clause
Group:          Development/Libraries/Python
Packager:       Roberto Colistete Jr. <matplotlib-devel@lists.sourceforge.net>
Source:         %{name}-%{version}.tar.gz
# Source:         http://sourceforge.net/projects/numpy/files/NumPy/%{version}/%{modname}-%{version}.tar.gz
# PATCH-FIX-OPENSUSE numpy-buildfix.patch -- openSUSE-specific build fixes
Patch0:         numpy-buildfix.patch
# PATCH-FIX-OPENSUSE numpy-1.9.1-remove-__declspec.patch -- fix for spurious compiler warnings that cause build failure
Patch1:         numpy-1.9.1-remove-__declspec.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildRequires:  blas-devel
#BuildRequires:  lapack-devel
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-Cython
Requires:       python >= %{py_ver}
Provides:       numpy = %{version}
BuildRequires:  fdupes
#BuildRequires:  gcc-fortran

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type which also makes NumPy suitable for
interfacing with general-purpose data-base applications.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.

%package devel
Summary:        Development files for %{modname} applications
Group:          Development/Libraries/Python
Requires:       %{name} = %{version}
#Requires:       blas-devel
#Requires:       lapack-devel
Requires:       python-devel
#Requires:       gcc-gfortran

%description devel
This package contains files for developing applications using %{modname}.

%package f2py
Summary:        Fortran to py for numpy
Group:          Development/Libraries/Python
Requires:       %{name} = %{version}
Requires:       python-devel
Provides:       f2py

%description f2py
This package includes a version of f2py that works properly with NumPy.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p1
%patch1 -p1
# Fix non-executable scripts
sed -i "1d" numpy/{compat/setup,distutils/{conv_template,cpuinfo,exec_command,from_template,setup,system_info},f2py/{__init__,auxfuncs,capi_maps,cb_rules,cfuncs,common_rules,crackfortran,diagnose,f2py2e,f90mod_rules,func2subr,rules,setup,use_rules},ma/setup,matrixlib/setup,setup,testing/{print_coercion_tables,setup}}.py

%build
CFLAGS="%{optflags} -fno-strict-aliasing" python setup.py build

%install
python setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
rm -rf %{buildroot}%{python_sitearch}/%{modname}/{,core,distutils,f2py,fft,lib,linalg,ma,matrixlib,oldnumeric,polynomial,random,testing}/tests 
# Don't package testsuite
%fdupes -s %{buildroot}%{_prefix}

%files
%defattr(-,root,root)
%doc *.txt
#%{_bindir}/f2py
%{python_sitearch}/%{modname}/
%{python_sitearch}/*.egg-info
%exclude %{python_sitearch}/%{modname}/*/*/*.c
%exclude %{python_sitearch}/%{modname}/*/*.h
%exclude %{python_sitearch}/%{modname}/*/*/*.h
%exclude %{python_sitearch}/%{modname}/*/*/*/*.h
%exclude %{python_sitearch}/%{modname}/core/lib/libnpymath.a

%files devel
%defattr(-,root,root)
%{python_sitearch}/%{modname}/*/*/*.c
%{python_sitearch}/%{modname}/*/*.h
%{python_sitearch}/%{modname}/*/*/*.h
%{python_sitearch}/%{modname}/*/*/*/*.h
%{python_sitearch}/%{modname}/core/lib/libnpymath.a

%files f2py
%defattr(-,root,root,-)
%{_bindir}/f2py
%{python_sitearch}/%{modname}/f2py