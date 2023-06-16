#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_scheduled_task - Windows Schedules Task check
#
# Copyright (C) 2020-2021  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pytest
from datetime import datetime
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import win_scheduled_task

EXAMPLE_STRING_TABLE = [
    ['\\Adobe Acrobat Update Task', '0', '02/19/2021 17:00:00', '02/20/2021 17:00:00'],
    ['\\Git for Windows Updater', '0', '02/19/2021 08:23:23', '02/20/2021 08:23:23'],
    ['\\BackToTheFuture', '0', '02/19/2021 18:01:01', '02/20/2021 18:01:01'],
    ['\\CreateExplorerShellUnelevatedTask', '1073807364', '08/15/2019 10:51:51'],
]
EXAMPLE_SECTION = {
    '\\Adobe Acrobat Update Task': {
        'lastResult': 0,
        'lastRun': datetime(2021, 2, 19, 17, 0),
        'nextRun': datetime(2021, 2, 20, 17, 0),
    },
    '\\Git for Windows Updater': {
        'lastResult': 0,
        'lastRun': datetime(2021, 2, 19, 8, 23, 23),
        'nextRun': datetime(2021, 2, 20, 8, 23, 23),
    },
    '\\BackToTheFuture': {
        'lastResult': 0,
        'lastRun': datetime(2021, 2, 19, 18, 1, 1),
        'nextRun': datetime(2021, 2, 20, 18, 1, 1),
    },
    '\\CreateExplorerShellUnelevatedTask': {
        'lastResult': 1073807364,
        'lastRun': datetime(2019, 8, 15, 10, 51, 51),
    }
}


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        EXAMPLE_STRING_TABLE,
        EXAMPLE_SECTION
    ),
])
def test_parse_win_scheduled_task(string_table, result):
    assert win_scheduled_task.parse_win_scheduled_task(string_table) == result


@pytest.mark.parametrize('params, section, result', [
    ([], {}, []),
    ([], EXAMPLE_SECTION, []),
    ([{'tasks': []}], EXAMPLE_SECTION, []),
    (
        [{'tasks': ['\\Git']}],
        EXAMPLE_SECTION,
        [Service(item='\\Git for Windows Updater', parameters={'tasks': ['\\Git for Windows Updater']})]
    ),
    (
        [{'groupname': 'GIT', 'tasks': ['\\Git']}],
        EXAMPLE_SECTION,
        [Service(item='GIT', parameters={'tasks': ['\\Git for Windows Updater']})]
    ),
    (
        [{'groupname': 'GIT', 'tasks': ['.*Update.*']}],
        EXAMPLE_SECTION,
        [Service(item='GIT', parameters={'tasks': ['\\Adobe Acrobat Update Task', '\\Git for Windows Updater']})]
    ),
])
def test_discovery_win_scheduled_task(params, section, result):
    assert list(win_scheduled_task.discovery_win_scheduled_task(params, section)) == result


@pytest.mark.parametrize('params, result', [
    (
        {'states': {0: 0}, 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.OK, summary='last result: 0'),
            Result(state=State.OK, notice='Last Run: 9 hours 36 minutes'),
        ]
    ),
    (
        {'states': {1: 0}, 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.CRIT, summary='last result: 0'),
            Result(state=State.OK, notice='Last Run: 9 hours 36 minutes'),
        ]
    ),
    (
        {'states': {1: 0}, 'else': 1, 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.WARN, summary='last result: 0'),
            Result(state=State.OK, notice='Last Run: 9 hours 36 minutes'),
        ]
    ),
    (
        {'states': {0: 0}, 'tasks': ['\\Adobe Acrobat Update Task', '\\Git for Windows Updater']},
        [
            Result(state=State.OK, notice='\\Adobe Acrobat Update Task last result: 0'),
            Result(state=State.OK, notice='Last Run: 1 hour 0 minutes'),
            Result(state=State.OK, notice='\\Git for Windows Updater last result: 0'),
            Result(state=State.OK, notice='Last Run: 9 hours 36 minutes'),
        ]
    ),
    (
        {'states': {0: 0}, 'tasks': ['\\Adobe Acrobat Update Task', '\\CreateExplorerShellUnelevatedTask']},
        [
            Result(state=State.OK, notice='\\Adobe Acrobat Update Task last result: 0'),
            Result(state=State.OK, notice='Last Run: 1 hour 0 minutes'),
            Result(state=State.CRIT, summary='\\CreateExplorerShellUnelevatedTask last result: 1073807364'),
            Result(state=State.OK, notice='Last Run: 1 year 189 days'),
        ]
    ),
    (
        {'states': {0: 0}, 'maxage': (36000, 40000), 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.OK, summary='last result: 0'),
            Result(state=State.OK, notice='Last Run: 9 hours 36 minutes'),
        ]
    ),
    (
        {'states': {0: 0}, 'maxage': (3600, 40000), 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.OK, summary='last result: 0'),
            Result(state=State.WARN, notice='Last Run: 9 hours 36 minutes (warn/crit at 1 hour 0 minutes/11 hours 6 minutes)'),
        ]
    ),
    (
        {'states': {0: 0}, 'maxage': (3600, 4000), 'tasks': ['\\Git for Windows Updater']},
        [
            Result(state=State.OK, summary='last result: 0'),
            Result(state=State.CRIT, notice='Last Run: 9 hours 36 minutes (warn/crit at 1 hour 0 minutes/1 hour 6 minutes)'),
        ]
    ),
    (
        {'states': {0: 0}, 'tasks': ['\\BackToTheFuture']},
        [
            Result(state=State.OK, summary='last result: 0'),
            Result(state=State.OK, notice='Last Run in: 1 minute 1 second'),
        ]
    ),
])
def test_check_win_scheduled_task(freezer, params, result):
    freezer.move_to('2021-02-19 18:00')
    assert list(win_scheduled_task.check_win_scheduled_task('item', params, EXAMPLE_SECTION)) == result
