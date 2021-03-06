# Copyright 2018 BMW Car IT GmbH
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.


from zuul.ansible import paths
from ansible.errors import AnsibleError
command = paths._import_ansible_action_plugin("command")


class ActionModule(command.ActionModule):

    def run(self, tmp=None, task_vars=None):
        if paths._is_localhost_task(self):
            raise AnsibleError("Executing local code is prohibited")

        # we need the zuul_log_id on shell and command tasks
        host = paths._sanitize_filename(task_vars.get('inventory_hostname'))
        if self._task.action in ('command', 'shell'):
            self._task.args['zuul_log_id'] = "%s-%s" % (self._task._uuid, host)

        return super(ActionModule, self).run(tmp, task_vars)
