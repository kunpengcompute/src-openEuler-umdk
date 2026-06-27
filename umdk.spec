# SPDX-License-Identifier: MIT
# Copyright (c) Huawei Technologies Co., Ltd. 2021-2025. All rights reserved.

# add --with asan option, i.e. disable asan by default
%bcond_with asan

# add --with tsan option, i.e. disable tsan by default
%bcond_with tsan

# add --with gcov option, i.e. disable gcov by default
%bcond_with gcov

# add --with test option, i.e. disable test by default
%bcond_with test

# add --with ubagg_disable option, i.e. enable ubagg by default
%bcond_with ubagg_disable

# add --with release_enable option, i.e. disable release by default
%bcond_with release_enable

# add --with urma option, i.e. disable urma by default
%bcond_with urma

# add --with ums option, i.e. disable ums by default
%bcond_with ums

# add --with urpc option, i.e. disable urpc by default
%bcond_with urpc

# add --with dlock option, i.e. disable dlock by default
%bcond_with dlock

# add --with extra_ubcore_symbols option, i.e. disable by default
%bcond_with extra_ubcore_symbols

%ifarch aarch64
%define with_64kb  %{?_with_64kb: 1} %{?!_with_64kb: 0}
%else
%define with_64kb  0
%endif

%if %{with_64kb}
%define kernel_devel_pkg kernel-64k-devel
%define ums_suffix -64kb
%define ums_summary kmod file of UMS (64KB page size)
%define ums_desc UMS kernel module for transparent TCP acceleration via shared memory over UB
%define ums_conflict umdk-ums
%define ums_kernel_req kernel-64k
%else
%define kernel_devel_pkg kernel-devel
%define ums_suffix %{nil}
%define ums_summary kmod file of ums
%define ums_desc UMS kernel module for transparent TCP acceleration via shared memory over UB
%define ums_conflict umdk-ums-64kb
%define ums_kernel_req kernel
%endif

%define build_all 1

%if %{with ums} || %{with urma} || %{with urpc} || %{with dlock}
    %define build_all 0
%endif

%if %{defined kernel_version}
    %define kernel_build_path /lib/modules/%{kernel_version}/build
%else
    %define kernel_version %(
        KERNEL_DEVEL_COUNT=$(rpm -qa %{kernel_devel_pkg} 2>/dev/null | wc -l);
        if [ "$KERNEL_DEVEL_COUNT" -eq 1 ]; then
            rpm -q --qf '%%{VERSION}-%%{RELEASE}.%%{ARCH}' %{kernel_devel_pkg} 2>/dev/null;
        else
            uname -r;
        fi
    )
    %define kernel_build_path /lib/modules/%{kernel_version}/build
%endif
%define kernel_requires_version %(echo %{kernel_version} | awk -F"." 'OFS="."{$NF="";print}' | sed 's/\.$//g')

%if %{undefined rpm_release}
    %define rpm_release B015
%endif

Name          : umdk
Summary       : Unified memory development kit
Version       : 26.06.0
Release       : %{rpm_release}%{?dist}
Group         : umdk
License       : MIT
Vendor        : Huawei Technologies Co., Ltd
Source0       : %{name}-%{version}.tar.gz
BuildRoot     : %{_buildirootdir}/%{name}-%{version}-build
buildArch     : x86_64 aarch64
ExclusiveArch : aarch64

BuildRequires : rpm-build, make, cmake, gcc, gcc-c++, glibc-devel, libummu-devel
%if %{build_all} || %{with ums}
BuildRequires : %{kernel_devel_pkg}
%endif
Requires: glibc, glib2, libummu
%if %{with asan}
Requires: libasan
%endif
%if %{with tsan}
Requires: libtsan
%endif
%if %{build_all}
Requires: umdk-urma-lib = %{version}
Requires: umdk-urma-devel = %{version}
Requires: umdk-urma-tools = %{version}
Requires: umdk-urma-bin = %{version}
Requires: umdk-urpc-framework = %{version}
Requires: umdk-urpc-framework-devel = %{version}
Requires: umdk-urpc-framework-tools = %{version}
Requires: umdk-urpc-umq = %{version}
Requires: umdk-urpc-umq-devel = %{version}
Requires: umdk-urpc-umq-tools = %{version}
Requires: umdk-dlock-lib = %{version}
Requires: umdk-dlock-devel = %{version}
Requires: umdk-ums-kmod = %{version}
Requires: umdk-ums-tools = %{version}
Requires: umdk-ums-agent = %{version}
%files
%endif

%description
A new system interconnect architecture

%if %{build_all} || %{with urma} || %{with urpc}
%package urma-lib
Requires:       libummu
Summary:        Basic URMA libraries of UMDK

%description urma-lib
This package contains basic URMA libraries of UMDK, such as liburma.so.

%package urma-devel
Summary:        Include Files and Libraries mandatory for URMA
AutoReqProv:    on

%description urma-devel
This package contains all necessary include files and libraries needed
to develop applications that require the provided includes and
libraries.

%package urma-tools
Summary:        tools of urma
Requires:       umdk-urma-lib = %{version}
%description urma-tools
tools of urma, contains  urma_perftest, urma_admin, urma_ping.

%package urma-bin
Summary:        binary file of urma
Requires:       glibc
%description urma-bin
binary file of urma

%package urma-example
Summary:        UMDK examples
Requires:       umdk-urma-lib = %{version}
AutoReqProv:    on
%description urma-example
This package contains all the executable examples of UMDK.

%if %{with test}
%package urma-test
Summary:        Include Libraries for URMA test
Requires:       umdk-urma-lib = %{version}
AutoReqProv:    on
%description urma-test
This package contains all necessary libraries needed
to develop applications based on urma_test.
%endif
%endif

%if %{build_all} || %{with urpc}
%package urpc-framework
Summary:        URPC framework shared library
BuildRequires:  openssl-devel
Requires:       umdk-urma-lib
%description urpc-framework
This package contains the URPC framework shared libraries (e.g. liburpc.so).

%package urpc-umq
Summary:        URPC umq shared library
BuildRequires:  openssl-devel
Requires:       umdk-urma-lib
%description urpc-umq
This package contains the URPC umq shared libraries (e.g. libumq.so).

%package urpc-framework-devel
Summary:        URPC framework development headers
Requires:       umdk-urpc-framework = %{version}
AutoReqProv:    on
%description urpc-framework-devel
This package contains all necessary headers for URPC framework development.

%package urpc-umq-devel
Summary:        UMQ development headers
Requires:       umdk-urpc-umq = %{version}
AutoReqProv:    on
%description urpc-umq-devel
This package contains all necessary headers for UMQ development.

%package urpc-framework-example
Summary:        URPC framework example
Requires:       umdk-urma-lib umdk-urpc-framework-devel = %{version}
AutoReqProv:    on
%description urpc-framework-example
This package contains example for URPC framework.

%package urpc-umq-example
Summary:        UMQ example
Requires:       umdk-urma-lib umdk-urpc-umq-devel = %{version}
AutoReqProv:    on
%description urpc-umq-example
This package contains example for URPC umq.

%package urpc-framework-tools
Summary:        URPC framework tools
Requires:       umdk-urma-lib umdk-urpc-framework-devel = %{version}
AutoReqProv:    on
%description urpc-framework-tools
This package contains urpc_admin and related URPC framework tools.

%package urpc-umq-tools
Summary:        UMQ tools
Requires:       umdk-urma-lib umdk-urpc-umq-devel = %{version}
AutoReqProv:    on
%description urpc-umq-tools
This package contains umq_perftest and related UMQ tools.
%endif

%if %{build_all} || %{with dlock}
%package dlock-lib
Summary:        Library files of dlock
BuildRequires:  openssl-devel
Requires:       umdk-urma-lib = %{version}

%description dlock-lib
This package contains the libdlock*.so files for the distributed lock feature.

%package dlock-devel
Summary:        Include development libraries and headers for dlock
Requires:       umdk-dlock-lib = %{version}
AutoReqProv:    on

%description dlock-devel
This package contains all necessary include files and libraries needed
to develop applications based on dlock.

%package dlock-example
Summary:        Executable examples of dlock
Requires:       umdk-dlock-lib = %{version}
AutoReqProv:    on

%description dlock-example
This package contains all the executable examples of dlock.
%endif

%if %{build_all} || %{with ums}
%package ums%{ums_suffix}
Summary:        %{ums_summary}
BuildRequires:  glib2-devel, libnl3-devel, %{kernel_devel_pkg}
Requires:       glib2, libnl3, %{ums_kernel_req}
Provides:       umdk-ums-kmod = %{version}
Conflicts:      %{ums_conflict}
%description ums%{ums_suffix}
%{ums_desc}

%package ums-tools
Summary:        tools of ums
%description ums-tools
tools of ums, contains ums_run

%package ums-agent
Summary:        UMS Agent daemon for secure token exchange
BuildRequires:  systemd-devel, glib2-devel, libnl3-devel, openssl-devel, keyutils-libs-devel
Requires:       systemd-libs, glib2, libnl3, openssl, keyutils
Requires(pre):  shadow-utils
%description ums-agent
UMS Agent is a user-space daemon for secure TokenValue exchange
between UMS kernel modules via TLS 1.3 channel.
%endif

%prep
%autosetup -c -n %{name}-%{version} -p1

%build
    cmake ./src/ -DCMAKE_INSTALL_PREFIX=/usr\
    -DBUILD_DATE=%{rpm_build_date} \
%if %{with asan}
    -DASAN="enable" \
%endif
%if %{with tsan}
    -DTSAN="enable" \
%endif
%if %{with gcov}
    -DCODE_COVERAGE="enable" \
%endif
%if %{with release_enable}
    -DRELEASE_ENABLE="enable" \
%endif
%if %{with test}
    -DURMA_TEST="enable" \
    -DRELEASE_ENABLE="disable" \
%endif
%if %{defined kernel_version}
    -DKERNEL_RELEASE=%{kernel_version} \
    -DKERNEL_PATH=%{kernel_build_path} \
%endif
%if %{without ubagg_disable}
    -DUB_AGG="enable" \
%endif
%if %{with dfx_tool}
    -DDFX_TOOL="enable" \
%endif
%if %{build_all}
    -DBUILD_ALL="enable" \
%else
    -DBUILD_ALL="disable" \
%endif
%if %{build_all} || %{with urma} || %{with urpc}
    -DBUILD_URMA="enable" \
%else
    -DBUILD_URMA="disable" \
%endif
%if %{with ums}
    -DBUILD_UMS="enable" \
%endif
%if %{build_all} || %{with urpc}
    -DBUILD_URPC="enable" \
%else
    -DBUILD_URPC="disable" \
%endif
%if %{with dlock}
    -DBUILD_DLOCK="enable" \
%endif
%if %{without udma_stb64_disable}
    -DUDMA_ST64B="enable" \
%endif

%if %{with extra_ubcore_symbols}
    -DBUILD_EXTRA_UBCORE_SYMBOLS="enable" \
%endif

make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if %{with gcov}
    mkdir -p %{buildroot}/var/lib/umdk/gcov/%{name}
    find %{_builddir} -name '*.gcno' -exec cp --parents {} %{buildroot}/var/lib/umdk/gcov/%{name} \;
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{build_all} || %{with urma} || %{with urpc}
%files urma-lib
%defattr(-,root,root)
    %{_libdir}/liburma.so.*
    %{_libdir}/liburma_common.so.*
    %{_libdir}/urma/liburma_ubagg.so.*
    %{_libdir}/urma/liburma-udma.so
    /etc/rsyslog.d/urma.conf
    /etc/logrotate.d/urma

%post urma-lib
if [ -x %{_bindir}/systemctl ] && [ -x %{_sbindir}/rsyslogd ]; then
    %{_bindir}/systemctl restart rsyslog >/dev/null  2>&1
fi

%files urma-devel
%defattr(-,root,root)
    %{_libdir}/liburma.so
    %{_libdir}/liburma_common.so
    %{_libdir}/urma/liburma_ubagg.so
    %{_libdir}/urma/liburma-udma.so
    %dir %{_includedir}/ub/umdk/urma
    %dir %{_includedir}/ub/umdk/urma/udma
    %{_includedir}/ub/umdk/urma/urma_*.h
    %{_includedir}/ub/umdk/urma/uvs_api.h
    %{_includedir}/ub/umdk/urma/uvs_types.h
    %{_includedir}/ub/umdk/urma/udma/udma_u_ctl.h
%if %{with gcov}
    %dir /var/lib/umdk/gcov/%{name}
    /var/lib/umdk/gcov/%{name}/
%endif

%pre urma-tools
if [ -d /usr/bin/urma_admin ] && [ ! -L  /usr/bin/urma_admin ];then
    rm -rf /usr/bin/urma_admin
fi

%files urma-tools
%defattr(-,root,root)
    %{_bindir}/urma_admin
    /etc/rsyslog.d/urma_admin.conf
    %{_bindir}/urma_perftest
    %{_bindir}/urma_ping

%post urma-tools
if [ -x %{_bindir}/systemctl ] && [ -x %{_sbindir}/rsyslogd ]; then
    %{_bindir}/systemctl restart rsyslog >/dev/null  2>&1
fi

%files urma-bin
%defattr(-,root,root)
    /etc/rsyslog.d/tpsa.conf
    /etc/logrotate.d/tpsa
    %{_libdir}/libtpsa.so
    %{_libdir}/libtpsa.so.*
%post urma-bin
if [ -x %{_bindir}/systemctl ]; then
    %{_bindir}/systemctl daemon-reload >/dev/null  2>&1
fi
if [ -x %{_bindir}/systemctl ] && [ -x %{_sbindir}/rsyslogd ]; then
    %{_bindir}/systemctl restart rsyslog >/dev/null  2>&1
fi

%files urma-example
%defattr(-,root,root)
    %{_bindir}/urma_sample
    %dir %{_docdir}/umdk-examples
    %dir %{_docdir}/umdk-examples/urma_example
    %{_docdir}/umdk-examples/urma_example/README.md
%endif

%if %{build_all} || %{with urpc}
%files urpc-framework
%defattr(-,root,root)
    %{_libdir}/liburpc_framework.so.*
    /etc/rsyslog.d/urpc_framework.conf
    /etc/logrotate.d/urpc_framework

%files urpc-umq
%defattr(-,root,root)
    %{_libdir}/libumq.so.*
    %{_libdir}/libumq_buf.so.*
    %{_libdir}/libumq_ub.so.*
    /etc/rsyslog.d/umq.conf
    /etc/logrotate.d/umq

%files urpc-framework-devel
%defattr(-,root,root)
    %{_libdir}/liburpc_framework.so
    %dir %{_includedir}/ub
    %dir %{_includedir}/ub/umdk
    %dir %{_includedir}/ub/umdk/urpc
    %{_includedir}/ub/umdk/urpc/urpc_framework_api.h
    %{_includedir}/ub/umdk/urpc/urpc_framework_types.h
    %{_includedir}/ub/umdk/urpc/urpc_framework_errno.h

%files urpc-umq-devel
%defattr(-,root,root)
    %{_libdir}/libumq.so
    %{_libdir}/libumq_buf.so
    %{_libdir}/libumq_ub.so
    %dir %{_includedir}/ub
    %dir %{_includedir}/ub/umdk
    %dir %{_includedir}/ub/umdk/urpc
    %dir %{_includedir}/ub/umdk/urpc/umq
    %{_includedir}/ub/umdk/urpc/umq/umq_api.h
    %{_includedir}/ub/umdk/urpc/umq/umq_errno.h
    %{_includedir}/ub/umdk/urpc/umq/umq_pro_api.h
    %{_includedir}/ub/umdk/urpc/umq/umq_pro_types.h
    %{_includedir}/ub/umdk/urpc/umq/umq_types.h
    %{_includedir}/ub/umdk/urpc/umq/umq_dfx_api.h
    %{_includedir}/ub/umdk/urpc/umq/umq_dfx_types.h

%files urpc-framework-example
%defattr(-,root,root)
    %{_bindir}/urpc_framework_example
    %dir %{_docdir}/umdk-examples/urpc_example/urpc_framework_example

%files urpc-umq-example
%defattr(-,root,root)
    %{_bindir}/umq_example
    %dir %{_docdir}/umdk-examples/urpc_example/umq_example

%files urpc-framework-tools
%defattr(-,root,root)
    %{_bindir}/urpc_admin
    %{_bindir}/urpc_framework_perftest

%files urpc-umq-tools
%defattr(-,root,root)
    %{_bindir}/umq_perftest
%endif

%if %{build_all} || %{with dlock}
%files dlock-lib
%defattr(-,root,root)
    %{_libdir}/libdlockm.so.*
    %{_libdir}/libdlocks.so.*
    %{_libdir}/libdlockc.so.*

%files dlock-devel
%defattr(-,root,root)
    %{_libdir}/libdlockm.so
    %{_libdir}/libdlocks.so
    %{_libdir}/libdlockc.so
    %dir %{_includedir}/ub
    %dir %{_includedir}/ub/umdk
    %dir %{_includedir}/ub/umdk/ulock
    %dir %{_includedir}/ub/umdk/ulock/dlock
    %{_includedir}/ub/umdk/ulock/dlock/dlock_client_api.h
    %{_includedir}/ub/umdk/ulock/dlock/dlock_types.h
    %{_includedir}/ub/umdk/ulock/dlock/dlock_server_api.h

%files dlock-example
%defattr(-,root,root)
    %{_bindir}/dlock_primary_test
    %{_bindir}/dlock_client_test
    %{_bindir}/dlock_client_object_test
%endif

%if %{build_all} || %{with ums}
%files ums%{ums_suffix}
%defattr(-,root,root)
    %dir /lib/modules/%{kernel_version}/extra/ums/
    /lib/modules/%{kernel_version}/extra/ums/ums.ko
    /etc/modules-load.d/ums.conf

%pre ums%{ums_suffix}
RUNTIME_PAGESIZE=$(getconf PAGESIZE)
%if %{with_64kb}
EXPECTED_PAGESIZE=65536
%else
EXPECTED_PAGESIZE=4096
%endif
if [ "$RUNTIME_PAGESIZE" != "$EXPECTED_PAGESIZE" ]; then
    fmt_size() { [ $1 -ge 1024 ] && echo "$(( $1 / 1024 ))KB" || echo "${1}B"; }
    echo "ERROR: umdk-ums%{ums_suffix} requires $(fmt_size $EXPECTED_PAGESIZE) page size kernel," \
         "but current is $(fmt_size $RUNTIME_PAGESIZE)." >&2
    exit 1
fi
exit 0

%post ums%{ums_suffix}
if [ -d /lib/modules/$(uname -r)/kernel/net/smc ]; then
    %{__rm} -rf /lib/modules/$(uname -r)/kernel/net/smc
fi
if [[ %{kernel_version} != $(uname -r) ]]; then
    mkdir -p /lib/modules/$(uname -r)/weak-updates/drivers/ums/
    echo "/lib/modules/%{kernel_version}/extra/ums/ums.ko" | /sbin/weak-modules --add-module --no-initramfs --verbose
fi

echo "omit_drivers+=\" ums \"" > /etc/dracut.conf.d/ums.conf

/sbin/depmod -a $(uname -r)

%postun ums%{ums_suffix}
if [ $1 -eq 0 ]; then
    if [[ %{kernel_version} != $(uname -r) ]]; then
        if [ -d /lib/modules/$(uname -r)/weak-updates/drivers ]; then
                %{__rm} -rf /lib/modules/$(uname -r)/weak-updates/drivers/ums/ums.ko
                %{__rm} -rf /lib/modules/$(uname -r)/weak-updates/drivers/ums/
            else
                %{__rm} -rf /lib/modules/$(uname -r)/weak-updates/ums/ums.ko
                %{__rm} -rf /lib/modules/$(uname -r)/weak-updates/ums/
        fi
    fi
fi
/sbin/depmod -a $(uname -r)

%files ums-tools
%defattr(-,root,root)
    /usr/lib/libums-preload.so
    /usr/bin/ums_run

%post ums-tools

%postun ums-tools
if [ $1 -eq 0 ]; then
    [ -f /usr/lib/libums-preload.so ] && %{__rm} -f /usr/lib/libums-preload.so || :
    [ -f /usr/bin/ums_run ] && %{__rm} -f /usr/bin/ums_run || :
fi

%pre ums-agent
getent passwd ums >/dev/null || \
    useradd -r -s /sbin/nologin -d /var/lib/ums ums

%post ums-agent
if [ -x %{_bindir}/systemctl ] && [ -x %{_sbindir}/rsyslogd ]; then
    %{_bindir}/systemctl restart rsyslog >/dev/null  2>&1
fi
%systemd_post ums_agent.service

%preun ums-agent
%systemd_preun ums_agent.service

%postun ums-agent
%systemd_postun ums_agent.service

%files ums-agent
%defattr(-,root,root)
    %attr(750,root,ums) %{_sbindir}/ums_agent
    %attr(644,root,root) %{_unitdir}/ums_agent.service
    %dir %attr(750,root,ums) /etc/ums_agent
    %attr(640,root,ums) %config(noreplace) /etc/ums_agent/ums_agent.conf
    %attr(644,root,root) /etc/rsyslog.d/ums_agent.conf
    %attr(644,root,root) /etc/logrotate.d/ums_agent
%endif

%changelog
* Sat Jun 27 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B015
- umdk: update cam Add structs for, reinforce ums smoke test, and fix ums case fail
- umq: update fix invalide poll tx, fix coredump in umq_uninit, add option timestamp, and add tiny qbuf pool
- urma: update DFX function adds interrupt, simplify urma_perftest socket api, refactor failback trigger in, and resend failed cr one
* Fri Jun 26 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B014
- urma: update optimize bond rearm jfc, optimization messages in get, use source MAC for, and correct spelling mistakes in
- umq: update add reference counting for, reset alloc/free trace, add param validate for, and resolve coredump caused by
* Thu Jun 25 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B013
- umdk: update ums fix orphan socket, test add ums ut, fix urpc case name, and fix urma case name
- urma: update optimize bondp_post_jetty_send_wr, copy extra vwr to, split remaining URMA UT, add thread local cache, and fix rqe_cnt err when
- umq: update add validation for rjetty_size, extract common qbuf pool, expose duplicate flow control, and add trace point and
- umdk: drop stale paths from refreshed tarball
* Wed Jun 24 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B012
- urma: update fix show_stats failed log, add param check when, refactor failback task management, del_tag_in_user, and refine log level for
- umdk: update cam fix cam docs
- umq: update support configuring the port and fix incorrect __ATOMIC_RELAXED usage
* Tue Jun 23 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B011
- umq: update flow-control SGE management, revert the patch that, add func str for, and reduce empty poll operations
- urma: update split common UT files, add print cna for, disable failback and health, and fix perftest tp aware
- umdk: update cam fix Chinese comments, ums new test cases, umq suport tp_type/tp_mode configration, and revise code according to
- umdk: drop stale paths from refreshed tarball
* Mon Jun 22 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B010
- urpc: update urpc/perftest bound framework eid, urpc/perftest bound concurrent latency, and fix urma_seg_t ext value
- umq: update umq/perftest bound string option, set correct rjetty flag, fix umq post tx, packet deduplication, and support wr trace
- urma: update fix potential out-of-bounds access, perftest log register need, umra fix rqe_cnt in, and remove stale netlink declarations
- umdk: update umq update max bind, converge related bug fix, urpc case fix, and cam fix linewidth and
* Thu Jun 18 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B009
- umdk: update docs clarify UMDK build, ums Adapting Compilation for, update urpc dev config, and cam format master a2
- urma: update urma/admin reserve nul when, urma/perftest reject zero size, using nlattr to query, and fix the data plane
- umq: update add shared transport public, jetty pool management, adapt urma_get_rjetty, support create/deatroy logic umq, and support logic umq post/poll
- umdk: drop stale paths from refreshed tarball

* Tue Jun 16 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B008
- urma: update recv wr list bath, add cna field to, add multi-transport types FLUSH_DMA, and enable without backup wr
- umq: update handle fc rx buf, optimize post recv wr, and optimize ub_imm structure with
- umdk: update ums support building umdk-ums-64kb
- umdk: add main package dependency metadata

* Mon Jun 15 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B007
- uvs: update fix cleancode issue
- urma: update fix cleancode issue, add jfc and jfs, Refactor the urma_admin show_res, and validate dst_chip_id in bondp
- umq: update Flow control exchanges umq_id, set rjetty in umq_bind_info, and transmit data with umq_id
- umdk: update cam fix bug to, fix ub device incorrect, ums fix codecheck problem, and fix umq bond dev
- dlock: fix add fd num check
- umdk: drop stale paths from refreshed tarball
* Wed Jun 10 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B006
- umdk: update cam update cam compile, ums fix the security, and cam fix compile bug
- urma: update respect iodie level in, fix bond cleanup and, Fix some formatting issues, and fix dev cap reserved
- umq: update change flow control sequence, SGE/imm_data interaction, and flow-control SGE management
- dlock: fix add TAG mechanism for and refactor control message receiving
- umdk: drop stale paths from refreshed tarball
* Mon Jun 8 2026 wangxin <luyicai1994@yeah.net> - 26.06.0-B005
-umq: modify qbuf default config in ctp mode
-urma: performance optimization post wr
-urma: add dfx log for bondp implement.
-urma: Refactored the URMA Bazel build to emit layered shared libraries.
-urma: support get tp list.
-urpc: add param validation
-umq: add ext_func for log_config_get
-urma: fix log for bondp implement.
-ums: remove auto-learn mode and enforce strict identity verification
-umdk:modify umdk package version to 26.06.0
-urma: increase topo max node limit to 1024
-urma: fix umdk urma IPoURMA case fail
-umq: flow control sge manage
-urma: add background worker thread for bond device
-umq: fix param validation and string terminator issues
-umq: remove redundant code
-fix umdk urma dev not correct
-ums:fix codecheck issues
-dlock:fixup update_locks_response processing out of bound bug
-urma: enhance URMA Bazel build configuration
-urma: Add DFX functionality for link removal and resource destruction
-urma: improve urma_ping arg parsing and EID logging
-umdk: fix ip over urma cases fail
* Thu Jun 4 2026 wangxin <wangxin554@huawei.com> - 26.06.0-B004
-urma: performance optimization post wr
-umq: alloc a id for umq
-urma: add main_ue_eid admin command support
-ums: remove auto-learn mode and enforce strict identity verification
-umq: support register ext_func for log
-urma: topology supports parallel planes
-urma: allow disabling of msn deduplication
* Thu May 28 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B003
-urma: support get jfce fd list by usr ctl.
-urma: add register log API and refactor user dfx.
-urma: fix bonding dev context, jetty import and bondp_import_jetty mem leak.
-urma: add bondp_create_jfc/jfr extended interface and port validation.
-urma: fix bazel compile and rename liburma-udma.so output.
-urpc: fetch umdk headers from gitcode when build.
-umq: update imm data to 64bit and support ctp.
-umq: improve buffer rollback, batch size, jfr/jfc port and IMM handling.
-ums: implement secure UB token exchange via ums_agent.
-ums: add netlink token exchange framework and agent fixes.
-ums: improve token proxy and TLS connection handling.
-dlock: fix peer_type, header len, batch lock and SSL buffer issues.
-cam: fix mask calculation error in combine.
-ub: udma support st64b_en function.
-umdk: add umdk main package.
* Wed May 20 2026 luyizhou <luyizhou1@huawei.com> - 26.06.0-B002
-urma: add Bazel build support.
-urpc: enhance ums agent security proxy.
-urpc: umq shared flow-control jfr.
-urma: enhance bonding multi-path.
* Thu Apr 30 2026 tianzhensong <tianzhensong@huawei.com> - 26.06.0-B001
-Initial UMDK-26.06.0 rpm spec file.
