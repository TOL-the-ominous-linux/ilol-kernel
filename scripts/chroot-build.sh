#!/usr/bin/env bash
# iLOL kernel — clean-chroot build (POL.md item 3).
# Run by the maintainer (needs sudo). Never on the user's desktop.
#
#   sudo bash "$HOME/tol-kernel/scripts/chroot-build.sh"
#
# Output: ~/tol-kernel/linux-ilol-*.pkg.tar.zst (+ -headers)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROOT=/var/lib/archbuild/tolroot

[[ -x /usr/bin/makechrootpkg ]] || { echo "cần devtools: sudo pacman -S devtools — rồi chạy lại"; exit 1; }
[[ -x /usr/bin/timeout ]] || true

echo "== 1. chroot root =="
if [[ ! -d $CHROOT ]]; then
  sudo mkdir -p "$CHROOT"
  sudo mkarchroot "$CHROOT/root" base-devel
else
  sudo arch-nspawn "$CHROOT/root" pacman -Syu --noconfirm
fi

echo "== 2. build (có thể 30–60 phút trên 16 thread) =="
sudo sh -c "cd '$REPO' && exec makechrootpkg -c -r '$CHROOT'"

echo "== xong. sản phẩm:"
ls -la "$REPO"/linux-ilol*.pkg.tar.zst 2>/dev/null
echo "== next: sudo pacman -U linux-ilol-… → uname -r xem -ilol"
