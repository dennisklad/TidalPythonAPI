import tidalapi
import xlsxwriter
import datetime
import os
import glob

x = str(datetime.datetime.now())
outWorkbook = xlsxwriter.Workbook('albums/albums'+x[:10]+'.xlsx')
outSheet = outWorkbook.add_worksheet('albums')
outSheet.write('A1', "Artist")
outSheet.write('B1', "Title")
outSheet.write('C1', "Release")
outSheet.write('D1', "Tracks")
outSheet.write('E1', "Duration")
session = tidalapi.Session()

session.login_oauth_simple()
favorites = tidalapi.Favorites(session, session.user.id)
albums = favorites.albums()
for item in range(len(albums)):
    partist =  ' & '.join([str(art.name) for art in albums[item].artists])
    outSheet.write(item+1, 0, partist)
    outSheet.write(item+1, 1, albums[item].name)
    outSheet.write(item+1, 2, albums[item].release_date.year)
    outSheet.write(item+1, 3, albums[item].num_tracks)
    outSheet.write(item+1, 4, int(albums[item].duration/60))

outWorkbook.close()