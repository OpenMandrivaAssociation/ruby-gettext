%define name ruby-gettext
%define version 1.10.0
%define release %mkrel 1

Summary: Native Language Support Library and Tools for Ruby
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://ponx.s5.xrea.com/hiki/ruby-gettext.html
Source0: http://rubyforge-files.ruby-forum.com/gettext/%{name}-package-%{version}.tar.gz
License: GPL
Group: Development/Ruby
Requires: ruby >= 1.8.2
BuildRequires: ruby-devel gettext-devel ruby-racc ruby-rake

%description
Ruby GetText Package is Native Language Support Library and Tools whichi
modeled after GNU gettext package, but is not a wrapper of GNU GetText.

%prep
%setup -q -n %{name}-package-%{version} 
sed -i 's/0555/0755/' setup.rb

%build
ruby setup.rb config 
ruby setup.rb setup
rm -f samples/cgi/ruby.bat
cd test
sed -i /gettext_test_rails.rb/d test.sh
./test.sh

%install
rm -rf %buildroot
ruby setup.rb install --prefix=%buildroot
%find_lang %name --all-name 

for f in `find samples %buildroot -name \*.rb`
do
	if head -n1 "$f" | grep '^#!' >/dev/null;
	then
		sed -i 's|/usr/local/bin|/usr/bin|' "$f"
		chmod 0755 "$f"
	else
		chmod 0644 "$f"
	fi
done

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%{ruby_sitearchdir}/*
%{ruby_sitelibdir}/gettext*
%{_bindir}/*

%doc COPYING README samples test ChangeLog 

