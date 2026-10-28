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

echo "== 0. GPG keys của kernel.org (một lần, idempotent) =="
GNUPG_HOME=/home/xogfredia/.gnupg
KEYS="ABAF11C65A2970B130ABE3C479BE3E4300411886 647F28654894E3BD457199BE38DBBDC86092693E 83BC8889351B5DEBBB68416EB8AC08600F108CDF"
for k in $KEYS; do
  if ! sudo -u xogfredia env GNUPGHOME="$GNUPG_HOME" gpg --list-keys "$k" >/dev/null 2>&1; then
    echo "import $k…"
    sudo -u xogfredia env GNUPGHOME="$GNUPG_HOME" gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys "$k"
  fi
done
echo "3 keys sẵn trong keyring của xogfredia"

echo "== 1. chroot root =="
if [[ ! -d $CHROOT ]]; then
  sudo mkdir -p "$CHROOT"
  sudo mkarchroot "$CHROOT/root" base-devel
else
  sudo arch-nspawn "$CHROOT/root" pacman -Syu --noconfirm
fi

echo "== 2. build (có thể 30–60 phút trên 16 thread) =="
BUILD_USER="${SUDO_USER:-$(logname 2>/dev/null || printf 'xogfredia')}"
sudo GNUPGHOME=/home/xogfredia/.gnupg sh -c "cd '$REPO' && exec makechrootpkg -c -U '$BUILD_USER' -r '$CHROOT'"

echo "== xong. sản phẩm:"
ls -la "$REPO"/linux-ilol*.pkg.tar.zst 2>/dev/null
echo "== next: sudo pacman -U linux-ilol-… → uname -r xem -ilol"
