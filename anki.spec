%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		anki
Version:	1.2.11
Release:	2
Summary:	Flashcard program for using space repetition learning

Group:		Education
# the file anki-%%{version}/libanki/anki/features/chinese/unihan.db 
# was created out of  Unihan.txt from www.unicode.org (MIT license)
License:	GPLv3+ and MIT
URL:		http://ankisrs.net/
Source0:	http://anki.googlecode.com/files/%{name}-%{version}.tgz
Source1:	anki.svg

# Config change: don't check for new updates.
Patch0:		anki-1.0-noupdate.patch
BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
BuildRequires:	python2-sqlalchemy
BuildRequires:	desktop-file-utils, PyQt4, python-simplejson
Requires:	qt4-common, python-qt4
Requires:	python-sqlalchemy, python-simplejson, python-sqlite2
Requires:	python-matplotlib
Requires:	pygame, python-beautifulsoup
Requires:	pyaudio, sox
BuildArch:	noarch

%description
Anki is a program designed to help you remember facts (such as words
and phrases in a foreign language) as easily, quickly and efficiently
as possible. Anki is based on a theory called spaced repetition.

%prep
%setup -q
%patch0 -F 9 -p1 -b .noupdate
%{__sed} -i -e '/^#!\//, 1d' ankiqt/ui/dropbox.py

%build
pushd libanki
%{__python2} setup.py build
popd

%{__python2} setup.py build


%install
pushd libanki
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --remove-category=KDE \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

install -d %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/

find %{buildroot} -type f -o -type l|sed '
s:'"%{buildroot}"'::
s:\(.*/lib/python2\..*/site-packages/ankiqt/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
s:\(.*/lib/python2\..*/site-packages/anki/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
s:^\([^%].*\)::
s:%lang(C) ::
/^$/d' > anki.lang


%files -f %{name}.lang
%doc ChangeLog
%doc COPYING CREDITS README*
# libankiqt
%dir %{python2_sitelib}/ankiqt
%{python2_sitelib}/ankiqt/*.py*
%{python2_sitelib}/ankiqt/ui
%{python2_sitelib}/ankiqt/forms

# libanki
%dir %{python2_sitelib}/anki
%{python2_sitelib}/anki/*.py*
%{python2_sitelib}/anki/importing
%{python2_sitelib}/anki/template

# locale
%dir %{python2_sitelib}/ankiqt/locale/
%dir %{python2_sitelib}/ankiqt/locale/*
%dir %{python2_sitelib}/ankiqt/locale/*/LC_MESSAGES
%dir %{python2_sitelib}/anki/locale/
%dir %{python2_sitelib}/anki/locale/*
%dir %{python2_sitelib}/anki/locale/*/LC_MESSAGES

%{python2_sitelib}/*egg-info
%{_bindir}/anki
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg


