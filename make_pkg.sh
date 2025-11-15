#!/bin/bash

set -e

APP_NAME="GhostLogic-Free"
APP_DIR="${APP_NAME}.app"
PKG_NAME="${APP_NAME}.pkg"
VERSION="1.0.0"

echo "Building ${APP_NAME} macOS installer..."

# Clean previous builds
rm -rf "${APP_DIR}"
rm -f "${PKG_NAME}"

# Create app bundle structure
mkdir -p "${APP_DIR}/Contents/MacOS"
mkdir -p "${APP_DIR}/Contents/Resources"
mkdir -p "${APP_DIR}/Contents/MacOS/watch"

# Copy binaries
cp dist/ghostlogic_free "${APP_DIR}/Contents/MacOS/"
cp dist/dashboard "${APP_DIR}/Contents/MacOS/"
cp dist/watchdog "${APP_DIR}/Contents/MacOS/"
chmod +x "${APP_DIR}/Contents/MacOS/ghostlogic_free"
chmod +x "${APP_DIR}/Contents/MacOS/dashboard"
chmod +x "${APP_DIR}/Contents/MacOS/watchdog"

# Copy icon
if [ -f icon.icns ]; then
    cp icon.icns "${APP_DIR}/Contents/Resources/"
fi

# Create test file
echo "GhostLogic Free Edition - Test File" > "${APP_DIR}/Contents/MacOS/watch/testfile.txt"

# Create Info.plist
cat > "${APP_DIR}/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>watchdog</string>
    <key>CFBundleIdentifier</key>
    <string>com.ghostlogic.free</string>
    <key>CFBundleName</key>
    <string>GhostLogic Free</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
EOF

# Create temporary root directory for packaging
PACKAGE_ROOT="$(mktemp -d)"
mkdir -p "${PACKAGE_ROOT}/Applications"
cp -R "${APP_DIR}" "${PACKAGE_ROOT}/Applications/"

# Build package
pkgbuild --root "${PACKAGE_ROOT}" \
         --identifier com.ghostlogic.free \
         --version "${VERSION}" \
         --install-location "/" \
         "${PKG_NAME}"

# Clean up temporary directory
rm -rf "${PACKAGE_ROOT}"

echo "Package created: ${PKG_NAME}"
echo "Install with: sudo installer -pkg ${PKG_NAME} -target /"
