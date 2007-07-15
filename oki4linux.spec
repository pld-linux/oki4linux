Summary:	OKIPAGE (4w, 4w Plus, 6w, 8w, 8w Lite, 8z), OL400w printer driver
Summary(pl.UTF-8):	Sterownik do drukarek OKIPAGE (4w, 4w Plus, 6w, 8w, 8w Lite, 8z), OL400w
Name:		oki4linux
Version:	2.1gst
Release:	0.1
Epoch:		0
License:	distributable (see COPYING)
Group:		Daemons
Source0:	http://www.linuxprinting.org/download/printing/%{name}-%{version}.tar.gz
# Source0-md5:	54c85488d2489d2431ce518916b20515
Source1:	%{name}.init
Patch0:		%{name}-daemon.patch
Patch1:		%{name}-a4.patch
URL:		http://www.linuxprinting.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User space based driver for OKIPAGE (4w, 4w Plus, 6w, 8w, 8w Lite,
8z), OL400w printers.

%description -l pl.UTF-8
Sterownik do drukarek OKIPAGE (4w, 4w Plus, 6w, 8w, 8w Lite, 8z),
OL400w zaimplementowany w przestrzeni użytkownika.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
cd src
rm -f oki4drv
%{__cc} %{rpmldflags} %{rpmcflags} -o oki4drv main.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,%{_mandir}/man1,/dev}

install src/oki4drv	$RPM_BUILD_ROOT%{_sbindir}
install src/oki4daemon	$RPM_BUILD_ROOT%{_sbindir}
install src/oki4drv.man	$RPM_BUILD_ROOT%{_mandir}/man1/oki4drv.1
install src/README.oki4daemon	./
install src/readback.c	doc/
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/oki4daemon
touch $RPM_BUILD_ROOT/dev/oki4drv

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add oki4daemon
%service oki4daemon restart

%preun
if [ "$1" = "0" ]; then
	%service oki4daemon stop
	/sbin/chkconfig --del oki4daemon
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING README README.oki4daemon crack doc samples
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man?/*
%attr(660,root,lp) %ghost /dev/oki4drv
