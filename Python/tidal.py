from pandas.core.frame import DataFrame
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
    merged_add = DataFrame({'Artist':[],'Title':[],'Release':[],'Tracks':[],'Duration':[]})
    merged_rem = DataFrame({'Artist':[],'Title':[],'Release':[],'Tracks':[],'Duration':[]})
    
    for idx in range(len(merged)):    
        if len(dfnew.loc[dfnew['Title']==merged.iloc[idx,1]])>0:
            print(idx, merged.iloc[idx,1], "was added.")
            merged_add.loc[len(merged_add.index)] = merged.iloc[idx]
        if len(dfold.loc[dfold['Title']==merged.iloc[idx,1]])>0:
            print(idx, merged.iloc[idx,1], "was removed.")
            merged_rem.loc[len(merged_rem.index)] = merged.iloc[idx]

    merged_add.to_excel("unique_added.xlsx")
    merged_rem.to_excel("unique_removed.xlsx")

    #Print values to console
    print(f"\nNew file {files[len(files)-1]} has {len(dfnew)} rows. \
        \nOld file {files[len(files)-2]} has {len(dfold)} rows. \
        \nYou added {len(merged_add)} albums since the last update. \
        \nYou removed {len(merged_rem)} albums since the last update. \
        \n")

#Call functions
write_tidal_albums(get_tidal_albums())
compare_new_albums()