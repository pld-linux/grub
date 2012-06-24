#
# TODO:
# - check VGA patch - doesn't work good, 0.92 works fine
#
Summary:	GRand Unified Bootloader
Summary(pl):	GRUB - bootloader dla x86
Summary(pt_BR):	Gerenciador de inicializa��o GRUB
Name:		grub
Version:	0.94
Release:	1.2
License:	GPL
Group:		Base
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
# Source0-md5:	299672a99cf59656e653d8ffd7851b56
Source1:	%{name}-linux-menu.lst
Source2:	%{name}-rebootin.awk
Source3:	%{name}_functions.sh
Source4:	%{name}-splash.xpm.gz
# Source4-md5:	2842e2955603e3b6d722690b3cdd48a9
Patch0:		%{name}-install.in.patch
Patch1:		%{name}-endedit.patch
Patch2:		%{name}-append.patch
Patch3:		%{name}-bootonce.patch
Patch4:		%{name}-graphics.patch
Patch5:		%{name}-splashimagehelp.patch
Patch6:		%{name}-graphics-bootterm.patch
Patch7:		%{name}-special-device-names.patch
URL:		http://www.gnu.org/software/grub/grub.en.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
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
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p1
%patch7 -p1

rm -rf doc/*info*

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
CFLAGS="-Os %{?debug:-g}" ; export CFLAGS
%configure \
	--enable-3c503 \
	--enable-3c507 \
	--enable-3c509 \
	--enable-3c529 \
	--enable-3c595 \
	--enable-3c90x \
	--enable-compex-rl2000-fix \
	--enable-cs89x0 \
	--enable-davicom \
	--enable-depca \
	--enable-diskless \
	--enable-eepro \
	--enable-eepro100 \
	--enable-epic100 \
	--enable-exos205 \
	--enable-lance \
	--enable-natsemi \
	--enable-ne \
	--enable-ne2100 \
	--enable-ni5010 \
	--enable-ni5210 \
	--enable-ni6510 \
	--enable-ns8390 \
	--enable-otulip \
	--enable-rtl8139 \
	--enable-sis900 \
	--enable-sk-g16 \
	--enable-smc9000 \
	--enable-tiara \
	--enable-tulip \
	--enable-via-rhine \
	--enable-w89c840 \
	--enable-wd \
	--disable-auto-linux-mem-opt
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/grub/%{_arch}-*/* \
	$RPM_BUILD_ROOT%{_datadir}/grub/

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/grub/menu.lst
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/rebootin
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
