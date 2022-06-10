%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name keystoneauth1

%global common_desc \
Keystoneauth provides a standard way to do authentication and service requests \
within the OpenStack ecosystem. It is designed for use in conjunction with \
the existing OpenStack clients and for simplifying the process of writing \
new clients.

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
%{?python_provide:%python_provide python3-%{pypi_name}}
%{?python_provide:%python_provide python3-keystoneauth}

BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-six
BuildRequires: python3-pbr >= 2.0.0

# test requires
BuildRequires: python3-betamax >= 0.7.0
BuildRequires: python3-fixtures >= 1.3.1
BuildRequires: python3-mock
BuildRequires: python3-oslotest
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-utils
BuildRequires: python3-stestr
BuildRequires: python3-oauthlib
BuildRequires: python3-requests
BuildRequires: python3-os-service-types
BuildRequires: python3-stevedore
BuildRequires: python3-iso8601
BuildRequires: python3-requests-mock >= 1.1

BuildRequires: python3-PyYAML
BuildRequires: python3-lxml
BuildRequires: python3-requests-kerberos

Requires:      python3-iso8601 >= 0.1.11
Requires:      python3-os-service-types >= 1.2.0
Requires:      python3-pbr >= 2.0.0
Requires:      python3-requests >= 2.14.2
Requires:      python3-six => 1.10.0
Requires:      python3-stevedore >= 1.20.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Identity Authentication Library

BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-apidoc
BuildRequires: python3-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Identity Authentication Library
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i '/sphinx.ext.intersphinx.*$/d'  doc/source/conf.py

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove syntax tests
rm keystoneauth1/tests/unit/test_hacking_checks.py

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
# Disabling warning-is-error because of issue with python2 giving a warning:
# "The config value `apidoc_module_dir' has type `unicode', expected to ['str']."
sphinx-build-3 -b html -d doc/build/doctrees doc/source doc/build/html
rm -rf doc/build/html/.buildinfo
%endif

%check
PYTHON=%{__python3} stestr-3 run

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
