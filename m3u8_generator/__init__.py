import datetime
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)


class PlaylistGenerator(object):

    header_template = "\n".join([
        '#EXTM3U',
        '#EXT-X-VERSION:{version}',
        '#EXT-X-TARGETDURATION:{duration}',
        '#EXT-X-PROGRAM-DATE-TIME:{start_time}',
    ])

    def __init__(self, playlist_entries, version=3, end_playlist=True, start_time=0, target_duration=None):
        if playlist_entries is None:
            raise ValueError
        if start_time == 0:
            raise ValueError
        if target_duration is None:
            raise ValueError

        self.end_playlist = end_playlist
        self.playlist_entries = playlist_entries
        self.version = version
        self.sequence = 0
        self.duration = target_duration
        self.start_time = datetime.datetime.fromtimestamp(start_time, tz=ZoneInfo('UTC')).isoformat(timespec='milliseconds')

    def _generate_playlist(self, sequence):
        playlist = "{}\n{}".format(self._m3u8_header_template(sequence), self._generate_playlist_entries())
        if self.end_playlist:
            playlist += "\n#EXT-X-ENDLIST"
        return playlist

    def _generate_playlist_entries(self):
        playlist = ""
        for entry in self.playlist_entries:
            playlist += "#EXT-X-DISCONTINUITY\n#EXTINF:{duration},\n{media}\n".format(
                duration=float(entry['duration']), media=(entry['name'])
            )

        return playlist.replace(" ", "")

    def _generate(self, sequence):
        return self._generate_playlist(sequence)

    def _m3u8_header_template(self, sequence):
        header = self.header_template.format(
            version=self.version, duration=self.duration, start_time=self.start_time
        ).strip()

        if sequence:
            header += '\n#EXT-X-MEDIA-SEQUENCE:{}'.format(sequence)

        return header

    def generate(self, sequence=None):
        """ This is a proxy for _generate makes it
        difficult to edit the real method for future."""
        return self._generate(sequence)
