#!/bin/bash
# Push AI Privacy License Detector SDK to GitHub
# Repo: https://github.com/nabanitade/AIPrivacyLicenseDetect

set -e
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo ""

# If no .git, initialize
if [ ! -d .git ]; then
  echo "🔧 Initializing git repository..."
  git init
else
  echo "✅ Git repository already exists."
fi

# Add all files (respects .gitignore)
echo "📦 Adding files..."
git add .

# Show status
echo ""
echo "📋 Files to be committed:"
git status --short
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Initial commit: AI Privacy License Detector SDK"

# Ensure main branch
git branch -M main

# Add remote (remove first if it exists, to avoid error on re-run)
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/nabanitade/AIPrivacyLicenseDetect.git

echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Repo: https://github.com/nabanitade/AIPrivacyLicenseDetect"
