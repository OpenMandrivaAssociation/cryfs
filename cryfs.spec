%global optflags %{optflags} -O3 -fPIC -I%{_includedir}/libunwind

Summary:	Cryptographic filesystem for the cloud
Name:		cryfs
Version:	1.0.1
Release:	3
License:	LGPLv3+
Group:		File tools
Url:		https://www.cryfs.org
Source0:	https://github.com/cryfs/cryfs/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(spdlog)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	gomp-devel
BuildRequires:	openmp-devel
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	range-v3-devel
Requires:	fuse2

%patchlist
cryfs-0.10.1-static-unmount-library.patch
cryfs-0.10.1-static-cryfs-cli.patch
cryfs-0.10.3-libstdc++-11.2.patch
cryfs-0.11.4-boost-1.88.patch
cryfs-1.0.1-system-cryptopp.patch

%description
CryFS provides a FUSE-based mount that encrypts file contents, file
sizes, metadata and directory structure. It uses encrypted same-size
blocks to store both the files themselves and the blocks' relations
to one another. These blocks are stored as individual files in the
base directory, which can then be synchronized to remote storage
(using an external tool).

%prep
%autosetup -c -p1
# Use system cryptopp
rm -rf vendor/cryptopp
find . -name "*.cpp" -o -name "*.h" |xargs sed -i -e 's,vendor_cryptopp,cryptopp,g'
sed -i -e '/cryptopp/d' vendor/CMakeLists.txt

# try fix build with boost 1.89, Patch fix is available but it not apply on current rel. So for now lets try use faster way.
sed -i -e 's/\<system\>//' -e 's/  */ /g' cmake-utils/Dependencies.cmake

%build
export LDFLAGS="%{build_ldflags} -lboost_thread -lboost_program_options -lboost_filesystem -lcryptopp -lboost_chrono -lfuse -lcurl"

%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DBoost_USE_STATIC_LIBS=OFF \
	-DBUILD_TESTING=OFF \
	-DCRYFS_UPDATE_CHECKS=OFF \
	-DBUILD_TESTING=ON \
        -DDEPENDENCY_CONFIG="../cmake-utils/DependenciesFromLocalSystem.cmake" \
%ifarch %{x86_64}
 	-DCMAKE_CXX_FLAGS="-msse4.1" \
%endif
    -G Ninja

%ninja

%install
%ninja_install -C build

%files
%doc README.md ChangeLog.txt
%license LICENSE.txt
%{_bindir}/cryfs*
%doc %{_mandir}/man?/cryfs*
