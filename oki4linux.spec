Summary:	Okipage 4w/4w+ printer driver
Summary(pl):	Driver do drukarki Okipage 4w/4w+
Name:		oki4linux
Version:	2.1gst
Release:	0.1
Epoch:		0
License:	distribuatable (see COPYING)
Group:		Daemons
Source0:	http://www.linuxprinting.org/download/printing/%{name}-%{version}.tar.gz
# Source0-md5:	54c85488d2489d2431ce518916b20515
Source1:	%{name}.init
Patch0:		%{name}-daemon.patch
URL:		http://www.linuxprinting.org
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Okipage 4w/4w+ printer driver.

%description -l pl
Sterownik do drukarki Okipage 4w/4w+.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
cd src
rm -f oki4drv
%{__cc} %{rpmcflags} -o oki4drv main.c
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,%{_mandir}/man1,/dev}
mv -f src/oki4drv	$RPM_BUILD_ROOT%{_sbindir}
mv -f src/oki4daemon	$RPM_BUILD_ROOT%{_sbindir}
mv -f src/oki4drv.man	$RPM_BUILD_ROOT%{_mandir}/man1/oki4drv.1
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/oki4daemon
touch $RPM_BUILD_ROOT/dev/oki4drv

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add oki4daemon
if [ -f /var/lock/subsys/oki4daemon ]; then
	/etc/rc.d/init.d/oki4daemon restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/oki4daemon start\" to start oki4daemon daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/oki4daemon ]; then
		/etc/rc.d/init.d/oki4daemon stop 1>&2
	fi
	/sbin/chkconfig --del oki4daemon
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING README crack doc samples
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man?/*
%attr(660,root,lp) %ghost /dev/oki4drv
