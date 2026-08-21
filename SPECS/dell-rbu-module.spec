%define uname  %{kernel_version}
%define module_dir extra

Summary: Driver dell_rbu.ko for DELL openmanage
Name: dell-rbu-module
Version: 4.19.0+1
Release: 4%{?dist}
# Built against new kABI after cip rebase
Requires: xcpng-kernel-kabi = 4.19.325-cip134+

License: GPLv2
#Source: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/drivers/firmware/dell_rbu.c?h=v4.19.19
#wget -O dell_rbu.c https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/drivers/firmware/dell_rbu.c?h=v4.19.19
Source0: dell_rbu.c
Source1: Makefile

BuildRequires: kernel-devel
BuildRequires: gcc
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
dell_rbu Linux Device Driver for DELL systems.
It is needed to start & use openmanage related services.

%prep
%setup -c -T -n %{name}-%{version}
cp %{SOURCE0} .
cp %{SOURCE1} .

%build
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{uname}/*/*.ko

%changelog
* Mon Aug 31 2026 Quentin Casasnovas <quentin.casasnovas@vates.tech> - 4.19.0+1-4
- Rebuild for kernel v4.19.325-cip134

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.19.0+1-3
- Rebuild for XCP-ng 8.3

* Tue Jun 30 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.19.0+1-2
- Rebuild for XCP-ng 8.2

* Fri Jan 31 2020 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.19.0+1-1
- Added driver dell-rbu as module rpm
