%define name grub
%define version 0.5.93.1
%define release 3mdk

Summary: GRand Unified Bootloader
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.debian.org/debian/dists/potato/main/source/base/%{name}_%{version}.tar.bz2
Source1: install_grub_on_floppy
Patch0: grub-mdkconf.patch.bz2
Copyright: GPL
Group: System Environment/Base
BuildRoot: /tmp/%{name}-buildroot

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems.  In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible loading
of multiple boot images (needed for modular kernels such as the GNU
Hurd).

%prep
%setup
%patch0 -p1 -b .mdkconf

%build
./configure --prefix=/usr %{_target_platform}
make
make -C docs/ dvi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/

install -m755 %{SOURCE1} $RPM_BUILD_ROOT/usr/sbin/
perl -p -i -e 's|VERSION|%{version}|' $RPM_BUILD_ROOT/usr/sbin/$(basename %{SOURCE1})

# dangerous ?
install -d $RPM_BUILD_ROOT/boot/grub/
mv $RPM_BUILD_ROOT/usr/share/grub/%{_arch}-%{_vendor}/* $RPM_BUILD_ROOT/boot/grub/

rm -f $RPM_BUILD_ROOT/usr/info/dir*
bzip2 -9f $RPM_BUILD_ROOT/usr/info/* $RPM_BUILD_ROOT/usr/man/*/*
strip -s $RPM_BUILD_ROOT/usr/sbin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/grub.info.bz2 \
    /usr/info/dir --entry="* GRUB: (grub).                 The GRand Unified Bootloader."
/sbin/install-info /usr/info/multiboot.info.bz2 \
    /usr/info/dir --entry="* Multiboot Standard: (multiboot).   Multiboot Standard"

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete /usr/info/grub.info.bz2 \
	--info-dir=/usr/info/ --entry="* GRUB: (grub).                 The GRand Unified Bootloader."

   /sbin/install-info --delete /usr/info/multiboot.info.bz2 \
	--info-dir=/usr/info/ --entry="* Multiboot Standard: (multiboot).   Multiboot Standard"
fi

%files
%defattr(-,root,root)
%doc TODO BUGS NEWS ChangeLog docs/menu.lst
%doc docs/grub.dvi docs/multiboot.dvi
%config /boot/grub/stage1
%config /boot/grub/stage2
%config /boot/grub/stage1_lba 
/boot/grub/e2fs_stage1_5  
/boot/grub/fat_stage1_5  
/boot/grub/ffs_stage1_5  
/boot/grub/minix_stage1_5  
/usr/info/*
/usr/man/*/*
/usr/sbin/*

%changelog
* Tue Jan 4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.93.1-3mdk
- Add install_grub_on_floppy script (thnks b.bodin).
- Add dvi docs (tknks b.bodin).

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.5.93.1-2mdk
- Add %packager (thnks rpmlint).
- Remove CFLAGS.

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First spec file for Mandrake distribution based on debian version.
