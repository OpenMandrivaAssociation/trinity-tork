%bcond clang 1
%bcond embedded_geoip 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg tork
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.33
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Anonymity Manager for TDE
Group:		Applications/Internet
URL:		sourceforge.net/projects/tolrk/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DBUILD_ALL=ON -DWITH_ALL_OPTIONS=ON  
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}
BuildOption:    -DWITH_EMBEDDED_GEOIP=%{!?with_embedded_geoip:OFF}%{?with_embedded_geoip:ON}


BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdepim-devel >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# GNUTLS
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(gnutls)

# TORSOCKS support
BuildRequires:	torsocks-devel

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# GEOIP
%{?with_embedded_geoip:BuildRequires:  pkgconfig(geoip)}

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
TorK is an Anonymity Manager for the TDE Desktop. Browse anonymously on 
Konqueror/Firefox/Opera. Send anonymous email via the MixMinion network.
Use ssh/irc/IM anonymously. Control and monitor your anonymous traffic 
on the Tor network.

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md TODO USINGTORK
%{tde_prefix}/bin/tork
%{tde_prefix}/bin/torkarkollon
%{tde_prefix}/bin/usewithtor
%{tde_prefix}/%{_lib}/trinity/kickermenu_tork.la
%{tde_prefix}/%{_lib}/trinity/kickermenu_tork.so
%{tde_prefix}/%{_lib}/trinity/tdehtml_tork.la
%{tde_prefix}/%{_lib}/trinity/tdehtml_tork.so
%{tde_prefix}/%{_lib}/trinity/tdeio_torioslave.la
%{tde_prefix}/%{_lib}/trinity/tdeio_torioslave.so
%{tde_prefix}/share/applications/tde/tork_plug_in.desktop
%{tde_prefix}/share/apps/kicker/menuext/torkmenu.desktop
%{tde_prefix}/share/apps/tdehtml/kpartplugins/tork_plug_in.rc
%{tde_prefix}/share/services/torioslave.protocol
%{tde_prefix}/share/applications/tde/tork.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/tork_downloadwithfirefox.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/tork_downloadwithkonqueror.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/tork_downloadwithopera.desktop
%{tde_prefix}/share/apps/tork/
%{tde_prefix}/share/config.kcfg/torkconfig.kcfg
%{tde_prefix}/share/doc/tde/HTML/en/tork/
%{tde_prefix}/share/icons/hicolor/*/apps/tork.png
%dir %{tde_prefix}/share/menu
%{tde_prefix}/share/menu/tork
%dir %{tde_prefix}/share/pixmaps
%{tde_prefix}/share/pixmaps/tork.xpm
%{tde_prefix}/share/man/man1/tork.1*
%{tde_prefix}/share/man/man1/torkarkollon.1*
%lang(it) %{tde_prefix}/share/locale/it/LC_MESSAGES/libkickermenu_tork.mo
%lang(ka) %{tde_prefix}/share/locale/ka/LC_MESSAGES/*.mo
%lang(ru) %{tde_prefix}/share/locale/ru/LC_MESSAGES/libkickermenu_tork.mo

