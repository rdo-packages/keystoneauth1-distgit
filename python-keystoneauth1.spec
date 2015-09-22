%global pypi_name keystoneauth1

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-%{pypi_name}
Version:    1.0.0
Release:    1%{?dist}
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{pypi_name}
Source0:    http://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:  noarch

%description
Keystoneauth provides a standard way to do authentication and service requests
within the OpenStack ecosystem. It is designed for use in conjunction with
the existing OpenStack clients and for simplifying the process of writing
new clients.

%package -n     python2-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
Provides:       python-%{pypi_name} = %{version}-%{release}
Provides:       python-keystoneauth = %{version}-%{release}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-six
BuildRequires: python-pbr

Requires:      python-stevedore
Requires:      python-iso8601 >= 0.1.9
Requires:      python-oslo-config
Requires:      python-requests >= 2.5.2
Requires:      python-six => 1.9.0

%description -n python2-%{pypi_name}
Keystoneauth provides a standard way to do authentication and service requests
within the OpenStack ecosystem. It is designed for use in conjunction with
the existing OpenStack clients and for simplifying the process of writing
new clients.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
Provides:       python3-keystoneauth = %{version}-%{release}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 1.3
BuildRequires: python3-sphinx

Requires:      python3-stevedore
Requires:      python3-iso8601 >= 0.1.9
Requires:      python3-oslo-config
Requires:      python3-requests >= 2.5.2
Requires:      python3-six => 1.9.0


%description -n python3-%{pypi_name}
Keystoneauth provides a standard way to do authentication and service requests
within the OpenStack ecosystem. It is designed for use in conjunction with
the existing OpenStack clients and for simplifying the process of writing
new clients.
%endif

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
%setup -q -n %{pypi_name}-%{version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.egg-info
%endif


%files doc
%license LICENSE
%doc doc/build/html

%changelog
* Thu Sep 17 2015 Thomas Oulevey <thomas.oulevey@cern.ch> - 1.0.0-1
- Initial specfile
