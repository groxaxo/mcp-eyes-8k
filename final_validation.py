#!/usr/bin/env python3
"""
Final validation script - runs all tests and checks.
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}")
    print(f"Running: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout[:500]}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr[:500]}")
        return False

def main():
    print("="*70)
    print("  MCP Eyes 8K - Final Validation")
    print("="*70)
    
    tests = [
        ("python test_suite.py", "Core Functionality Tests"),
        ("python test_server.py", "Server Startup Tests"),
        ("python demo_usage.py", "Usage Demonstration"),
        ("python -c 'from active_vision import examine_image; print(\"Import check: OK\")'", "Module Import Check"),
        ("ls -l test_images/", "Test Images Check"),
    ]
    
    results = []
    for cmd, desc in tests:
        results.append((desc, run_command(cmd, desc)))
    
    print("\n" + "="*70)
    print("  VALIDATION SUMMARY")
    print("="*70)
    
    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {desc}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All validation tests passed!")
        print("The MCP Eyes 8K project is fully functional and ready to use!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
