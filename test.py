#!/usr/bin/env python2.7
# coding:UTF-8

import re
import unittest

from os import listdir, path

file_pattern = re.compile("^test[a-z]+\\.py$")
module_pattern = re.compile("^test[a-z]+$")
class_pattern = re.compile("^Test[A-Z][a-zA-Z]+$")

test_dir = path.dirname(path.abspath(__file__)) + "/__tests__"
parent_modules = [__import__("__tests__." + f.replace(".py", "")) for f in listdir(test_dir) if file_pattern.match(f)]
test_modules = set([t[1] for parent_module in parent_modules for t in parent_module.__dict__.items() if module_pattern.match(t[0])])
test_suites = [t[1] for test_module in test_modules for t in test_module.__dict__.items() if class_pattern.match(t[0])]

runner = unittest.TextTestRunner()
runner.run(unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(test_suite) for test_suite in test_suites]))
