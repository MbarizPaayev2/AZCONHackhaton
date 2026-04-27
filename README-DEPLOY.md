# AzCSPM Backend Deployment Guide

Deploy the **AzCSPM Backend** on a DigitalOcean Droplet. The frontend is already on Vercel at [https://azconhakaton.vercel.app](https://azconhakaton.vercel.app).

---

## Step 1: Create a DigitalOcean Droplet

1. Log in to [DigitalOcean](https://cloud.digitalocean.com)
2. Click **Create** → **Droplets**
3. Configure:
   - **Region:** Frankfurt (FRA1)
   - **Image:** Ubuntu 24.04 (LTS) x64
   - **Size:** 8 GB RAM / 4 vCPUs
   - **Auth:** SSH keys
   - **Hostname:** `azcspm-backend`
4. Click **Create Droplet**
5. Note the **IPv4 address** — this is `YOUR_DO_IP`

---

## Step 2: SSH into the Server

```bash
ssh root@YOUR_DO_IP
```

---

## Step 3: Run the Deployment Script

```bash
curl -fsSL https://raw.githubusercontent.com/MbarizPaayev2/AZCONHackhaton/main/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

The script installs Docker, clones the repo, and starts all backend services.

---

## Step 4: Update .env with Your Droplet IP

```bash
cd azconhackhatonvercel
nano .env
```

Replace `YOUR_DO_IP` with your actual droplet IPv4 address in these lines:

```env
API_BASE_URL=http://YOUR_DO_IP:8080/api/v1
NEXT_PUBLIC_API_BASE_URL=${API_BASE_URL}
NEXT_PUBLIC_API_DOCS_URL=http://YOUR_DO_IP:8080/api/v1/docs
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,prowler-api,YOUR_DO_IP
```

Save (`Ctrl+O`, `Enter`, `Ctrl+X`), then restart:

```bash
sudo docker compose -f docker-compose.backend.yml restart api
```

---

## Step 5: Open Firewall Ports

In DigitalOcean Cloud Console:
- **Networking** → **Firewalls** → **Create Firewall**
- Name: `azcspm-backend-fw`
- Add inbound rules:
  - SSH TCP 22 (your IP only)
  - Custom TCP 8080 (all)
  - Custom TCP 8000 (all)
- Apply to your droplet

On the server:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable
```

---

## Step 6: Check Service Health

```bash
sudo docker compose -f docker-compose.backend.yml ps
```

All services should show `Up (healthy)` or `Up`.

---

## Step 7: View Logs

**API logs:**
```bash
sudo docker compose -f docker-compose.backend.yml logs -f api
```

**All services:**
```bash
sudo docker compose -f docker-compose.backend.yml logs -f
```

---

## Step 8: Connect Vercel Frontend to Backend

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your AzCSPM frontend project
3. **Settings** → **Environment Variables**
4. Update:
   - `NEXT_PUBLIC_API_BASE_URL` → `http://YOUR_DO_IP:8080/api/v1`
5. **Save**
6. **Deployments** → **Redeploy**

---

## Maintenance Commands

| Action | Command |
|--------|---------|
| Stop all | `sudo docker compose -f docker-compose.backend.yml down` |
| Start all | `sudo docker compose -f docker-compose.backend.yml up -d` |
| Restart API | `sudo docker compose -f docker-compose.backend.yml restart api` |
| Update images | `sudo docker compose -f docker-compose.backend.yml pull && sudo docker compose -f docker-compose.backend.yml up -d` |
| Resource usage | `sudo docker stats` |
| Backup DB | `sudo docker exec <postgres-container> pg_dump -U prowler_admin prowler_db > backup.sql` |

---

## Troubleshooting

**API restarting:** Check `sudo docker compose -f docker-compose.backend.yml logs api`. Ensure `.env` has correct `YOUR_DO_IP`.

**DB errors:** Ensure postgres is healthy before api starts. Check `sudo docker compose -f docker-compose.backend.yml logs postgres`.

**Port already in use:** Ensure no other service uses 8080 or 8000 on the host.
