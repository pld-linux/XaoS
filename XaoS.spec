#
# Conditional build:
#
# _without_aa   		- without aalib output support
# _without_svga 		- without svga output support
# _without_ncurses 		- without ncurses output support
#
%ifnarch %{ix86} alpha
%define _without_svgalib 1
%endif
Summary:	A fast, portable real-time interactive fractal zoomer
Summary(pl):	Szybki, przeno¶ny i interaktywny explorator fraktali
Name:		XaoS
Version:	3.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/xaos/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-nosuid.patch
Patch1:		%{name}-brokenasm.patch
URL:		http://xaos.theory.org/
BuildRequires:	XFree86-devel
%{!?_without_aa:BuildRequires:		aalib-devel}
BuildRequires:	autoconf
BuildRequires:	libpng-devel
%{!?_without_ncurses:BuildRequires:	ncurses-devel}
%{!?_without_svga:BuildRequires:	svgalib-devel}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--with-x \
	--with-x11-driver=yes \
	%{?_without_aa:		--with-aa-driver=no} \
	%{?_without_ncurses:	--with-curses-driver=no} \
	%{?_without_svga:	--with-svga-driver=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/XaoS
install -d $RPM_BUILD_ROOT%{_datadir}/XaoS/tutorial
install -d $RPM_BUILD_ROOT%{_datadir}/XaoS/examples
install -d $RPM_BUILD_ROOT%{_datadir}/XaoS/catalogs
install -d $RPM_BUILD_ROOT%{_datadir}/XaoS/doc
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man6
install -d $RPM_BUILD_ROOT%{_infodir}
install -d $RPM_BUILD_ROOT%{_applnkdir}
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install bin/xaos $RPM_BUILD_ROOT%{_bindir}
install tutorial/*.x[ah]f $RPM_BUILD_ROOT%{_datadir}/XaoS/tutorial
install examples/* $RPM_BUILD_ROOT%{_datadir}/XaoS/examples
install catalogs/* $RPM_BUILD_ROOT%{_datadir}/XaoS/catalogs
install doc/xaos.6 $RPM_BUILD_ROOT%{_mandir}/man6
install doc/xaos.info $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc doc/{README,README.bugs,compilers.txt,ANNOUNCE,PROBLEMS,tutorial.txt}
%attr(755,root,root) %{_bindir}/xaos
%{_mandir}/man6/*
%{_infodir}/*.info*
%dir %{_datadir}/XaoS
%{_datadir}/XaoS/tutorial
%{_datadir}/XaoS/examples
%{_datadir}/XaoS/catalogs
%{_pixmapsdir}/XaoS.png
%{_applnkdir}/XaoS.desktop
