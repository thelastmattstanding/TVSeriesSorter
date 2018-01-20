# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 17:49:29 2018

@author: Matt James
"""

import os
from bs4 import BeautifulSoup
import sys
import urllib
import re

def showrequest(fol) :
    
    showname = os.path.split(fol)[1]
    showlink = showname.replace(" ", "%20")
    url = "http://www.imdb.com/find?q=" + showlink + "&s=tt&ttype=tv&ref_=fn_tv"
    searchsoup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
    searchresult = searchsoup.find_all("td", class_= "result_text")
    if (searchresult != [] and (showname.lower() in searchresult[0].text.lower())) :
        
        searchlink = searchresult[0].find_all("a", href=True)[0]['href']

    else :
        
        print("\nUnfortunately we couldn't find your TV show!")
        print("Have you named your folder containing the TV series correctly?")
        print("Try Again!")
        sys.exit()
        
    searchlink = "http://www.imdb.com" + searchlink
    searchsoup = BeautifulSoup(urllib.request.urlopen(searchlink), "lxml")
    searchresult = searchsoup.find_all("div", class_= "seasons-and-year-nav")[0].find_all("a")
    slinks = []
    
    for result in searchresult :
        
        if("season" in result['href']) :
            
            slinks.append("http://www.imdb.com" + result['href'])
            
    epref = {}
    
    for link in slinks :
        
        searchsoup = BeautifulSoup(urllib.request.urlopen(link), "lxml")
        season = searchsoup.find_all("option", selected="selected")[0]['value']
        eptags = searchsoup.find_all("a", title=True, itemprop="name")
        episodes = searchsoup.find_all("meta", itemprop="episodeNumber")
        for i in range(len(episodes)) :
                     
            ep = episodes[i]['content']
            if(len(ep) == 1 and len(season) == 1) :
                epref["s0" + season + "e0" + ep]  = eptags[i].text
            elif(len(ep) == 1) :
                epref["s" + season + "e0" + ep]  = eptags[i].text
            elif(len(season) == 1) :
                epref["s0" + season + "e" + ep]  = eptags[i].text
            else :
                epref["s" + season + "e" + ep]  = eptags[i].text

    return epref 
    
    
def findkey (eppath) :
    
    episode = os.path.split(eppath)[1].lower()
    episode = episode.replace("season", "s")
    episode = episode.replace("episode", "e")
    
    if((re.search(r"s\s*[0-9]+", episode) != None) and (re.search(r"e\s*[0-9]+", episode) != None)) :
        
           snum = re.search("s\s*[0-9]+", episode).group()
           snum = snum.replace(" ", "")
           enum = re.search("e\s*[0-9]+", episode).group()
           enum = enum.replace(" ", "")

    elif(re.search(r"[0-9]+\s*x\s*[0-9]+", episode) != None) :
        
        keynum = re.search(r"[0-9]+\s*x\s*[0-9]+", episode).group()
        keynum = keynum.replace(" ", "")
        snum = "s" + keynum.split("x")[0]
        enum = "e" + keynum.split("x")[1]      

    else :
        
        return "None"

    if(len(snum[1:]) == 1) :
               
               snum = snum[0] + "0" +  snum[1:]

    if(len(enum[1:]) == 1) :
               
               enum = enum[0] + "0" +  snum[1:]

    key = snum + enum
    
    return key
'''                 
def folsort1(tvpath) :
    
    tvname = os.path.split(tvpath)[1]
    
    if(key == "None") :
        
        path = os.path.join(tvfol,"Others")
        if (os.path.exists (path) == False) :                                                                             #os.path.exists() checks whether a path exists or not
        
            os.mkdir (path)
            
        copy2(tvpath, path)
        
    else :
        
        folname = "Season " + str(int(key.split("e")[0][1:]))
        path = os.path.join(tvfol, folname)
        if (os.path.exists (path) == False) :                                                                             #os.path.exists() checks whether a path exists or not
        
            os.mkdir (path)
            
        copy2(tvpath, path)
        newpath = os.path.join(path, tvname)
        title = key.upper() + " - " + eplist[key] + os.path.splitext(tvname)[1]
        os.rename(newpath,os.path.join(path, title))                
    
''' 
def folsort() :
    
    tvname = os.path.split(tvpath)[1]
    if(key == "None") :
        
        path = os.path.join(tvfol,"Others")
        title = tvname
        
    else :
        
        folname = "Season " + str(int(key.split("e")[0][1:]))
        path = os.path.join(tvfol, folname)
        epname = eplist[key]
        illchar = "\\/:*?\"<>|"
        for char in illchar :
            
            epname = epname.replace(char, "")
            
        title = key.upper() + " - " + epname + os.path.splitext(tvname)[1]
        
    if (os.path.exists (path) == False) :                                                                             #os.path.exists() checks whether a path exists or not
        
            os.mkdir (path)
        
    os.rename(tvpath,os.path.join(path, title))     
    
def checkloc(dloc) :
    
    '''
    The function is used to check whether the directory address passed exists
    or not.
    '''
    
    if (os.path.isdir (dloc) == False) :                                                                              #os.path.isdir() checks whether a directory exists or not
        
        print ("\nTHE DIRECTORY ENTERED DOESN'T SEEM TO EXIST!")
        dloc = input ("PLEASE RE-ENTER THE DIRECTORY : ")                    
        checkloc (dloc)
        
    return dloc
        
def checkfol (fol) :
    
    '''
    The function is used to check whether the directory passed exists (using checkloc()),
    and if it does, dispays the folder chosen, and asks the user whether the folder chosen
    is correct or not. If the folder chosen is wrong, the user can enter a new directory
    and the process is retried.
    '''
    
    fol = checkloc (fol)                                                                                              #checks whether directory exists or not
    
    if (fol.endswith (os.path.sep)) :                                                                                 #os.path.sep is the path separator used by the OS
    
    	fol = fol.rstrip (os.path.sep)                                                                                  #rstrip() removes a given substring from the right end of a string
    
    tail = os.path.split (fol)                                                                                        #os.path.split() splits the path into a list [head, tail], where the tail is the last pathname
    
    while True :
        
        print ("\nTHE FOLDER SELECTED IS : ", tail[1])
        choice = input ("IS THIS CORRECT? (YES/NO) : ")
    
        if ((choice == "no") or (choice == "NO")) :
        
            fol = input ("PLEASE ENTER THE CORRECT DIRECTORY : ")               
            fol = checkfol (fol)
            break
        
        elif ((choice == "yes") or (choice == "YES")) :
            
            break
    
        else :
            
            print ("\nYOU AREN'T JOKING, ARE YOU? I DON'T REMEMBER EVER LISTING SUCH AN OPTION!")
        
    return fol
    
def dirfile (fol, num = 0) :
    
    '''
    The function is used to write all the paths into a file, and return the 
    total number of required paths present in the folder.
    '''
    
    folpaths = os.listdir (fol)                                                                                         #os.listdir creates a list of all the objects present (files, folders, etc.) in the folder
    tvext = (".mp4", ".avi", ".m4v", ".mov", ".mkv", ".3gp")
    
    for path in folpaths :
        
        direc = os.path.join (fol, path)                                                                                #os.path.join() joins two paths together
        
        if (os.path.isfile (direc) == False) :                                                                          #os.path.isfile() checks whether a given path is a file path or not
            
            num = dirfile (direc, num)                                                                                  #The function is called again in order to access the sub-folders in the folder
        
        else :
            
            if (direc.lower().endswith(tvext)) :                                                                       #endswith() checks if a string ends with a given substring
                
                num = num + 1
                filetv.write (direc + os.linesep)
             
    return num

filetv = open ("tvpath.txt", "w+")
tvfol = input("Enter the tv series folder path : ")

tvfol = checkfol (tvfol)
numtv = dirfile (tvfol)
        
if (numtv == 0) :                                                                                              
            
    print ("\nTHERE ARE NO MEDIA FILES IN THIS FOLDER!")
    print("\nTRY AGAIN!")
    sys.exit()

filetv.seek(0)
eplist = showrequest(tvfol)
tvfol = os.path.join(tvfol,"Sorted")

if (os.path.exists (tvfol) == False) :                                                                             #os.path.exists() checks whether a path exists or not
        
        os.mkdir (tvfol)   

for tv in range (numtv) :
        
    tvpath = filetv.readline() 
    if (tvpath == "\n") :                                                                                            #every alternate line read from the file is '\n', and has to be skipped
            
        tvpath = filetv.readline()
        
    tvpath = tvpath.rstrip("\n")
    key = findkey(tvpath)
    print (key)
    folsort()
    
print("\nHopefully should've worked...")        

    


'''
connectivity issue
handling multiple files with same name
imdb name error
key error
'''