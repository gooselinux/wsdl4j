# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.5.2
Release:        7.8%{?dist}
Epoch:          0
Group:          Text Processing/Markup/XML
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
BuildArch:      noarch
Source0:        wsdl4j-%{version}-src-RHCLEAN.tar.gz
##cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j login
##cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j export -r wsdl4j-1_5_2 wsdl4j
Source1:        %{name}-MANIFEST.MF
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       jaxp_parser_impl, java
BuildRequires:  ant, ant-junit, java-devel
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows the
creation, representation, and manipulation of WSDL documents describing
services.  This codebase will eventually serve as a reference implementation
of the standard created by JSR110.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}-%{version}

%build
export OPT_JAR_LIST="ant/ant-junit junit"
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
ant -Dbuild.compiler=modern compile test javadocs

%install
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/%{name}.jar META-INF/MANIFEST.MF

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

for jar in %{name}.jar qname.jar ; do
	vjar=$(echo $jar | sed s+.jar+-%{version}.jar+g)
	install -m 644 build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/$vjar
	pushd $RPM_BUILD_ROOT%{_javadir}
	   ln -fs $vjar %{name}.jar
	popd
done

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc license.html
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-7.8
- Drop gcj_support.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.5.2-7.7
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-6.6
- Update OSGi manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-6.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-5.5
- Add osgi manifest for eclipse-dtp.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5jpp.3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.5.2-5jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.2
- Rebuild for ppc32 execmem issue and new build-id
- Add %%{?dist} as per new policy

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.1
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.5.2-3jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-3jpp_1fc
- Remove name/release/version defines as applicable.

* Tue Jul 18 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-2jpp
- Merge changes from fc.
- Add conditional native compilation.

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1jpp
- update to 1.5.2
- move qname*.jar to %{_javadir}/wsdl4j/qname*.jar
  to make place for qname provided by geronimo-specs

* Thu Jun 02 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.1-1jpp
- update to 1.5.1

* Fri Mar 11 2005 Ralph Apel <r.apel at r-apel.de> 0:1.5-1jpp
- update to 1.5

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Build with ant-1.6.2

* Thu Jun 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.4-2jpp
- Do not drop qname.jar

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.4-1jpp
- 1.4
- update for JPackage 1.5

* Sat Sep  7 2002 Ville Skytt� <ville.skytta at iki.fi> 1.1-1jpp
- First JPackage release.
