%global optflags %{optflags} -O3 -fPIC -I%{_includedir}/libunwind

Summary:	Cryptographic filesystem for the cloud
Name:		cryfs
Version:	0.10.3
Release:	2
License:	LGPLv3+
Group:		File tools
Url:		https://www.cryfs.org
Source0:	https://github.com/cryfs/cryfs/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0:		cryfs-0.10.1-static-unmount-library.patch
Patch1:		cryfs-0.10.1-static-cryfs-cli.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	gomp-devel openmp-devel
BuildRequires:	pkgconfig(libunwind)
Requires:	fuse2

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

%build
export LDFLAGS="%{ldflags} -lboost_thread -lboost_program_options -lboost_filesystem -lcryptopp -lboost_chrono -lfuse"

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBoost_USE_STATIC_LIBS=OFF \
    -DBUILD_TESTING=OFF \
    -DCRYFS_UPDATE_CHECKS=OFF \
    -DBUILD_TESTING=OFF \
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
%{_mandir}/man?/cryfs*
