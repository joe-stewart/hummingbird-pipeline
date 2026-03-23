# Jetson Install Notes

## Python environment
- virtualenv at `/opt/cv-env/`
- Activate with alias: `cv`
- Service uses `/opt/cv-env/bin/python3` directly

## Wheels
Do not commit `.whl` files to the repo. Jetson-specific wheels go stale
quickly across JetPack versions. Document source and version here instead.

| Package | Version | Source |
|---------|---------|--------|
| TBD     | TBD     | TBD    |

## Deploy
```bash
cd ~/Development/hummer-capture
bash deploy.sh
```
