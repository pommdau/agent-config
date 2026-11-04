#!/bin/sh
# originと追跡ブランチの設定済みリポジトリで使う。
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_dir"
git remote get-url origin >/dev/null
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' >/dev/null
lock_dir="$repo_dir/.git/backup.lock"
if ! mkdir "$lock_dir" 2>/dev/null; then
    echo 'バックアップが実行中、または前回のロックが残っています。' >&2
    exit 1
fi
trap 'rmdir "$lock_dir"' EXIT
trap 'exit 1' HUP INT TERM
if test -n "$(git diff --name-only --diff-filter=U)"; then
    echo '未解決の競合があります。' >&2
    exit 1
fi
git add -- README.md .gitignore rules skills hooks scripts
if ! git diff --cached --quiet; then
    git commit -m "Backup agent configuration $(date '+%Y-%m-%d %H:%M:%S %z')"
fi
# 今回変更がなくても、以前送信に失敗したコミットを送る。
git push
