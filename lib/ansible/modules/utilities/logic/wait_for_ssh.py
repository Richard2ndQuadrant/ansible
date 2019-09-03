#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2ndQuadrant Limited <info@2ndquadrant.com>
# (c) 2017, Dag Wieers <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': '2ndQuadrant'}


DOCUMENTATION = r'''
---
module: wait_for_ssh
short_description: Waits until remote system is reachable/usable via ssh
description:
- Waits for a total of C(timeout) seconds.
- Tests the transport connection every C(sleep) seconds.
- This module does not depend on Python being installed on the target.
version_added: "2.3"
options:
  delay:
    description:
      - Number of seconds to wait before starting to poll.
    default: 0
  sleep:
    default: 1
    description:
      - Number of seconds to sleep between checks.
  timeout:
    description:
      - Maximum number of seconds to wait for.
    default: 600
author: "Abhijit Menon-Sen (@amenonsen)"
'''

EXAMPLES = r'''
- name: Wait 600 seconds for target connection to become reachable/usable
  wait_for_ssh:

- name: Wait 300 seconds, but only start checking after 60 seconds
  wait_for_ssh:
    delay: 60
    timeout: 300
'''

RETURN = r'''
elapsed:
  description: The number of seconds that elapsed waiting for the connection to appear.
  returned: always
  type: int
  sample: 23
'''
