#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# win_schedules_task - Windows NFS Share check
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@scs.ch>
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
    Dictionary,
    DropdownChoice,
    ListOf,
    ListOfStrings,
    MonitoringState,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
    RulespecGroupCheckParametersDiscovery,
    HostRulespec,
)


def _valuespec_inventory_win_scheduled_task_rules():
    return Dictionary(
        title=_("Windows Scheduled Task Discovery"),
        elements=[
            ('groupname',
             TextAscii(
                 title=_("Name of group"),
                 help=_('Group the matchedscheduled tasks.'),
                 size=10,
             ),
            ),
            ('tasks',
             ListOfStrings(
                 title=_("Scheduled Tasks (Regular Expressions)"),
                 help=_('Regular expressions matching the begining of the path and name '
                        'of the scheduled task.'
                        'If no name is given then this rule will match all scheduled tasks. The '
                        'match is done on the <i>beginning</i> of the service name. It '
                        'is done <i>case sensitive</i>. You can do a case insensitive match '
                        'by prefixing the regular expression with <tt>(?i)</tt>. Example: '
                        '<tt>(?i).*mssql</tt> matches all services which contain <tt>MSSQL</tt> '
                        'or <tt>MsSQL</tt> or <tt>mssql</tt> or...'),
                 orientation="horizontal",
             )),
        ],
        help=_(
            'This rule can be used to configure the inventory of the windows scheduled task check. '
            'You can configure specific scheduled task to be monitored by the windows check by '
            'selecting them by name, current state during the inventory, or start mode.'),
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupCheckParametersDiscovery,
        match_type="all",
        name="inventory_win_scheduled_task_rules",
        valuespec=_valuespec_inventory_win_scheduled_task_rules,
    ))

def _item_spec__win_scheduled_tasks():
    return TextAscii(title=_("Name of the scheduled task"),
                     allow_empty=False)

def _parameter_valuespec_services():
    return Dictionary(elements=[
        ("maxage",
         Tuple(
             title=_("Maximal time since last run"),
             elements=[
                 Age(title=_("Warning if older than")),
                 Age(title=_("Critical if older than")),
             ],
         )),
        ("states",
         ListOf(
             Tuple(orientation="horizontal",
                   elements=[
                       Integer(
                           title=_("Expected state"),
                       ),
                       MonitoringState(title=_("Resulting state"),),
                   ],
                   default_value=(0, 0)),
             title=_("Services states"),
             help=_("You can specify a separate monitoring state for each "
                    "lastr un state."
             ),
         )), (
             "else",
             MonitoringState(
                 title=_("State if no entry matches"),
                 default_value=2,
             ),
         ),
    ],)

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="win_scheduled_tasks",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_win_scheduled_tasks,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_win_scheduled_tasks,
        title=lambda: _("Windows Scheduled Tasks"),
    ))
