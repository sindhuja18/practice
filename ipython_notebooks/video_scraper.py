# -*- coding: utf-8 -*-
import os
import json
import csv
import unicodecsv
import shutil, glob
from operator import itemgetter
from pandas import DataFrame
import pandas as pd
import unicodedata
import urllib2
import codecs
import StringIO
from StringIO import StringIO
from bs4 import BeautifulSoup,Tag
from bs4 import NavigableString
import itertools
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser







global reject_list_file_dict
global rejected_reviews_file_dict
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(BASE_DIR,'csvs')


# String to unicode problemo
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        try:
            value = unicode_or_str.decode('utf-8')
        except UnicodeDecodeError:
            print unicode_or_str
            exit()
    else:
        value = unicode_or_str
    return value  # Instance of unicode


def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of str

# Google oAuth stuff
GOOGLE_CLIENT_ID = '644499655555-oklvcc2ci1dufi8r1ki69u1e340aotf5'
GOOGLE_CLIENT_SECRET = 'bnny967zOZFkPmpn6r3V9moO'
REDIRECT_URI = '/authorized' # one of the Redirect URIs from Google APIs console
# Google oAuth stuff



def video_scraper(product_details=None):

    DEVELOPER_KEY = "AIzaSyCNq4UR4zj4rP5M82TTMlQFoVis824HpxQ"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    # Yea - counter-intuitively named the video urls file as Image_Urls - any way - all it needs is product ID and productname
    file_path = os.path.join(directory_path+"/videos.csv")
    vide_reviews_output_file=open(file_path,'w')
    csv_out=unicodecsv.writer(vide_reviews_output_file,delimiter='~')
    # Suprised at the square brackets below? It is required because the csv writer needs a sequence in a list. If I had just given the string, without
    # square brackets, it would have written every character in the string separately - like |p|r|o|d|u|c|t|_|i|d| instead of |product_id|
    '''
    #    delete from product_video_review;
    #set foreign_key_checks=0;
    #LOAD DATA local INFILE '/Users/ShyamR/Desktop/internal_dashboard/Microblog/static/videos.csv' INTO TABLE product_video_review FIELDS TERMINATED BY '~'	 LINES TERMINATED BY '\n' IGNORE 1 LINES (product_id, video_loc, review_title, review_date, review_text,reviewer);
    #set foreign_key_checks=1;
    '''
    csv_out.writerow(['product_id','video_loc','review_title','review_date','review_text','reviewer'])
    if not product_details:
        video_urls_input_file = open(os.path.join(directory_path+"/product_list.csv"),'rU')

        video_data = csv.reader(video_urls_input_file)
    else:
        video_data = product_details
    i =1
    for line in video_data:
        if i!=0:
            print line

            search_response = youtube.search().list(q=line[1]+ " review",type="video",part="id,snippet",maxResults=30).execute()

            search_videos = []

          # Merge video ids
            video_ids = ''
            for search_result in search_response.get("items", []):
                search_videos.append(search_result["id"]["videoId"])
                video_ids = ",".join(search_videos)

          # Call the videos.list method to retrieve location details for each video.
            video_response = youtube.videos().list(id=video_ids,part='snippet, recordingDetails').execute()

            videos = []


            # We need 5 things (dB mappings in brackets) - videoId(video_loc), title(review_title),description(review_text), publishedAt(review_date), channelTitle(reviewer)
          # Add each result to the list, and then display the list of matching videos.
            for video_result in video_response.get("items", []):
                #print video_result['snippet']
                #print video_result['id']
                # Taking care to remove extra tabs, extra new line characters etc within the information fields.
                # Also taking care to have a new line character at the end of the last field.
                # We are going to use tilde (~) as the delimiter - so we are making sure that none of the data has any tilde signs
                # (If any field in our data had a tilde sign, the tilde sign would mistakenly be construed as the end of that field,
                # and it would needlessly start a new field. E.g. - say Review Text (which is one field) has the value "ABD~asd~asd".
                # Then in that case, the value of Review Text (one field) is the one string ABD~asd~asd.
                # However, the delimiter if used as tilde, will mistakenly consider ~ as the end of that field, and
                # therefore, create three fields ABD, asd and asd in place of a single field.
                # All tilde signs are replaced with @. This will make sure the CSV importer doesn't get confused.
                '''
                LOAD DATA local INFILE '/Users/ShyamR/Desktop/internal_dashboard/Microblog/static/videos.csv' INTO TABLE product_video_review FIELDS TERMINATED BY '~'	 LINES TERMINATED BY '\n' IGNORE 1 LINES (product_id, video_loc, review_title, review_date, review_text,reviewer);

                '''
                # Not required to add \n at the end of the last element. Write row takes care of it automatically. Infact, if you
                # add \n, the import command will insert one extra empty row for each record
                # Evil hack to make sure the stupid CSV writer is not confused. It gets confused when it sees a comma, while writing,
                # even if you have properly informed the moronic CSV writer by entering each column separately. The hack is to replace
                #commas by ^ symbol.
                tuple_row=(to_unicode(line[0]),to_unicode(str(video_result['id'])),
                           to_unicode(video_result["snippet"]["title"].replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"','')),
                           to_unicode(video_result['snippet']['publishedAt'].replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"','').replace("'",'')),
                           to_unicode(video_result['snippet']['description'].replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"','').replace("'",'')),
                           to_unicode(video_result['snippet']['channelTitle'].replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"','').replace("'",'')))
                videos.append(tuple_row)

            #print "Videos:\n", "\n".join(videos), "\n"



            for row in videos:
                row_as_string = "~".join(row)
                csv_out.writerow(row)


    return file_path