%global optflags %{optflags} -O3 -fPIC

Summary:	Cryptographic filesystem for the cloud
Name:		cryfs
Version:	0.10.1
Release:	3
License:	LGPLv3+
Group:		File tools
Url:		https://www.cryfs.org
Source0:	https://github.com/cryfs/cryfs/releases/download/%{version}/%{name}-%{version}.tar.xz
Patch0:		cryfs-0.10.1-static-unmount-library.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	gomp-devel openmp-devel
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

%build
%ifarch znver1
# with clang 8.0.1-0.359956:
# ld: ../lib/Linker/IRMover.cpp:1006: llvm::Error (anonymous namespace)::IRLinker::linkFunctionBody(llvm::Function &, llvm::Function &): Assertion `Dst.isDeclaration() && !Src.isDeclaration()' failed.
# clang-8: error: unable to execute command: Aborted (core dumped)
export CC=gcc
export CXX=g++
%endif
export LDFLAGS="-L%{_libdir} -lboost_thread -lboost_program_options -lboost_filesystem -lcryptopp -lboost_chrono -lfuse"

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBoost_USE_STATIC_LIBS=OFF \
    -DBUILD_TESTING=OFF \
    -DCRYFS_UPDATE_CHECKS=OFF \
    -DBUILD_TESTING=OFF \
    -G Ninja

%ninja

%install
%ninja_install -C build

%files
%doc README.md ChangeLog.txt
%license LICENSE.txt
%{_bindir}/cryfs*
%{_mandir}/man?/cryfs*
