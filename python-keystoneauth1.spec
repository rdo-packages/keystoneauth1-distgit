%global pypi_name keystoneauth1

%global common_desc \
Keystoneauth provides a standard way to do authentication and service requests \
within the OpenStack ecosystem. It is designed for use in conjunction with \
the existing OpenStack clients and for simplifying the process of writing \
new clients.

%if 0%{?fedora} >= 24  || 0%{?rhel} > 7
%global with_python3 1
%endif

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
%{?python_provide:%python_provide python2-%{pypi_name}}
%{?python_provide:%python_provide python2-keystoneauth}

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-six
BuildRequires: python2-pbr >= 2.0.0

# test requires
BuildRequires: python2-betamax >= 0.7.0
BuildRequires: python2-fixtures >= 1.3.1
BuildRequires: python2-mock
BuildRequires: python2-oslotest
BuildRequires: python2-oslo-config
BuildRequires: python2-oslo-utils
BuildRequires: python2-stestr
BuildRequires: python2-oauthlib
BuildRequires: python2-requests
BuildRequires: python2-os-service-types
BuildRequires: python2-stevedore
BuildRequires: python2-iso8601

%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: python2-pyyaml
BuildRequires: python2-lxml
BuildRequires: python2-requests-kerberos
BuildRequires: python2-requests-mock >= 1.1
BuildRequires: python2-pep8
%else
BuildRequires: PyYAML
BuildRequires: python-lxml
BuildRequires: python-requests-kerberos
BuildRequires: python-requests-mock >= 1.1
BuildRequires: python-pep8
%endif

Requires:      python2-iso8601 >= 0.1.11
Requires:      python2-os-service-types >= 1.2.0
Requires:      python2-pbr >= 2.0.0
Requires:      python2-requests >= 2.14.2
Requires:      python2-six => 1.10.0
Requires:      python2-stevedore >= 1.20.0

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
Provides:       python3-keystoneauth = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0

# test requres
BuildRequires: python3-betamax >= 0.7.0
BuildRequires: python3-fixtures >= 1.3.1
BuildRequires: python3-lxml
BuildRequires: python3-mock
BuildRequires: python3-requests-kerberos
BuildRequires: python3-requests-mock >= 1.1
BuildRequires: python3-oslo-config
BuildRequires: python3-oslotest
BuildRequires: python3-oslo-utils
BuildRequires: python3-stestr
BuildRequires: python3-oauthlib
BuildRequires: python3-requests
BuildRequires: python3-PyYAML
BuildRequires: python3-pep8
BuildRequires: python3-os-service-types
BuildRequires: python3-stevedore
BuildRequires: python3-iso8601

Requires:      python3-iso8601 >= 0.1.11
Requires:      python3-os-service-types
Requires:      python3-pbr >= 2.0.0
Requires:      python3-requests >= 2.14.2
Requires:      python3-six => 1.10.0
Requires:      python3-stevedore >= 1.20.0

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Identity Authentication Library

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-mox3

%description doc
Documentation for OpenStack Identity Authentication Library
%endif


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

%if 0%{?with_doc}
# generate html docs
%{__python} setup.py build_sphinx -b html
rm -rf doc/build/html/.buildinfo
%endif

%check
PYTHON=python2 stestr run
%if 0%{?with_python3}
PYTHON=python3 stestr-3 run
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

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/keystoneauth/commit/?id=0c34f0f8ff3964efdc27a1e7299683294d60535d
