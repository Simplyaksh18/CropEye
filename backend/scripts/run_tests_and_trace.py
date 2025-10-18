"""
Run unittest discovery programmatically, then trace open sqlite3 connections in the same process.
This helps find connections that would otherwise be closed at process exit.
"""
import unittest
import sys
import subprocess

loader = unittest.TestLoader()
suite = loader.discover(start_dir='.', pattern='test_*.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# After tests, run the tracer
from scripts.trace_close_sqlite import *

# Exit with non-zero if tests failed
if not result.wasSuccessful():
    sys.exit(1)
