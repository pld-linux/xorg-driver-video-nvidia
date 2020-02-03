# TODO
# - should -libs Require main package?
# - drop binary-only nvidia-settings from here, and use nvidia-settings.spec for it?
# - kernel-drm is required on never kernels. driver for kernel-longterm not requires drm
#
# Conditional build:
%bcond_with	system_libglvnd	# do not use system libglvnd
%bcond_without	kernel		# without kernel packages
%bcond_without	userspace	# don't build userspace programs
%bcond_with	settings	# package nvidia-settings here (GPL version of same packaged from nvidia-settings.spec)
%bcond_with	verbose		# verbose build (V=1)

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		no_install_post_check_so 1

%define		rel	1
%define		pname	xorg-driver-video-nvidia
Summary:	Linux Drivers for nVidia GeForce/Quadro Chips
Summary(hu.UTF-8):	Linux meghajtók nVidia GeForce/Quadro chipekhez
Summary(pl.UTF-8):	Sterowniki do kart graficznych nVidia GeForce/Quadro
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
# when updating version here, keep nvidia-settings.spec in sync as well
Version:	440.59
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
Epoch:		1
License:	nVidia Binary
Group:		X11
Source0:	http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
# Source0-md5:	596a63329c35d24cd787dc4e7e72d2d1
Source2:	%{pname}-xinitrc.sh
Source3:	gl.pc.in
Source4:	10-nvidia.conf
Source5:	10-nvidia-modules.conf
Patch0:		X11-driver-nvidia-desktop.patch
URL:		http://www.nvidia.com/object/unix.html
BuildRequires:	rpmbuild(macros) >= 1.701
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.32}}
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 24.1
Requires:	xorg-xserver-server(videodrv-abi) >= 4.0
Provides:	ocl-icd(nvidia)
Provides:	ocl-icd-driver
Provides:	vulkan(icd) = 1.1.119
Provides:	xorg-driver-video
Provides:	xorg-xserver-module(glx)
Obsoletes:	XFree86-driver-nvidia
Obsoletes:	XFree86-nvidia
Conflicts:	XFree86-OpenGL-devel <= 4.2.0-3
ExclusiveArch:	%{?with_userspace:%{ix86}} %{x8664}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libnvcuvid.so
# libnvidia-encode.so.*.* links with libnvcuvid.so instead of libnvcuvid.so.1
%define		_noautoreq	libnvcuvid.so

%description
This driver set adds improved 2D functionality to the Xorg X server as
well as high performance OpenGL acceleration, AGP support, support for
most flat panels, and 2D multiple monitor support. Supported hardware:
modern NVIDIA GeForce (from GeForce2 MX) and Quadro (Quadro4 and up)
based graphics accelerators.

The older graphics chips are unsupported:
- NV1 and RIVA 128/128ZX chips are supported in the base Xorg install
  (nv driver)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 are suported by -legacy
  drivers.

%description -l hu.UTF-8
Ez a meghajtó kibővíti az Xorg X szerver 2D működését OpenGL
gyorsítással, AGP támogatással és támogatja a több monitort.
Támogatott hardverek: modern NVIDIA GeForce (GeForce2 MX-től) és
Quadro (Quadro4 és újabbak) alapú grafikai gyorsítók.

A régekbbi grafikus chipek nem támogatottak:
- NV1 és RIVA 128/128ZX chipek az alap Xorg telepítéssel (nv meghajtó)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 a -legacy driverekkel
  támogatottak.

%description -l pl.UTF-8
Usprawnione sterowniki dla kart graficznych nVidia do serwera Xorg,
dające wysokowydajną akcelerację OpenGL, obsługę AGP i wielu monitorów
2D. Obsługują w miarę nowe karty NVIDIA GeForce (od wersji GeForce2
MX) oraz Quadro (od wersji Quadro4).

Starsze układy graficzne nie są obsługiwane przez ten pakiet:
- NV1 i RIVA 128/128ZX są obsługiwane przez sterownik nv z Xorg
- TNT/TNT2/GeForce 256/GeForce 2 Ultra/Quadro 2 są obsługiwane przez
  sterowniki -legacy

%package libs
Summary:	OpenGL (GL and GLX) Nvidia libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) Nvidia
Group:		X11/Development/Libraries
Requires(post,postun):	/sbin/ldconfig
%if %{with system_libglvnd}
Requires:	libglvnd
Requires:	libglvnd-libGL
Requires:	libglvnd-libGLES
%endif
Requires:	libvdpau >= 0.3
Provides:	OpenGL = 3.3
Provides:	OpenGL-GLX = 1.4
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libs
NVIDIA OpenGL (GL and GLX only) implementation libraries.

%description libs -l pl.UTF-8
Implementacja OpenGL (tylko GL i GLX) firmy NVIDIA.

%package devel
Summary:	OpenGL (GL and GLX) header files
Summary(hu.UTF-8):	OpenGL (GL és GLX) fejléc fájlok
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGL (GL i GLX)
Group:		X11/Development/Libraries
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 2.1
Obsoletes:	X11-OpenGL-devel-base
Obsoletes:	XFree86-OpenGL-devel-base
Obsoletes:	XFree86-driver-nvidia-devel
Conflicts:	XFree86-OpenGL-devel < 4.3.99.902-0.3

%description devel
OpenGL header files (GL and GLX only) for NVIDIA OpenGL
implementation.

%description devel -l hu.UTF-8
OpenGL fejléc fájlok (csak GL és GLX) NVIDIA OpenGL implementációhoz.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenGL (tylko GL i GLX) dla implementacji OpenGL
firmy NVIDIA.

%package doc
Summary:	Documentation for NVIDIA Graphics Driver
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
NVIDIA Accelerated Linux Graphics Driver README and Installation
Guide.

%package progs
Summary:	Tools for advanced control of nVidia graphic cards
Summary(hu.UTF-8):	Eszközök az nVidia grafikus kártyák beállításához
Summary(pl.UTF-8):	Narzędzia do zarządzania kartami graficznymi nVidia
Group:		Applications/System
Requires:	%{pname} = %{epoch}:%{version}
Suggests:	pkgconfig
Obsoletes:	XFree86-driver-nvidia-progs

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l hu.UTF-8
Eszközök az nVidia grafikus kártyák beállításához.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%ifarch %{x8664}
%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-nvidia\
Summary:	nVidia kernel module for nVidia Architecture support\
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung\
Summary(hu.UTF-8):	nVidia Architektúra támogatás Linux kernelhez.\
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires:	dev >= 2.7.7-10\
%requires_releq_kernel\
%if %{_kernel_version_code} >= %{_kernel_version_magic 3 10 0}\
Requires:	%{releq_kernel -n drm}\
%endif\
Requires(postun):	%releq_kernel\
Requires:	%{pname} = %{epoch}:%{version}\
Provides:	X11-driver-nvidia(kernel)\
Obsoletes:	XFree86-nvidia-kernel\
\
%description -n kernel%{_alt_kernel}-video-nvidia\
nVidia Architecture support for Linux kernel.\
\
%description -n kernel%{_alt_kernel}-video-nvidia -l de.UTF-8\
Die nVidia-Architektur-Unterstützung für den Linux-Kern.\
\
%description -n kernel%{_alt_kernel}-video-nvidia -l hu.UTF-8\
nVidia Architektúra támogatás Linux kernelhez.\
\
%description -n kernel%{_alt_kernel}-video-nvidia -l pl.UTF-8\
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez\
sterownik nVidii dla Xorg/XFree86.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-video-nvidia\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
%endif\
\
%post	-n kernel%{_alt_kernel}-video-nvidia\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-video-nvidia\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
cd kernel\
#cat >> Makefile <<'EOF'\
#\
#$(obj)/nv-kernel.o: $(src)/nv-kernel.o.bin\
#	cp $< $@\
#EOF\
#mv nv-kernel.o{,.bin}\
#build_kernel_modules -m nvidia\
%{__make} SYSSRC=%{_kernelsrcdir} clean\
%{__make} SYSSRC=%{_kernelsrcdir} IGNORE_CC_MISMATCH=1 NV_VERBOSE=1 CC=%{__cc} module\
cd ..\
%install_kernel_modules -D installed -m kernel/nvidia,kernel/nvidia-drm,kernel/nvidia-modeset -d misc\
%install_kernel_modules -D installed -m kernel/nvidia-uvm -d misc\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}
%endif

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86_64-%{version}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{version}
%patch0 -p1
echo 'EXTRA_CFLAGS += -Wno-pointer-arith -Wno-sign-compare -Wno-unused' >> kernel/Makefile.kbuild

%build
%ifarch %{x8664}
%{?with_kernel:%{expand:%build_kernel_packages}}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/{nvidia,xorg/modules/{drivers,extensions/nvidia}} \
	$RPM_BUILD_ROOT{%{_libdir}/vdpau,%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/etc/X11/xinit/xinitrc.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{OpenCL/vendors,ld.so.conf.d,X11/xorg.conf.d} \
	$RPM_BUILD_ROOT%{_datadir}/{glvnd/egl_vendor.d,nvidia,vulkan/icd.d}

%ifarch %{x8664}
%if %{with settings}
install -p nvidia-settings $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-settings.1* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p nvidia-settings.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh
%endif

install -p nvidia-{smi,xconfig,bug-report.sh} $RPM_BUILD_ROOT%{_bindir}
install -p nvidia-cuda-mps-{control,server} $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-{smi,xconfig,cuda-mps-control}.1* $RPM_BUILD_ROOT%{_mandir}/man1
install -p nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
sed -i -e 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-modules.conf
install -p nvidia-drm-outputclass.conf $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf

install -p nvidia-application-profiles-%{version}-key-documentation $RPM_BUILD_ROOT%{_datadir}/nvidia
install -p nvidia-application-profiles-%{version}-rc $RPM_BUILD_ROOT%{_datadir}/nvidia
%endif

%ifarch %{ix86}
%define	srcdir	32
%else
%define	srcdir	.
%endif

for f in \
%if %{without system_libglvnd}
	%{srcdir}/libGL.so.1.7.0				\
	%{srcdir}/libGLX.so.0				\
	%{srcdir}/libOpenGL.so.0				\
	%{srcdir}/libGLdispatch.so.0			\
	%{srcdir}/libGLESv1_CM.so.1.2.0			\
	%{srcdir}/libGLESv2.so.2.1.0			\
	%{srcdir}/libEGL.so.1.1.0				\
%endif
	%{srcdir}/libGLX_nvidia.so.%{version}		\
	%{srcdir}/libEGL_nvidia.so.%{version}		\
	%{srcdir}/libGLESv1_CM_nvidia.so.%{version}	\
	%{srcdir}/libGLESv2_nvidia.so.%{version}		\
%ifarch %{x8664}
	%{srcdir}/libnvidia-egl-wayland.so.1.1.4		\
	%{srcdir}/libnvidia-eglcore.so.%{version}		\
%endif
	%{srcdir}/libcuda.so.%{version}			\
	%{srcdir}/libnvcuvid.so.%{version}		\
%ifarch %{x8664}
	%{srcdir}/libnvidia-cbl.so.%{version}	\
	%{srcdir}/libnvidia-cfg.so.%{version}		\
	%{srcdir}/libnvidia-rtcore.so.%{version}	\
	%{srcdir}/libnvoptix.so.%{version}	\
%endif
	%{srcdir}/libnvidia-compiler.so.%{version}	\
	%{srcdir}/libnvidia-encode.so.%{version}		\
	%{srcdir}/libnvidia-fatbinaryloader.so.%{version}	\
	%{srcdir}/libnvidia-fbc.so.%{version}	\
	%{srcdir}/libnvidia-glcore.so.%{version}		\
	%{srcdir}/libnvidia-glsi.so.%{version}		\
	%{srcdir}/libnvidia-glvkspirv.so.%{version}		\
	%{srcdir}/libnvidia-ifr.so.%{version}		\
	%{srcdir}/libnvidia-ml.so.%{version}		\
	%{srcdir}/libnvidia-opencl.so.%{version}		\
	%{srcdir}/libnvidia-ptxjitcompiler.so.%{version}	\
	%{srcdir}/libnvidia-tls.so.%{version}		\
; do
	install -p $f $RPM_BUILD_ROOT%{_libdir}/nvidia
done

install -p %{srcdir}/libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau

%ifarch %{x8664}
install -p libglxserver_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
ln -s libglxserver_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglxserver_nvidia.so
install -p nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so.%{version}
ln -s nvidia_drv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%endif

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/nvidia
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia

ln -sf libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

%ifarch %{x8664}
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
%else
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

# OpenGL ABI for Linux compatibility
%if %{without system_libglvnd}
ln -sf libGL.so.1.7.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so
ln -sf libGLX.so.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX.so
ln -sf libOpenGL.so.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libOpenGL.so
ln -sf libGLESv1_CM.so.1.2.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM.so.1
ln -sf libGLESv1_CM.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM.so
ln -sf libGLESv2.so.2.1.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2.so.2
ln -sf libGLESv2.so.2 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2.so
ln -sf libEGL.so.1.1.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL.so.1
ln -sf libEGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL.so
%endif
ln -sf libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX_nvidia.so.0
ln -sf libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX_indirect.so.0
ln -sf libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL_nvidia.so.0
ln -sf libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.1
ln -sf libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2_nvidia.so.2

%ifarch %{x8664}
install -p 10_nvidia.json $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d
%endif
ln -sf libcuda.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libcuda.so
ln -sf libnvcuvid.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libnvcuvid.so

%ifarch %{x8664}
install -p nvidia_icd.json $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d
%endif
%endif

%ifarch %{x8664}
%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e '
	s|@@prefix@@|%{_prefix}|g;
	s|@@libdir@@|%{_libdir}|g;
	s|@@version@@|%{version}|g' < %{SOURCE3} \
	> $RPM_BUILD_ROOT%{_pkgconfigdir}/gl.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << 'EOF'
NOTE: You must also install kernel module for this driver to work
  kernel%{_alt_kernel}-video-nvidia-%{version}

EOF

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%ifarch %{x8664}
%files
%defattr(644,root,root,755)
%doc LICENSE NVIDIA_Changelog README.txt
%dir %{_libdir}/xorg/modules/extensions/nvidia
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglxserver_nvidia.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglxserver_nvidia.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-modules.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
%endif

%files libs
%defattr(644,root,root,755)
%ifarch %{x8664}
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%endif}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/nvidia*.conf
%dir %{_libdir}/nvidia
%if %{without system_libglvnd}
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.1.7.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLX.so.0
%attr(755,root,root) %{_libdir}/nvidia/libOpenGL.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLdispatch.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM.so.1.2.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv1_CM.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2.so.2.1.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv2.so.2
%attr(755,root,root) %{_libdir}/nvidia/libEGL.so.1.1.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libEGL.so.1
%endif
%attr(755,root,root) %ghost %{_libdir}/nvidia/libEGL_nvidia.so.0
%attr(755,root,root) %{_libdir}/nvidia/libEGL_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv1_CM_nvidia.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv2_nvidia.so.2
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLX_indirect.so.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLX_nvidia.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLX_nvidia.so.*.*
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-egl-wayland.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-egl-wayland.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-eglcore.so.*.*
%endif
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libcuda.so.1
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvcuvid.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cbl.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cfg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-cfg.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-rtcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvoptix.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvoptix.so.1
%endif
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-compiler.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-encode.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-encode.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-fatbinaryloader.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-fbc.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-fbc.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glsi.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glvkspirv.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-ifr.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ifr.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ml.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-ml.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-opencl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-opencl.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-tls.so.*.*
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/vdpau/libvdpau_nvidia.so.1
%ifarch %{x8664}
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%{_datadir}/vulkan/icd.d/nvidia_icd.json
%endif

%files devel
%defattr(644,root,root,755)
%if %{without system_libglvnd}
%attr(755,root,root) %{_libdir}/nvidia/libGL.so
%attr(755,root,root) %{_libdir}/nvidia/libGLX.so
%attr(755,root,root) %{_libdir}/nvidia/libOpenGL.so
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM.so
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2.so
%attr(755,root,root) %{_libdir}/nvidia/libEGL.so
%endif
%{_pkgconfigdir}/gl.pc

%files doc
%defattr(644,root,root,755)
%doc html/*

%ifarch %{x8664}
%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-bug-report.sh
%attr(755,root,root) %{_bindir}/nvidia-cuda-mps-control
%attr(755,root,root) %{_bindir}/nvidia-cuda-mps-server
%attr(755,root,root) %{_bindir}/nvidia-smi
%attr(755,root,root) %{_bindir}/nvidia-xconfig
%{_mandir}/man1/nvidia-cuda-mps-control.1*
%{_mandir}/man1/nvidia-smi.1*
%{_mandir}/man1/nvidia-xconfig.1*
%if %{with settings}
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%attr(755,root,root) %{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_desktopdir}/nvidia-settings.desktop
%{_pixmapsdir}/nvidia-settings.png
%endif
%endif
%endif
