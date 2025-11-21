#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Function to get latest LibreOffice version
get_latest_version() {
    echo "Fetching latest LibreOffice version..." >&2
    # Try to get the latest version from the download page
    LATEST_VERSION=$(curl -s https://download.documentfoundation.org/libreoffice/stable/ | \
        grep -oP 'href="\d+\.\d+\.\d+/"' | \
        grep -oP '\d+\.\d+\.\d+' | \
        sort -V | \
        tail -n 1)

    if [ -z "$LATEST_VERSION" ]; then
        echo "Failed to fetch latest version, using fallback version 25.2.5" >&2
        echo "25.2.5"
    else
        echo "Latest version found: $LATEST_VERSION" >&2
        echo "$LATEST_VERSION"
    fi
}

# Get the latest version dynamically
LIBREOFFICE_VERSION=$(get_latest_version)

echo "Starting LibreOffice installation at runtime..."

# Create temp directory for LibreOffice downloads
mkdir -p /tmp/libreoffice
cd /tmp/libreoffice

# Download the LibreOffice .deb package
# Using double quotes for URL to ensure variable expansion works
wget "https://download.documentfoundation.org/libreoffice/stable/${LIBREOFFICE_VERSION}/deb/x86_64/LibreOffice_${LIBREOFFICE_VERSION}_Linux_x86-64_deb.tar.gz"

# Extract the package
tar -xzf "LibreOffice_${LIBREOFFICE_VERSION}_Linux_x86-64_deb.tar.gz"

# Change into the DEBS directory and install them
# Using double quotes for wildcard expansion to be safe
cd "LibreOffice_${LIBREOFFICE_VERSION}"*_Linux_x86-64_deb/DEBS

# Install DEB packages
dpkg -i *.deb

# Fix missing dependencies after dpkg -i
# This is crucial for manual .deb installs to ensure all necessary runtime libraries are present
apt-get update
apt-get install -f -y

# Optional: Create symlink for 'soffice' for easier access, as discussed before.
# This makes it easier to call LibreOffice from your Python code, e.g., using 'soffice' command.
#ln -s /opt/libreoffice/program/soffice /usr/local/bin/soffice

# Clean up temporary LibreOffice files
rm -rf /tmp/libreoffice

echo "LibreOffice installation complete."

# Create a generic symlink for easier access
# Find the installed LibreOffice binary and create a generic symlink
LIBRE_CMD=$(find /opt/libreoffice*/program -name "soffice" 2>/dev/null | head -n 1)
if [ -n "$LIBRE_CMD" ]; then
    ln -sf "$LIBRE_CMD" /usr/local/bin/libreoffice-generic
    echo "Created generic LibreOffice symlink: /usr/local/bin/libreoffice-generic"
else
    echo "Could not find LibreOffice installation to create symlink"
fi

# Verify installation (optional, for debugging this script)
/usr/local/bin/libreoffice-generic --headless --version || echo "LibreOffice generic command not found, check installation."