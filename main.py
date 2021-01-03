from song.info import *
import psycopg2
import time

conn = psycopg2.connect(private_constant.connect_info)
cur = conn.cursor()

song_id = 26
while song_id < 27:
    time.sleep(1)
    print(f'start song_id: {song_id}')
    song = Song(id_=str(song_id))

    if not song.title():
        print('Page is invalid and skipped')
        continue

    song_sql = 'insert into t_song values (%s, %s, %s, %s, %s, %s, %s, %s);'
    song_data = song.to_song_list()
    cur.execute(song_sql, song_data)
    print(f'-- song_data: {song_data}')

    royalty_sql = 'insert into t_royalty values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    royalty_data = song.to_recent_royalty_list()
    cur.execute(royalty_sql, royalty_data)
    print(f'-- royalty_data: {royalty_data}')

    monthly_royalty_sql = 'insert into t_royalty (song_id, calculate_dt, month_royalty) values(%s, %s, %s)'
    monthly_royalty_data = song.to_monthly_royalty_list()
    for data in monthly_royalty_data:
        cur.execute(monthly_royalty_sql, data)
    print(f'-- monthly_royalty_data: {monthly_royalty_data}')

    print(f'end song_id: {song_id}')
    song_id += 1

conn.commit()
cur.close()
conn.close()

# print(song.title())
# print(song.artist())
# print(song.detail())
# print(song.auction_id())
# print(song.copy_info())
# royalties = song.recent_5years_royalties()
# print(Song.recent_month_royalty(royalties))
# print(song.recent_12months_royalties())
# print(song.recent_12months_royalty_total())
# print(song.auction_info())
