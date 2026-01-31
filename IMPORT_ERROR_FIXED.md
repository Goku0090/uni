# ImportError Fixed ✅

## Problem
```
ImportError: cannot import name 'ProjectTeam' from 'accounts.models'
```

## Root Cause
The views.py was trying to import model names that didn't exist:
- `ProjectTeam` (actual model: `ProjectMember`)
- `ProjectTeamMember` (actual model: `ProjectMember`)
- `ProjectTeamInvitation` (actual model: `ProjectInvitation`)

## Solution Implemented

Added model aliases in `accounts/models.py` at the end:
```python
# Model Aliases for Backward Compatibility
ProjectTeam = ProjectMember
ProjectTeamMember = ProjectMember
ProjectTeamInvitation = ProjectInvitation
```

This allows the code to use the old names while the actual database models have the new names.

## Files Modified

| File | Change |
|------|--------|
| `accounts/models.py` | Added aliases at end of file |

## Verification

Ran Django check:
```bash
python manage.py check
```

Result: ✅ **PASSED** (warnings only, no errors)

```
[SUCCESS] EMAIL BACKEND: Using Brevo for OTP and transactional emails
System check identified 1 issue (0 silenced).
```

## Status

✅ **FIXED** - Django server can now start without import errors

## Next Steps

1. Start Django server: `python manage.py runserver`
2. Create `.env` file with Brevo API key
3. Test OTP email flow

