#
# Conditional build:
#
# _without_aa   	- without aalib output support
# _without_ggi		- without ggi output support
# _without_ncurses 	- without ncurses output support
# _without_svga 	- without svga output support
#
%ifnarch %{ix86} alpha
%define _without_svgalib 1
%endif
Summary:	A fast, portable real-time interactive fractal zoomer
Summary(pl):	Szybki, przeno¶ny i interaktywny explorator fraktali
Name:		XaoS
Version:	3.1
%define	pre	pre5
Release:	0.%{pre}.1
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
%{!?_without_aa:BuildRequires:		aalib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_ggi:BuildRequires:		libggi-devel}
BuildRequires:	libpng-devel
%{!?_without_ncurses:BuildRequires:	ncurses-devel}
%{!?_without_svga:BuildRequires:	svgalib-devel}
BuildRequires:	texinfo
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
XaoS jest szybkim, przeno¶nym i interaktywnym exploratorem fraktali.
Efekty jego dzia³ania mo¿na ogl±daæ z u¿yciem drajwerów X11, aalib,
ncurses oraz SVGAlib. XaoS wy¶wietla zbiór Mandelbrota (i nie tylko) i
pozwala na p³ynne powiêkszanie/pomniejszanie widocznego zakresu.
Dostêpne s± ró¿ne rodzaje kolorowania dla punktów w wybranym zbiorze,
jak i poza nim. Dodatkowo, mo¿liwe jest prze³±czanie miêdzy fraktalem
Mandelbrota, a odpowiadaj±cym mu fraktalem Julii (i w drug± stronê).
Pierwsza wersja (Tomasa) by³a kiepsko napisanym wy¶wietlaczem zbioru
Mandelbrota. Zosta³a zmodyfikowana przez Jana aby umo¿liwiaæ szybkie
powiêkszanie. Inne zmiany, zrobione pó¼niej to autopilot, zmiana
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
%configure \
	--with-x \
	--with-x11-driver=yes \
	%{?_without_aa:		--with-aa-driver=no} \
	%{?_without_ggi:	--with-ggi-driver=no} \
	%{?_without_ncurses:	--with-curses-driver=no} \
	%{?_without_svga:	--with-svga-driver=no}

%{__make}

cd doc
makeinfo --no-split xaos.texinfo
makeinfo --no-split xaosdev.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_applnkdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_datadir}/locale/{hu,es,fr,cs,de}/LC_MESSAGES

%{__make} install \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	LOCALEDIR=$RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}
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
%{_applnkdir}/XaoS.desktop
