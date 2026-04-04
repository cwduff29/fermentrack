#!/usr/bin/env bash
# Fermentrack installer for https://github.com/cwduff29/fermentrack
set -e

REPO_URL="https://github.com/cwduff29/fermentrack.git"
INSTALL_DIR="/home/fermentrack/fermentrack"

red=$(tput setaf 1 2>/dev/null || true)
green=$(tput setaf 2 2>/dev/null || true)
reset=$(tput sgr0 2>/dev/null || true)

info()  { printf "${green}[INFO]${reset} %s\n" "$*"; }
error() { printf "${red}[ERROR]${reset} %s\n" "$*" >&2; exit 1; }

# Must run as root
if [ "$EUID" -ne 0 ]; then
    error "Please run as root: curl -L <url> | sudo bash"
fi

# Check for Pi OS / Debian-based system
if ! command -v apt-get &>/dev/null; then
    error "This installer requires a Debian-based OS (Raspberry Pi OS, Ubuntu, etc.)"
fi

# Install Docker if not present
if ! command -v docker &>/dev/null; then
    info "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
else
    info "Docker already installed: $(docker --version)"
fi

# Install docker compose plugin if not present
if ! docker compose version &>/dev/null; then
    info "Installing docker-compose-plugin..."
    apt-get install -y docker-compose-plugin
else
    info "Docker Compose already installed: $(docker compose version)"
fi

# Install git if not present
if ! command -v git &>/dev/null; then
    info "Installing git..."
    apt-get install -y git
fi

# Create fermentrack user if not present
if ! id fermentrack &>/dev/null; then
    info "Creating fermentrack user..."
    useradd -m -G docker fermentrack
else
    info "fermentrack user already exists"
    # Ensure user is in docker group
    usermod -aG docker fermentrack
fi

# Clone the repo
if [ -d "$INSTALL_DIR" ]; then
    info "Repo already exists at $INSTALL_DIR — pulling latest..."
    sudo -u fermentrack git -C "$INSTALL_DIR" pull
else
    info "Cloning Fermentrack from $REPO_URL..."
    sudo -u fermentrack git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Set up environment files
info "Setting up environment files..."
mkdir -p .envs/.production

if [ ! -f .envs/.production/.django ]; then
    cp .envs/.prod-sample/.django .envs/.production/.django

    # Generate a random secret key
    SECRET_KEY=$(tr -dc 'A-Za-z0-9!@#%^&*(-_=+)' </dev/urandom | head -c 50)
    sed -i "s|{secret_key}|${SECRET_KEY}|g" .envs/.production/.django

    # Set a default admin URL
    ADMIN_URL="admin-$(tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
    sed -i "s|{admin_url}|${ADMIN_URL}|g" .envs/.production/.django

    info "Django admin URL will be: /${ADMIN_URL}/"
fi

if [ ! -f .envs/.production/.postgres ]; then
    cp .envs/.prod-sample/.postgres .envs/.production/.postgres

    # Generate random postgres credentials
    PG_USER="fermentrack"
    PG_PASS=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24)
    sed -i "s|{postgres_user}|${PG_USER}|g" .envs/.production/.postgres
    sed -i "s|{postgres_password}|${PG_PASS}|g" .envs/.production/.postgres
fi

# Fix ownership
chown -R fermentrack:fermentrack "$INSTALL_DIR"

# Build and start (excluding tiltbridge-junior)
info "Building and starting Fermentrack (this may take 20-45 minutes on a Pi)..."
sudo -u fermentrack docker compose up -d --build django postgres redis nginx

info ""
info "Installation complete!"
info "Fermentrack is running at http://$(hostname -I | awk '{print $1}')"
info "Django admin URL: $(grep DJANGO_ADMIN_URL .envs/.production/.django | cut -d= -f2)"
