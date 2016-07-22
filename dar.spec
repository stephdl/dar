#
# Specfile for DAR, the disk archiver
#
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=210790
#

# Static build is disabled by default by fedora policy, but also because the
# latest versions of glibc don't seem to compile proper static binaries.  Use
# "--with static" to enable the static subpackage
%define with_static %{?_with_static: 1} %{?!_with_static: 0}

#
# Basic descriptive tags for this package:
#
Name:           dar
Version:        2.5.2
Release:        1%{?dist}
Summary:        Software for making/restoring incremental CD/DVD backups

Group:          Applications/Archiving
License:        GPLv2+
URL:            http://dar.linux.free.fr/

################################################################################

Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        README.Fedora

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

################################################################################

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  libattr-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:	lzo-devel
BuildRequires:	libgcrypt-devel
Requires:       par2cmdline

################################################################################

%description
DAR is a command line tool to backup a directory tree and files. DAR is
able to make differential backups, split them over a set of disks or files
of a given size, use compression, filter files or subtrees to be saved or
not saved, directly access and restore given files. DAR is also able
to handle extented attributes, and can make remote backups through an
ssh session for example. Finally, DAR handles save and restore of hard
and symbolic links.

################################################################################

%package -n libdar
Group:      System Environment/Libraries
Summary:    Library providing support for the DAR API

%description -n libdar
Common library code for DAR.

################################################################################

%package -n libdar-devel
Group:      Development/Libraries
Summary:    Development files for libdar
Requires:   libdar = %{version}-%{release}

%description -n libdar-devel
This package contains the header files and libraries for developing
programs that use the DAR API (libdar).

################################################################################
# The following two subpackages are only built when enabled via "--with static"
################################################################################

%if %{with_static}

%package -n dar-static
Group:      Applications/System
Summary:    Statically linked version of dar

%description -n dar-static
Statically linked version of dar that can be installed onto backup disks for
easier file retrieval.

%package -n libdar-static-devel
Group:      Development/Libraries
Summary:    Statically linked dar library files

%description -nlibdar-static-devel
Statically linked version of dar libraries that can be installed onto backup
disks for easier file retrieval.

%endif

################################################################################

%prep
%setup -q

################################################################################

%build

# Options
%if %{with_static}
    STATIC=""
%else
    STATIC="--disable-dar-static --disable-static"
%endif

%configure --disable-build-html $STATIC

# Remove Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

################################################################################

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

# Remove the libtool archive files
rm -f  $RPM_BUILD_ROOT/%{_libdir}/*.la

# Delete the sample files that we can't seem to disable
rm -rf $RPM_BUILD_ROOT/%{_datadir}/dar/

# Remove the doc makefiles so they don't get installed along with the other files.
rm -f doc/Makefile*
rm -f doc/*/Makefile*

# Rename the documentation directory so it makes more sense after installation.
mv doc html

# Sample scripts should not be executable
chmod 0644 html/samples/*

# Install the fedora readme
cp -a %{SOURCE1} .

################################################################################

%clean
rm -rf $RPM_BUILD_ROOT

################################################################################

%post   -n libdar -p /sbin/ldconfig
%postun -n libdar -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc html/ AUTHORS ChangeLog COPYING NEWS README THANKS TODO README.Fedora

%{_bindir}/dar
%{_bindir}/dar_cp
%{_bindir}/dar_manager
%{_bindir}/dar_slave
%{_bindir}/dar_split
%{_bindir}/dar_xform
%config(noreplace) %{_sysconfdir}/darrc
%{_mandir}/man1/*

################################################################################

%files -n libdar
%defattr(-,root,root,-)
%{_libdir}/*.so.*

################################################################################

%files -n libdar-devel
%defattr(-,root,root,-)
%{_includedir}/dar/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

################################################################################

%if %{with_static}

%files -n dar-static
%defattr(-,root,root,-)
%{_bindir}/dar_static

################################################################################

%files -n libdar-static-devel
%defattr(-,root,root,-)
%{_libdir}/*.a

################################################################################
%endif

%changelog
* Mon Dec 07 2015 Luis Bazan <lbazan@fedoraproject.org> - 2.5.2-1
- New upstream version

* Tue Sep 15 2015 Luis Bazan <lbazan@fedoraproject.org> - 2.4.18-1
- new upstream version

* Tue Mar 10 2015 Luis Bazan <lbazan@fedoraproject.org> - 2.4.17-1
- new upstream version

* Mon Nov 03 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.15-2
- add pkgconfig

* Wed Sep 10 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.15-1
- new upstream version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.14-1
- new upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tomáš Mráz <tmraz@redhat.com> - 2.4.12-4
- Rebuild for new libgcrypt

* Wed Feb 05 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.12-3
- add config noreplace 

* Wed Feb 05 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.12-2
- fix changelog

* Tue Feb 04 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.12-1
- new upstream version

* Tue Feb 04 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.4.11-2
- Fix BZ# 1060412

* Tue Oct 29 2013 Luis Bazan <lbazan@fedoraproject.org> - 2.4.11-1
- New Upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Luis Bazan <lbazan@fedoraproject.org> - 2.4.10-2
- thanks echevemaster for help in this packages
- add requires needed to compile

* Wed May 22 2013 Luis Bazan <lbazan@fedoraproject.org> - 2.4.10-1
- New Upstream version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-9
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-7
- Rebuilt for glibc bug#747377

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.8-5
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> 2.3.8-2
- rebuild with new openssl

* Mon Aug 04 2008 Marcin Garski <mgarski[AT]post.pl> 2.3.8-1
- Update to 2.3.8 (#434519, #438953)
- Own dar's include directory
- Remove Rpath
- Update BR's

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.6-5
- fix license tag

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.6-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Chris Petersen <rpm@forevermore.net>                  2.3.6-3
- Add openssl requirement

* Sun Nov 18 2007 Chris Petersen <rpm@forevermore.net>                  2.3.6-2
- failed "make tag"

* Sun Nov 18 2007 Chris Petersen <rpm@forevermore.net>                  2.3.6-1
- Update to 2.3.6

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.3.4-2
- Rebuild for selinux ppc32 issue.

* Tue Jul 03 2007 Chris Petersen <rpm@forevermore.net>                  2.3.4-1
- Update to 2.3.4

* Mon May 28 2007 Chris Petersen <rpm@forevermore.net>                  2.3.3-1
- Update to 2.3.3
- Remove man.dar.patch, which was added upstream

* Wed Nov 15 2006 Chris Petersen <rpm@forevermore.net>                  2.3.1-4
- Change the main summary -- this is no longer a "collection of scripts"

* Tue Nov 14 2006 Chris Petersen <rpm@forevermore.net>                  2.3.1-3
- Fix/standardize Requires/Provides for libdar and libdar-devel
- Remove redundant zlib-devel (covered by openssl-devel)
- Update README.Fedora with my name/date, as requested in the ticket
- Add a patch to fix a funky character in man/dar.1

* Sat Nov 04 2006 Chris Petersen <rpm@forevermore.net>                  2.3.1-2
- Add README.Fedora explaining why we do not include static binaries (upstream's request)
- Add libdar-static-devel subpackage to hold the *.a files
- Disable static subpackages by default, enabled via "--with static" for those who want to compile them

* Thu May 11 2006 Chris Petersen <rpm@forevermore.net>                  2.3.1-1
- Initial package, compiled from half a dozen third party packages

