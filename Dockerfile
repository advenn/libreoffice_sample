# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for LibreOffice
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gdebi-core \
    tar \
    xz-utils \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
    libglx0 \
    libdbus-glib-1-2 \
    fonts-dejavu \
    python3 \
    python3-pip \
    libsm6 \
    libxinerama1 \
    libxrandr2 \
    libxcursor1 \
    libpng16-16 \
    libfreetype6 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip
# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt


# --- LIBREOFFICE INSTALLATION IN DOCKERFILE (PRIMARY BUILD-TIME ATTEMPT) ---
# Create temp directory for LibreOffice downloads
RUN mkdir -p /tmp/libreoffice
WORKDIR /tmp/libreoffice

# Copy and run the LibreOffice installation script that detects latest version
COPY scripts/install_libre.sh /tmp/install_libre.sh
RUN chmod +x /tmp/install_libre.sh && /tmp/install_libre.sh && rm /tmp/install_libre.sh

# Create soffice symlink for easier access in PATH (important for the runtime check)

# Verify installation using the generic symlink
RUN /usr/local/bin/libreoffice-generic --headless --version || echo "LibreOffice verification failed in build, will re-attempt at runtime if needed."

# Go back to /app for subsequent steps
WORKDIR /app

# Copy the LibreOffice installation script (for runtime fallback)
# Assumes 'scripts' directory is at the same level as Dockerfile
COPY scripts/install_libre.sh /usr/local/bin/install_libre.sh
RUN chmod +x /usr/local/bin/install_libre.sh

# Copy the application startup wrapper script
COPY scripts/start_app.sh /usr/local/bin/start_app.sh
RUN chmod +x /usr/local/bin/start_app.sh

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/pdf

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["python3", "-m", "uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]