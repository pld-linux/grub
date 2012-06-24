#
# TODO:
# cleanups, maybe more patches for lowmem (Conectiva) ?,
# TESTING !!! 
#
Summary:	GRand Unified Bootloader
Summary(pl):	GRUB - bootloader dla x86
Summary(pt_BR):	Gerenciador de inicializa��o GRUB
Name:		grub
Version:	0.93
Release:	0.1
License:	GPL
Group:		Base
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
Source1:	%{name}-linux-menu.lst
Source2:	%{name}-rebootin.awk
Source3:	%{name}_functions.sh
Source4:	%{name}-splash.xpm.gz
Patch0:		%{name}-install.in.patch
Patch1:		%{name}-installcopyonly.patch
Patch2:		%{name}-addsyncs.patch
Patch3:		%{name}-staticcurses.patch
Patch4:		%{name}-automake16.patch
Patch5:		%{name}-endedit.patch
Patch6:		%{name}-largedisk.patch
Patch7:		%{name}-append.patch
Patch8:		%{name}-bootonce.patch
Patch9:		%{name}-graphics.patch
Patch10:	%{name}-splashimagehelp.patch
Patch11:	%{name}-graphics-bootterm.patch
Patch12:	%{name}-serial-terminfo.patch
Patch13:	%{name}-special-device-names.patch
Patch14:	%{name}-ncurses.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-static
# needed for 'cmp' program
Requires:	diffutils
Provides:	bootloader
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_datadir	/boot

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

%description -l pl
GRUB jest bootloaderem na licencji GNU, maj�cym na celu unifikacj�
procesu bootowania na systemach x86. Potrafi nie tylko �adowa� j�dra
Linuksa i *BSD: posiada r�wnie� implementacje standardu Multiboot,
kt�ry pozwala na elastyczne �adowanie wielu obraz�w bootowalnych
(czego wymagaj� modu�owe j�dra, takie jak GNU Hurd).

%description -l pt_BR
Esse � o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usu�rios mais
avan�ados e que querem mais recursos de seu boot loader.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0
%patch13 -p1
%patch14 -p1

rm -rf doc/*info*

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
CFLAGS="-Os -g" ; export CFLAGS
%configure \
	--disable-auto-linux-mem-opt
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/grub/%{_arch}-*/* \
	$RPM_BUILD_ROOT%{_datadir}/grub/

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/grub/menu.lst
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/rebootin
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/grub/splash.xpm.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc TODO BUGS NEWS ChangeLog docs/menu.lst
%dir %{_datadir}/grub
%{_datadir}/grub/*stage*
%{_datadir}/grub/splash.xpm.gz
%config(noreplace) %verify(not mtime md5 size) %{_datadir}/grub/menu.lst
%attr(754,root,root) %{_bindir}/*
%attr(754,root,root) %{_sbindir}/*
%{_infodir}/*.info*
%{_mandir}/*/*
/etc/sysconfig/rc-boot/%{name}_functions.sh
