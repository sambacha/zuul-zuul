# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import fixtures
import tempfile
import testtools

import zuul.cmd


class TestCmd(testtools.TestCase):
    def test_read_config_with_environment(self):
        "Test that readConfig interpolates environment vars"

        with tempfile.NamedTemporaryFile() as test_config:
            test_config.write(b'[DEFAULT]\nfoo=%(ENV_TEST)s\n')
            test_config.flush()
            with fixtures.EnvironmentVariable('ENV_TEST', 'baz'):
                app = zuul.cmd.ZuulApp()
                app.parseArguments(['-c', test_config.name])
                app.readConfig()
                self.assertEquals('baz', app.config.get('DEFAULT', 'foo'))
