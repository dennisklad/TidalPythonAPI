import tidalapi
import xlsxwriter
import datetime
import glob
import os
import pandas as pd

def getTidalAlbums():
    #Log in Tidal with Browser and get albums
    session = tidalapi.Session()
    session.login_oauth_simple()
    return tidalapi.Favorites(session, session.user.id).albums()

def writeTidalAlbums(albums):
    #Open File to write
    outWorkbook = xlsxwriter.Workbook('albums/albums'+str(datetime.datetime.now())[:10]+'.xlsx')
    outSheet = outWorkbook.add_worksheet('albums')
    #Create headers
    [outSheet.write(0, idx, data) for idx, data in enumerate(["Artist","Title","Release","Tracks","Duration"])]
    #Write data to file
    for item in range(len(albums)):
        partist =  ' & '.join([str(art.name) for art in albums[item].artists])
        outSheet.write(item+1, 0, partist)
        outSheet.write(item+1, 1, albums[item].name)
        outSheet.write(item+1, 2, albums[item].release_date.year)
        outSheet.write(item+1, 3, albums[item].num_tracks)
        outSheet.write(item+1, 4, int(albums[item].duration/60))
    outWorkbook.close()

def compareNewAlbums():
    #Compare new rows that were added in the latest iteration
    files = os.listdir('albums/')
    fnew = files[len(files)-1]
    fold = files[len(files)-2]
    print ("fnew: " + fnew)
    print ("fold: " + fold)
    dfnew=pd.read_excel('albums/' + fnew)
    dfold=pd.read_excel('albums/' + fold)
    print(f"New file has {len(dfnew)} rows, old file has {len(dfold)} rows. You added {len(dfnew)-len(dfold)} albums since the last update.\n")
    merged = dfnew.append(dfold)
    merged = merged.drop_duplicates(keep=False).sort_index()
    print (merged)
    merged.to_excel("unique.xlsx")

writeTidalAlbums(getTidalAlbums())
compareNewAlbums()