#
# Conditional build:
#
%bcond_without	aalib	# without aalib output support
%bcond_without	ggi	# without ggi output support
%bcond_without	ncurses # without ncurses output support
%bcond_without	svga 	# without svga output support
#
Summary:	A fast, portable real-time interactive fractal zoomer
Summary(pl):	Szybki, przeno�ny i interaktywny eksplorator fraktali
Name:		XaoS
Version:	3.1
%define	pre	pre5
Release:	0.%{pre}.3
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/xaos/%{name}-%{version}%{pre}.tar.gz
# Source0-md5:	904691517303d2bedddf33b3d68f97cc
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-nosuid.patch
Patch1:		%{name}-brokenasm.patch
Patch2:		%{name}-ggi-fix.patch
Patch3:		%{name}-svga-fix.patch
Patch4:		%{name}-info.patch
URL:		http://xaos.theory.org/
BuildRequires:	XFree86-devel
%{?with_aalib:BuildRequires:		aalib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_ggi:BuildRequires:		libggi-devel}
BuildRequires:	libpng-devel
%{?with_ncurses:BuildRequires:	ncurses-devel}
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XaoS is a fast portable real-time interactive fractal zoomer. It
supports outputs such as X11, aalib, ncurses and SVGAlib. It displays
the Mandelbrot set (among other escape time fractals) and allows you
zoom smoothly into the fractal. Various coloring modes are provided
for both the points inside and outside the selected set. In addition,
switching between Julia and Mandelbrot fractal types is provided. The
first version was a poorly written Mandelbrot view by Thomas later
modified by Jan to support high frame-rate zooming. Other additions
were later made including autopilot (for those of you without drivers
licenses), palette changing, PNG saving, and fractal inversion.

%description -l pl
XaoS jest szybkim, przeno�nym i interaktywnym eksploratorem fraktali.
Efekty jego dzia�ania mo�na ogl�da� z u�yciem drajwer�w X11, aalib,
ncurses oraz SVGAlib. XaoS wy�wietla zbi�r Mandelbrota (i nie tylko) i
pozwala na p�ynne powi�kszanie/pomniejszanie widocznego zakresu.
Dost�pne s� r�ne rodzaje kolorowania dla punkt�w w wybranym zbiorze,
jak i poza nim. Dodatkowo, mo�liwe jest prze��czanie mi�dzy fraktalem
Mandelbrota, a odpowiadaj�cym mu fraktalem Julii (i w drug� stron�).
Pierwsza wersja (Tomasa) by�a kiepsko napisanym wy�wietlaczem zbioru
Mandelbrota. Zosta�a zmodyfikowana przez Jana aby umo�liwia� szybkie
powi�kszanie. Inne zmiany, zrobione p�niej to autopilot, zmiana
palety, zapisywanie PNG i inwersja fraktali.

%prep
%setup -q -n %{name}-%{version}%{pre}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
LDFLAGS="%{rpmldflags} -L/usr/X11R6/%{_lib}"
%configure \
	--with-x \
	--with-x11-driver=yes \
	%{?with_aalib:	--with-aa-driver=no} \
	%{?with_ggi:	--with-ggi-driver=no} \
	%{?with_ncurses:--with-curses-driver=no} \
	%{?with_svga:	--with-svga-driver=no}

%{__make}

cd doc
makeinfo --no-split xaos.texinfo
makeinfo --no-split xaosdev.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_datadir}/locale/{hu,es,fr,cs,de}/LC_MESSAGES

%{__make} install \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	LOCALEDIR=$RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%find_lang xaos

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f xaos.lang
%defattr(644,root,root,755)
%doc TODO doc/{ANNOUNCE,AUTHORS,PROBLEMS,README{,.bugs,.ggi},SPONSORS}
%attr(755,root,root) %{_bindir}/xaos
%dir %{_datadir}/XaoS
%dir %{_datadir}/XaoS/catalogs
%lang(cs) %{_datadir}/XaoS/catalogs/cesky.cat
%lang(de) %{_datadir}/XaoS/catalogs/deutsch.cat
%{_datadir}/XaoS/catalogs/english.cat
%lang(es) %{_datadir}/XaoS/catalogs/espanhol.cat
%lang(fr) %{_datadir}/XaoS/catalogs/francais.cat
%lang(hu) %{_datadir}/XaoS/catalogs/magyar.cat
%{_datadir}/XaoS/examples
%{_datadir}/XaoS/help
%{_datadir}/XaoS/tutorial
%{_mandir}/man6/*
%{_infodir}/*.info*
%{_pixmapsdir}/XaoS.png
%{_desktopdir}/XaoS.desktop
