# TODO: enable GTK+ UI when it becomes stable
#
# Conditional build:
%bcond_without	aalib	# without aalib output support
%bcond_without	ggi	# without ggi output support
%bcond_without	ncurses	# without ncurses output support
%bcond_without	svga	# without svga output support
#
Summary:	A fast, portable real-time interactive fractal zoomer
Summary(pl.UTF-8):	Szybki, przenośny i interaktywny eksplorator fraktali
Name:		XaoS
Version:	3.4
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/xaos/%{name}-%{version}.tar.gz
# Source0-md5:	366fd8151e9642a0d9afce889912e388
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-nosuid.patch
Patch1:		%{name}-ggi-fix.patch
Patch2:		%{name}-svga-fix.patch
Patch3:		%{name}-info.patch
URL:		http://xaos.theory.org/
%{?with_aalib:BuildRequires:		aalib-devel}
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	gettext-tools
%{?with_ggi:BuildRequires:		libggi-devel}
BuildRequires:	libpng-devel
%{?with_ncurses:BuildRequires:	ncurses-devel}
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	texinfo
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
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

%description -l pl.UTF-8
XaoS jest szybkim, przenośnym i interaktywnym eksploratorem fraktali.
Efekty jego działania można oglądać z użyciem drajwerów X11, aalib,
ncurses oraz SVGAlib. XaoS wyświetla zbiór Mandelbrota (i nie tylko) i
pozwala na płynne powiększanie/pomniejszanie widocznego zakresu.
Dostępne są różne rodzaje kolorowania dla punktów w wybranym zbiorze,
jak i poza nim. Dodatkowo, możliwe jest przełączanie między fraktalem
Mandelbrota, a odpowiadającym mu fraktalem Julii (i w drugą stronę).
Pierwsza wersja (Tomasa) była kiepsko napisanym wyświetlaczem zbioru
Mandelbrota. Została zmodyfikowana przez Jana aby umożliwiać szybkie
powiększanie. Inne zmiany, zrobione później to autopilot, zmiana
palety, zapisywanie PNG i inwersja fraktali.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# workaround for gettext 0.15 compatibility
touch src/i18n/POTFILES.in

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure \
	--with-x \
	--with-x11-driver=yes \
	%{!?with_aalib:--with-aa-driver=no} \
	%{!?with_ggi:--with-ggi-driver=no} \
	%{!?with_ncurses:--with-curses-driver=no} \
	%{!?with_svga:--with-svga-driver=no}

%{__make}

cd doc
makeinfo --no-split xaos.texinfo
makeinfo --no-split xaosdev.texinfo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%find_lang xaos

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f xaos.lang
%defattr(644,root,root,755)
%doc RELEASE_NOTES TODO doc/{AUTHORS,PROBLEMS,README{,.bugs,.ggi},SPONSORS,built-in_formulas.txt}
%attr(755,root,root) %{_bindir}/xaos
%dir %{_datadir}/XaoS
%dir %{_datadir}/XaoS/catalogs
%lang(cs) %{_datadir}/XaoS/catalogs/cesky.cat
%lang(de) %{_datadir}/XaoS/catalogs/deutsch.cat
%{_datadir}/XaoS/catalogs/english.cat
%lang(es) %{_datadir}/XaoS/catalogs/espanhol.cat
%lang(fr) %{_datadir}/XaoS/catalogs/francais.cat
%lang(it) %{_datadir}/XaoS/catalogs/italiano.cat
%lang(hu) %{_datadir}/XaoS/catalogs/magyar.cat
%lang(ro) %{_datadir}/XaoS/catalogs/romanian.cat
%{_datadir}/XaoS/examples
%{_datadir}/XaoS/help
%{_datadir}/XaoS/tutorial
%{_mandir}/man6/xaos.6*
%{_infodir}/xaos.info*
%{_pixmapsdir}/XaoS.png
%{_desktopdir}/XaoS.desktop
