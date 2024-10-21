from .common import InfoExtractor
from ..utils import (
    float_or_none,
    try_get,
)


class GameDevTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?gamedev\.tv/dashboard/courses/(?P<id>\d+)'
    _TEST = {
        'url': 'https://www.gamedev.tv/courses/complete-blender-creator',
        'md5': '94202bb82884a4e6b2e3dab06f70110c',
        'info_dict': {
            'id': '565801ef-ee86-4c80-8cda-a50e970c6388-1',
            'ext': 'mp4',
            'title': 'promo vid.mp4',
            'thumbnail': r're:https?://.*\.jpg',
            'timestamp': 1713171606,
            'upload_date': '20240415',
            'age_limit': 0,
            '_old_archive_ids': ['generic 565801ef-ee86-4c80-8cda-a50e970c6388'],
            'duration': 94.0,
            'description': 'Learn How To Use Blender to Create Beautiful 3D models for Video Games, 3D Printing & More',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        data = self._parse_json(
            self._search_regex(
                r'(?s)runParams\s*=\s*({.+?})\s*;?\s*var',
                webpage,
                'runParams',
            ),
            video_id,
        )

        title = data['title']

        formats = self._extract_m3u8_formats(
            data['replyStreamUrl'],
            video_id,
            'mp4',
            entry_protocol='m3u8_native',
            m3u8_id='hls',
        )

        return {
            'id': video_id,
            'title': title,
            'thumbnail': data.get('coverUrl'),
            'uploader': try_get(data, lambda x: x['followBar']['name'], str),
            'timestamp': float_or_none(data.get('startTimeLong'), scale=1000),
            'formats': formats,
        }
