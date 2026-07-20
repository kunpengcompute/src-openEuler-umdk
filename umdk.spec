# add --with asan option, i.e. disable asan by default
%bcond_with asan

# add --with tsan option, i.e. disable tsan by default
%bcond_with tsan

# add --with gcov option, i.e. disable gcov by default
%bcond_with gcov

# add --with test option, i.e. disable test by default
%bcond_with test

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

%define build_all 1

%if %{with ums} || %{with urma} || %{with urpc} || %{with dlock}
    %define build_all 0
%endif

# add --without udma option, i.e. enable udma by default
%bcond_without udma

%if %{defined kernel_version}
    %define kernel_build_path /lib/modules/%{kernel_version}/build
%else
    %define kernel_version %(
        KERNEL_DEVEL_COUNT=$(rpm -qa kernel-devel 2>/dev/null | wc -l);
        if [ "$KERNEL_DEVEL_COUNT" -eq 1 ]; then
            rpm -q --qf '%%{VERSION}-%%{RELEASE}.%%{ARCH}' kernel-devel 2>/dev/null;
        else
            uname -r;
        fi
    )
    %define kernel_build_path /lib/modules/%{kernel_version}/build
%endif
%define kernel_requires_version %(echo %{kernel_version} | awk -F"." 'OFS="."{$NF="";print}' | sed 's/\.$//g')

%if %{undefined rpm_release}
    %define rpm_release B113
%endif

Name          : umdk
Summary       : Unified memory development kit
Version       : 25.12.0
Release       : %{rpm_release}%{?dist}
Group         : umdk
License       : MIT
Vendor        : Huawei Technologies Co., Ltd
Source0       : %{name}-%{version}.tar.gz
BuildRoot     : %{_buildirootdir}/%{name}-%{version}-build
buildArch     : x86_64 aarch64
ExclusiveArch : aarch64

BuildRequires : rpm-build, make, cmake, gcc, gcc-c++, glibc-devel
%if %{build_all} || %{with ums}
BuildRequires : kernel-devel
%endif
Requires: glibc, glib2
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
Requires: umdk-ums = %{version}
Requires: umdk-ums-tools = %{version}
Requires: umdk-ums-agent = %{version}
%files
%endif

%description
A new system interconnect architecture

%if %{build_all} || %{with urma} || %{with urpc}
%package urma-lib
%if %{with udma}
BuildRequires:  libummu-devel
Requires:       libummu
%endif
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
%package ums
Summary:        kmod file of ums
BuildRequires:  glib2-devel, libnl3-devel, kernel-devel
Requires:       glib2, libnl3
%description ums
kmod file of ums

%package ums-tools
Summary:        tools of ums
%description ums-tools
tools of ums, contains ums_run

%package ums-agent
Summary:        UMS Agent daemon for secure token exchange
BuildRequires:  systemd-devel, keyutils-libs-devel, openssl-devel
Requires:       systemd-libs, glib2, libnl3, openssl, keyutils
Requires(pre):  shadow-utils
%description ums-agent
UMS Agent is a user-space daemon for secure TokenValue exchange
between UMS kernel modules via TLS 1.3 channel.
%endif

%if "%{build_all}" == "0"
    %global debug_package %{nil}
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
%if %{without udma}
    -DBUILD_UDMA="disable" \
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
%if %{with udma}
    %{_libdir}/urma/liburma-udma.so
%endif
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
    %dir %{_includedir}/ub/umdk/urma
    %{_includedir}/ub/umdk/urma/urma_*.h
    %{_includedir}/ub/umdk/urma/uvs_types.h
    %{_includedir}/ub/umdk/urma/uvs_api.h
%if %{with udma}
    %dir %{_includedir}/ub/umdk/urma/udma
    %{_includedir}/ub/umdk/urma/udma/udma_u_ctl.h
%endif
%if %{with gcov}
    %dir /var/lib/umdk/gcov/%{name}
    /var/lib/umdk/gcov/%{name}/
%endif

%pre urma-tools
if [ -d /usr/bin/urma_admin ] && [ ! -L /usr/bin/urma_admin ]; then
    rm -rf /usr/bin/urma_admin
fi

%files urma-tools
%defattr(-,root,root)
    %{_bindir}/urma_admin
    %{_bindir}/urma_ping
    /etc/rsyslog.d/urma_admin.conf
    %{_bindir}/urma_perftest

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
%files ums
%defattr(-,root,root)
    %dir /lib/modules/%{kernel_version}/extra/ums/
    /lib/modules/%{kernel_version}/extra/ums/ums.ko
    /etc/modules-load.d/ums.conf

%post ums
if [ -d /lib/modules/$(uname -r)/kernel/net/smc ]; then
    %{__rm} -rf /lib/modules/$(uname -r)/kernel/net/smc
fi
if [[ %{kernel_version} != $(uname -r) ]]; then
    mkdir -p /lib/modules/$(uname -r)/weak-updates/drivers/ums/
    echo "/lib/modules/%{kernel_version}/extra/ums/ums.ko" | /sbin/weak-modules --add-module --no-initramfs --verbose
fi

echo "omit_drivers+=\" ums \"" > /etc/dracut.conf.d/ums.conf

/sbin/depmod -a $(uname -r)

%postun ums
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
* Mon Jul 20 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B113
- urma: update fix bondp tjetty valid, encapsulate bond topology map, make bond CR batch, and fix tp_aware ty_type error
- umq: update fix poll rx core and fix errno and update
* Sat Jul 18 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B112
- urma: update remove legacy bond health, fix potential data race, print error code when, and fix duplicate UDMA library
- umq: update only one qbuf can, support thread_key register ops, add headroom param check, and total allocated credit is
- umdk: update ums fix kmod build
- umdk: drop stale paths from refreshed tarball
* Wed Jul 15 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B111
- urma: update fix perf command netlink and support bonding link health
- umq: update fix buf overflow problem and fix the issue of
* Wed Jul 15 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B110
- umdk: git reset to B108
* Wed Jul 15 2026 huying <huying21@huawei.com> - 25.12.0-B109
- ums: remove umdk-ums-64kb build and roll back to B105
* Tue Jul 14 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B108
- urma: update perftest_run_test Fix memory leak, perftest_resources Fix incompatible sizeof, urma_sample Add NULL check, and bondp_api Add NULL check
- umq: update optimize log, fix the issue where, do not allocate credit, fix null pointer access, and fix mismatch param type/num
* Mon Jul 13 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B107
- umq: update prevent resource-exhaustion DoS attacks, optimize perf thread local, fix credit starvation issue, and fix issue of delayed
- urma: update perftest support delegated connection, bondp_poll_jfc supports cocurrent access, check failover route by, and fix perftest connect failed
- umdk: drop stale paths from refreshed tarball
* Sat Jul 11 2026 caihongxu <caihongxu@huawei.com> - 25.12.0-B106
- urma: Fix missing is_msn_enabled in JFR import causing recv CR loss
- umq: fix credit starvation issue
* Thu Jul 9 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B105
- umq: update umq fix the expansion and add sub_umq_id for poll
- umdk: update ums remove TFO to
* Wed Jul 8 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B104
- urma: update fix UT mock stability, init enabled_indices at create_context, fix log format for, and fix rate limit log
- umq: update fix logic umq credit_clean_up, add trace timestamp/umq_id, and fix trace bug of
* Tue Jul 7 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B103
- umq: update add trace for post and Fix the issue of
- urma: update clarify bond WR conversion
* Mon Jul 6 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B102
- umq: update add jetty pool alloc
- urma: update udma drop blanket -Wno-error, reject out-of-range order_type in, fix route failover of, and remove redundant per-jetty recv_wr_buf
- umdk: update fix spell error
- umdk: drop stale paths from refreshed tarball
* Sat Jul 4 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B101
- urma: bondp unregister pseg when user call unregister
* Fri Jul 3 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B100
- urma: update refactor perftest communication into, inline perftest communication fields, allocate bond topo map, and fix bond datapath get
- umq: update fix the return value
- umdk: drop stale paths from refreshed tarball
* Fri Jul 3 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B099
- urma: update harden urma_perftest TCP connection, bug fix for balance, change type of bdp_tseg, and Use drv ext to
- umq: update intercept logical umq when
* Thu Jul 2 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B098
- urma: update optimize bondp_poll_jfc and handle_send_cr_with_store, fix urma_perftest for tpid, fix UT script on, and forbid massive illegal state
- umq: update fix umq thread closure, fix the error in, change spin lock to, and support jfr lock_free
- umdk: drop stale paths from refreshed tarball
* Wed Jul 1 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B097
- umq: update qbuf DFX tiny pool, delete ipc/ubmm code, fix the coredump that, and fix perftest in enqueue/dequeue
- urma: update add trans_mode/tp_type/order_type combination check, optimize handle_recv_cr_without_backup, add fork constraint to, build, and disable urma_admin netlink auto
- umdk: drop stale paths from refreshed tarball
* Tue Jun 30 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B096
- umq: update add qbuf alloc/free perf, revert fc sge management, adaptive send threshold, and fix logic umq return
- urma: update fix perftest bond_mode balance, add API fuzz coverage, urma_perftest comm use cfg-based, and fix urma_perftest log level
- umdk: drop stale paths from refreshed tarball
* Mon Jun 29 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B095
- umq: update fix ipc free core, support flow control status, fix the blk_num data, and fix interrupt problem
- urma: update urma_perftest support wait_jfc with, remove netdev info for, ut bug_fix, add dv121 relation feature, and Resolved existing issues in
- umdk: update cam add fused_deep_moe op, cam add moe dispatch, cam add moe combine, and cam add basic files
- urpc: update fix share jfr queue, update doc/ch/urpc/UMQ Buffer ch, fix umq log bug, umdk test, and umdk urpclib test code
- dlock: fix modify jetty/jfs to error, support ub token, fix UT compilation issues, test folder commit, and umdk test
- uvs: update rpm reorganize umdk spec and fix cleancode issue
- umdk: drop stale paths from refreshed tarball

* Fri Jun 26 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B093
- umdk: update OE SP4
* Wed Jun 10 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B092
- urma: update fix log for bondp, increase topo max node, bond worker, performance, build, argument parsing, and cleanup
- umq: update flow-control SGE management, validation, cleanup, packet deduplication, change flow control sequence, and SGE/imm_data interaction
- dlock: fix update_locks_response bounds handling
- umdk: add SP3 patches 0218-0236, skipped 2 empty changes
* Thu Jun 4 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B091
- urma: increase topo max node limit to 1024
* Wed Jun 3 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B090
- urma: sync SP3 patches (!2144-!2229), perftest/log/bazel/topo/main_ue_eid
* Sat May 30 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B089
- urpc: fix tp bugs
* Fri May 29 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B088
- urma: add register location log API
* Tue May 26 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B087
- urma: fix copy to user failed problems
* Fri May 22 2026 wujie <wujie66@huawei.com> - 25.12.0-B086
- umdk: add umdk main package
* Fri May 22 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B085
- urma: fix bondp import jetty mem leak
* Wed May 20 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B084
- urma: support bazel compile
* Wed May 13 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B083
- urpc: support qbuf escape and share flow control jfr
* Wed May 13 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B082
- urma: make urma_perf_is_enabled a proper prototype (void)
* Tue May 5 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B081
- urma: enhance bonding schedule with random balance selection support
* Sat May 2 2026 jilei <jilei8@huawei.com> - 25.12.0-B080
- urma: bonding schedule send balance support random select
* Fri May 1 2026 chenyutao <chenyutao2@huawei.com> - 25.12.0-B079
- urma: urma_get_perf_info bug fix
* Fri May 1 2026 chenyutao <chenyutao2@huawei.com> - 25.12.0-B078
- urma: bonding device move wr buf from jfc to comp
* Wed Apr 29 2026 chenwen <chenwen54@huawei.com> - 25.12.0-B075
- urma: bugfix retry send msg
* Wed Apr 29 2026 chenwen <chenwen54@huawei.com> - 25.12.0-B074
* urma: bugfix bonding should not use wr entry if jetty deleted
* Tue Apr 28 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B073
- urma: fix double install urma error
* Mon Apr 27 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B072
- urma: bonding tseg and tjetty support ref
* Mon Apr 27 2026 chenwen <chenwen54@huawei.com> - 25.12.0-B071
- urma: fix bonding failover issue
* Mon Apr 20 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B070
- urpc: enable urma CLOS networking and failover
* Sun Apr 19 2026 chenwen <chenwen54@huawei.com> - 25.12.0-B069
- umdk: supports CLOS networking and failover, health checks, shared TP, and reliable link establishment.
* Mon Apr 13 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B068
- urma: fix bondp balance mode datapath
* Thu Apr 9 2026 huying <huying21@huawei.com> - 25.12.0-B067
- ums: fix and prevent credits deadlock by reserving emergency credits
* Thu Apr 9 2026 huying <huying21@huawei.com> - 25.12.0-B066
- ums: fix softirq context safety in ums_link_put
* Wed Apr 8 2026 zhangwentao <zhangwentao88@h-partners.com> - 25.12.0-B065
- urma: support custom dev_name in urma_admin agg add command
* Wed Apr 8 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B064
- urma: update validation checks for single path and aggregation mode
* Thu Apr 2 2026 bishulei <bishulei@huawei.com> - 25.12.0-B063
- urma: support create agg dev with explicit dev_name
* Wed Apr 1 2026 zhangwentao <zhangwentao88@h-partners.com> - 25.12.0-B062
- urma: rctp reuse in urma_bind_jetty
* Tue Mar 31 2026 bishulei <bishulei@huawei.com> - 25.12.0-B061
- urma: sync bugfix of urma
* Fri Mar 27 2026 luyizhou  <luyizhou1@huawei.com> - 25.12.0-B060
- urma: fix default parameters of urma_perftest
* Wed Mar 25 2026 Chen Wen  <chenwen54@huawei.com> - 25.12.0-B059
- urma: update version kernel commit
* Wed Mar 25 2026 Chen Wen  <chenwen54@huawei.com> - 25.12.0-B058
- urma: fix bondig poll and device create bugs
* Tue Mar 24 2026 huying <huying21@huawei.com> - 25.12.0-B057
- ums: adapt to ubcore API change, set jetty priority by tp_type
* Fri Mar 20 2026 huying <huying21@huawei.com> - 25.12.0-B056
- dlock: initialize reserved field, prevent heap bits leaks
* Fri Mar 20 2026 Wei Qin <qinwei61@huawei.com> - 25.12.0-B055
- udma: fix a bug related to clean jfc
* Fri Mar 20 2026 huying <huying21@huawei.com> - 25.12.0-B054
- dlock: synchronize jetty flush flags to avoid data race issue
* Fri Mar 20 2026 huying <huying21@huawei.com> - 25.12.0-B053
- dlock: adapt to urma API change, set jetty priority by tp_type
* Fri Mar 20 2026 huying <huying21@huawei.com> - 25.12.0-B052
- dlock: adapt to urma bondp API change, remove bond user ctl code
* Thu Mar 19 2026 Chen Wen <chenwen54@huawei.com> - 25.12.0-B051
- urma: perftest para optimization
* Wed Mar 18 2026  luyizhou <luyizhou1@huawei.com> - 25.12.0-B050
- urma: update urma_admin show for bonding devices
* Tue Mar 17 2026  chenyutao <chenyutao2@huawei.com> - 25.12.0-B049
- urma: do not parse vendor and device for bonding device
* Mon Mar 16 2026  luyizhou <luyizhou1@huawei.com> - 25.12.0-B048
- urma: update urma_admin agg expose
* Sat Mar 14 2026  luyizhou <luyizhou1@huawei.com> - 25.12.0-B047
- urma: support SL functionality; update bondp&urma_admin
* Sat Mar 14 2026  chenyutao <chenyutao2@huawei.com> - 25.12.0-B046
- urma: sync for liburma and bondp implementation
* Thu Mar 12 2026  luyizhou <luyizhou1@huawei.com> - 25.12.0-B045
- urma: cleancode fix for bondp
* Thu Mar 12 2026  chenyutao <chenyutao2@huawei.com> - 25.12.0-B044
- urma: change uvs and urma_admin log format
* Wed Mar 11 2026  luyicai <luyicai1994@yeah.net> - 25.12.0-B043
- sync bugfix of urma
* Tue Mar 10 2026 chenyutao <chenyutao2@huawei.com> - 25.12.0-B042
- urma: correct log format for construct and destruct
* Sat Mar 7 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B041
- urma: optimize urma_admin usage printing
* Wed Mar 4 2026 Yongqiang Guo <guoyongqiang12@huawei.com> - 25.12.0-B040
- urma: hotfix bondp topo to adapt loopback changes.
* Wed Mar 4 2026 Wei Qin <qinwei61@huawei.com> - 25.12.0-B039
- udma: bugfix related to user ctl
* Wed Mar 4 2026 Chen Wen <chenwen54@huawei.com> - 25.12.0-B038
- urma: bugfix userctl
* Wed Mar 4 2026 chenyutao <chenyutao2@huawei.com> - 25.12.0-B037
- urma: bondp datapath optimization
* Tue Mar 18 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B036
- urma: bugfix query sl resource
* Tue Mar 3 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B035
- urpc support adaptive flowcontrol and log enhancement
* Tue Mar 3 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B034
- urma: support uboe
* Mon Mar 2 2026 tianzhensong <tianzhensong@huawei.com> - 25.12.0-B033
- ums: fix codecheck warnings
* Mon Mar 2 2026 huying <huying21@huawei.com> - 25.12.0-B032
- dlock: fix codecheck warnings
* Mon Mar 2 2026 wanghang <wanghang73@huawei.com> - 25.12.0-B031
- urma: make bondp seg cache default disable
* Fri Feb 27 2026 huying <huying21@huawei.com> - 25.12.0-B030
- dlock: fix example issue, client_init/deinit() calls need to be locked
* Fri Feb 27 2026 huying <huying21@huawei.com> - 25.12.0-B029
- ums: prevent Send WR from being posted to Jetty when ubcore_bind_jetty fails
* Fri Feb 27 2026 huying <huying21@huawei.com> - 25.12.0-B028
- ums: fix the issue of links not being shareable
* Fri Feb 27 2026 wanghang <wanghang73@huawei.com> - 25.12.0-B027
- add urma_ping client
* Fri Feb 27 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B026
- urpc rollback of flowcontrol and log enhancement
* Fri Feb 27 2026 bishulei <bishulei@huawei.com> - 25.12.0-B025
- optimize EID lookup logic
* Thu Feb 26 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B024
- urma: set CTP priority to 6 as workaround
* Wed Feb 25 2026 bishulei <bishulei@huawei.com> - 25.12.0-B023
- sync bugfix of urma
* Tue Feb 24 2026 luyicai <luyicai1994@yeah.net> - 25.12.0-B022
- sync bugfix of urma
* Sat Feb 14 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B021
- urpc support adaptive flowcontrol and log enhancement
* Fri Feb 6 2026 wangxin <wangxin554@huawei.com> - 25.12.0-B020
- urpc support rnr-free flowcontrol
* Wed Feb 4 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B019
- bugfix of urma container
* Tue Feb 3 2026 Wei Qin <qinwei61@huawei.com> - 25.12.0-B018
- bugfix of create sq and free tid
* Tue Jan 20 2026 luyizhou <luyizhou1@huawei.com> - 25.12.0-B017
- bugfix of urma container
* Tue Jan 20 2026 simonhua97 <huayu9@huawei.com> - 25.12.0-B016
- urpc support shared jfr
* Wed Jan 14 2026 wuyuyan_98 <wuyuyan@huawei.com> - 25.12.0-B015
- urma add container support
* Wed Dec 24 2025 luyicai <luyicai1994@yeah.net> - 25.12.0-B014
- adapt ums compile issue when multiple kernel-devel are installed
* Thu Dec 18 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B013
- urma bugfix perftest and flush jetty
* Mon Dec 15 2025 luyicai <luyicai1994@yeah.net> - 25.12.0-B012
- urma, dlock, ums, and umq fix some bugs
* Wed Dec 10 2025 luyicai <luyicai1994@yeah.net> - 25.12.0-B011
- udma add compilation macro and umq fix bugs
* Mon Dec 8 2025 luyicai <luyicai1994@yeah.net> - 25.12.0-B010
- urma and urpc fix some bugs
* Sat Dec 6 2025 huying <huying21@huawei.com> - 25.12.0-B009
- ums fix the issue of illegal segment access permission settings
* Thu Dec 4 2025 tianzhensong <tianzhensong@huawei.com> - 25.12.0-B008
- ums adapt to ubcore_get_route_list and add compile ums by default
* Thu Dec 4 2025 caihongxu <caihongxu@huawei.com> - 25.12.0-B007
- umq update read/write code
* Thu Dec 4 2025 caihongxu <caihongxu@huawei.com> - 25.12.0-B006
- umq adapt urma topo query
* Wed Dec 3 2025 caihongxu <caihongxu@huawei.com> - 25.12.0-B005
- umq add read/write for post/poll
* Tue Dec 2 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B004
- urma supports querying topo information for a single device.
* Thu Nov 27 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B003
- urma added set/get tp_attr functionality interfaces
* Sat Nov 22 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B002
- urma added the tp_type feature
* Tue Dec 30 2025 Chen Wen <chenwen54@huawei.com> - 25.12.0-B001
- Initial UMDK-25.12.0 rpm spec file
