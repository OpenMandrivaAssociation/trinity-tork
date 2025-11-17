#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tork
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.33
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Anonymity Manager for TDE
Group:		Applications/Internet
URL:		sourceforge.net/projects/tolrk/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdepim-devel >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# GNUTLS
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(gnutls)

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# TORSOCKS support
BuildRequires:	torsocks-devel

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# GEOIP
%define with_embedded_geoip 1
BuildRequires:  pkgconfig(geoip)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
TorK is an Anonymity Manager for the TDE Desktop. Browse anonymously on 
Konqueror/Firefox/Opera. Send anonymous email via the MixMinion network.
Use ssh/irc/IM anonymously. Control and monitor your anonymous traffic 
on the Tor network.

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  \
  -DBUILD_ALL=ON \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_EMBEDDED_GEOIP=%{?with_embedded_geoip:ON}%{?!with_embedded_geoip:OFF} \
%if 0%{?pclinuxos} == 0
  -DWITH_GNUTLS=ON \
%endif
  \
  ..

%__make %{?_smp_mflags}


%install
%__make install DESTDIR=$RPM_BUILD_ROOT -C build

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md TODO USINGTORK
%{tde_bindir}/tork
%{tde_bindir}/torkarkollon
%{tde_bindir}/usewithtor
%{tde_tdelibdir}/kickermenu_tork.la
%{tde_tdelibdir}/kickermenu_tork.so
%{tde_tdelibdir}/tdehtml_tork.la
%{tde_tdelibdir}/tdehtml_tork.so
%{tde_tdelibdir}/tdeio_torioslave.la
%{tde_tdelibdir}/tdeio_torioslave.so
%{tde_tdeappdir}/tork_plug_in.desktop
%{tde_datadir}/apps/kicker/menuext/torkmenu.desktop
%{tde_datadir}/apps/tdehtml/kpartplugins/tork_plug_in.rc
%{tde_datadir}/services/torioslave.protocol
%{tde_tdeappdir}/tork.desktop
%{tde_datadir}/apps/konqueror/servicemenus/tork_downloadwithfirefox.desktop
%{tde_datadir}/apps/konqueror/servicemenus/tork_downloadwithkonqueror.desktop
%{tde_datadir}/apps/konqueror/servicemenus/tork_downloadwithopera.desktop
%{tde_datadir}/apps/tork/
%{tde_datadir}/config.kcfg/torkconfig.kcfg
%{tde_tdedocdir}/HTML/en/tork/
%{tde_datadir}/icons/hicolor/*/apps/tork.png
%dir %{tde_datadir}/menu
%{tde_datadir}/menu/tork
%dir %{tde_datadir}/pixmaps
%{tde_datadir}/pixmaps/tork.xpm
%{tde_mandir}/man1/tork.1*
%{tde_mandir}/man1/torkarkollon.1*
%lang(it) %{tde_datadir}/locale/it/LC_MESSAGES/libkickermenu_tork.mo
%lang(ka) %{tde_datadir}/locale/ka/LC_MESSAGES/*.mo
%lang(ru) %{tde_datadir}/locale/ru/LC_MESSAGES/libkickermenu_tork.mo

