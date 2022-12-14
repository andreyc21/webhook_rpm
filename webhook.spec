Summary:  webhook is a lightweight configurable tool that allows you to easily create HTTP endpoints (hooks) on your server
Name: webhook 
Version: %{version} 
Release: 0
License: MIT
Group: Development/Tools
Source0: webhook 
Source1: webhook.service
%define _build_id_links none

%description
webhook is a lightweight configurable tool written in Go, that allows
you to easily create HTTP endpoints (hooks) on your server, which you
can use to execute configured commands. You can also pass data from
the HTTP request (such as headers, payload or query variables) to your
commands. webhook also allows you to specify rules which have to be
satisfied in order for the hook to be triggered.

%install
mkdir -p %{buildroot}/usr/sbin/
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp %{SOURCE0} %{buildroot}/usr/sbin/%{name}
cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

%files
%attr(755, root, root) /usr/sbin/%{name}
%attr(644, root, root) /usr/lib/systemd/system/%{name}.service

%post 
if [ $1 -eq 1 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then 
    # Initial installation 
    /usr/lib/systemd/systemd-update-helper install-system-units webhook.service || : 
fi 

%preun 
if [ $1 -eq 0 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then 
    # Package removal, not upgrade 
    /usr/lib/systemd/systemd-update-helper remove-system-units webhook.service || : 
fi

%postun 
if [ $1 -ge 1 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then 
    # Package upgrade, not uninstall 
    /usr/lib/systemd/systemd-update-helper mark-restart-system-units webhook.service || : 
fi
