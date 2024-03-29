%define ver 3.0
%if %{?rel:0}%{!?rel:1}
%define rel 6.1
%endif
%if %{?srcext:0}%{!?srcext:1}
%define srcext .gz
%endif
Summary: ARGUS Software
Name: argus
Version: %ver
Release: %{rel}
License: see COPYING file
Group: Applications/Internet
Source: %{name}-%{version}.%{rel}.tar%{srcext}
URL: http://qosient.com/argus
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
The ARGUS (Audit Record Generation And Utilization System) is an data 
network transaction auditing tool.  The data generated by argus can be used
for a wide range of tasks such as network operations, security and performance
management.

Copyright: (c) 2000-2012 QoSient, LLC

%define argusdir	/usr/local
%define argusman	/usr/local/share/man
%define argusdocs	/usr/local/share/doc/argus-%{ver}

%define argusbin	%{argusdir}/bin
%define argussbin	%{argusdir}/sbin

%prep
%setup -n %{name}-%{ver}.%{rel}
%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

install -D -m 0600 support/Config/argus.conf $RPM_BUILD_ROOT/etc/argus.conf
install -D -m 0755 support/Startup/argus $RPM_BUILD_ROOT/etc/rc.d/init.d/argus
install -D -m 0755 support/Archive/argusarchive $RPM_BUILD_ROOT/%{argusbin}/argusarchive

%post
/sbin/chkconfig --add argus
service argus start >/dev/null 2>&1

%preun
if [ "$1" = 0 ] ; then
  service argus stop >/dev/null 2>&1
  /sbin/chkconfig --del argus
fi

%postun
if [ "$1" -ge "1" ]; then
  service argus condrestart >/dev/null 2>&1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{argussbin}/argus
%{argusbin}/argus-lsof
%{argusbin}/argus-snmp
%{argusbin}/argus-vmstat
%{argusbin}/argusbug
%{argusbin}/argusarchive

%doc %{argusdocs}
%{argusman}/man5/argus.conf.5
%{argusman}/man8/argus.8

/etc/rc.d/init.d/argus

%config /etc/argus.conf
