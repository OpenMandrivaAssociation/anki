%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		anki
Version:	1.2.9
Release:	%mkrel 1
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
# Avoid unicode error message on startup
Patch1:		anki-1.2.9-unicode.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	python-devel, python-setuptools, python-sqlalchemy
BuildRequires:	desktop-file-utils, PyQt4, python-simplejson
Requires:	qt4, PyQt4
Requires:	python-sqlalchemy, python-simplejson, python-sqlite2
Requires:	python-matplotlib
Requires:	pygame, python-BeautifulSoup
Requires:	pyaudio, sox
BuildArch:	noarch

%description
Anki is a program designed to help you remember facts (such as words
and phrases in a foreign language) as easily, quickly and efficiently
as possible. Anki is based on a theory called spaced repetition.

%prep
%setup -q
%patch0 -F 9 -p1 -b .noupdate
%patch1 -p1 -b .unicode
%{__sed} -i -e '/^#!\//, 1d' ankiqt/ui/dropbox.py

%build
pushd libanki
%{__python} setup.py build
popd

%{__python} setup.py build


%install
rm -rf %{buildroot}
pushd libanki
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

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



%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog
%doc COPYING CREDITS README*
# libankiqt
%dir %{python_sitelib}/ankiqt
%{python_sitelib}/ankiqt/*.py*
%{python_sitelib}/ankiqt/ui
%{python_sitelib}/ankiqt/forms

# libanki
%dir %{python_sitelib}/anki
%{python_sitelib}/anki/*.py*
%{python_sitelib}/anki/importing
%{python_sitelib}/anki/template

# locale
%dir %{python_sitelib}/ankiqt/locale/
%dir %{python_sitelib}/ankiqt/locale/*
%dir %{python_sitelib}/ankiqt/locale/*/LC_MESSAGES
%dir %{python_sitelib}/anki/locale/
%dir %{python_sitelib}/anki/locale/*
%dir %{python_sitelib}/anki/locale/*/LC_MESSAGES

%{python_sitelib}/*egg-info
%{_bindir}/anki
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
