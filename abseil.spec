# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: abseil
Epoch: 100
Version: 20230802.2
Release: 1%{?dist}
Summary: Abseil Common Libraries (C++)
License: Apache-2.0
URL: https://github.com/abseil/abseil-cpp/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
%endif
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: gcc-c++

%description
Abseil is an open-source collection of C++ library code designed to
augment the C++ standard library. The Abseil library code is collected
from Google's C++ codebase and has been extensively tested and used in
production. In some cases, Abseil provides pieces missing from the C++
standard; in others, Abseil provides alternatives to the standard for
special needs.

%package -n abseil-cpp
Summary: Abseil Common Libraries (C++)

%description -n abseil-cpp
Abseil is an open-source collection of C++ library code designed to
augment the C++ standard library. The Abseil library code is collected
from Google's C++ codebase and has been extensively tested and used in
production. In some cases, Abseil provides pieces missing from the C++
standard; in others, Abseil provides alternatives to the standard for
special needs.

%package -n abseil-cpp-devel
Summary: Abseil Common Libraries (C++) (development files)
Requires: abseil-cpp = %{epoch}:%{version}-%{release}

%description -n abseil-cpp-devel
This package contains header files and other data necessary for
developing with Abseil.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-11/enable
%endif
mkdir -p build
pushd build && \
    cmake \
        .. \
        -DABSL_BUILD_TESTING=OFF \
        -DABSL_ENABLE_INSTALL=ON \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr && \
popd
pushd build && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
popd

%install
pushd build && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd
fdupes -qnrps %{buildroot}

%post -n abseil-cpp -p /sbin/ldconfig
%postun -n abseil-cpp -p /sbin/ldconfig

%files -n abseil-cpp
%license LICENSE
%{_libdir}/*.so.*

%files -n abseil-cpp-devel
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/absl
%{_includedir}/absl
%{_libdir}/*.so
%{_libdir}/cmake/absl/*.cmake
%{_libdir}/pkgconfig/*.pc

%changelog
