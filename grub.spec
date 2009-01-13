# TODO:
# - check VGA patch - doesn't work good, 0.92 works fine
# - upgrading grub makes installed grub in MBR lose track of menu.lst, with
#   console access can write 'configfile /grub/menu.lst' but without console
#   access your machine stays in grub on boot!
#
# Conditional build:
%bcond_with	splashimage	# removes some ethernet cards support (too much memory occupied?)
%bcond_without	static		# don't build static version
#
Summary:	GRand Unified Bootloader
Summary(de.UTF-8):	GRUB - ein Bootloader für x86
Summary(pl.UTF-8):	GRUB - bootloader dla x86
Summary(pt_BR.UTF-8):	Gerenciador de inicialização GRUB
Name:		grub
Version:	0.97
Release:	15
License:	GPL
Group:		Base
Source0:	ftp://alpha.gnu.org/gnu/grub/%{name}-%{version}.tar.gz
# Source0-md5:	cd3f3eb54446be6003156158d51f4884
Source1:	%{name}-linux-menu.lst
Source2:	%{name}-rebootin.awk
Source3:	%{name}_functions.sh
Source4:	%{name}-splash.xpm.gz
# Source4-md5:	2842e2955603e3b6d722690b3cdd48a9
Patch0:		%{name}-install.in.patch
Patch1:		%{name}-endedit.patch
Patch2:		%{name}-append.patch
Patch3:		%{name}-graphics.patch
Patch4:		%{name}-splashimagehelp.patch
Patch5:		%{name}-graphics-bootterm.patch
Patch6:		%{name}-special-device-names.patch
# from http://www.linuxfromscratch.org/patches/downloads/grub/
Patch7:		%{name}-%{version}-disk_geometry-1.patch
Patch8:		%{name}-%{version}-256byte_inode-1.patch
Patch9:		%{name}-cciss-devicemap.patch
Patch10:	%{name}-gcc4.patch
Patch11:	%{name}-useless.patch
Patch12:	%{name}-ac.patch
Patch13:	%{name}-i2o.patch
Patch14:	%{name}-pxe.patch
URL:		http://www.gnu.org/software/grub/grub.en.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
%if %{with static}
BuildRequires:	glibc-static
BuildRequires:	ncurses-static
%endif
%ifarch %{x8664}
BuildRequires:	/usr/lib/libc.a
%endif
# needed for 'cmp' program
Requires:	diffutils
Provides:	bootloader
Obsoletes:	fedora-logos
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_libdir		/boot

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible
loading of multiple boot images (needed for modular kernels such as
the GNU Hurd).

%description -l de.UTF-8
GRUB (GRand Unified Boot-loader) ist ein Bootloader, der oft auf
Rechnern eingesetzt wird, auf denen das freie Betriebssystem Linux
läuft. GRUB löst den betagten LILO (Linux-Loader) ab.

GRUB wurde innerhalb des GNU Hurd-Projektes als Boot-Loader entwickelt
und wird unter der GPL vertrieben. Aufgrund seiner höheren
Flexibilität verdrängt GRUB in vielen Linux-Distributionen den
traditionellen Boot-Loader LILO.

%description -l es.UTF-8
Éste es GRUB - Grand Unified Boot Loader - un administrador de
inicialización capaz de entrar en la mayoría de los sistemas
operacionales libres - Linux, FreeBSD, NetBSD, GNU Mach, etc. como
también en la mayoría de los sistemas operacionales comerciales para
PC.

El administrador GRUB puede ser una buena alternativa a LILO, para
usuarios conmás experiencia y que deseen obtener más recursos de su
cargador de inicialización (boot loader).

%description -l pl.UTF-8
GRUB jest bootloaderem na licencji GNU, mającym na celu unifikację
procesu bootowania na systemach x86. Potrafi nie tylko ładować jądra
Linuksa i *BSD: posiada również implementacje standardu Multiboot,
który pozwala na elastyczne ładowanie wielu obrazów bootowalnych
(czego wymagają modułowe jądra, takie jak GNU Hurd).

%description -l pt_BR.UTF-8
Esse é o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usuários mais
avançados e que querem mais recursos de seu boot loader.

%package nb
Summary:	Grub's network boot image for the Network Image Proposal
Summary(pl.UTF-8):	Obraz dla gruba służący technologii Network Image Proposal
Group:		Networking/Admin

%description nb
This is a network boot image for the Network Image Proposal used by
some network boot loaders, such as Etherboot. This is mostly the same
as Stage 2, but it also sets up a network and loads a configuration
file from the network.

%description nb -l pl.UTF-8
To jest obraz służący zdalnemu uruchamianiu komputera bezdyskowego,
oparty na standardzie nazwanym 'Network Image Proposal'. Jest niemal
identyczny z tym ze Stage 2, ale uruchamia sieć oraz ładuje z niej
plik konfiguracyjny.

%package pxe
Summary:	Grub's network boot image for the Preboot Execution Environment
Summary(pl.UTF-8):	Obraz dla gruba służący technologii Preboot Execution Environment
Group:		Networking/Admin

%description pxe
This is another network boot image for the Preboot Execution
Environment used by several Netboot ROMs. This is identical to nbgrub,
except for the format. This is mostly the same as Stage 2, but it also
sets up a network and loads a configuration file from the network.

%description pxe -l pl.UTF-8
To jest obraz służący zdalnemu uruchamianiu komputera bezdyskowego,
oparty na standardzie nazwanym 'Preboot Execution Environment' (PXE).
Jest niemal identyczny z tym ze Stage 2, ale uruchamia sieć oraz
ładuje z niej plik konfiguracyjny.

%package -n rc-boot-grub
Summary:	grub support for rc-boot
Summary(pl.UTF-8):	Wsparcie gruba dla rc-boot
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	rc-boot
Provides:	rc-boot-bootloader

%description -n rc-boot-grub
grub support for rc-boot.

%description -n rc-boot-grub -l pl.UTF-8
Wsparcie gruba dla rc-boot.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%{?with_splashimage:%patch3 -p1}
%{?with_splashimage:%patch4 -p1}
%{?with_splashimage:%patch5 -p1}
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p0
%patch10 -p1

rm -rf doc/*info*

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%if %{with static}
LDFLAGS="-static"; export LDFLAGS
%endif
%configure \
%if %{without splashimage}
	--enable-3c595 \
	--enable-3c90x \
	--enable-davicom \
	--enable-e1000 \
	--enable-eepro100 \
	--enable-epic100 \
	--enable-natsemi \
	--enable-ns8390 \
	--enable-pcnet32 \
	--enable-rtl8139 \
	--enable-r8169 \
	--enable-sis900 \
	--enable-tg3 \
	--enable-tulip \
	--enable-tlan \
	--enable-via-rhine \
	--enable-w89c840 \
	--enable-compex-rl2000-fix \
	--enable-pxe \
	--enable-diskless \
%endif
	--disable-auto-linux-mem-opt
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/grub/%{_arch}-*/* \
	$RPM_BUILD_ROOT%{_libdir}/grub/

install %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/grub/menu.lst
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/rebootin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/grub/splash.xpm.gz

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# grubby will not work if /boot/grub/menu.lst is symlink
# so make sure menu.lst is file and grub.conf (if any) is symlink
if [ -L /boot/grub/menu.lst ] && [ -f /boot/grub/grub.conf ]; then
	mv -f /boot/grub/menu.lst{,.rpmsave}
	mv -f /boot/grub/{grub.conf,menu.lst}
	ln -sf menu.lst /boot/grub/grub.conf
fi

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc TODO BUGS NEWS ChangeLog docs/menu.lst
%dir %{_libdir}/grub
%{_libdir}/grub/stage1
%{_libdir}/grub/*stage1_5
%verify(not md5 mtime) %{_libdir}/grub/stage2
%{_libdir}/grub/stage2_eltorito
%{_libdir}/grub/splash.xpm.gz
%config(noreplace) %verify(not md5 mtime size) %{_libdir}/grub/menu.lst
%attr(754,root,root) %{_bindir}/*
%attr(754,root,root) %{_sbindir}/*
%{_infodir}/*.info*
%{_mandir}/*/*

%if %{without splashimage}
%files nb
%defattr(644,root,root,755)
%{_libdir}/grub/nbgrub

%files pxe
%defattr(644,root,root,755)
%{_libdir}/grub/pxegrub
%endif

%files -n rc-boot-grub
%defattr(644,root,root,755)
/etc/sysconfig/rc-boot/%{name}_functions.sh
