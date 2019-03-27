%define debug_package %{nil}
%define source_version 0.2.0-dev

Name:    bind_exporter
Version: 0.2.0.dev
Release: 1%{?dist}
Summary: Prometheus exporter for BIND v9+ service metrics
License: ASL 2.0
URL:        https://github.com/digitalocean/bind_exporter
Source0:    https://github.com/digitalocean/bind_exporter/releases/download/v%{source_version}/bind_exporter
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for BIND v9+ service metrics (https://bind9.net/). 

%prep

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{_sourcedir}/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%caps(cap_net_raw=ep) %{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
