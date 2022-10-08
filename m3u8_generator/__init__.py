import logging

logger = logging.getLogger(__name__)


class PlaylistGenerator(object):

    header_template = "\n".join([
        '#EXTM3U',
        '#EXT-X-VERSION:{version}',
        '#EXT-X-TARGETDURATION:{duration}',
        '#EXT-X-ALLOW-CACHE:{allow_cache}'
    ])

    def __init__(self, playlist_entries=None, version=3, end_playlist=True):
        if playlist_entries is None:
            raise ValueError

        self.end_playlist = end_playlist
        self.playlist_entries = playlist_entries
        self.version = version
        self.sequence = 0
        self.duration = len(self.playlist_entries)

    def _generate_playlist(self):
        playlist = "{}\n{}".format(self._m3u8_header_template(), self._generate_playlist_entries())
        if self.end_playlist:
            playlist += "\n#EXT-X-ENDLIST"
        return playlist

    def _generate_playlist_entries(self):
        playlist = ""
        for entry in self.playlist_entries:
            playlist += "#EXTINF:{duration},\n{media}\n".format(
                duration=float(entry['duration']), media=(entry['name'])
            )

        return playlist.replace(" ", "")

    def _generate(self):
        return self._generate_playlist()

    def _m3u8_header_template(self):
        header = self.header_template.format(
            version=self.version, duration=self.duration,
            allow_cache='YES' if self.end_playlist else 'NO'
        ).strip()

        return header

    def generate(self):
        """ This is a proxy for _generate makes it
        difficult to edit the real method for future."""
        return self._generate()
