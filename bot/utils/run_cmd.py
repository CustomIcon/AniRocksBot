import shlex
import asyncio
from typing import Tuple, Optional
from os.path import basename, join, exists


screen_shot = 'downloads/'


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal."""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode('utf-8', 'replace').strip(),
        stderr.decode('utf-8', 'replace').strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ''
) -> Optional[str]:
    """take a screenshot."""
    ttl = duration // 2
    thumb_image_path = path or join(
        screen_shot,
        f'{basename(video_file)}.jpg',
    )
    command = "ffmpeg -ss {} -i '{}' -vframes 1 '{}'".format(
        ttl,
        video_file,
        thumb_image_path,
    )
    err = (await run_cmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if exists(thumb_image_path) else None