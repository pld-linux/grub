Summary:	GRand Unified Bootloader
Name:		grub
Version:	0.5.94
Release:	2
License:	GPL
Group:		Base
Group(pl):	Podstawowe
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source1:	install_grub_on_floppy
Source2:	grub-linux-menu.lst
Patch0:		grub-config.patch
Patch1:		grub-info.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels, it
implements the Multiboot standard, which allows for flexible loading of
multiple boot images (needed for modular kernels such as the GNU Hurd).

%description -l pl
GRUB jest bootloaderem na licencji GNU, maj±cym na celu unifikacjê procesu
bootowania na systemach x86. Potrafi nie tylko ³adowaæ j±dra Linuksa i *BSD:
posiada równie¿ implementacje standardu Multiboot, który pozwala na elastyczne
³adowanie wielu obrazów bootowalnych (czego wymagaj± modu³owe j±dra,
takie jak GNU Hurd).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
rm -rf doc/*info*

%build
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/
perl -p -i -e 's|VERSION|%{version}|' $RPM_BUILD_ROOT%{_sbindir}/$(basename %{SOURCE1})

# dangerous ?
install -d $RPM_BUILD_ROOT/boot/grub/
mv $RPM_BUILD_ROOT%{_datadir}/grub/%{_arch}-%{_vendor}/* $RPM_BUILD_ROOT/boot/grub/
install %{SOURCE2} $RPM_BUILD_ROOT/boot/grub/menu.lst

gzip -9nf $RPM_BUILD_ROOT{%{_infodir}/*,%{_mandir}/*/*} \
	TODO BUGS NEWS ChangeLog docs/menu.lst

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -x /usr/sbin/fix-info-dir ] && /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%preun
[ -x /usr/sbin/fix-info-dir ] && /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz docs/menu.lst.gz
%dir /boot/grub
%config(noreplace) %verify(not mtime md5 size) /boot/grub/menu.lst
/boot/grub/*stage*
%{_infodir}/*.info.gz
%{_mandir}/*/*
%attr(754,root,root) %{_bindir}/*
%attr(754,root,root) %{_sbindir}/*
