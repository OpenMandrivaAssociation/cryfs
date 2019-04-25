# (tpg) disable LTO 2019-04-25
#/tmp/lto-llvm-f8f7f6.o:ld-temp.o:function cryfs_unmount::program_options::ProgramOptions::ProgramOptions(boost::filesystem::path): error: undefined reference to 'boost::filesystem::detail::current_path(boost::system::error_code*)'
#/tmp/lto-llvm-f8f7f6.o:ld-temp.o:function cryfs_unmount::program_options::ProgramOptions::ProgramOptions(boost::filesystem::path): error: undefined reference to 'boost::filesystem::absolute(boost::filesystem::path const&, boost::filesystem::path const&)'
%define _disable_lto 1
%global optflags %{optflags} -O3 -fPIC

Summary:	Cryptographic filesystem for the cloud
Name:		cryfs
Version:	0.10.1
Release:	1
License:	LGPLv3+
Group:		File tools
Url:		https://www.cryfs.org
Source0:	https://github.com/cryfs/cryfs/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0:		cryfs-0.10.1-add-missing-boost-linkage.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(cryptopp)
Requires:	fuse2

%description
CryFS provides a FUSE-based mount that encrypts file contents, file
sizes, metadata and directory structure. It uses encrypted same-size
blocks to store both the files themselves and the blocks' relations
to one another. These blocks are stored as individual files in the
base directory, which can then be synchronized to remote storage
(using an external tool).

%prep
%autosetup -c -p0

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBoost_USE_STATIC_LIBS=OFF \
    -DBUILD_TESTING=OFF \
    -DCRYFS_UPDATE_CHECKS=OFF \
    -G Ninja

%ninja

%install
%ninja_install -C build

%files
%doc README.md ChangeLog.txt
%license LICENSE
%{_bindir}/cryfs*
%{_mandir}/man?/cryfs*
