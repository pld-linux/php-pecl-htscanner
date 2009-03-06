%define		_modname	htscanner
%define		_status		alpha
Summary:	PHP Module to emulate .htaccess support in PHP engine
Summary(pl.UTF-8):	Moduł PHP do emulacji obsługi .htaccess w silniku PHP
Name:		php-pecl-htscanner
Version:	0.9.0
Release:	1
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/htscanner-%{version}.tgz
# Source0-md5:	ad8f28e4cdfec6d3a5a990e1531a1a12
URL:		http://pecl.php.net/package/htscanner
BuildRequires:	php-devel >= 3:5.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-htscanner
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
When using a CGI version of PHP (plain old CGI or Fast-CGI) Apache
can't pass any PHP settings from htaccess files it parses. This can be
solved by giving each user it's own php.ini file, but I didn't like
that solution.

This extension parses these configuration files (in most cases
.htaccess) and changes the settings. It will search all directories
for a configuration file from the docroot until the directory where
the request scripts is found.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Przy używaniu PHP w wersji CGI (zwykłej CGI lub Fast-CGI) Apache nie
może przekazać ustawień PHP z plików htaccess. Można to rozwiązać
dając każdemu użytkownikowi własny plik php.ini, ale nie wszystkim to
rozwiązanie odpowiada.

To rozszerzenie analizuje wspomniane pliki konfiguracyjne (w
większości przypadków .htaccess) i zmienia ustawienia. Szuka pliku
konfiguracyjnego we kwszystkich katalogach od głównego (DocumentRoot)
co katalogu zawierającego żadane skrypty.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -n htscanner-%{version}

%build
phpize
%configure \
	--enable-htscanner
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so

;htscanner.config_file		= .htaccess
;htscanner.default_docroot	= /
;htscanner.default_ttl		= 300
;htscanner.stop_on_error	= 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
