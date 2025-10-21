from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="google-maps-scraper-app",
    version="1.0.0",
    author="Google Maps Scraper Team",
    author_email="support@example.com",
    description="Desktop application for Google Maps data scraping via Apify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/google-maps-scraper-app",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "google-maps-scraper=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["resources/*", "resources/**/*"],
    },
)
