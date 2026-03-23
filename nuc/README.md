# NUC

Development machine and frame viewer (192.168.1.12).

## Frames
Captured frames are NOT committed to the repo. Pull them from the Jetson:

```bash
bash rsync_frames.sh
```

Frames land in `nuc/frames/` which is gitignored.

## Viewer
See `viewer.py` — not yet implemented. Options:
- Samba share from Jetson (simplest, phone-accessible)
- Flask web UI
- inotify-triggered auto-rsync

## Samsung SSD
- Mounted at `/mnt/samsung`
- 916G, ext4, USB 3.2 Gen 2 via Sabrent enclosure
- UAS driver confirmed
- Sequential write: 875 MB/s, read: 1.1 GB/s
