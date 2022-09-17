#!/usr/bin/env python

# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from main import calculate_score

class TestCalculateScore(unittest.TestCase):
    def test_failed(self):
        self.assertEqual(calculate_score('X'), 0)

    def test_1_attempt(self):
        self.assertEqual(calculate_score('1'), 6)

    def test_6_attempts(self):
        self.assertEqual(calculate_score('6'), 1)

    def test_8_attempt(self):
        with self.assertRaises(ValueError):
            calculate_score('8')

    def test_negative_attempt(self):
        self.assertEqual(calculate_score('-1'), 0)

    def test_invalid_char(self):
        self.assertEqual(calculate_score('Y'), 0)


if __name__ == "__main__":
    unittest.main()
