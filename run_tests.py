#!/usr/bin/env python
"""
Test runner script for SwissAxa Portal
"""
import sys
import subprocess

def run_tests():
    """Run pytest with coverage"""
    print("=" * 60)
    print("Running SwissAxa Portal Test Suite")
    print("=" * 60)
    print()
    
    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short',
        '--cov=app',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--cov-report=xml'
    ]
    
    # Add any command line arguments
    cmd.extend(sys.argv[1:])
    
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == '__main__':
    sys.exit(run_tests())

