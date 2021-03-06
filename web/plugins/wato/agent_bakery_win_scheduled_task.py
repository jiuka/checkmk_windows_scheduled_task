#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)

try:
    from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsWindowsAgent
except:
    from cmk.gui.plugins.wato import RulespecGroupCheckParametersStorage as RulespecGroupMonitoringAgentsWindowsAgent

def _valuespec_agent_config_win_scheduled_task():
    return DropdownChoice(
        title=_("Windows Scheduled Task"),
        help=_("This will deploy the agent plugin <tt>win_scheduled_task</tt> "
               "for checking Windows Scheduled Task."),
        choices=[
            (True, _("Deploy Windows Scheduled Task plugin")),
            (None, _("Do not deploy Windows Scheduled Task plugin")),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsWindowsAgent,
        name="agent_config:win_scheduled_task",
        valuespec=_valuespec_agent_config_win_scheduled_task,
    ))
