# Deployment Checklist: Comments Visibility Fix

## Pre-Deployment (Local Testing)

### Code Verification
- [x] File modified: `accounts/templates/includes/comment_section.html`
- [x] 4 fetch calls updated (lines 241, 281, 375, 427)
- [x] All paths changed from `/api/` to `/accounts/`
- [x] No syntax errors
- [x] No other files modified

### Local Testing Setup
```bash
# 1. Start development server
python manage.py runserver

# 2. Create test database
python manage.py migrate

# 3. Create test users
python manage.py createsuperuser  # User A
# Then create another user: User B (via web interface)

# 4. Create test project
# - Login as User A
# - Go to http://localhost:8000/accounts/post-project/
# - Create a test project
```

### Functional Testing Checklist

#### Test 1: Comments Load
- [ ] Visit project detail page as logged-in user
- [ ] Comments section loads without errors
- [ ] Browser console shows no errors (F12)
- [ ] Network tab shows 200 status for comment requests

#### Test 2: Post Comment
- [ ] As User A, type comment in text area
- [ ] Click "Post" button
- [ ] Comment appears immediately below input
- [ ] Comment visible to User A

#### Test 3: Other User Sees Comment
- [ ] Open second browser/incognito window
- [ ] Login as User B
- [ ] Visit same project
- [ ] User A's comment is visible
- [ ] Comment count is accurate

#### Test 4: Add Comment as User B
- [ ] As User B, post a comment
- [ ] Comment appears for User B
- [ ] Switch to User A's window and refresh
- [ ] User B's comment is visible to User A

#### Test 5: Edit Comment
- [ ] As User A, find own comment
- [ ] Click "Edit" button
- [ ] Modify text in prompt dialog
- [ ] Comment updates successfully
- [ ] User B can see updated text

#### Test 6: Delete Comment
- [ ] As User A, find own comment
- [ ] Click "Delete" button
- [ ] Confirm deletion
- [ ] Comment disappears
- [ ] User B sees comment removed

#### Test 7: Permission Checks
- [ ] User B can only see Edit/Delete on own comments
- [ ] User A (owner) can delete User B's comment
- [ ] User B cannot delete User A's comment

#### Test 8: Comment Display
- [ ] User profile photo displays correctly
- [ ] Username displays correctly
- [ ] Timestamp displays correctly
- [ ] Comment text displays correctly
- [ ] Formatting preserved (line breaks, etc.)

### Browser Compatibility Testing
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (if available)
- [ ] Mobile browser (if available)

### Console Validation
In browser DevTools (F12):
- [ ] No 404 errors
- [ ] No CORS errors
- [ ] No CSRFToken errors
- [ ] All fetch calls return 200/201
- [ ] No JavaScript exceptions

---

## Staging Deployment

### Pre-Deployment
- [ ] Code review completed
- [ ] All local tests pass
- [ ] Changes committed to git
- [ ] No uncommitted changes

### Deployment Steps
```bash
# 1. Switch to staging branch
git checkout staging

# 2. Pull latest changes
git pull origin staging

# 3. Merge fix from main/develop
git merge main
# or
git merge develop

# 4. Deploy to staging
# (depends on your deployment platform)
# Example for Render/Railway:
# - Push to staging branch
# - Auto-deploy triggers
# - Check deployment logs

# 5. Verify deployment
# - Check staging site logs
# - No deployment errors
```

### Staging Testing Checklist
- [ ] Staging server started successfully
- [ ] Static files loaded correctly
- [ ] Database migrations applied (if any)
- [ ] All tests pass
- [ ] Repeat all local tests on staging
- [ ] Check server logs for errors
- [ ] Monitor CPU/Memory usage
- [ ] Load test if applicable

### Staging Sign-off
- [ ] QA/PM approves
- [ ] No critical issues
- [ ] Ready for production

---

## Production Deployment

### Pre-Deployment Checklist
- [ ] Staging testing complete
- [ ] All tests pass
- [ ] Backup taken
- [ ] Rollback plan ready
- [ ] Team notified
- [ ] Maintenance window scheduled (if needed)
- [ ] Monitoring alerts enabled

### Deployment Execution

```bash
# 1. Final code review
git diff main staging
# Review changes - should be exactly 4 lines

# 2. Tag release (optional but recommended)
git tag -a v1.0.1 -m "Fix comments visibility"

# 3. Merge to main branch
git checkout main
git merge staging

# 4. Push to production
git push origin main

# 5. Production deployment triggers
# (auto-deploy if configured)
```

### Post-Deployment Validation
- [ ] Site loads without errors
- [ ] Static files load correctly
- [ ] Database connections working
- [ ] Comments section loads
- [ ] Existing comments visible
- [ ] Can post new comments
- [ ] Edit/delete functionality works
- [ ] No 404 errors
- [ ] No 500 errors
- [ ] Server logs clean
- [ ] Monitoring shows normal metrics

### Smoke Testing (Production)

#### Test 1: Basic Functionality
```bash
# Visit production site
1. Go to https://yourdomain.com
2. Login with test account
3. View project with existing comments
4. Verify comments load
5. Post new comment
6. Verify comment appears
```

#### Test 2: Monitor Errors
```bash
# Check error tracking
1. Open Sentry dashboard
2. No new errors related to comments
3. No increased error rate
4. Check server logs for warnings
```

#### Test 3: Performance
```bash
# Check performance metrics
1. Page load time normal
2. Comment load time < 500ms
3. Post comment time < 2s
4. CPU usage normal
5. Memory usage normal
```

---

## Rollback Plan (If Issues Arise)

### Emergency Rollback
```bash
# If critical issues found:

# 1. Revert the commit
git revert HEAD

# 2. Push revert
git push origin main

# 3. Monitor deployment
# Auto-deploy should trigger
# Previous version restored

# 4. Restore from backup (if needed)
# (depends on your system)
```

### Rollback Checklist
- [ ] Identify critical issue
- [ ] Execute rollback command
- [ ] Verify previous version deployed
- [ ] Test comments still work (if they worked before)
- [ ] Monitor error rates return to normal
- [ ] Notify team
- [ ] Post-mortem analysis

---

## Post-Deployment Monitoring

### First 24 Hours
- [ ] Error rates normal
- [ ] No increase in 404 errors
- [ ] No CSRF token errors
- [ ] Comment posts successful
- [ ] Comments visible to all users
- [ ] User feedback positive
- [ ] No support tickets related to comments

### First Week
- [ ] All metrics stable
- [ ] No unexpected issues
- [ ] Comment engagement normal
- [ ] Database performance normal
- [ ] Cache hit rates normal

### Documentation Updates
- [ ] Update README if needed
- [ ] Update changelog
- [ ] Update team documentation
- [ ] Notify users if applicable

---

## Communication Timeline

### Before Deployment
- [ ] Notify stakeholders: "Deploying comments fix"
- [ ] Estimated deployment time: 5-10 minutes
- [ ] Expected downtime: None
- [ ] Rollback capability: Yes

### During Deployment
- [ ] Monitor error logs
- [ ] Monitor performance metrics
- [ ] Be ready for rollback

### After Deployment
- [ ] Confirm all tests pass
- [ ] Send deployment notification
- [ ] Monitor for 24 hours
- [ ] Document any issues

---

## Sign-Off

### Developer
- [ ] Code reviewed
- [ ] Tests passed
- [ ] Ready for deployment

### QA/Testing
- [ ] All tests passed
- [ ] No critical issues
- [ ] Approved for production

### Product Manager
- [ ] Feature approved
- [ ] User impact understood
- [ ] Approved for release

### DevOps/Operations
- [ ] Infrastructure ready
- [ ] Monitoring configured
- [ ] Rollback plan ready
- [ ] Approved for deployment

---

## Success Criteria

Deployment is successful if:
- ✅ No 404 errors for comment endpoints
- ✅ Comments load within 500ms
- ✅ Users can post comments
- ✅ Comments visible to all users
- ✅ Edit/delete functionality works
- ✅ No increase in error rate
- ✅ Server performance normal
- ✅ User feedback positive

---

## Issue Escalation

### If Issues Arise
1. **Immediate**: Check error logs (Sentry)
2. **Assess**: Determine severity
3. **Decide**: Rollback or fix?
4. **Communicate**: Notify team
5. **Execute**: Rollback or hotfix
6. **Monitor**: Watch for side effects
7. **Document**: Post-mortem analysis

### Critical Issues (Rollback)
- 500 errors affecting > 5% of users
- 404 errors on comment endpoints
- Comments deleted unexpectedly
- Data corruption
- Security issues

### Minor Issues (Hotfix)
- UI glitches
- Slow performance < 2s
- Display issues
- Notification delays

---

## Deployment Completed Checklist

After deployment:
- [ ] All tests pass
- [ ] No errors in logs
- [ ] Comments visible to users
- [ ] Performance metrics normal
- [ ] Monitoring alerts clean
- [ ] User feedback collected
- [ ] Documentation updated
- [ ] Team notified
- [ ] Post-mortem scheduled (if issues)

---

## Maintenance After Deployment

### Daily
- [ ] Monitor error rates
- [ ] Check comment functionality
- [ ] Review user feedback

### Weekly
- [ ] Review performance metrics
- [ ] Check database size
- [ ] Verify backups

### Monthly
- [ ] Review logs for patterns
- [ ] Analyze user behavior
- [ ] Plan next improvements

---

## Contact Information

For deployment issues:
1. **Error Tracking**: Sentry dashboard
2. **Server Logs**: Server administration panel
3. **Database**: DBeaver/pgAdmin
4. **Team Chat**: (your messaging platform)
5. **On-Call**: (your on-call engineer)

---

## Summary

- **Change**: 4 API endpoint paths corrected
- **Risk Level**: Very Low
- **Downtime**: None
- **Rollback**: < 5 minutes
- **Effort**: 5 minutes deployment + 15 minutes testing
- **Impact**: Comments fully functional for all users

**Status**: ✅ Ready for Production Deployment
