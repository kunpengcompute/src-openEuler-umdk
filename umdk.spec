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

%define build_all 1

%if %{with ums} || %{with urma} || %{with urpc} || %{with dlock}
    %define build_all 0
%endif

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
    %define rpm_release B057
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

BuildRequires : rpm-build, make, cmake, gcc, gcc-c++, glibc-devel, openssl-devel, glib2-devel, libnl3-devel, kernel-devel, libummu-devel
Requires: glibc, glib2, libummu
%if %{with asan}
Requires: libasan
%endif
%if %{with tsan}
Requires: libtsan
%endif

Patch0000: 0000-umdk-urma-add-container-support.patch
Patch0001: 0001-umdk-urpc-support-shared-jfr.patch
Patch0002: 0002-umdk-urma-bugfix-container.patch
Patch0003: 0003-umdk-udma-Fix-a-bug-related-to-create-sq.patch
Patch0004: 0004-umdk-udma-Support-for-the-separate-page-table-feature.patch
Patch0005: 0005-umdk-udma-bugfix-related-to-log-print.patch
Patch0006: 0006-umdk-udma-bugfix-related-to-free-tid.patch
Patch0007: 0007-umdk-urma-bugfix-related-to-uvs.patch
Patch0008: 0008-umdk-urma-bugfix-related-to-uvs-and-urma-admin.patch
Patch0009: 0009-umdk-urma-bugfix-of-topo-info.patch
Patch0010: 0010-umdk-urma-support-ipourma.patch
Patch0011: 0011-umdk-urpc-support-rnr-free-flowcontrol.patch
Patch0012: 0012-umdk-urpc-support-adaptive-flowcontrol-and-log-enhancement.patch
Patch0013: 0013-umdk-urma-Fix-urma_perftest-size-check-for-send-opc.patch
Patch0014: 0014-umdk-urma-modify-log-for-liburma-bondp.patch
Patch0015: 0015-umdk-urma-modify-urma-log-format.patch
Patch0016: 0016-umdk-urma-optimize-the-logs-of-bondp-and-liburma.patch
Patch0017: 0017-umdk-urma-refine-uvs-logging.patch
Patch0018: 0018-umdk-urma-set-get-sl-priority.patch
Patch0019: 0019-umdk-udma-support-disable-compile-udma.patch
Patch0020: 0020-umdk-urma-standalone-aggregate-mode-currently-does-not-support-WQE-list.patch
Patch0021: 0021-umdk-urma-add-entity_id-into-bondp-and-admin-topo.patch
Patch0022: 0022-umdk-urma-bondp-support-half-loopback.patch
Patch0023: 0023-umdk-urma-change-logic-between-device_list-and-eid_list.patch
Patch0024: 0024-umdk-urma-fix-expose-agg-dev.patch
Patch0025: 0025-umdk-urma-optimize-efficiency-of-expose-agg-dev.patch
Patch0026: 0026-umdk-urma-set-CTP-priority-to-6-as-workaround.patch
Patch0027: 0027-umdk-urma-optimize-EID-lookup-logic.patch
Patch0028: 0028-umdk-urma-add-urma-ping-client.patch
Patch0029: 0029-umdk-ums-fix-the-issue-of-links-not-being-shareable.patch
Patch0030: 0030-umdk-ums-prevent-Send-WR-from-being-posted-to-Jetty-when-ubcore_bind_jetty-fails.patch
Patch0031: 0031-umdk-dlock-fix-example-issue-client_init-deinit-calls-need-to-be-locked.patch
Patch0032: 0032-umdk-urma-seg-cache-default-disable.patch
Patch0033: 0033-umdk-urma-fix-timing-bug-in-urma-ping.patch
Patch0034: 0034-umdk-dlock-fix-codecheck-warnings.patch
Patch0035: 0035-umdk-ums-fix-codecheck-warnings.patch
Patch0036: 0036-umdk-urma-support-uboe.patch
Patch0037: 0037-umdk-urpc-normalize-line-ending-and-bugfix.patch
Patch0038: 0038-umdk-urma-bugfix-query-sl-resource.patch
Patch0039: 0039-umdk-urma-bondp-datapath-optimization.patch
Patch0040: 0040-umdk-urma-userctl-header-file-in-user-space.patch
Patch0041: 0041-umdk-urma-User-space-implementation-of-Jetty-extension-interface.patch
Patch0042: 0042-umdk-udma-Support-uboe-function.patch
Patch0043: 0043-umdk-udma-Support-user-ctl-function.patch
Patch0044: 0044-umdk-urma-hotfix-bondp-topo-to-adapt-loopback-changes.patch
Patch0045: 0045-umdk-urma-bugfix-of-urma_admin.patch
Patch0046: 0046-umdk-urma-optimize-urma_admin-usage-printing.patch
Patch0047: 0047-umdk-urma-urma_perftest-support-page_size-config-value.patch
Patch0048: 0048-umdk-urma-bugfix-for-urma_perftest.patch
Patch0049: 0049-umdk-urma-add-new-param-checks-for-urma_ping-client.patch
Patch0050: 0050-umdk-urma-correct-log-format.patch
Patch0051: 0051-umdk-urma-cleancode-fix-for-sync.patch
Patch0052: 0052-umdk-urma-cleancode-fix-for-sync-urma-ping.patch
Patch0053: 0053-umdk-urma-simplify-bondp-import.patch
Patch0054: 0054-umdk-urma-bond-import-without-user-mode-topo.patch
Patch0055: 0055-umdk-urma-remove-unused-bond-code.patch
Patch0056: 0056-umdk-urma-Disable-deletion-operations-on-bonding_dev_0.patch
Patch0057: 0057-umdk-urma-fix-cleancode.patch
Patch0058: 0058-umdk-urma-add-signal-handler-for-urma_ping.patch
Patch0059: 0059-umdk-urma-bugfix-for-inline_data.patch
Patch0060: 0060-umdk-urma-cleancode-fix-for-bondp_segment-etc.patch
Patch0061: 0061-umdk-urma-fix-bondp_datapath-cleancode.patch
Patch0062: 0062-umdk-urma-clean-code-fo-topo_info.patch
Patch0063: 0063-umdk-urma-urma_admin-cleancode.patch
Patch0064: 0064-umdk-urma-urma_perftest-cleancode.patch
Patch0065: 0065-umdk-urma-cleancode-fix-for-ping_parameters.patch
Patch0066: 0066-umdk-urma-check-ioctl-errno-value.patch
Patch0067: 0067-umdk-urma-change-uvs-and-urma_admin-log-format.patch
Patch0068: 0068-umdk-urma-cleancode-fix-for-bond.patch
Patch0069: 0069-umdk-urma-bondp-seg-cache-should-not-import-vseg-twice.patch
Patch0070: 0070-umdk-urma-bond-device-no-longer-requires.patch
Patch0071: 0071-umdk-urma-add-comments-for-urma_wait_jfc0.patch
Patch0072: 0072-umdk-urma-bonding-dev-adapts-to-SL-functionality.patch
Patch0073: 0073-umdk-urma-remove-unused-bondp-code.patch
Patch0074: 0074-umdk-urma-add-eid_idx-validity-check-when-set-eid-to-ns.patch
Patch0075: 0075-umdk-urma-for-updates-to-external-files-or-APIs.patch
Patch0076: 0076-umdk-urma-update-urma-admin-agg-expose.patch
Patch0077: 0077-umdk-urma-do-not-parse-vendor-and-device-for-bonding-device.patch
Patch0078: 0078-umdk-urma-update-urma_admin-show.patch
Patch0079: 0079-umdk-urma-add-param-check-for-target-port.patch
Patch0080: 0081-umdk-urma-fix-codecheck.patch
Patch0081: 0081-umdk-urma-optimize-perftest-tool-parameters.patch
Patch0082: 0082-umdk-dlock-adapt-to-urma-bondp-API-change-remove-bond-user-ctl-code.patch
Patch0083: 0083-umdk-dlock-adapt-to-urma-API-change-set-jetty-priority-by-tp_type.patch
Patch0084: 0084-umdk-dlock-synchronize-jetty-flush-flags-to-avoid-data-race-issue.patch
Patch0085: 0085-umdk-udma-bugfix-related-to-clean-jfc.patch
Patch0086: 0086-umdk-dlock-initialize-reserved-field-prevent-heap-bits-leaks.patch
Patch0087: 0087-umdk-ums-adapt-to-ubcore-API-change-set-jetty-priority-by-tp_type.patch

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
tools of urma, contains  urma_perftest, urma_admin, ubagg_cli.

%package urma-bin
Summary:        binary file of urma
BuildRequires:  gcc
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

%if %{build_all} || %{with dlock}
%package dlock-lib
Summary:        Library files of dlock
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

%files dlock-example
%defattr(-,root,root)
    %{_bindir}/dlock_primary_test
    %{_bindir}/dlock_client_test
    %{_bindir}/dlock_client_object_test
%endif

%if %{build_all} || %{with urpc}
%package urpc-framework
Summary:        URPC framework shared library
Requires:       umdk-urma-lib
%description urpc-framework
This package contains the URPC framework shared libraries (e.g. liburpc.so).

%package urpc-umq
Summary:        URPC umq shared library
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

%if %{build_all} || %{with ums}
%package ums
Summary:        kmod file of ums
BuildRequires:  glib2-devel, libnl3-devel
Requires:       glib2, libnl3
%description ums
kmod file of ums

%package ums-tools
Summary:        tools of ums
%description ums-tools
tools of ums, contains ums_run
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
    %dir /var/lib/ub/umdk/urma/gcov/%{name}
    /var/lib/ub/umdk/urma/gcov/%{name}/
%endif

%files urma-tools
%defattr(-,root,root)
    %{_bindir}/urma_admin
    /etc/rsyslog.d/urma_admin.conf
    %{_bindir}/urma_perftest
    %{_bindir}/ubagg_cli
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
    %{_libdir}/libumq_ipc.so.*
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
    %{_libdir}/libumq_ipc.so
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
    %dir /lib/modules/$(uname -r)/weak-updates/drivers/ums/
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
%endif

%changelog
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
