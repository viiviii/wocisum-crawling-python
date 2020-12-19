from song.info import *

song = Song(id_='936')
print(song.title())
print(song.artist())
print(song.detail())
print(song.auction_id())
print(song.copy_info())
royalties = song.recent_5years_royalties()
print(Song.recent_month_royalty(royalties))
print(song.recent_12months_royalties())
print(song.recent_12months_royalty_total())
