%define module r8192se
%define version 0015.0127.2010
%define card Realtek RTL8191SE/RTL8192SE WiFi cards

%define distname rtl8192se_linux_2.6.%{version}

Summary: dkms package for %{module} driver
Name: dkms-%{module}
Version: %{version}
Release: %mkrel 1
Source0: %{distname}.tar.gz
License: GPLv2
Group: System/Kernel and hardware
URL: http://www.realtek.com.tw
Requires(preun): dkms
Requires(post): dkms
Requires: rtl8192se-firmware
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
This package contains the %{module} driver for
%{card}.

%package -n rtl8192se-firmware
Summary: firmware package for %{module} driver
Group: System/Kernel and hardware

%description -n rtl8192se-firmware
This package contains the firmware for %{name} driver.

%prep
%setup -q -n %{distname}

# Remove not needed source files
rm -f ifcfg-wlan0 RadioPower.sh runwpa wireless-rtl-ac-dc-power.sh \
      wlan0dhcp wlan0down wlan0up wpa1.conf wpa_supplicant-*.tar.gz

# Fix permissions
find -type f -exec chmod 0644 {} \;

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{version}-%{release}

DEST_MODULE_LOCATION[0]=/kernel/drivers/net/wireless
BUILT_MODULE_NAME[0]=%{module}_pci
BUILT_MODULE_LOCATION[0]=HAL/rtl8192

MAKE[0]="make KSRC=\$kernel_source_dir"
AUTOINSTALL="yes"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/
rm -rf %{buildroot}/usr/src/%{module}-%{version}-%{release}/firmware
mkdir -p %{buildroot}/lib/firmware
cp -a firmware/RTL8192SE %{buildroot}/lib/firmware/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/usr/src/%{module}-%{version}-%{release}/

%files -n rtl8192se-firmware
%defattr(0644,root,root,0755)
/lib/firmware/RTL8192SE

%post -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
exit 0

%preun -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
exit 0
