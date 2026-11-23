#!/usr/bin/env python3
"""Track a review package and assemble the approved scene clips."""
import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FILE = 'production.json'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def load(folder):
    return json.loads((folder / FILE).read_text(encoding='utf-8'))

def save(folder, data):
    folder.mkdir(parents=True, exist_ok=True)
    temp = folder / (FILE + '.tmp')
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temp.replace(folder / FILE)

def fingerprint(data):
    payload = {'scene_count': data['scene_count'], 'files': {}}
    for key, value in data['review_files'].items():
        path = Path(value)
        if not path.is_file():
            raise ValueError(f'Missing {key}: {path}')
        payload['files'][key] = {'path': str(path.resolve()), 'sha256': digest(path)}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def check(data):
    approved = data.get('approval')
    if not approved or approved['fingerprint'] != fingerprint(data):
        raise ValueError('Review package is not approved or has changed; obtain explicit approval before proceeding.')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('prepare', help='Record script, storyboard visual, source notes and scene count')
    q.add_argument('folder', type=Path); q.add_argument('--script', type=Path, required=True)
    q.add_argument('--visual', type=Path, required=True); q.add_argument('--source', type=Path, required=True)
    q.add_argument('--scenes', type=int, required=True)
    for name in ['status', 'approve', 'check', 'stitch']:
        q = sub.add_parser(name); q.add_argument('folder', type=Path)
        if name == 'stitch': q.add_argument('--output', default='final.mp4')
    q = sub.add_parser('add-clip'); q.add_argument('folder', type=Path)
    q.add_argument('--scene', type=int, required=True); q.add_argument('--file', type=Path, required=True)
    a = p.parse_args(); folder = a.folder.resolve()
    if a.command == 'prepare':
        if a.scenes < 1 or a.scenes > 100: raise ValueError('Scene count must be between 1 and 100.')
        paths = {k: str(getattr(a, k).resolve()) for k in ('script', 'visual', 'source')}
        data = {'scene_count': a.scenes, 'review_files': paths, 'approval': None, 'clips': {}}
        fingerprint(data)
        if (folder / FILE).exists(): raise ValueError('Production already exists; use a new folder to preserve its record.')
        save(folder, data); print('Review package recorded. Obtain explicit user approval before approve.')
        return
    data = load(folder)
    if a.command == 'approve':
        data['approval'] = {'fingerprint': fingerprint(data), 'approved_at': dt.datetime.now(dt.timezone.utc).isoformat()}
        save(folder, data); print('Approval recorded for the current review package.'); return
    if a.command == 'status':
        try: check(data); state = 'approved'
        except ValueError: state = 'not approved or changed'
        print(json.dumps({'approval': state, 'scenes': data['scene_count'], 'clips': data['clips']}, indent=2)); return
    check(data)
    if a.command == 'check': print('Approval is valid.'); return
    if a.command == 'add-clip':
        if not 1 <= a.scene <= data['scene_count']: raise ValueError('Scene number is outside the approved range.')
        source = a.file.resolve()
        if not source.is_file(): raise ValueError(f'Clip not found: {source}')
        clips = folder / 'clips'; clips.mkdir(exist_ok=True)
        target = clips / f'scene-{a.scene:02d}{source.suffix.lower()}'
        if target.exists(): raise ValueError(f'Clip already exists: {target}; preserve it and use a new production record for revisions.')
        shutil.copy2(source, target)
        data['clips'][str(a.scene)] = {'path': str(target), 'sha256': digest(target)}
        save(folder, data); print(f'Saved {target}'); return
    if a.command == 'stitch':
        if Path(a.output).name != a.output or not a.output.lower().endswith('.mp4'): raise ValueError('Output must be a plain .mp4 filename.')
        target = folder / a.output
        if target.exists(): raise ValueError(f'Output already exists: {target}')
        clips = []
        for n in range(1, data['scene_count'] + 1):
            entry = data['clips'].get(str(n))
            if not entry: raise ValueError(f'Missing scene {n}.')
            path = Path(entry['path'])
            if not path.is_file() or digest(path) != entry['sha256']: raise ValueError(f'Scene {n} missing or changed.')
            clips.append(path)
        try:
            import imageio_ffmpeg
        except ImportError as exc:
            raise ValueError('Install imageio-ffmpeg in the InstaAgent virtual environment.') from exc
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        with tempfile.TemporaryDirectory(prefix='instaagent-') as tmp:
            normalized = []
            for i, clip in enumerate(clips):
                out = Path(tmp) / f'{i:03}.mp4'
                cmd = [ffmpeg, '-nostdin', '-hide_banner', '-loglevel', 'error', '-i', str(clip), '-map', '0:v:0', '-map', '0:a:0', '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(out)]
                subprocess.run(cmd, check=True); normalized.append(out)
            listing = Path(tmp) / 'clips.txt'
            listing.write_text(''.join(f"file '{p}'\n" for p in normalized), encoding='utf-8')
            assembled = Path(tmp) / 'assembled.mp4'
            subprocess.run([ffmpeg, '-nostdin', '-hide_banner', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(assembled)], check=True)
            shutil.copyfile(assembled, target)
        print(f'Saved {target}. Review playback, audio and transitions before delivery.')

if __name__ == '__main__':
    try: main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f'Error: {e}', file=sys.stderr); sys.exit(1)
