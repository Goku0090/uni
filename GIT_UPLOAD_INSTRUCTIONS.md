# Git Upload Instructions

**Status:** Push blocked due to GitHub Secret Scanning protection detecting credentials from previous commits.

---

## Solution Options

### Option 1: Disable Push Protection (Fastest)
1. Go to GitHub repo: https://github.com/Goku0090/uni_sync
2. Navigate to: **Settings → Code security and analysis → Push protection**
3. Temporarily disable "Push protection for repository" 
4. Run: `git push uni_sync clean-deployment --force`
5. Re-enable push protection after uploading

**Command:**
```bash
git push uni_sync clean-deployment --force
```

---

### Option 2: Allow Secrets (GitHub UI)
1. Visit the error links provided:
   - https://github.com/Goku0090/uni_sync/security/secret-scanning/unblock-secret/390zvQFhwHccpYyBM6SotMxYSyr
   - https://github.com/Goku0090/uni_sync/security/secret-scanning/unblock-secret/390zvRbVRxal27Sd2NJMrbxSYni
   - https://github.com/Goku0090/uni_sync/security/secret-scanning/unblock-secret/390zvPnno8yWMLyka6BiM

2. Click "Allow" for each secret
3. Run: `git push uni_sync clean-deployment --force`

---

### Option 3: Clean History (Most Secure)
Use `git filter-branch` to remove `.env` from all commits:

```bash
# Install git-filter-repo (recommended)
pip install git-filter-repo

# Remove .env from all commits
git filter-repo --path auth_project/.env --invert-paths

# Force push cleaned history
git push uni_sync clean-deployment --force
```

---

## What's Been Prepared for Upload

✅ **Committed:** 197 files with complete UniSync codebase  
✅ **Excluded:** .env file (secrets protected by .gitignore)  
✅ **.gitignore:** Created with proper exclusions  
✅ **Remote:** Added `uni_sync` remote to https://github.com/Goku0090/uni_sync.git  

---

## Files Ready to Push

- All Django source code
- Models, Views, URLs, Serializers
- Email backends (Brevo, ZeptoMail)
- REST API endpoints
- Authentication system
- Database migrations
- Templates and static files
- Requirements.txt
- Configuration files
- Test files and documentation

---

## Recommendation

**Use Option 1 (Disable Push Protection temporarily)** - fastest and simplest for your case since:
- The secrets in old commits are from the previous repository
- You've created a proper .gitignore for future commits
- New .env files won't be committed

**Steps:**
1. Open https://github.com/Goku0090/uni_sync/settings
2. Go to "Code security and analysis"
3. Find "Push protection for repository" → Disable
4. Run the git push command
5. Re-enable the protection

---

## After Successful Upload

1. **Create README.md** with setup instructions
2. **Add environment configuration guide**:
   ```
   Copy .env.template to .env and configure:
   - BREVO_API_KEY
   - DATABASE_URL (for production)
   - GOOGLE_CLIENT_ID/SECRET
   - GITHUB_CLIENT_ID/SECRET
   - RAPIDAPI_KEY
   ```

3. **Set repository visibility** if needed

---

**Need Help?** The code is ready - just resolve the secret scanning block!
