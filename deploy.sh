#!/bin/bash
# AzCSPM Backend Deployment Script for DigitalOcean
# This script sets up Docker, clones the repo, and starts all backend services.

set -euo pipefail

echo "==================================="
echo " AzCSPM Backend Deployment Script"
echo "==================================="
echo ""

# 1. Update system packages
echo "[1/6] Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Install Docker using the official get.docker.com script
echo "[2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    rm -f get-docker.sh
    echo "Docker installed successfully."
else
    echo "Docker is already installed."
fi

# Install Docker Compose plugin (if not present)
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    sudo apt-get install -y docker-compose-plugin
fi

# 3. Install git
echo "[3/6] Installing git..."
sudo apt-get install -y git

# 4. Clone the repository
echo "[4/6] Cloning repository..."
REPO_URL="https://github.com/MbarizPaayev2/AZCONHackhaton.git"
REPO_DIR="AZCONHackhaton"

if [ -d "$REPO_DIR" ]; then
    echo "Directory $REPO_DIR already exists. Pulling latest changes..."
    cd "$REPO_DIR"
    git pull origin main
    cd ..
else
    git clone "$REPO_URL"
fi

# 5. Start backend services with Docker Compose
echo "[5/6] Starting backend services..."
cd "$REPO_DIR"

# Create required data directories
mkdir -p ./_data/api ./_data/postgres ./_data/valkey ./_data/neo4j

# Pull latest images and start services
sudo docker compose -f docker-compose.backend.yml pull
sudo docker compose -f docker-compose.backend.yml up -d

echo ""
echo "[6/6] Checking service status..."
echo ""
sleep 5
sudo docker compose -f docker-compose.backend.yml ps

echo ""
echo "==================================="
echo " Deployment Complete!"
echo "==================================="
echo ""
echo "API (Django):    http://$(curl -s ifconfig.me):8080/api/v1"
echo "API Docs:        http://$(curl -s ifconfig.me):8080/api/v1/docs"
echo "MCP Server:      http://$(curl -s ifconfig.me):8000"
echo ""
echo "Useful commands:"
echo "  View API logs:      sudo docker compose -f docker-compose.backend.yml logs -f api"
echo "  View all logs:      sudo docker compose -f docker-compose.backend.yml logs -f"
echo "  Stop services:      sudo docker compose -f docker-compose.backend.yml down"
echo "  Restart services:   sudo docker compose -f docker-compose.backend.yml restart"
echo ""
echo "Next steps:"
echo "  1. Update .env: replace YOUR_DO_IP with your actual DigitalOcean Droplet IP"
echo "  2. Restart API container after .env update: sudo docker compose -f docker-compose.backend.yml restart api"
echo "  3. Update Vercel frontend env var NEXT_PUBLIC_API_BASE_URL to your DO IP"
echo ""
