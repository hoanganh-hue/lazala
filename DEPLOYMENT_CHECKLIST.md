# Deployment Checklist

## Pre-Build Checklist

- [ ] Code is committed and pushed to main branch
- [ ] All tests are passing (run `python run_tests.py`)
- [ ] Version number is updated in:
  - [ ] `setup.py`
  - [ ] `installer.iss`
  - [ ] `CHANGELOG.md`
- [ ] Documentation is up to date:
  - [ ] `README.md`
  - [ ] `WINDOWS_BUILD_GUIDE.md`
  - [ ] `docs/huong_dan_su_dung.md`
- [ ] API credentials are NOT hardcoded
- [ ] Debug flags are disabled
- [ ] Logging is set to appropriate level

## Build Process

- [ ] Running on Windows 10/11 64-bit
- [ ] Virtual environment is activated
- [ ] Dependencies are installed: `pip install -r requirements.txt`
- [ ] Clean previous builds: `python build.py --clean`
- [ ] Run tests: `python run_tests.py --type unit`
- [ ] Build executable: `python build.py`
- [ ] Verify executable exists: `dist/GoogleMapsScraper.exe`
- [ ] Verify installer exists: `installer/GoogleMapsScraper_Setup_v1.0.0.exe`

## Testing Executable

- [ ] Test on build machine:
  - [ ] Application starts without errors
  - [ ] GUI displays correctly
  - [ ] All menu items work
  - [ ] Settings dialog opens
  - [ ] About dialog shows correct version
- [ ] Test on clean Windows machine (without Python):
  - [ ] Application starts
  - [ ] No missing dependencies errors
  - [ ] Basic functionality works

## Testing Installer

- [ ] Test on clean Windows 10 machine:
  - [ ] Installer runs without admin errors
  - [ ] Installation completes successfully
  - [ ] Desktop icon is created
  - [ ] Start menu shortcuts are created
  - [ ] Application starts from shortcuts
  - [ ] Uninstaller works correctly
- [ ] Test on clean Windows 11 machine:
  - [ ] Same tests as Windows 10

## Functional Testing

- [ ] API Configuration:
  - [ ] Can enter API token
  - [ ] Can save configuration
  - [ ] Can test connection
  - [ ] Error handling works
- [ ] Basic Search:
  - [ ] Can enter search query
  - [ ] Can start scraping
  - [ ] Progress indicator works
  - [ ] Results display correctly
- [ ] Data Export:
  - [ ] Can export to Excel
  - [ ] Can export to CSV
  - [ ] Can export to JSON
  - [ ] Export files open correctly
- [ ] Advanced Features:
  - [ ] Filters work
  - [ ] Language selection works
  - [ ] Add-ons can be enabled/disabled

## GitHub Release

- [ ] Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release:
  - [ ] Go to repository → Releases → "Create a new release"
  - [ ] Select tag: `v1.0.0`
  - [ ] Title: "Google Maps Scraper v1.0.0"
  - [ ] Upload installer: `GoogleMapsScraper_Setup_v1.0.0.exe`
  - [ ] Add release notes (see template below)
  - [ ] Mark as pre-release (if beta)
  - [ ] Publish release

## Post-Release

- [ ] Update README.md with latest release link
- [ ] Test download from GitHub releases
- [ ] Test installer from GitHub releases
- [ ] Announce release:
  - [ ] Update project website (if any)
  - [ ] Post on social media
  - [ ] Send email to users (if applicable)
- [ ] Monitor for issues:
  - [ ] Check GitHub issues
  - [ ] Check user feedback
  - [ ] Prepare hotfix if needed

## Release Notes Template

```markdown
## Google Maps Scraper v1.0.0

### 🎉 Highlights
- [Brief description of major features/changes]

### ✨ New Features
- Feature 1: Description
- Feature 2: Description

### 🐛 Bug Fixes
- Fixed issue with X
- Fixed crash when Y

### 🔧 Improvements
- Improved performance for Z
- Enhanced UI for better UX

### 📚 Documentation
- Added comprehensive build guide
- Updated user manual

### 🔄 Changes
- Changed behavior of X to Y
- Updated dependency version

### ⚠️ Breaking Changes
- None

### 📦 Installation
1. Download `GoogleMapsScraper_Setup_v1.0.0.exe`
2. Run the installer
3. Follow the installation wizard
4. Launch from desktop icon

### 📋 Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space
- Internet connection
- Apify API token

### 🆘 Support
- Issues: https://github.com/hoanganh-hue/lazala/issues
- Documentation: https://github.com/hoanganh-hue/lazala/blob/main/README.md

### 🙏 Contributors
- @username1
- @username2

### 📈 Statistics
- Lines of code: [number]
- Test coverage: [percentage]%
- Tests passed: 32/32
```

## Rollback Plan

If critical issues are found after release:

- [ ] Create hotfix branch
- [ ] Fix the critical issue
- [ ] Test thoroughly
- [ ] Build new version (e.g., v1.0.1)
- [ ] Deploy as hotfix release
- [ ] Mark previous release as deprecated
- [ ] Notify users to upgrade

## Security Checklist

- [ ] No hardcoded credentials
- [ ] All user inputs are validated
- [ ] API calls use HTTPS
- [ ] Sensitive data is not logged
- [ ] File paths are sanitized
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities (if web components)
- [ ] Dependencies have no known vulnerabilities:
  ```bash
  pip install safety
  safety check
  ```

## Performance Checklist

- [ ] Application starts in < 5 seconds
- [ ] UI is responsive (no freezing)
- [ ] Memory usage is acceptable (< 500MB)
- [ ] No memory leaks during extended use
- [ ] File operations are efficient
- [ ] API calls are optimized
- [ ] Large datasets are handled properly

## Documentation Checklist

- [ ] README.md is complete
- [ ] WINDOWS_BUILD_GUIDE.md is accurate
- [ ] QUICK_START.md is user-friendly
- [ ] API documentation is up to date
- [ ] Inline code comments are clear
- [ ] Changelog is updated
- [ ] License file is present
- [ ] Contributing guidelines exist (if open source)

## Legal Checklist

- [ ] License is clearly stated
- [ ] Third-party licenses are acknowledged
- [ ] Copyright notices are correct
- [ ] Terms of service are clear
- [ ] Privacy policy exists (if collecting data)
- [ ] Compliance with Apify TOS
- [ ] Compliance with Google Maps TOS

---

**Note**: This checklist should be reviewed and updated for each release.
