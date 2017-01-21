# TODO:
# - php (lib/php)
# - swift (lib/swift)
#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
#
Summary:	EmojiOne - complete open source emoji set
Summary(pl.UTF-8):	EmojiOne - pełny zbiór piktogramów emoji o otwartych źródłach
Name:		nodejs-emojione
Version:	2.2.7
Release:	1
License:	MIT (code), CC-BY v4.0 (artwork)
Group:		Libraries
#Source0Download: https://github.com/Ranks/emojione/releases
Source0:	https://github.com/Ranks/emojione/archive/v%{version}/emojione-%{version}.tar.gz
# Source0-md5:	0690ff19597b898a5c37fafb553863f8
URL:		https://github.com/Ranks/emojione
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
Requires:	nodejs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emoji One is a complete set of emojis designed for the web. It
includes libraries to easily convert unicode characters to shortnames
(:smile:) and shortnames to our custom emoji images. PNG and SVG
formats provided for the emoji images.

%description -l pl.UTF-8
Emoji One to pełny zbiór piktogramów emoji zaprojektowany dla WWW.
Zawiera biblioteki łatwo konwertujące znaki unikodowe na krótkie nazwy
(:smile:) i krótkie nazwy na załączone obrazki emoji. Załączone są
piktogramy w formatach PNG i SVG.

%package -n python-emojipy
Summary:	Python 2 library for working with emoji
Summary(pl.UTF-8):	Biblioteka Pythona 2 do pracy z piktogramami emoji
Group:		Development/Languages/Python
Requires:	python-modules >= 1:2.7
Requires:	python-six

%description -n python-emojipy
Python 2 library for working with emoji.

%description -n python-emojipy -l pl.UTF-8
Biblioteka Pythona 2 do pracy z piktogramami emoji.

%package -n python3-emojipy
Summary:	Python 3 library for working with emoji
Summary(pl.UTF-8):	Biblioteka Pythona 3 do pracy z piktogramami emoji
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.4
Requires:	python3-six

%description -n python3-emojipy
Python 3 library for working with emoji.

%description -n python3-emojipy -l pl.UTF-8
Biblioteka Pythona 3 do pracy z piktogramami emoji.

%prep
%setup -q -n emojione-%{version}

%build
cd lib/python
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/emojione/lib/{js,emojione-awesome}

cp -pr assets $RPM_BUILD_ROOT%{nodejs_libdir}/emojione
cp -pr lib/meteor $RPM_BUILD_ROOT%{nodejs_libdir}/emojione/lib
cp -p lib/js/*.js $RPM_BUILD_ROOT%{nodejs_libdir}/emojione/lib/js
cp -p emoji*.json package.json $RPM_BUILD_ROOT%{nodejs_libdir}/emojione

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd lib/python
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install

# only build time, requires cog module
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/emojipy/create_ruleset.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%{nodejs_libdir}/emojione
%{_examplesdir}/%{name}-%{version}

%if %{with python2}
%files -n python-emojipy
%defattr(644,root,root,755)
%doc lib/python/README.md
%{py_sitescriptdir}/emojipy
%{py_sitescriptdir}/emojipy-0.1-py*.egg-info
%endif

%if %{with python3}
%files -n python3-emojipy
%defattr(644,root,root,755)
%doc lib/python/README.md
%{py3_sitescriptdir}/emojipy
%{py3_sitescriptdir}/emojipy-0.1-py*.egg-info
%endif
