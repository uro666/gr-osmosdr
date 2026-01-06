%define major 0
%define devname %mklibname gr-osmosdr -d

Name:		gr-osmosdr
Version:	0.2.6
Release:	1
Source0:	https://github.com/osmocom/gr-osmosdr/archive/v%{version}/%{name}-%{version}.tar.gz
Summary:	Generic gnuradio SDR I/O block
URL:		https://osmocom.org/projects/gr-osmosdr/wiki/GrOsmoSDR
License:	GPL-3.0-or-later
Group:		Communications/Radio
Patch0:		gr-osmosdr-remove-boost-system.patch

BuildSystem:	cmake
BuildRequires:	cmake
BuildRequires:	cmake(funcube)
BuildRequires:	cmake(gnuradio-iqbalance)
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	gnuradio-pmt-devel
BuildRequires:	gnuradio-utils
BuildRequires:	graphviz
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(gmpxx)
BuildRequires:	pkgconfig(gnuradio-blocks)
BuildRequires:	pkgconfig(gnuradio-fft)
BuildRequires:	pkgconfig(gnuradio-filter)
BuildRequires:	pkgconfig(gnuradio-runtime)
BuildRequires:	pkgconfig(gnuradio-uhd)
BuildRequires:	pkgconfig(libairspy)
BuildRequires:	pkgconfig(libairspyhf)
BuildRequires:	pkgconfig(libbladeRF)
BuildRequires:	pkgconfig(libhackrf)
BuildRequires:	pkgconfig(libmirisdr)
BuildRequires:	pkgconfig(libosmodsp)
BuildRequires:	pkgconfig(librtlsdr)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(SoapySDR)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(spdlog)
BuildRequires:	pkgconfig(uhd)
BuildRequires:	pkgconfig(volk) >= 3.2
BuildRequires:	pkgconfig(libxtrxll)
BuildRequires:	python%{pyver}dist(mako)
BuildRequires:	python%{pyver}dist(six)


%description
%{name} - generic gnuradio SDR I/O block

While originally being developed for the OsmoSDR hardware, this block
has become a generic SDR I/O block for a variety of SDR hardware, including:

    FUNcube Dongle / Pro+ through gr-funcube
    RTL2832U based DVB-T dongles through librtlsdr
    RTL-TCP spectrum server (see librtlsdr project)
    MSi2500 based DVB-T dongles through libmirisdr
    SDRplay RSP through SDRplay API library
    gnuradio .cfile input through libgnuradio-blocks
    RFSPACE SDR-IQ, SDR-IP, NetSDR (incl. X2 option), Cloud-IQ, and CloudSDR
    AirSpy Wideband Receiver through libairspy
    CCCamp 2015 rad1o Badge through libhackrf
    Great Scott Gadgets HackRF through libhackrf
    Nuand LLC bladeRF through libbladeRF library
    Ettus USRP Devices through Ettus UHD library
    Fairwaves UmTRX through Fairwaves' module for UHD
    Fairwaves XTRX through libxtrx
    Red Pitaya SDR transceiver http://bazaar.redpitaya.com
    FreeSRP through libfreesrp

By using the gr-osmosdr block you can take advantage of a common software API
in your application(s) independent of the underlying radio hardware.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Libraries/Other
Requires:	%{name} = %{EVRD}
Suggests:	%{name}-doc = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

OsmoSDR Gnuradio Source supports the OsmoSDR hardware, but it
also offers a wrapper functionality for FunCube Dongle,
Ettus UHD and rtl-sdr radios.

%package -n python-%{name}
Summary:	Python bindings for FCD and FCDpro Plus
Group:		Development/Libraries/Python
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
Python Bindings for gr-osmosdr.
OsmoSDR Gnuradio Source supports the OsmoSDR hardware, but it
also offers a wrapper functionality for FunCube Dongle,
Ettus UHD and rtl-sdr radios.

%package doc
Summary:	Documentation for gr-funcube
Group:		Documentation/Other
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description doc
Documentation for %{name} module for GNU Radio.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags} -Wno-dev"
%cmake \
	-DGR_TEST_LIBRARY_DIRS=../lib \
	-DGR_PKG_DOC_DIR=%{_docdir}/%{name} \
	-DENABLE_DOXYGEN=ON \
	-DENABLE_PYTHON=ON \
	-DENABLE_FREESRP=OFF \
	-DENABLE_XTRX=OFF \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%check
pushd build
%ninja_test
popd

%files
%exclude %{_docdir}/%{name}/html
%exclude %{_docdir}/%{name}/xml
%license COPYING
%doc README.md
%{_bindir}/osmocom_fft
%{_bindir}/osmocom_siggen_nogui
%{_datadir}/gnuradio/grc/blocks/*.yml
%{_libdir}/libgnuradio-osmosdr.so.%{major}*

%files -n %{devname}
%{_includedir}/osmosdr
%{_libdir}/libgnuradio-osmosdr.so
%{_libdir}/cmake/osmosdr

%files -n python-%{name}
%{python_sitearch}/osmosdr

%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/html
%{_docdir}/%{name}/xml

