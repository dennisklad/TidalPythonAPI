import tidalapi
import xlsxwriter
import datetime
import glob
import os
import pandas as pd

PATH_ALBUMS = "albums/"

def get_tidal_albums():
    #Log in Tidal with Browser and get albums
    session = tidalapi.Session()
    session.login_oauth_simple()
    return tidalapi.Favorites(session, session.user.id).albums()

def write_tidal_albums(albums):
    #Open File to write
    out_workbook = xlsxwriter.Workbook(PATH_ALBUMS+'albums'+str(datetime.datetime.now())[:10]+'.xlsx')
    out_sheet = out_workbook.add_worksheet('albums')
    #Create headers
    [out_sheet.write(0, idx, data) for idx, data in enumerate(["Artist","Title","Release","Tracks","Duration"])]
    #Write data to file
    for row_num in range(len(albums)):
        out_sheet.write(row_num+1, 0, ' & '.join([str(artist.name) for artist in albums[row_num].artists]))
        out_sheet.write(row_num+1, 1, albums[row_num].name)
        out_sheet.write(row_num+1, 2, albums[row_num].release_date.year)
        out_sheet.write(row_num+1, 3, albums[row_num].num_tracks)
        out_sheet.write(row_num+1, 4, int(albums[row_num].duration/60))
    out_workbook.close()

def compare_new_albums():
    #Compare new rows that were added in the latest iteration
    files = os.listdir(PATH_ALBUMS)
    dfnew, dfold = pd.read_excel(PATH_ALBUMS + files[len(files)-1]), pd.read_excel(PATH_ALBUMS + files[len(files)-2])
    merged = dfnew.append(dfold)
    merged = merged.drop_duplicates(keep=False).sort_index()
    merged.to_excel("unique.xlsx")
    #Print values to console
    print(f"\nNew file {files[len(files)-1]} has {len(dfnew)} rows. \
        \nOld file {files[len(files)-2]} has {len(dfold)} rows. \
        \nYou added {len(dfnew)-len(dfold)} albums since the last update. \
        \n", merged)

#Call functions
write_tidal_albums(get_tidal_albums())
compare_new_albums()