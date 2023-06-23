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
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order flake8-docstrings

Name:       python-%{pypi_name}
Version:    XXX
Release:    XXX
Summary:    Authentication Library for OpenStack Clients
License:    Apache-2.0
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
%{?python_provide:%python_provide python3-keystoneauth}

BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Identity Authentication Library

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

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove syntax tests
rm keystoneauth1/tests/unit/test_hacking_checks.py

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif


%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
# Disabling warning-is-error because of issue with python2 giving a warning:
# "The config value `apidoc_module_dir' has type `unicode', expected to ['str']."
%tox -e docs
rm -rf doc/build/html/.buildinfo
%endif

%check
%tox -e %{default_toxenv}

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
