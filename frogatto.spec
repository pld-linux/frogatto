Summary:	An open-source "platformer" game
Name:		frogatto
Version:	1.1.1
Release:	7
License:	GPL v3+
Group:		X11/Applications/Games
Source0:	http://www.frogatto.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	bf5a2ee4c3254a424766895ff250758b
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-assertion.patch
Patch2:		%{name}-libpng15.patch
Patch3:		%{name}-no_fbo_assert.patch
URL:		http://www.frogatto.com/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel >= 1.2.7
BuildRequires:	SDL_image-devel >= 1.2.0
BuildRequires:	SDL_mixer-devel >= 1.2.0
BuildRequires:	SDL_ttf-devel >= 2.0.8
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	ccache
BuildRequires:	glew-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Frogatto is an open-source "platformer" game, which means you're given
a cross-section view into the world, and you help a small green fellow
named Frogatto walk and jump between solid footholds whilst you lead
him through his story. There's a long history to the genre, so just by
being in it we inevitably have a lot in common with other games,
however, we're not trying to clone any specific game.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix linking with our boost libs
%{__sed} -i 's,-mt,,g' Makefile

# set proper paths
%{__sed} -i 's,data/,%{_datadir}/frogatto/data/,g' `find -name "*.[ch]pp" -o -name "*.po*" -o -name "*.cfg"`
%{__sed} -i 's,./images/,%{_datadir}/frogatto/images/,g' `find -name "*.cpp"`
%{__sed} -i 's,./locale/,%{_datadir}/locale/,g' src/i18n.cpp
%{__sed} -i 's,music/,%{_datadir}/frogatto/music/,g' src/sound.cpp
%{__sed} -i 's,sounds/,%{_datadir}/frogatto/sounds/,g' src/sound.cpp

%build
%{__make} \
	CXX="%{__cxx}" \
	OPT="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/frogatto,%{_datadir}/locale}

cp -a game $RPM_BUILD_ROOT%{_bindir}/frogatto
cp -a data $RPM_BUILD_ROOT%{_datadir}/frogatto
cp -a images $RPM_BUILD_ROOT%{_datadir}/frogatto
cp -a locale/* $RPM_BUILD_ROOT%{_datadir}/locale
cp -a music $RPM_BUILD_ROOT%{_datadir}/frogatto
cp -a sounds $RPM_BUILD_ROOT%{_datadir}/frogatto

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGELOG
%attr(755,root,root) %{_bindir}/frogatto
%{_datadir}/frogatto
