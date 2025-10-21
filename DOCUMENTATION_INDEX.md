# 📚 Documentation Index

Welcome to the Google Maps Scraper documentation! This index will help you find the right documentation for your needs.

## 🎯 I want to...

### ...use the application
→ **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start guide
- Download and install
- Configure API
- Start scraping
- Export data

### ...build the application from source
→ **[WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)** - Complete build guide
- Environment setup
- Dependencies installation
- Build executable
- Create installer
- Troubleshooting

### ...understand the build architecture
→ **[BUILD_SOLUTION_SUMMARY.md](BUILD_SOLUTION_SUMMARY.md)** - Technical overview
- Project structure
- Technologies used
- Build process
- Deployment workflow

→ **[BUILD_PROCESS_DIAGRAM.md](BUILD_PROCESS_DIAGRAM.md)** - Visual guide
- Architecture diagrams
- Build flow
- File size breakdown
- CI/CD pipeline

### ...deploy a new release
→ **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Release checklist
- Pre-build checks
- Build process
- Testing procedures
- Release creation
- Post-release tasks

### ...learn how to use the app
→ **[docs/huong_dan_su_dung.md](docs/huong_dan_su_dung.md)** - User manual (Vietnamese)
- Detailed feature guide
- Screenshots
- Step-by-step tutorials

### ...understand the API
→ **[docs/api_reference.md](docs/api_reference.md)** - API documentation
- Code structure
- API methods
- Integration guide

### ...see project metrics
→ **[docs/PROJECT_METRICS.md](docs/PROJECT_METRICS.md)** - Statistics
- Code metrics
- Test coverage
- Performance data

### ...check project completion status
→ **[docs/BAO_CAO_HOAN_THANH_DU_AN.md](docs/BAO_CAO_HOAN_THANH_DU_AN.md)** - Completion report
- Feature completion (100%)
- Quality assessment
- Test results (32/32 passed)

### ...see version history
→ **[CHANGELOG.md](CHANGELOG.md)** - Version history
- Release notes
- New features
- Bug fixes
- Breaking changes

## 📖 Documentation by User Type

### For End Users 👥
1. **[QUICK_START.md](QUICK_START.md)** - Start here!
2. **[docs/huong_dan_su_dung.md](docs/huong_dan_su_dung.md)** - Detailed user guide
3. **[README.md](README.md)** - Project overview

### For Developers 💻
1. **[WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)** - Build instructions
2. **[BUILD_SOLUTION_SUMMARY.md](BUILD_SOLUTION_SUMMARY.md)** - Technical overview
3. **[BUILD_PROCESS_DIAGRAM.md](BUILD_PROCESS_DIAGRAM.md)** - Visual guide
4. **[docs/api_reference.md](docs/api_reference.md)** - API documentation
5. **[BUILD.md](BUILD.md)** - Original build guide

### For Release Managers 🚀
1. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Release checklist
2. **[release.bat](release.bat)** - Release automation script
3. **[CHANGELOG.md](CHANGELOG.md)** - Version history
4. **[.github/workflows/](. github/workflows/)** - CI/CD pipelines

### For Project Managers 📊
1. **[BUILD_SOLUTION_SUMMARY.md](BUILD_SOLUTION_SUMMARY.md)** - Project summary
2. **[docs/BAO_CAO_HOAN_THANH_DU_AN.md](docs/BAO_CAO_HOAN_THANH_DU_AN.md)** - Completion report
3. **[docs/PROJECT_METRICS.md](docs/PROJECT_METRICS.md)** - Metrics
4. **[TASK_COMPLETION_SUMMARY.md](TASK_COMPLETION_SUMMARY.md)** - Task summary

## 📁 File Reference

### Root Directory

| File | Type | Purpose |
|------|------|---------|
| **README.md** | Doc | Main project overview |
| **QUICK_START.md** | Doc | 5-minute getting started guide |
| **WINDOWS_BUILD_GUIDE.md** | Doc | Comprehensive build instructions |
| **BUILD_SOLUTION_SUMMARY.md** | Doc | Technical solution overview |
| **BUILD_PROCESS_DIAGRAM.md** | Doc | Visual build process guide |
| **DEPLOYMENT_CHECKLIST.md** | Doc | Release deployment checklist |
| **BUILD.md** | Doc | Original build documentation |
| **CHANGELOG.md** | Doc | Version history and release notes |
| **build.py** | Script | Python build automation script |
| **build.bat** | Script | Windows batch build script |
| **release.bat** | Script | Windows release automation script |
| **build.spec** | Config | PyInstaller configuration |
| **installer.iss** | Config | Inno Setup installer configuration |
| **requirements.txt** | Config | Python dependencies |
| **setup.py** | Config | Package configuration |

### docs/ Directory

| File | Purpose |
|------|---------|
| **huong_dan_su_dung.md** | User manual (Vietnamese) |
| **api_reference.md** | API documentation |
| **BAO_CAO_HOAN_THANH_DU_AN.md** | Project completion report |
| **PROJECT_METRICS.md** | Code metrics and statistics |
| **EXECUTIVE_SUMMARY.md** | Executive summary |
| **TOM_TAT_NHANH.md** | Quick summary (Vietnamese) |
| **INDEX.md** | Documentation index |

### .github/ Directory

| File | Purpose |
|------|---------|
| **workflows/ci.yml** | Continuous Integration pipeline |
| **workflows/build-windows.yml** | Windows release build pipeline |

## 🔍 Quick Reference

### Common Tasks

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run tests | `python run_tests.py` |
| Run application | `python src/main.py` |
| Build executable | `python build.py --skip-installer` |
| Build installer | `python build.py` |
| Complete build | `build.bat` |
| Create release | `release.bat` |

### File Locations

| What | Where |
|------|-------|
| Source code | `src/` |
| Tests | `tests/` |
| Resources | `resources/` |
| Built executable | `dist/GoogleMapsScraper.exe` |
| Installer | `installer/GoogleMapsScraper_Setup_v1.0.0.exe` |
| Logs (when running) | `logs/` |
| Configuration | `config.ini` |

## 🆘 Getting Help

### Issues & Bugs
- **GitHub Issues**: [Create an issue](https://github.com/hoanganh-hue/lazala/issues)
- Check existing issues first
- Include error messages and logs
- Describe steps to reproduce

### Questions & Discussions
- **GitHub Discussions**: [Start a discussion](https://github.com/hoanganh-hue/lazala/discussions)
- Ask questions
- Share ideas
- Help other users

### Documentation Issues
- Found a typo or error in docs?
- Documentation unclear or missing?
- Create an issue or submit a PR

## 🎓 Learning Path

### Beginner (Just want to use the app)
1. Read **[QUICK_START.md](QUICK_START.md)**
2. Download and install from releases
3. Follow user guide: **[docs/huong_dan_su_dung.md](docs/huong_dan_su_dung.md)**

### Intermediate (Want to build from source)
1. Read **[WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)**
2. Set up development environment
3. Build and test locally
4. Review **[BUILD_PROCESS_DIAGRAM.md](BUILD_PROCESS_DIAGRAM.md)**

### Advanced (Want to contribute or modify)
1. Review **[BUILD_SOLUTION_SUMMARY.md](BUILD_SOLUTION_SUMMARY.md)**
2. Study **[docs/api_reference.md](docs/api_reference.md)**
3. Read source code in `src/`
4. Check **[docs/PROJECT_METRICS.md](docs/PROJECT_METRICS.md)**
5. Follow **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**

## 📊 Documentation Statistics

- **Total Documents**: 15+ files
- **Total Words**: ~25,000+
- **Languages**: English, Vietnamese
- **Formats**: Markdown, Text, Scripts
- **Last Updated**: 2024

## 🔄 Documentation Updates

This documentation is actively maintained. If you notice:
- Outdated information
- Missing documentation
- Broken links
- Unclear instructions

Please open an issue or submit a pull request!

---

**Need help?** Start with **[QUICK_START.md](QUICK_START.md)** or **[README.md](README.md)**
