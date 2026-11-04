#!/usr/bin/env python3
"""スキル単位のリンク作成。既定はプレビュー。既存の異なる項目は上書きしない。"""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'skills'
    target = args.target.expanduser().absolute()
    if target.exists() and not target.is_dir():
        parser.error('リンク先がディレクトリではありません')
    planned = []
    conflicts = []
    for skill in sorted(source.iterdir()):
        if skill.name.startswith('.') or not (skill / 'SKILL.md').is_file():
            continue
        dest = target / skill.name
        if dest.is_symlink() and dest.resolve() == skill.resolve():
            print(f'変更なし: {skill.name}')
        elif dest.exists() or dest.is_symlink():
            conflicts.append(dest)
        else:
            planned.append((skill, dest))
    if conflicts:
        for dest in conflicts:
            print(f'既存項目と衝突: {dest}')
        raise SystemExit('変更せず停止しました。既存項目を確認してください。')
    if args.apply:
        target.mkdir(parents=True, exist_ok=True)
    for skill, dest in planned:
        print(f'{"作成" if args.apply else "予定"}: {dest} → {skill}')
        if args.apply:
            dest.symlink_to(skill, target_is_directory=True)


if __name__ == '__main__':
    main()
