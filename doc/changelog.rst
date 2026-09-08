.. SPDX-License-Identifier: GPL-2.0-or-later

Changelog
=========

v4.2.0 (2026-09-08)
-------------------

**What's Changed**

- Add ``--dry-run`` option to preview tests before execution
- Add configurable fault injection interval option
- Persist and export partial results when a session is aborted mid-suite
- Fix ``--exec-timeout`` not killing tests in the shell channel
- Fix JSON report file being opened in read/write instead of write-only mode
- Fix incorrect log message when test parameters are missing in LTP metadata
- Fix exception handling in the event subsystem
- Fix ``--randomize`` command-line description
- Major documentation update (quickstart, SSH, LTX, QEMU, and plugins)
- Move IOBuffer implementations inside the sut module
- Improve test suite coverage and fix flaky test cases


**New Contributors**

* `@nhitar <https://github.com/nhitar>`__ made their first contribution in `#98 <https://github.com/linux-test-project/kirk/pull/98>`__

**Full Changelog**: `v4.1.0...v4.2.0 <https://github.com/linux-test-project/kirk/compare/v4.1.0...v4.2.0>`__

v4.1.0 (2026-03-30)
-------------------

**What's Changed**

* ltp: support network tests configurations by `@acerv <https://github.com/acerv>`__ in `#95 <https://github.com/linux-test-project/kirk/pull/95>`__
* ltp: Remove unused PASSWD, RUSER variables by `@pevik <https://github.com/pevik>`__ in `#96 <https://github.com/linux-test-project/kirk/pull/96>`__
* monitor: fix mismatch between event and its name
* minor fixes and code stabilization

**Full Changelog**: `v4.0.0...v4.1.0 <https://github.com/linux-test-project/kirk/compare/v4.0.0...v4.1.0>`__

v4.0.0 (2026-02-23)
-------------------

**What's Changed**

* Remove ``--env`` option by `@acerv <https://github.com/acerv>`__ in `#89 <https://github.com/linux-test-project/kirk/pull/89>`__
* pyproject: include sub-packages in pip package by `@roxell <https://github.com/roxell>`__ in `#91 <https://github.com/linux-test-project/kirk/pull/91>`__
* libkirk: Print /proc/cmdline by `@pevik <https://github.com/pevik>`__ in `#92 <https://github.com/linux-test-project/kirk/pull/92>`__
* ui: simplify report by `@acerv <https://github.com/acerv>`__ in `#93 <https://github.com/linux-test-project/kirk/pull/93>`__
* many bugs fixes and code optimizations


**New Contributors**

* `@roxell <https://github.com/roxell>`__ made their first contribution in `#91 <https://github.com/linux-test-project/kirk/pull/91>`__

**Full Changelog**: `v3.2.1...v4.0 <https://github.com/linux-test-project/kirk/compare/v3.2.1...v4.0>`__

v3.2.1 (2026-01-28)
-------------------

**What's Changed**

* ltp: correctly fetch LTPROOT by `@acerv <https://github.com/acerv>`__ in `#88 <https://github.com/linux-test-project/kirk/pull/88>`__


**Full Changelog**: `v3.2...v3.2.1 <https://github.com/linux-test-project/kirk/compare/v3.2...v3.2.1>`__

v3.2 (2026-01-12)
-----------------

**What's Changed**

* Framework is no longer a plugin by `@acerv <https://github.com/acerv>`__ in `#86 <https://github.com/linux-test-project/kirk/pull/86>`__
* sut: add ``--optimize-sut`` option by `@acerv <https://github.com/acerv>`__ in `#87 <https://github.com/linux-test-project/kirk/pull/87>`__
* stabilized tests execution for CI

**Full Changelog**: `v3.1...v3.2 <https://github.com/linux-test-project/kirk/compare/v3.1...v3.2>`__

v3.1 (2025-12-10)
-----------------

**What's Changed**

* ssh: stabilize SSH MaxSessions read by `@acerv <https://github.com/acerv>`__ in `#82 <https://github.com/linux-test-project/kirk/pull/82>`__
* ssh: ignore decoding errors in utf-8 during connection by `@acerv <https://github.com/acerv>`__ in `#84 <https://github.com/linux-test-project/kirk/pull/84>`__
* session: implement forcibly stop by `@acerv <https://github.com/acerv>`__ in `#83 <https://github.com/linux-test-project/kirk/pull/83>`__
* updated documentation

**Full Changelog**: `v3.0...v3.1 <https://github.com/linux-test-project/kirk/compare/v3.0...v3.1>`__

v3.0 (2025-10-23)
-----------------

**What's Changed**

* Support SUT customizations via plugins by `@acerv <https://github.com/acerv>`__ in `#71 <https://github.com/linux-test-project/kirk/pull/71>`__
* scheduler: set CONF status for timed out tests by `@acerv <https://github.com/acerv>`__ in `#81 <https://github.com/linux-test-project/kirk/pull/81>`__


**Full Changelog**: `v2.3...v3.0 <https://github.com/linux-test-project/kirk/compare/v2.3...v3.0>`__

v2.3 (2025-09-22)
-----------------

**What's Changed**

* ltp: don't override LTP_TIMEOUT_MUL if set by user by `@wangli5665 <https://github.com/wangli5665>`__ in `#70 <https://github.com/linux-test-project/kirk/pull/70>`__
* Make the hvc0 parameter explicit by `@grisu48 <https://github.com/grisu48>`__ in `#74 <https://github.com/linux-test-project/kirk/pull/74>`__
* ssh: catch ConnectionError in communicate by `@acerv <https://github.com/acerv>`__ in `#76 <https://github.com/linux-test-project/kirk/pull/76>`__
* documentation improvements
* improve strong typing support via ruff and pyrefly


**New Contributors**

* `@grisu48 <https://github.com/grisu48>`__ made their first contribution in `#74 <https://github.com/linux-test-project/kirk/pull/74>`__

**Full Changelog**: `v2.2.2...v2.3 <https://github.com/linux-test-project/kirk/compare/v2.2.2...v2.3>`__

v2.2.2 (2025-08-26)
-------------------

Fix a Qemu critical bug that was introduced in v2.2.1 and it was making Qemu support unusable:
* `fea2f6363a77ef4f7740dbe7e162ccf21cd90b4b <https://github.com/linux-test-project/kirk/commit/fea2f6363a77ef4f7740dbe7e162ccf21cd90b4b>`__

**Full Changelog**: `v2.2.1...v2.2.2 <https://github.com/linux-test-project/kirk/compare/v2.2.1...v2.2.2>`__

v2.2.1 (2025-08-25)
-------------------

**What's Changed**

This minor version introduces significant changes to the code due to the implementation of strong typing. The decision to add strong typing to the Python code stems from the need to identify bugs before introducing new features by cross-checking multiple types and ensuring we do not inadvertently mix them up. This is achieved using pyrefly and ruff, which are currently among the fastest and most comprehensive tools available.

* Static typing support by `@acerv <https://github.com/acerv>`__ in `#68 <https://github.com/linux-test-project/kirk/pull/68>`__
* complete dict and list typing by `@acerv <https://github.com/acerv>`__ in `24d85e0c9fe0a4ba114b0c26dba400da03d2e225 <https://github.com/linux-test-project/kirk/commit/24d85e0c9fe0a4ba114b0c26dba400da03d2e225>`__

**Full Changelog**: `v2.2...v2.2.1 <https://github.com/linux-test-project/kirk/compare/v2.2...v2.2.1>`__

v2.2 (2025-08-18)
-----------------

**What's Changed**

* scheduler: fix wrong execution time on runtime by `@acerv <https://github.com/acerv>`__ in `#55 <https://github.com/linux-test-project/kirk/pull/55>`__
* Respect LTPROOT from environment if set by `@dev-japo <https://github.com/dev-japo>`__ in `#56 <https://github.com/linux-test-project/kirk/pull/56>`__
* ui: rearrange UI to show information in a better way by `@acerv <https://github.com/acerv>`__ in `#57 <https://github.com/linux-test-project/kirk/pull/57>`__
* ltp: leave quotes when parsing commands in runtest files by `@acerv <https://github.com/acerv>`__ in `#61 <https://github.com/linux-test-project/kirk/pull/61>`__
* ui: make parallel ui less interactive by `@acerv <https://github.com/acerv>`__ in `#59 <https://github.com/linux-test-project/kirk/pull/59>`__
* ltp: use regex to parse test arguments in runtest file by `@acerv <https://github.com/acerv>`__ in `#62 <https://github.com/linux-test-project/kirk/pull/62>`__
* New kirk documentation by `@acerv <https://github.com/acerv>`__ in `#63 <https://github.com/linux-test-project/kirk/pull/63>`__
* kirk: Add results JSON to logs convertor script by `@wangli5665 <https://github.com/wangli5665>`__ in `#53 <https://github.com/linux-test-project/kirk/pull/53>`__
* Fault injection support by `@acerv <https://github.com/acerv>`__ in `#66 <https://github.com/linux-test-project/kirk/pull/66>`__


**New Contributors**

* `@dev-japo <https://github.com/dev-japo>`__ made their first contribution in `#56 <https://github.com/linux-test-project/kirk/pull/56>`__
* `@wangli5665 <https://github.com/wangli5665>`__ made their first contribution in `#53 <https://github.com/linux-test-project/kirk/pull/53>`__

**Full Changelog**: `v2.1...v2.2 <https://github.com/linux-test-project/kirk/compare/v2.1...v2.2>`__

v2.1 (2025-05-27)
-----------------

* ssh module now supports ``known_hosts``
* removed external frameworks implementation (`515a5053170a04d3b6f9db0be7217f66fb6cfcb8 <https://github.com/linux-test-project/kirk/commit/515a5053170a04d3b6f9db0be7217f66fb6cfcb8>`__, `#44 <https://github.com/linux-test-project/kirk/pull/44>`__)
* fix: complete ui events on keyboard interrupt
* fix: correctly handle all ssh errors

v2.0 (2025-04-16)
-----------------

**What's Changed**

* add script to convert kirk output to HTML
* new option ``--run-pattern``
* new option ``--suite-iterate``
* new option ``--randomize``
* new option ``--monitor``
* new option ``--runtime``
* introduced introducing ``<value> + suffix`` for timeout values
* much faster user interface
* fix tainted stderr handling
* gracefully stop after user interrupt
* many clean-ups

v1.5 (2025-02-12)
-----------------

**What's Changed**

* Fix stats calculation of aggregate results by `@jkchen1095 <https://github.com/jkchen1095>`__ in `#26 <https://github.com/linux-test-project/kirk/pull/26>`__
* libkirk/events: register the event handler for suite_timeout by `@Chunyu-Hu <https://github.com/Chunyu-Hu>`__ in `#30 <https://github.com/linux-test-project/kirk/pull/30>`__
* using toml format for setuptools
* fixed typos

**Full Changelog**: `v1.4...v1.5 <https://github.com/linux-test-project/kirk/compare/v1.4...v1.5>`__

v1.4 (2024-07-26)
-----------------

- fixed setuptools information
- pypi package

v1.3 (2024-06-10)
-----------------

**What's Changed**

* Fix cgroup kselftests collection by `@acerv <https://github.com/acerv>`__ in `#14 <https://github.com/linux-test-project/kirk/pull/14>`__
* Kselftests fix test name by `@acerv <https://github.com/acerv>`__ in `#15 <https://github.com/linux-test-project/kirk/pull/15>`__
* Wait for SSH command to complete after execution by `@acerv <https://github.com/acerv>`__ in `#16 <https://github.com/linux-test-project/kirk/pull/16>`__
* Fix SSH execution not redirecting output properly by `@acerv <https://github.com/acerv>`__ in `#17 <https://github.com/linux-test-project/kirk/pull/17>`__
* SSH module is not showing live stdout/stderr by `@acerv <https://github.com/acerv>`__ in `#18 <https://github.com/linux-test-project/kirk/pull/18>`__


**Full Changelog**: `v1.2...v1.3 <https://github.com/linux-test-project/kirk/compare/v1.2...v1.3>`__

v1.2 (2024-01-09)
-----------------

- show both stdout and stderr when executing tests on host
- support for external commands on different SUTs
- warning message when SUT doesn't support parallel execution
- more stable epoll() communication with LTX
- minor fixes
- updated documentation

v1.1 (2023-09-15)
-----------------

- fix RuntimeError exception when SIGINT is received
- filter LTP tests by max_runtime
