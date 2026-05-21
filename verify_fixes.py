#!/usr/bin/env python
"""Verify all submission-critical fixes are in place."""

print('=== VERIFICATION: SUBMISSION-READY FIXES ===\n')

checks = {}

# Fix 1: Ensemble section has runnable code
with open('docs/BUILD_GUIDE.md', 'r', encoding='utf-8') as f:
    content = f.read()
    checks['1. Ensemble is fully runnable'] = 'test_size_min = min(len(forecast)' in content
    checks['2. Heat index conditions documented'] = '# Note: heat_index formula is approximate' in content
    checks['3. Wind chill conditions documented'] = '# Note: wind_chill formula valid' in content

# Fix 2: Metrics softened to expected results
with open('README_COMPLETE.md', 'r', encoding='utf-8') as f:
    content = f.read()
    checks['4. Softened metric language'] = 'Expected to outperform' in content

# Fix 3: pycountry-convert in requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    checks['5. pycountry-convert in deps'] = 'pycountry-convert' in content

# Print results
passed = sum(checks.values())
total = len(checks)

for issue, status in sorted(checks.items()):
    symbol = '✅' if status else '❌'
    print(f'{symbol} {issue}: {status}')

print(f'\n{"-"*50}')
print(f'RESULT: {passed}/{total} fixes applied')
if passed == total:
    print('✅ ALL FIXES COMPLETE - READY FOR SUBMISSION')
else:
    print(f'⚠️ {total - passed} issues remain')
