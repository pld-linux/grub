Summary:	GRand Unified Bootloader
Summary(es):	GRUB boot loader
Summary(pt):	GRUB boot loader
Name:		grub
Version:	0.5.95
Release:	1
License:	GPL
Group:		Base
Group(pl):	Podstawowe
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source1:	install_grub_on_floppy
Source2:	grub-linux-menu.lst
Patch0:		grub-config.patch
Patch1:		grub-info.patch
Patch2:		grub-bigpatch.patch
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible
loading of multiple boot images (needed for modular kernels such as
the GNU Hurd).

%description -l es
�ste es GRUB - Grand Unified Boot Loader - un administrador de
inicializaci�n capaz de entrar en la mayor�a de los sistemas
operacionales libres - Linux, FreeBSD, NetBSD, GNU Mach, etc. como
tambi�n en la mayor�a de los sistemas operacionales comerciales para
PC.

El administrador GRUB puede ser una buena alternativa a LILO, para
usuarios conm�s experiencia y que deseen obtener m�s recursos de su
cargador de inicializaci�n (boot loader).

%description -l pt
Esse � o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usu�rios mais
avan�ados e que querem mais recursos de seu boot loader.

%description -l pl
GRUB jest bootloaderem na licencji GNU, maj�cym na celu unifikacj�
procesu bootowania na systemach x86. Potrafi nie tylko �adowa� j�dra
Linuksa i *BSD: posiada r�wnie� implementacje standardu Multiboot,
kt�ry pozwala na elastyczne �adowanie wielu obraz�w bootowalnych
(czego wymagaj� modu�owe j�dra, takie jak GNU Hurd).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -rf doc/*info*

%build
LDFLAGS="-s"; export LDFLAGS
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz docs/menu.lst.gz
%dir /boot/grub
%config(noreplace) %verify(not mtime md5 size) /boot/grub/menu.lst
/boot/grub/*stage*
%{_infodir}/*.info*.gz
%{_mandir}/*/*
%attr(754,root,root) %{_bindir}/*
%attr(754,root,root) %{_sbindir}/*
