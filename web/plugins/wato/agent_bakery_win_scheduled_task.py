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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

try:
    from cmk.gui.cee.plugins.wato.agent_bakery import (
        RulespecGroupMonitoringAgentsWindowsAgent
    )
except Exception:
    RulespecGroupMonitoringAgentsWindowsAgent = None


def _valuespec_agent_config_win_scheduled_task():
    return DropdownChoice(
        title=_('Windows Scheduled Task'),
        help=_('This will deploy the agent plugin <tt>win_scheduled_task</tt> '
               'for checking Windows Scheduled Task.'),
        choices=[
            (True, _('Deploy Windows Scheduled Task plugin')),
            (None, _('Do not deploy Windows Scheduled Task plugin')),
        ],
    )


if RulespecGroupMonitoringAgentsWindowsAgent is not None:
    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsWindowsAgent,
            name='agent_config:win_scheduled_task',
            valuespec=_valuespec_agent_config_win_scheduled_task,
        ))
