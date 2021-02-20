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

import pytest  # type: ignore[import]
import check_parameters_win_scheduled_task


class TestVsDiscoveryWinSchedulesTaskRules:
    @pytest.fixture
    def vs(self):
        return check_parameters_win_scheduled_task._valuespec_inventory_win_scheduled_task_rules()

    @pytest.mark.parametrize('data', [
        ({'tasks': ['Win/.*']}),
        ({'tasks': ['Win/.*', 'MS/.*']}),
        ({'groupname': 'groupname', 'tasks': ['Win/.*', 'MS/.*']}),
    ])
    def test_validate_datatype(self, vs, data):
        assert vs.validate_datatype(data, '') is None


class TestVsParametersWinSchedulesTask:
    @pytest.fixture
    def vs(self):
        return check_parameters_win_scheduled_task._parameter_valuespec_win_scheduled_tasks()

    @pytest.mark.parametrize('data', [
        ({'states': []}),
        ({'states': {}}),
        ({'states': [(0, 1), (2, 3)]}),
        ({'states': {0: 1, 2: 3}}),
        ({'else': 2}),
        ({'maxage': (10, 20)}),
    ])
    def test_validate_datatype(self, vs, data):
        assert vs.validate_datatype(data, '') is None

    @pytest.mark.parametrize('input, output', [
        ({'states': []}, {'states': {}}),
        ({'states': {}}, {'states': {}}),
        ({'states': [(0, 1), (2, 3)]}, {'states': {0: 1, 2: 3}}),
        ({'states': {0: 1, 2: 3}}, {'states': {0: 1, 2: 3}}),
    ])
    def test_transform_value(self, vs, input, output):
        assert vs.transform_value(input) == output
