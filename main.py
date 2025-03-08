import re
import os
import click
import json
import sys
from loguru import logger
from tiktokcomment import TiktokComment
from tiktokcomment.typing import Comments

# Pastikan output di terminal menggunakan UTF-8
sys.stdout.reconfigure(encoding='utf-8')

__title__ = 'TikTok Comment Scrapper'
__version__ = '2.0.1'


@click.command(help=__title__)
@click.version_option(version=__version__, prog_name=__title__)
@click.option(
    "--aweme_id",
    help='ID video TikTok',
    callback=lambda _, __, value: match.group(0) if (
        match := re.match(r"^\d+$", value)) else None
)
@click.option(
    "--output",
    default='data/',
    help='Directory output data'
)
def main(aweme_id: str, output: str):
    if not aweme_id:
        raise ValueError('Example ID: 7418294751977327878')

    logger.info(f'Start scraping comments for {aweme_id}')

    # Scrape comments
    comments: Comments = TiktokComment()(aweme_id=aweme_id)

    # Pastikan direktori output ada
    output_dir = os.path.abspath(output)
    os.makedirs(output_dir, exist_ok=True)

    # Path file output JSON
    final_path = os.path.join(output_dir, f"{aweme_id}.json")

    # Simpan hasil scraping ke file JSON dengan encoding UTF-8
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(comments.dict, f, ensure_ascii=False, indent=4)

    logger.info(f'Comments saved for {aweme_id} at {final_path}')


if __name__ == '__main__':
    main()
