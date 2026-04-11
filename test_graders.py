#!/usr/bin/env python3
"""Test script to verify graders work correctly."""

import sys
sys.path.insert(0, '/Users/admin/openenv-round1-email-triage')

# Test 1: Import from root grader.py
print("=" * 50)
print("TEST 1: Import from root grader.py")
print("=" * 50)
try:
    import grader
    print(f"✓ grader module imported")
    print(f"  - grade_easy: {grader.grade_easy}")
    print(f"  - grade_medium: {grader.grade_medium}")
    print(f"  - grade_hard: {grader.grade_hard}")
except Exception as e:
    print(f"✗ Failed to import grader: {e}")
    sys.exit(1)

# Test 2: Call graders with empty state
print("\n" + "=" * 50)
print("TEST 2: Call graders with empty state")
print("=" * 50)
state = {"category_done": False, "priority_done": False, "reply_done": False}
try:
    score_easy = grader.grade_easy(state)
    score_medium = grader.grade_medium(state)
    score_hard = grader.grade_hard(state)
    print(f"✓ grade_easy(empty_state) = {score_easy}")
    print(f"✓ grade_medium(empty_state) = {score_medium}")
    print(f"✓ grade_hard(empty_state) = {score_hard}")
    
    # Check bounds
    for name, score in [("easy", score_easy), ("medium", score_medium), ("hard", score_hard)]:
        if 0 < score < 1:
            print(f"  ✓ {name} score {score} is strictly between 0 and 1")
        else:
            print(f"  ✗ {name} score {score} is NOT strictly between 0 and 1")
            sys.exit(1)
except Exception as e:
    print(f"✗ Grader call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Call with full state
print("\n" + "=" * 50)
print("TEST 3: Call graders with full state")
print("=" * 50)
full_state = {"category_done": True, "priority_done": True, "reply_done": True}
try:
    score_easy = grader.grade_easy(full_state)
    score_medium = grader.grade_medium(full_state)
    score_hard = grader.grade_hard(full_state)
    print(f"✓ grade_easy(full_state) = {score_easy}")
    print(f"✓ grade_medium(full_state) = {score_medium}")
    print(f"✓ grade_hard(full_state) = {score_hard}")
    
    for name, score in [("easy", score_easy), ("medium", score_medium), ("hard", score_hard)]:
        if 0 < score < 1:
            print(f"  ✓ {name} score {score} is strictly between 0 and 1")
        else:
            print(f"  ✗ {name} score {score} is NOT strictly between 0 and 1")
            sys.exit(1)
except Exception as e:
    print(f"✗ Grader call failed: {e}")
    sys.exit(1)

# Test 4: Parse openenv.yaml
print("\n" + "=" * 50)
print("TEST 4: Parse openenv.yaml")
print("=" * 50)
try:
    import yaml
    with open('/Users/admin/openenv-round1-email-triage/openenv.yaml') as f:
        config = yaml.safe_load(f)
    print(f"✓ openenv.yaml parsed")
    print(f"  - spec_version: {config.get('spec_version')}")
    print(f"  - app: {config.get('app')}")
    print(f"  - port: {config.get('port')}")
    tasks = config.get('tasks', [])
    print(f"  - tasks: {len(tasks)} found")
    for task in tasks:
        print(f"    - {task.get('id')}: grader={task.get('grader')}")
    if len(tasks) != 3:
        print(f"✗ Expected 3 tasks, got {len(tasks)}")
        sys.exit(1)
except ImportError:
    print("⚠ PyYAML not installed, skipping")
except Exception as e:
    print(f"✗ YAML parsing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("ALL TESTS PASSED ✓")
print("=" * 50)
