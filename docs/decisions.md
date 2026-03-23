# Decisions

## DHCP / Kea
- reservations-out-of-pool: true required on all subnets
- reCamera fix required BOTH: reservations-out-of-pool AND removing udhcpc from auto.sh
- Neither change alone was sufficient

## Buildroot
Explored but not in active use. Modding running system in place.
Not a blocker.

## Model Weights
Do not commit weights to repo. Store name, version, source URL, and
checksum in docs/models.md. Revisit when training custom models.

## DVC
Too early. Revisit when captured data starts accumulating.

## WOL
Both Jetson and RPi2 go fully dark on shutdown — NIC loses standby power.
Smart plug is the correct solution. WOL investigation closed.

## SSH
IdentitiesOnly yes in ~/.ssh/config for 192.168.2.* — prevents MaxAuthTries.

## Jetson Wheels
Do not commit .whl files. Document source and version in jetson/install_notes.md.
Wheels go stale across JetPack versions.

## hummingbird systemd user
Dedicated system user (no login, no home) for principle of least privilege.
joe added to hummingbird group for frame access.
/opt/hummingbird/frames/ at 775.

## Dev vs Production paths
- Dev: ~/Development/hummer-capture/ (Jetson, joe)
- Production: /opt/hummingbird/ (Jetson, hummingbird user)
- deploy.sh promotes dev → production

## Camera placement
OV5647 fixed focus ~1m to infinity. Optimal feeder distance: 1-2 meters.
Use flexible wire mount during data collection for varied angles/positions.
Lock down position for production after model training.

## Arduino warn frame
Bird icon impractical at 8x12 pixels. Hexagon with 45° slash chosen as
warn frame — clear and readable at that resolution.

## Repo structure
Single repo, folders per device. NUC gets its own dir for viewer and
rsync tooling. Frames gitignored everywhere — runtime output not source.
