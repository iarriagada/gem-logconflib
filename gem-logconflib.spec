%define _prefix __auto__
%define gemopt opt
%define name gem-logconflib
%define version __auto__
%define release __auto__
%define repository gemini
%define debug_package %{nil}
# The line below is used so if the python script compilation fails,
# it doesn't terminate the rpm creation
%define _python_bytecompile_errors_terminate_build 0

Summary: %{name} Package: Gemini Log Configuration Library
Name: %{name}
Version: %{version}
Release: %{release}.%{dist}.%{repository}
License: GPL
## Source:%{name}-%{version}.tar.gz
Group: Gemini
Source0: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArch: %{arch}
#Prefix: %{_prefix}
## You may specify dependencies here
BuildRequires: gemini-top
Requires: gemini-top gemini-setup python3 rpm-build subversion
## Switch dependency checking off
# AutoReqProv: no

%description
Collection of python variables and methods to manage dynamic log configuration

## If you want to have a devel-package to be generated uncomment the following:
# %package devel
# Summary: %{name}-devel Package
# Group: Development/Gemini
# Requires: %{name}
# %description devel
# This is a default description for the %{name}-devel package

## Of course, you also can create additional packages, e.g for "doc". Just
## follow the same way as I did with "%package devel".

%prep
## Do some preparation stuff, e.g. unpacking the source with
%setup -n %{name}


%build
## Write build instructions here, e.g
# sh configure
# make

%install
## Write install instructions here, e.g
## install -D zzz/zzz  $RPM_BUILD_ROOT/%{_prefix}/zzz/zzz
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/local/lib/python3.6/site-packages/gemlogconflib/
install -D -m 644 lib/* $RPM_BUILD_ROOT/usr/local/lib/python3.6/site-packages/gemlogconflib/
#exit 0

## if you want to do something after installation uncomment the following
## and list the actions to perform:
#%post
## actions, e.g. /sbin/ldconfig

## If you want to have a devel-package to be generated and do some
## %post-stuff regarding it uncomment the following:
# %post devel

## if you want to do something after uninstallation uncomment the following
## and list the actions to perform. But be aware of e.g. deleting directories,
## see the example below how to do it:
%postun
if [ "$1" = "0" ]; then
    rm -rf /usr/local/lib/python3.6/site-packages/gemlogconflib
fi

## If you want to have a devel-package to be generated and do some
## %postun-stuff regarding it uncomment the following:
# %postun devel

## Its similar for %pre, %preun, %pre devel, %preun devel.
#%preun

%clean
## Usually you won't do much more here than
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
## list files that are installed here, e.g
## %{_prefix}/zzz/zzz
/usr/local/lib/python3.6/site-packages/gemlogconflib/*

## If you want to have a devel-package to be generated uncomment the following
# %files devel
# %defattr(-,root,root)
## list files that are installed by the devel package here, e.g
## %{_prefix}/zzz/zzz


%changelog
## Write changes here, e.g.
# * Thu Dec 6 2007 John Doe <jdoe@gemini.edu> VERSION-RELEASE
# - change made
# - other change made
* Sat Oct 9 2021 Ignacio Arriagada <ignacio.arriagada@noirlab.edu>
- Package created
