# -*- coding: utf-8 -*-
# Copyright © 2ndQuadrant Limited <info@2ndquadrant.com>
#
# Loosely based on wait_for_connection.py, which is:
# (c) 2017, Dag Wieers <dag@wieers.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# CI-required python3 boilerplate
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
from datetime import datetime, timedelta

from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class TimedOutException(Exception):
    pass


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    DEFAULT_CONNECT_TIMEOUT = 5
    DEFAULT_DELAY = 0
    DEFAULT_SLEEP = 1
    DEFAULT_TIMEOUT = 600

    def do_until_success_or_timeout(self, what, timeout, connect_timeout, what_desc, sleep=1):
        max_end_time = datetime.utcnow() + timedelta(seconds=timeout)

        e = None
        while datetime.utcnow() < max_end_time:
            try:
                what(connect_timeout)
                if what_desc:
                    display.debug("wait_for_ssh: %s success" % what_desc)
                return
            except Exception as e:
                error = e  # PY3 compatibility to store exception for use outside of this block
                if what_desc:
                    display.debug("wait_for_ssh: %s fail (expected), retrying in %d seconds..." % (what_desc, sleep))
                time.sleep(sleep)

        raise TimedOutException("timed out waiting for %s: %s" % (what_desc, error))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        connect_timeout = int(self._task.args.get('connect_timeout', self.DEFAULT_CONNECT_TIMEOUT))
        delay = int(self._task.args.get('delay', self.DEFAULT_DELAY))
        sleep = int(self._task.args.get('sleep', self.DEFAULT_SLEEP))
        timeout = int(self._task.args.get('timeout', self.DEFAULT_TIMEOUT))

        if self._play_context.check_mode:
            display.vvv("wait_for_ssh: skipping for check_mode")
            return dict(skipped=True)

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        def raw_test(connect_timeout):
            display.vvv("wait_for_ssh: attempting raw test")
            raw_result = self._low_level_execute_command('echo pong')
            if raw_result['stdout'].strip() != 'pong':
                raise Exception('raw test failed')

        start = datetime.now()

        if delay:
            time.sleep(delay)

        try:
            self.do_until_success_or_timeout(raw_test, timeout, connect_timeout, what_desc="raw test", sleep=sleep)

        except TimedOutException as e:
            result['failed'] = True
            result['msg'] = str(e)

        elapsed = datetime.now() - start
        result['elapsed'] = elapsed.seconds

        return result
