%define		_modname	htscanner
%define		_status		alpha

Summary:	%{_modname} - htaccess support for PHP
Summary(pl):	%{_modname} - obs³uga htaccess dla PHP
Name:		php-pecl-%{_modname}
Version:	0.6.2
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	44e04cf7b396cbd48f7ccbe8e247a725
URL:		http://pecl.php.net/package/htscanner/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allow one to use htaccess-like file to configure PHP per directory,
just like Apache's htaccess. It is especially useful with fastcgi.

In PECL status of this extension is: %{_status}.

%description -l pl
Pakiet ten pozwala na wykorzystanie plików w stylu htaccess do
konfiguracji PHP per katalog, w sposób podobny do plików htaccess
Apache'a. Jest to szczególnie przydatne w przypadku korzystania z
fastcgi.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
%doc %{_modname}-%{version}/README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
