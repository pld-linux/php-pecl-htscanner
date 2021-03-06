%define		php_name	php%{?php_suffix}
%define		modname	htscanner
%define		status		stable
Summary:	%{modname} - PHP module to emulate .htaccess support in PHP engine
Summary(pl.UTF-8):	%{modname} - moduł PHP do emulacji obsługi .htaccess w silniku PHP
Name:		%{php_name}-pecl-htscanner
Version:	1.0.1
Release:	8
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/htscanner-%{version}.tgz
# Source0-md5:	7fbef47361933fd932a2ff8f44849f0e
URL:		http://pecl.php.net/package/htscanner/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-htscanner < 1.0.1-7
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

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Przy używaniu PHP w wersji CGI (zwykłej CGI lub Fast-CGI) Apache nie
może przekazać ustawień PHP z plików htaccess. Można to rozwiązać
dając każdemu użytkownikowi własny plik php.ini, ale nie wszystkim to
rozwiązanie odpowiada.

To rozszerzenie analizuje wspomniane pliki konfiguracyjne (w
większości przypadków .htaccess) i zmienia ustawienia. Szuka pliku
konfiguracyjnego we kwszystkich katalogach od głównego (DocumentRoot)
co katalogu zawierającego żadane skrypty.

To rozszerzenie ma w PECL status: %{status}.

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
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
