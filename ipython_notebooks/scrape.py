# -*- coding: utf-8 -*-

import os
import json
import csv
import unicodecsv
import unicodedata
import urllib2
import itertools
import re
from bs4 import BeautifulSoup,Tag
from bs4 import NavigableString


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(BASE_DIR, 'csvs')
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        try:
            value = unicode_or_str.decode('utf-8')
        except UnicodeDecodeError:
            #print unicode_or_str
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

def device_specs_built_in_scraper(product_details=None):
    if not product_details:
        upcoming_file = open(os.path.join(project_dir,'upcoming_products_file.csv'),'rU')
        products_data = csv.reader(upcoming_file)
    if product_details:
        products_data = product_details
    device_specs=[]
    device_specs_output=open(os.path.join(project_dir,'device_specs.csv'),'w')
    csv_out=unicodecsv.writer(device_specs_output,delimiter='~',quoting=unicodecsv.QUOTE_ALL)
    csv_out.writerow(["product_id","country_id","colval_1","colval_2","colval_3","colval_4","colval_5","colval_6","colval_7","colval_8",
                    "colval_9","colval_10","colval_11","colval_12","colval_13","colval_14","colval_15","colval_16","colval_17","colval_18",
                    "colval_19","colval_20","colval_21","colval_22","colval_23","colval_24","colval_25","colval_26","colval_27","colval_28",
                    "colval_29","colval_30","colval_31","colval_32","colval_33","colval_34","colval_35","colval_36","colval_37","colval_38",
                    "colval_39","colval_40","colval_41","colval_42","colval_43","colval_44","colval_45","colval_46","colval_47","colval_48",
                    "colval_49","colval_50","colval_51","colval_52","colval_53","colval_54","colval_55","colval_56","colval_57","colval_58",
                    "colval_59","colval_60","colval_61","colval_62","colval_63","colval_64","colval_65","colval_66","colval_67","colval_68",
                    "colval_69","colval_70","colval_71","colval_72","colval_73","colval_74","colval_75"])
    i =0
    for line in products_data:
        i=i+1
        if i:
            product_url=line[2]
            if product_url !='':
                product_id = line[0]
                country_id = 1
                brand = ''
                model_name=''
                operating_system=''
                processor_speed=''
                gpu=''
                sim_size=''
                sim_type=''
                dimensions_size=''
                dimensions_weight=''
                display_size=''
                display_resolution=''
                display_type=''
                primary_camera=''
                secondary_camera=''
                camera_flash=''
                camera_video_recording=''
                camera_hd_recording=''
                camera_other_features=''
                storage_internal=''
                storage_expandable=''
                performance_ram=''
                battery_capacity=''
                battery_talktime_2g=''
                battery_talktime_3g=''
                battery_talktime_4g=''
                connectivity_data=''
                connectivity_data_reporter=''
                connectivity_data_has_2g=False
                connectivity_data_has_3g=False
                connectivity_data_has_4g=False
                networks_already_traversed=False
                connectivity_bluetooth=''
                connectivity_wifi=''
                connectivity_tethering=''
                connectivity_navigation_tech=''
                connectivity_DLNA=''
                connectivity_HDMI=''
                release_date=''
                source_id=''
                novelty=''
                performance_chipset=''
                performance_number_cores=''
                camera_frame_rate=''
                design_color=''
                design_body_material=''
                connectivity_networks=''
                performance_ui_os=''
                performance_cpu=''
                display_touch_features=''
                features_sensors=''
                camera_secondary_video_rate=''
                camera_secondary_frame_rate=''
                av_radio=''
                usb_connector_type=''
                usb_version=''
                usb_features=''
                connectivity_connector_type=''
                primary_video_resolution=''
                secondary_video_resolution=''
                av_audio_format=''
                av_video_format=''
                battery_type=''
                battery_features=''
                display_ppi=''
                display_screen_protection=''
                battery_standby_3g=''
                battery_standby_2g=''
                battery_standby_4g=''
                camera_sensor_type=''
                camera_sensor_model=''
                camera_sensor_size=''
                camera_pixel_size=''
                camera_aperture=''
                camera_extra_features=''
                secondary_camera_extra_features=''
                line_item_string=""
                master_list=list()
                #product_id= request.values.get('product_id')
                req = urllib2.Request(product_url)
                response=urllib2.urlopen(req)
                content=response.read()
                #print type(content)
                soup=BeautifulSoup(content.decode('utf-8'),'html.parser')
                all_tables_list=soup.find_all('table', attrs={'class':'model-information-table row-selection'})


                dimensions_to_sort = []
                value_error = False

                for word in all_tables_list:
                    ##print word
                    rows = word.findAll('tr')
                    for element in rows:
                        element_data=element.findAll('td')
                        #if (element_data[0].contents[0]=='Brand'):
                            #brand=element_data[0].findNext('td').contents[0]
                        master_list.append(element_data)
                        ##print element_data
                        ##print master_list
                for line in master_list:
                    if line[0]:
                        if line[0].contents:
                            if line[0].contents[0]=='Brand':
                                brand=line[0].findNext('td').contents[0]
                            if line[0].contents[0]=='Model':
                                model_name=line[0].findNext('td').contents[0]
                            if line[0].contents[0]=='Operating system (OS)':
                                operating_system=line[0].findNext('td').contents[1]
                            if line[0].contents[0]=='CPU frequency':
                                speed = line[0].findNext('td').contents[0]
                                try:
                                    value, unit = speed.split()
                                    value = float(value)
                                    if unit == "MHz":
                                        freq = ' '.join([str(value/1000), 'GHz'])
                                    else:
                                        freq = speed
                                except ValueError:
                                    freq = speed
                                processor_speed = freq
                            if line[0].contents[0]=='GPU':
                                gpu=line[0].findNext('td').contents[0]
                            if line[0].contents[0]=='SIM card type':
                                sim_size=line[0].findNext('td').contents[1]
                            if line[0].contents[0]=='Number of SIM cards':
                                num_sims = line[0].findNext('td').contents[0]
                                if num_sims == '1':
                                    sim_type = 'Single SIM'
                                elif num_sims == '2':
                                    sim_type = 'Dual SIM'
                                else:
                                    sim_type = num_sims
                            if line[0].contents[0]=='Width' or line[0].contents[0]=='Height' or line[0].contents[0]=='Thickness':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if line_item_string.find(' mm')>0:

                                                        if data_point_type=="Design":
                                                            #print line_item_string.find(' mm'),'-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-00-'
                                                            dimensions_size += (' x ' if dimensions_size else '')+line_item_string.strip(' mm')
                                                            #print line_item_string.strip(' mm'),'\n\n\n\n'
                                                            try:
                                                                dimensions_to_sort.append(float(line_item_string.strip(' mm')))
                                                                #print dimensions_to_sort
                                                            except ValueError:
                                                                value_error = True
                                                                pass

                                                            break
                                                    #dimensions_size=line_item
                                                    #break

                            if line[0].contents[0]=='Weight':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    if weight_item_string.find(' g ')>0:
                                                        weight_item_sp = weight_item_string.split()
                                                        dimensions_weight=weight_item_sp[0] + ' gms'
                                                        break
                            if line[0].contents[0]=='Resolution':
                                display_resolution=line[0].findNext('td').contents[0].title()
                            if line[0].contents[0]=='Type/technology':
                                display_type=line[0].findNext('td').contents[0]
                                display_size_container=line[0].findNext('td').findNext('td').findNext('td').contents
                                for display_item in display_size_container:
                                                #print type(display_item)
                                                if isinstance(display_item,NavigableString):
                                                    display_item_string=to_str(display_item)
                                                    if display_item.find(' in ')>0:
                                                        ##print weight_item_string.find(' g ')
                                                        sc_size_item_sp = display_item_string.split()
                                                        display_size=sc_size_item_sp[0] + ' Inches'
                                                        break
                            if line[0].contents[0] == 'Image resolution':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if line_item_string.find(' MP')>0:
                                                        #print line_item_string.find(' MP')
                                                        if data_point_type.lower()=="primary camera":
                                                            primary_camera=line_item_string
                                                            break
                                                        elif data_point_type.lower() == 'secondary camera':
                                                            secondary_camera=line_item_string
                                                            break

                            if line[0].contents[0]=='Flash type':
                                camera_flash=line[0].findNext('td').contents[0]
                            if line[0].contents[0]=='Features':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if data_point_type=="Primary camera":
                                                        camera_other_features+=line_item_string+' , '
                                                        result_data_for_camera_extra_features = line[0].findNext('td').findNext('td').findNext('td').contents
                                                        camera_extra_features=''
                                                        for element in result_data_for_camera_extra_features:
                                                            if isinstance(element,NavigableString):
                                                                camera_extra_features+=element
                                                    elif data_point_type=='USB':
                                                        usb_features=line_item_string
                                                    elif data_point_type=='Battery':
                                                        battery_features+=(" , " if battery_features else '')+line_item_string

                            if line[0].contents[0]=='Storage':
                                storage_internal=line[0].findNext('td').contents[1]
                                print storage_internal
                                try:
                                    if not line[0].findNext('td').contents[5] is None:
                                        storage_internal=storage_internal+' / '+line[0].findNext('td').contents[5]
                                    if not line[0].findNext('td').contents[9] is None:
                                        storage_internal=storage_internal+' / '+line[0].findNext('td').contents[9]
                                except IndexError as err:
                                    print 'indexError'
                            if line[0].contents[0]=='RAM capacity':
                                performance_ram=line[0].findNext('td').contents[1]
                            if line[0].contents[0]=='Capacity':
                                battery_capacity=line[0].findNext('td').contents[0]
                            if line[0].contents[0]=='3G talk time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' hours ')>0:
                                                        #print talk_time_string.find(' hours ')
                                                        battery_talktime_3g=talk_time_string
                                                        break
                                connectivity_data_has_3g=True
                            if line[0].contents[0]=='2G talk time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' hours ')>0:
                                                        #print talk_time_string.find(' hours ')
                                                        battery_talktime_2g=talk_time_string
                                                        #battery_talktime_2g=talk_time_string
                                                        break
                                connectivity_data_has_2g=True
                            if line[0].contents[0]=='4G talk time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' hours ')>0:
                                                        #print talk_time_string.find(' hours ')
                                                        battery_talktime_4g=talk_time_string
                                                        break
                                connectivity_data_has_4g=True
                            if connectivity_data_has_2g==True:
                                connectivity_data+='2G'
                            if connectivity_data_has_3g==True:
                                connectivity_data+=" /3G "
                            if connectivity_data_has_4g==True:
                                connectivity_data+=" /4g"


                            if line[0].contents[0]=='3G stand-by time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' h')>0:
                                                        #print talk_time_string.find(' h')
                                                        battery_standby_3g=talk_time_string
                                                        break
                            if line[0].contents[0]=='4G stand-by time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' h')>0:
                                                        #print talk_time_string.find(' h')
                                                        battery_standby_4g=talk_time_string
                                                        break


                            if line[0].contents[0]=='2G stand-by time':
                                talk_time_container=line[0].findNext('td').contents
                                for talk_time in talk_time_container:
                                                #print type(talk_time)
                                                if isinstance(talk_time,NavigableString):
                                                    talk_time_string=to_str(talk_time)
                                                    if talk_time_string.find(' hours ')>0:
                                                        #print talk_time_string.find(' hours ')
                                                        battery_standby_2g=talk_time_string
                                                        break

                            if line[0].contents[0]=='Version':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if data_point_type=="Bluetooth":
                                                        connectivity_bluetooth=line_item_string
                                                    elif data_point_type=="USB":
                                                        usb_version=line_item_string
                            if line[0].contents[0]=='Wi-Fi':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        if line_item_string.find('802.11a')>0:
                                            connectivity_wifi+='802.11a'
                                        if line_item_string.find('802.11b')>0:
                                            connectivity_wifi+=' /b '
                                        if line_item_string.find('802.11g')>0:
                                            connectivity_wifi+=' /g '
                                        if line_item_string.find('802.11n')>0:
                                            connectivity_wifi+=' /n '
                                        if line_item_string.find('802.11ac')>0:
                                            connectivity_wifi+=' /ac '
                                        if line_item_string.find('802.11')<0:
                                            connectivity_tethering+=(" / " if connectivity_tethering else '')+line_item_string

                                        #print connectivity_wifi,'\]\]\]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]'

                            if line[0].contents[0]=='Tracking/Positioning':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        connectivity_navigation_tech+=(" / " if connectivity_navigation_tech else '')+line_item_string

                            if line[0].contents[0]=='Connectivity':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        connectivity_connector_type+=(" / " if connectivity_connector_type else '')+line_item_string

                            if line[0].contents[0]=='SoC':
                                performance_chipset=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='CPU cores':
                                number_cores=line[0].findNext('td').contents[0]
                                if number_cores == "1":
                                    y = 'Single Core'
                                elif number_cores == "2":
                                    y = 'Dual Core'
                                elif number_cores == "3":
                                    y = 'Tri Core'
                                elif number_cores == "4":
                                    y = 'Quad Core'
                                elif number_cores == "6":
                                    y = 'Hexa Core'
                                elif number_cores == "8":
                                    y = 'Octa Core'
                                elif number_cores == "10":
                                    y = 'Deca Core'
                                else:
                                    y = number_cores
                                performance_number_cores = y


                            if line[0].contents[0]=='Video FPS':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if data_point_type.lower()=="primary camera":
                                                        camera_frame_rate=line_item_string
                                                        break
                                                    elif data_point_type.lower()=="secondary camera":
                                                        camera_secondary_frame_rate=line_item_string
                                                        secondary_camera_extra_features_set = line[0].findNext('td').findNext('td').findNext('td').contents
                                                        secondary_camera_extra_features=''
                                                        for element in secondary_camera_extra_features_set:

                                                            if isinstance(element,NavigableString):
                                                                secondary_camera_extra_features+=element

                                                        break

                            if line[0].contents[0]=='Colors':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        design_color+=(" / " if design_color else '')+line_item_string

                            if line[0].contents[0]=='Body materials':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        design_body_material+=(" / " if design_body_material else '')+line_item_string



                            if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:
                                table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                for headings in table_heading:
                                    if headings:
                                        data_point_type=headings
                                        #print data_point_type
                                        if data_point_type=='Networks':
                                            if networks_already_traversed==False:
                                                networks_already_traversed=True
                                                new_result_set_data=table_heading.findNext('table')
                                                new_table_rows_list=new_result_set_data.findAll('tr')

                                                for table_row in new_table_rows_list:

                                                    table_dee=table_row.find('td')
                                                    for individual_stuff in table_dee:
                                                        if isinstance(individual_stuff,NavigableString):
                                                            connectivity_networks+=(" / " if connectivity_networks else '')+individual_stuff
                                                            break

                            if line[0].contents[0]=='User interface (UI)':
                                performance_ui_os=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='CPU':
                                performance_cpu=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Other features':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        display_touch_features+=(" / " if display_touch_features else '')+line_item_string
                                display_features_set=line[0].nextSibling.findNext('td').nextSibling
                                for line_item in display_features_set:
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        display_touch_features+=(" / " if display_touch_features else '')+line_item_string


                            if line[0].contents[0]=='Sensors':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        features_sensors+=(" / " if features_sensors else '')+line_item_string

                            if line[0].contents[0]=='Video resolution':
                                if line[0].parent and line[0].parent.parent and line[0].parent.parent.previousSibling:

                                    ##print line[0].parent
                                    ##print line[0].parent.parent
                                    ##print line[0].parent.parent.parent
                                    section_heading= line[0].parent.parent.previousSibling
                                    table_heading = line[0].parent.parent.previousSibling.find('h2',attrs={'class':'header'})
                                    for headings in table_heading:
                                        if headings:
                                            data_point_type=headings
                                            #print data_point_type
                                            result_data = line[0].findNext('td').contents
                                            for line_item in result_data:
                                                #print type(line_item)
                                                if isinstance(line_item,NavigableString):
                                                    line_item_string=to_str(line_item)
                                                    if line_item_string.find(' pixels')>0:
                                                        #print line_item_string.find(' pixels')
                                                        if data_point_type.lower()=="primary camera":
                                                            primary_video_resolution=line_item_string.title()
                                                            break
                                                        elif data_point_type.lower() == 'secondary camera':
                                                            secondary_video_resolution=line_item_string.title()
                                                            break

                            if line[0].contents[0]=='Radio':
                                av_radio=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Connector type':
                                usb_connector_type=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Audio file formats/codecs':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        av_audio_format+=(" / " if av_audio_format else '')+line_item_string

                            if line[0].contents[0]=='Video file formats/codecs':
                                result_data = line[0].findNext('td').contents
                                for line_item in result_data:
                                    #print type(line_item)
                                    if isinstance(line_item,NavigableString):
                                        line_item_string=to_str(line_item)
                                        av_video_format+=(" / " if av_video_format else '')+line_item_string

                            if line[0].contents[0]=='Type':
                                battery_type=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Pixel density':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    if weight_item_string.find(' ppi ')>0:
                                                        #print weight_item_string.find(' ppi ')
                                                        display_ppi=weight_item_string
                                                        break

                            if line[0].contents[0]=='Sensor model':
                                camera_sensor_model=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Sensor type':
                                camera_sensor_type=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Aperture':
                                camera_aperture=line[0].findNext('td').contents[0]

                            if line[0].contents[0]=='Sensor size':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    if weight_item_string.find(' mm ')>0:
                                                        #print weight_item_string.find(' mm ')
                                                        camera_sensor_size=weight_item_string
                                                    if weight_item_string.find(" in ")>0:
                                                        camera_sensor_size+=weight_item_string
                                                        break

                            if line[0].contents[0]=='Pixel size':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    if weight_item_string.find(' µm ')>0:
                                                        #print weight_item_string.find(' µm ')
                                                        camera_pixel_size=weight_item_string[:-4]+" micrometers "
                                                    if weight_item_string.find(" mm ")>0:
                                                        camera_pixel_size+=weight_item_string
                                                        break
                            #User interface (UI)
                            if line[0].contents[0]=='HDMI':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    connectivity_HDMI=weight_item_string
                                                    break
                            if line[0].contents[0]=='User interface (UI)':
                                weight_container=line[0].findNext('td').contents
                                for weight_item in weight_container:
                                                #print type(weight_item)
                                                if isinstance(weight_item,NavigableString):
                                                    weight_item_string=to_str(weight_item)
                                                    performance_ui_os=weight_item_string
                                                    break

                            #print connectivity_networks













                                                    #dimensions_size=line_item
                                                    #break






                                ##print dimensions_size
                if (connectivity_wifi==''):
                    connectivity_div=soup.find('div', attrs={"id":'model-brief-specifications'})
                    for item in connectivity_div.contents:
                        if type(item) is Tag:
                            if len(item.contents)>0:
                                if(item.contents[0]=='Wi-Fi'):
                                    connectivity_wifi=item.next_sibling
                                    break

                ##print brand
                ##print model_name
                ##print dimensions_weight
                dimension_size = dimensions_size[:-2]
                ##print dimensions_size
                ##print primary_camera
                ##print secondary_camera
                ##print display_resolution
                ##print display_type
                if connectivity_data.find('4G')>0:
                    connectivity_data_reporter+="2G / 3G / 4G"
                elif connectivity_data.find("3G")>0:
                    connectivity_data_reporter+="2G / 3G"
                elif connectivity_data.find("2G")>0:
                    connectivity_data_reporter+="2G"
                # connectivity_data_reporter.replace("G","G/ ")
                #connectivity_data_reporter=connectivity_data_reporter[:-2]


                

                if not value_error and dimensions_to_sort:
                    dimensions_to_sort.sort(reverse=True)
                    dimensions_to_sort = [str(x) for x in dimensions_to_sort]
                    dimensions_size = ' x '.join(dimensions_to_sort)
                if dimensions_size:
                    dimensions_size += ' mm'

                if display_resolution:
                    resolution = display_resolution.lower().replace('pixels','')
                    resolution = [float(x.strip()) for x in resolution.split('x')]
                    resolution.sort(reverse=True)
                    resolution = [str(int(x)) for x in resolution]
                    display_resolution = ' x '.join(resolution) + ' Pixels'

                if 'cmos' in camera_sensor_type.lower():
                    camera_sensor_type = 'CMOS'

                
                if 'micro' in sim_size.lower() and 'sim' in sim_size.lower():
                    sim_size = 'Micro SIM'
                if 'nano' in sim_size.lower() and 'sim' in sim_size.lower():
                    sim_size = 'Nano SIM'
                if operating_system:
                    mo = re.match('.+([0-9])[^0-9]*$', operating_system)
                    if mo:
                        pos = mo.start(1)
                        operating_system = operating_system[:pos+1]
                bluetooth_versions = ['1.0','1.0B','1.1','1.2','2.0','2.1','3.0','4.0','4.1','4.2']
                if connectivity_bluetooth:
                    for version in bluetooth_versions:
                        if version in connectivity_bluetooth:
                            connectivity_bluetooth = 'Bluetooth '+version
                            break
                if primary_video_resolution:
                    primary_res = primary_video_resolution.split(' X ')
                    primary_video_resolution = ' x '.join(primary_res)

                if secondary_video_resolution:
                    secondary_cam = secondary_video_resolution.split(' X ')
                    primary_video_resolution = ' x '.join(secondary_cam)

                wifi_technologies = ['a','b','g','n','ac','ad','ah','aj','ax','ay']
                if connectivity_wifi:
                    wifi_techs = [x for x in connectivity_wifi.replace(',',' ').replace(':','').replace('/',' ').split() if len(x)<=2]
                    techs = []
                    for tech in wifi_technologies:
                        if tech in wifi_techs:
                            techs.append(tech)
                        connectivity_wifi = '802.11 ' + '/ '.join(techs)

                standby_time = []
                if battery_standby_2g:
                    standby_time.append(battery_standby_2g+' 2G')
                if battery_standby_3g:
                    standby_time.append(battery_standby_3g+' 3G')
                if battery_standby_4g:
                    standby_time.append(battery_standby_4g+' 4G')
                if standby_time:
                    standby_time_custom = ' / '.join(standby_time)
                else:
                    standby_time_custom = ''

                talk_time = []
                if battery_talktime_2g:
                    talk_time.append(battery_talktime_2g+' 2G')
                if battery_talktime_3g:
                    talk_time.append(battery_talktime_3g+' 3G')
                if battery_talktime_4g:
                    talk_time.append(battery_talktime_4g+' 4G')
                if standby_time:
                    talk_time_custom = ' / '.join(talk_time)
                else:
                    talk_time_custom = ''
                #print standby_time,'-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0'

                    #Coz u only gotta write it once
                #my_header_list=
                #my_header_string="~".join(map(str,my_header_list))
                #f.write(my_header_string)
                    #f.write(["Brand", "Model Name","Price", "Operating System", "CPU Frequency", "GPU","SIM Size","SIM Type","Dimensions Size","","",
                     #                "Dimensions Weight","Display Size","Display Resolution","Display Type","Primary Camera","Secondary Camera",
                      #               "Camera Flash","Camera Video Recording","Camera HD Recording","Camera Other Features","Internal Storage","Expandable Storage",
                      #               "Performance RAM","Battery Capacity","Battery 2G Talktime","Battery 3G Talktime","Battery 4G Talktime","Connectivity Data",
                       #              "Connectivity Bluetooth","Connectivity Wifi", "Connectivity Tethering","Tracking/Positioning","HDMI",
                       #              "Release Date","","","Performance Chipset","Performance Cores",
                        #             "Camera Frame rate","Design Color","Design Body Material","Connectivity networks","","","","","","Performance UI Os","Performance CPU",
                        #             "Soc Other features","Features Sensors","Camera Secondary Video Rate","Camera Secondary Frame Rate","AV Radio",
                         #            "USB Connector Type","USB Version","USB Features","Connectivity Connector Type","AV Audio Format",
                         #            "AV Video Format","Battery Type","Battery Features","Display PPI","Display Screen Protection","Battery 2g Standby",
                          #           "Battery 3g standby","Battery 4G standby",
                           #          "Camera Sensor Model","Camera Sensor Type","Camera Sensor Size","Camera Pixel size","Camera Aperture",
                           #          "Display Extra features","Primary Camera Extra","Secondary Camera Extra"])
                tuple_row=(str(product_id), str(country_id), 
                            to_str(brand).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                            to_str(model_name).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           "".replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(operating_system).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                            to_str(processor_speed).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(gpu).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(sim_size).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(sim_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(dimensions_size).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           
                           to_str(dimensions_weight).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(display_size).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(display_resolution).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(display_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(primary_camera).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(secondary_camera).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_flash).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(primary_video_resolution).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_hd_recording).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_other_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(storage_internal).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(storage_expandable).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(performance_ram).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(battery_capacity).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(talk_time_custom).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_data_reporter).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_bluetooth).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_wifi).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(connectivity_tethering).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_navigation_tech).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_HDMI).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(release_date).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(source_id).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(novelty).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                            to_str(performance_chipset).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(performance_number_cores).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_frame_rate).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(design_color).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(design_body_material).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(connectivity_networks).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(performance_ui_os).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(performance_cpu).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(display_touch_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(features_sensors).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(secondary_video_resolution).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_secondary_frame_rate).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(av_radio).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(usb_connector_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(usb_version).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(usb_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(connectivity_connector_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(av_audio_format).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(av_video_format).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(battery_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(battery_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(display_ppi).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(display_touch_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(standby_time_custom).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_sensor_model).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                                 to_str(camera_sensor_type).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_sensor_size).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_pixel_size).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(camera_aperture).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           to_str(display_touch_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           # to_str(camera_extra_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"',''),
                           # to_str(secondary_camera_extra_features).replace('\t','').replace('\r','').replace('\n','').replace('~','@').replace('"','')
                           )
                device_specs.append(tuple_row)
            else:
                tuple_row=("\n")
                device_specs.append(tuple_row)

                #f.write([to_str(brand),to_str(model_name),"",to_str(operating_system),to_str(processor_speed),
                #                 to_str(gpu),to_str(sim_size),to_str(sim_type),to_str(dimensions_size),"","",to_str(dimensions_weight),to_str(display_size),
                #                 to_str(display_resolution),to_str(display_type),to_str(primary_camera),to_str(secondary_camera),to_str(camera_flash),
                #                 to_str(primary_video_resolution),to_str(camera_hd_recording),to_str(camera_other_features),to_str(storage_internal),
                #                 to_str(storage_expandable),to_str(performance_ram),to_str(battery_capacity),to_str(battery_talktime_2g),to_str(battery_talktime_3g),
                #                 to_str(battery_talktime_4g),to_str(connectivity_data_reporter),to_str(connectivity_bluetooth),to_str(connectivity_wifi),
                #                 to_str(connectivity_tethering),to_str(connectivity_navigation_tech),to_str(connectivity_HDMI),to_str(release_date),"","",
                #                 to_str(performance_chipset),to_str(performance_number_cores),to_str(camera_frame_rate),to_str(design_color),to_str(design_body_material),
                #                 to_str(connectivity_networks),"","","","","",to_str(performance_ui_os),to_str(performance_cpu),
                #                 to_str(display_touch_features),to_str(features_sensors),to_str(secondary_video_resolution),to_str(camera_secondary_frame_rate),
                #                 to_str(av_radio),to_str(usb_connector_type),to_str(usb_version),to_str(usb_features),to_str(connectivity_connector_type),
                #                 to_str(av_audio_format),to_str(av_video_format),to_str(battery_type),to_str(battery_features),to_str(display_ppi),
                #                 to_str(display_touch_features),to_str(battery_standby_2g),to_str(battery_standby_3g),to_str(battery_standby_4g),to_str(camera_sensor_model),
                #                 to_str(camera_sensor_type),to_str(camera_sensor_size),to_str(camera_pixel_size),to_str(camera_aperture),to_str(display_touch_features),to_str(camera_extra_features),to_str(secondary_camera_extra_features)])

    for row in device_specs:
        row_as_string = "~".join(row)
        ##print row_as_string
        #print row
        csv_out.writerow(row)
    # csv_out.close()
    return True