#!/bin/bash
# AzCSPM Backend Deployment Script for DigitalOcean
# This script sets up Docker, clones the repo, and starts all backend services.

set -euo pipefail

echo "==================================="
echo " AzCSPM Backend Deployment Script"
echo "==================================="
echo ""

# 1. Update system packages
echo "[1/7] Updating system packages..."
sudo apt-get update -y

# 2. Install Docker using the official get.docker.com script
echo "[2/7] Installing Docker..."
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

# 3. Install git and openssl
echo "[3/7] Installing git and openssl..."
sudo apt-get install -y git openssl

# 4. Clone the repository
echo "[4/7] Cloning repository..."
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

# 5. Configure environment
echo "[5/7] Configuring environment..."
cd "$REPO_DIR"

# Get the server's public IP
SERVER_IP=$(curl -s ifconfig.me)
echo "Detected server IP: $SERVER_IP"

# Generate secure random passwords
POSTGRES_ADMIN_PASSWORD=$(openssl rand -base64 24)
POSTGRES_PASSWORD=$(openssl rand -base64 24)
NEO4J_PASSWORD=$(openssl rand -base64 24)
AUTH_SECRET=$(openssl rand -base64 32)
ENCRYPTION_KEY=$(openssl rand -base64 32)

# Create .env file with correct configuration
cat > .env << EOF
#### Prowler API Configuration ####
PROWLER_API_VERSION=stable
PROWLER_UI_VERSION=stable
PROWLER_MCP_VERSION=stable

#### API URLs ####
API_BASE_URL=http://$SERVER_IP:8080/api/v1
NEXT_PUBLIC_API_BASE_URL=http://$SERVER_IP:8080/api/v1
NEXT_PUBLIC_API_DOCS_URL=http://$SERVER_IP:8080/api/v1/docs
AUTH_URL=https://ui-six-pearl.vercel.app

#### PostgreSQL settings ####
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432
POSTGRES_ADMIN_USER=prowler_admin
POSTGRES_ADMIN_PASSWORD=$POSTGRES_ADMIN_PASSWORD
POSTGRES_USER=prowler
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=prowler_db

#### Neo4j auth ####
NEO4J_HOST=neo4j
NEO4J_PORT=7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=$NEO4J_PASSWORD
NEO4J_DBMS_MAX__DATABASES=1000
NEO4J_SERVER_MEMORY_PAGECACHE_SIZE=1G
NEO4J_SERVER_MEMORY_HEAP_INITIAL__SIZE=1G
NEO4J_SERVER_MEMORY_HEAP_MAX__SIZE=1G
NEO4J_PLUGINS=["apoc"]
NEO4J_DBMS_SECURITY_PROCEDURES_ALLOWLIST=apoc.*
NEO4J_DBMS_SECURITY_PROCEDURES_UNRESTRICTED=
NEO4J_APOC_EXPORT_FILE_ENABLED=false
NEO4J_APOC_IMPORT_FILE_ENABLED=false
NEO4J_APOC_IMPORT_FILE_USE_NEO4J_CONFIG=true
NEO4J_APOC_TRIGGER_ENABLED=false
NEO4J_DBMS_CONNECTOR_BOLT_LISTEN_ADDRESS=0.0.0.0:7687

#### Valkey settings ####
VALKEY_SCHEME=redis
VALKEY_USERNAME=
VALKEY_PASSWORD=
VALKEY_HOST=valkey
VALKEY_PORT=6380
VALKEY_DB=0

#### Django settings ####
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,prowler-api,$SERVER_IP
DJANGO_CORS_ALLOWED_ORIGINS=https://ui-six-pearl.vercel.app,http://localhost:3000
DJANGO_BIND_ADDRESS=0.0.0.0
DJANGO_PORT=8080
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=config.django.production
DJANGO_LOGGING_FORMATTER=human_readable
DJANGO_LOGGING_LEVEL=INFO
DJANGO_WORKERS=4
DJANGO_ACCESS_TOKEN_LIFETIME=30
DJANGO_REFRESH_TOKEN_LIFETIME=1440
DJANGO_CACHE_MAX_AGE=3600
DJANGO_STALE_WHILE_REVALIDATE=60
DJANGO_MANAGE_DB_PARTITIONS=True
DJANGO_SECRETS_ENCRYPTION_KEY=$ENCRYPTION_KEY
DJANGO_BROKER_VISIBILITY_TIMEOUT=86400
DJANGO_THROTTLE_TOKEN_OBTAIN=50/minute
DJANGO_TMP_OUTPUT_DIRECTORY=/tmp/prowler_api_output
DJANGO_FINDINGS_BATCH_SIZE=1000

#### Auth ####
AUTH_TRUST_HOST=true
AUTH_SECRET=$AUTH_SECRET

#### MCP Server ####
MCP_SERVER_PORT=8001
PROWLER_MCP_SERVER_URL=http://mcp-server:8000/mcp

#### RSS Feed ####
RSS_FEED_SOURCES='[{"id":"prowler-releases","name":"Prowler Releases","type":"github_releases","url":"https://github.com/prowler-cloud/prowler/releases.atom","enabled":true}]'
EOF

echo "Environment file created with secure credentials."

# 6. Start backend services with Docker Compose
echo "[6/7] Starting backend services..."

# Clean up any previous failed neo4j data to avoid permission/lock issues
echo "Preparing data directories..."
sudo rm -rf ./_data/neo4j
mkdir -p ./_data/api ./_data/postgres ./_data/valkey ./_data/neo4j
chmod -R 777 ./_data/neo4j

# Pull latest images and start services
echo "Pulling images..."
sudo docker compose -f docker-compose.backend.yml pull

echo "Starting services..."
sudo docker compose -f docker-compose.backend.yml down --remove-orphans 2>/dev/null || true
sudo docker compose -f docker-compose.backend.yml up -d --remove-orphans

echo ""
echo "[7/7] Checking service status..."
echo ""
sleep 10
sudo docker compose -f docker-compose.backend.yml ps

echo ""
echo "==================================="
echo " Deployment Complete!"
echo "==================================="
echo ""
echo "Server IP:       $SERVER_IP"
echo "API (Django):    http://$SERVER_IP:8080/api/v1"
echo "API Docs:        http://$SERVER_IP:8080/api/v1/docs"
echo "MCP Server:      http://$SERVER_IP:8001"
echo ""
echo "Useful commands:"
echo "  View API logs:      sudo docker compose -f docker-compose.backend.yml logs -f api"
echo "  View worker logs:   sudo docker compose -f docker-compose.backend.yml logs -f worker"
echo "  View all logs:      sudo docker compose -f docker-compose.backend.yml logs -f"
echo "  Stop services:      sudo docker compose -f docker-compose.backend.yml down"
echo "  Restart services:   sudo docker compose -f docker-compose.backend.yml restart"
echo ""
echo "Next steps:"
echo "  1. Wait 2-3 minutes for all services to fully initialize"
echo "  2. Check service health: sudo docker compose -f docker-compose.backend.yml ps"
echo "  3. Update Vercel frontend env var NEXT_PUBLIC_API_BASE_URL to:"
echo "     http://$SERVER_IP:8080/api/v1"
