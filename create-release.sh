#!/bin/bash

# Script to create a GitHub release for Google Maps Scraper
# This will trigger GitHub Actions to build and upload the installer

set -e

VERSION="1.0.0"
TAG="v${VERSION}"
RELEASE_NAME="Google Maps Scraper v${VERSION}"
RELEASE_BODY="Release version ${VERSION} - See RELEASE_GUIDE.md for details"

echo "================================================"
echo "  Google Maps Scraper - Release Creator"
echo "================================================"
echo ""
echo "Version: ${VERSION}"
echo "Tag: ${TAG}"
echo ""

# Check if tag exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "❌ Error: Tag ${TAG} already exists!"
    echo ""
    echo "To recreate the tag, first delete it:"
    echo "  git tag -d ${TAG}"
    echo "  git push origin :refs/tags/${TAG}"
    echo ""
    exit 1
fi

# Check if we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: ${CURRENT_BRANCH}"
echo ""

# Confirm action
read -p "Do you want to create tag ${TAG} and trigger the release? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Creating tag ${TAG}..."
git tag -a "$TAG" -m "${RELEASE_NAME}"

echo "Pushing tag to GitHub..."
git push origin "$TAG"

echo ""
echo "✅ Success!"
echo ""
echo "Next steps:"
echo "1. Check GitHub Actions build: https://github.com/hoanganh-hue/lazala/actions"
echo "2. Wait 5-10 minutes for build to complete"
echo "3. Check release: https://github.com/hoanganh-hue/lazala/releases/tag/${TAG}"
echo ""
echo "The installer will be automatically uploaded to:"
echo "https://github.com/hoanganh-hue/lazala/releases/download/${TAG}/GoogleMapsScraper_Setup_v${VERSION}.exe"
echo ""
