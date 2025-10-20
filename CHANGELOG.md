# Changelog

All notable changes to the Google Maps Scraper Desktop App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### To Do
- Fix failing tests (6/36 tests)
- Fix regex bug in validator.py
- Fix auth manager validation
- Improve test coverage to 80%+
- Add integration tests
- Add UI screenshots to documentation
- Implement save/load search configurations
- Add auto-update mechanism
- Setup CI/CD with GitHub Actions

## [1.0.0] - 2025-10-20

### Added
- Initial release of Google Maps Scraper Desktop App
- **Core Features:**
  - Google Maps search with keywords and location
  - Advanced filtering (categories, ratings, website)
  - Reviews scraping with sorting options
  - Images and Q&A scraping
  - Contact information extraction
  - Business leads enrichment
  - Multi-language support (70+ languages)
  - Export to Excel, CSV, JSON formats
  - Multiple export views (all data, contacts, locations, reviews, leads)

- **User Interface:**
  - Main window with 5 comprehensive tabs
  - Search tab for basic queries
  - Filters tab for advanced filtering
  - Details tab for scraping configuration
  - Add-ons tab for premium features
  - Results tab with export functionality
  - Settings dialog for API configuration
  - Progress tracking with status updates
  - Statistics display

- **API Integration:**
  - Apify API client with async support
  - Authentication management
  - Token validation and storage
  - Connection testing
  - Run status polling
  - Dataset retrieval

- **Data Processing:**
  - Input validation
  - Data cleaning and deduplication
  - Statistics calculation
  - Filtering and sorting
  - Export management

- **Documentation:**
  - Comprehensive README with installation guide
  - Detailed BUILD.md with build instructions
  - User guide (huong_dan_su_dung.md) with 8 sections
  - API Reference (api_reference.md) with technical details
  - Project completion report (BAO_CAO_HOAN_THANH_DU_AN.md)
  - Quick summary (TOM_TAT_NHANH.md)

- **Build & Deployment:**
  - Automated build script (build.py)
  - PyInstaller configuration (build.spec)
  - Inno Setup installer script (installer.iss)
  - Windows executable creation
  - Installer generation

- **Resources:**
  - 4,000+ Google Maps categories database
  - Professional QSS styling (724 LOC)
  - Application icon

- **Testing:**
  - 36 unit tests for API and core modules
  - Pytest configuration
  - Test fixtures and mocking
  - Code coverage tracking

### Known Issues
- 6 unit tests currently failing:
  - `test_set_invalid_token` - Auth manager validation
  - `test_get_headers_no_token` - API error handling
  - `test_validate_api_token` - Token validation logic
  - `test_validate_location` - Regex syntax error
  - 4 async tests skipped (requires pytest-asyncio)
- Test coverage at 68% (target: 80%+)
- No integration or UI tests yet

### Technical Details
- Python 3.10+
- PyQt5 5.15.10 for GUI
- Async HTTP with aiohttp 3.9.1
- Data processing with pandas 2.1.4
- Excel export with openpyxl 3.1.2
- Total: ~5,600 lines of production code
- Total: ~800 lines of test code

### Dependencies
```
PyQt5==5.15.10
requests==2.31.0
aiohttp==3.9.1
pandas==2.1.4
openpyxl==3.1.2
python-dateutil==2.8.2
pyinstaller==6.3.0
pytest==7.4.3
```

---

## Version History

- **v1.0.0** (2025-10-20) - Initial release with core features
- **v0.1.0** (2025-10-15) - Development started

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
