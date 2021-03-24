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

# <<<win_scheduled_task:sep(9):encoding(cp437)>>>
# \Adobe Acrobat Update Task	0	02/19/2021 17:00:00	02/20/2021 17:00:00
# \Git for Windows Updater	0	02/19/2021 08:23:23	02/20/2021 08:23:23
# \CreateExplorerShellUnelevatedTask	1073807364	08/15/2019 10:51:51

import re
from datetime import datetime
from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Result,
    Service,
    State,
)


def parse_win_scheduled_task(string_table):
    parsed = {}

    for item in string_table:
        try:
            parsed[item[0]] = {
                'lastResult': int(item[1]),
            }
            if len(item) >= 3:
                parsed[item[0]]['lastRun'] = datetime.strptime(item[2], "%m/%d/%Y %H:%M:%S")
            if len(item) >= 4:
                parsed[item[0]]['nextRun'] = datetime.strptime(item[3], "%m/%d/%Y %H:%M:%S")
        except Exception:
            pass
    return parsed


register.agent_section(
    name='win_scheduled_task',
    parse_function=parse_win_scheduled_task,
)


def discovery_win_scheduled_task(params, section):
    for param in params:
        discoverd_tasks = set()
        if 'tasks' not in param:
            continue

        for task in param['tasks']:
            try:
                regex = re.compile(task)
                discoverd_tasks.update(filter(regex.match, section.keys()))
            except Exception:
                discoverd_tasks.update(filter(lambda t: t.startswith(task), section.keys()))

        if 'groupname' in param:
            yield Service(item=param['groupname'], parameters={'tasks': sorted(list(discoverd_tasks))})
        else:
            for task in discoverd_tasks:
                yield Service(item=task, parameters={'tasks': [task]})


def check_win_scheduled_task(item, params, section):
    now = datetime.now()

    states = params['states']
    if isinstance(params['states'], list):
        states = dict(params['states'])

    for taskname in params['tasks']:
        if taskname in section:
            task = section[taskname]
            state = State(states.get(task['lastResult'], params.get('else', 2)))

            if len(params['tasks']) > 1:
                yield Result(state=state, notice=f'{taskname} last result: {task["lastResult"]}')
            else:
                yield Result(state=state, summary=f'last result: {task["lastResult"]}')

            if 'lastRun' in task:
                age = now - task['lastRun']
                yield from check_levels(
                    value=age.total_seconds(),
                    levels_upper=params.get('maxage', None),
                    render_func=render.timespan,
                    label="Last Run",
                    notice_only=True,
                )
        else:
            yield Result(state=State.UNKNOWN, summary=f'{taskname} not found')


register.check_plugin(
    name='win_scheduled_task',
    service_name='Task %s',
    discovery_function=discovery_win_scheduled_task,
    discovery_ruleset_name='inventory_win_scheduled_task_rules',
    discovery_default_parameters={},
    discovery_ruleset_type=register.RuleSetType.ALL,
    check_function=check_win_scheduled_task,
    check_ruleset_name='win_scheduled_tasks',
    check_default_parameters={'states': {0: 0}, 'else': 1},
)
