%global pypi_name keystoneauth1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    http://tarballs.openstack.org/keystoneauth/keystoneauth-master.tar.gz

BuildArch:  noarch

Provides:      python-keystoneauth

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-six
BuildRequires: python-pbr >= 1.6.0

Requires:      python-stevedore >= 1.5.0
Requires:      python-iso8601 >= 0.1.9
Requires:      python-oslo-config
Requires:      python-requests >= 2.5.2
Requires:      python-six => 1.9.0
Requires:      python-argparse
Requires:      python-positional >= 1.0.1

%description
Keystoneauth provides a standard way to do authentication and service requests 
within the OpenStack ecosystem. It is designed for use in conjunction with 
the existing OpenStack clients and for simplifying the process of writing 
new clients.

%package doc
Summary:    Documentation for OpenStack Identity Authentication Library

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: python-mock
BuildRequires: python-pep8
BuildRequires: python-requests
BuildRequires: python-requests-mock
BuildRequires: python-mox3
BuildRequires: python-oslo-config
BuildRequires: python-stevedore
BuildRequires: python-iso8601
BuildRequires: python-fixtures

%description doc
Documentation for OpenStack Identity Authentication Library

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%check
%{__python2} setup.py test

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc doc/build/html

%changelog
