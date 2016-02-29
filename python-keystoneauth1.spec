%global pypi_name keystoneauth1

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    2.1.0
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

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-six
BuildRequires: python-pbr

# test requres
BuildRequires: python-betamax
BuildRequires: python-lxml
BuildRequires: python-requests-kerberos
BuildRequires: python-testrepository
BuildRequires: python-oslotest
BuildRequires: python-oslo-utils

Requires:      python-argparse
Requires:      python-iso8601 >= 0.1.9
Requires:      python-pbr >= 1.6.0
Requires:      python-requests >= 2.9.1
Requires:      python-six => 1.9.0
Requires:      python-stevedore >= 1.5.0

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

# test requres
BuildRequires: python3-betamax
BuildRequires: python3-fixtures >= 1.3.1
BuildRequires: python3-lxml
BuildRequires: python3-testrepository
BuildRequires: python3-oslotest
BuildRequires: python3-oslo-utils

Requires:      python3-argparse
Requires:      python3-iso8601 >= 0.1.9
Requires:      python3-pbr >= 1.6.0
Requires:      python3-requests >= 2.9.1
Requires:      python3-six => 1.9.0
Requires:      python3-stevedore >= 1.5.0

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
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i '/sphinx.ext.intersphinx.*$/d'  doc/source/conf.py

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# generate html docs
%{__python} setup.py build_sphinx
rm -rf doc/build/html/.buildinfo

%check
%{__python2} setup.py testr
%if 0%{?with_python3}
# cleanup testrepository
rm -rf .testrepository
%{__python3} setup.py testr
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
* Fri Feb 05 2016 Paul Belanger <pabelanger@redhat.com> - 2.1.0-1
- New upstream 2.1.0 release
- Disable intersphinx to disable downloads from the internet at build time
- Clean up build and requires dependencies
- Switch to python setup.py build_sphinx since this is what upstream uses

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 07 2015 Alan Pevec <alan.pevec@redhat.com> 1.1.0-2
- fix tests (Lukas Bezdicka)

* Tue Oct 06 2015 Alan Pevec <alan.pevec@redhat.com> 1.1.0-1
- Update to upstream 1.1.0

* Thu Sep 17 2015 Thomas Oulevey <thomas.oulevey@cern.ch> - 1.0.0-1
- Initial specfile
