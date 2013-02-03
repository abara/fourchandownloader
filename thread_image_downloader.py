import urllib2
import bs4
import sys
import os
import datetime

# TODO preencher o db de links com as imagens ja salvas!!!!

# he knows how to do!!!  http://mail.python.org/pipermail/tutor/2004-August/031232.html
LOG = ""

LINK_DB     = []

def write_log( text ):
    
    global LOG
    
    LOG += text + '\n'

def save_image_file_from_web( image_url , filename , folder_path ):
        
    write_log( '+-------------------------------------+\n|            Saving process           |\n+---+---------------------------------+\n| 1 | downloading pic [' + filename + ']\n+---+---------------------------------+\n' )

    socket_connector = urllib2.build_opener()
    
    html_image_page = socket_connector.open( image_url )
    
    picture_itself = html_image_page.read()
    
    write_log( '| 2 | saving into [' + folder_path + ']\n+---+---------------------------------+' )
    
    file_output_buffer = open( folder_path+'/'+filename , 'wb')
    
    file_output_buffer.write( picture_itself )
    
    file_output_buffer.close

    write_log( '| 3 | Bye Bye\n+---+---------------------------------+' )

# ----------------------------------------------------------------------

def get_filename( image_url ):
    
    return image_url.split('/')[-1]

# ----------------------------------------------------------------------

def extract_links ( thread_url ):
    
    CONNECTION_SOCKET = urllib2.urlopen( thread_url )
    
    html_page_source = CONNECTION_SOCKET.read()
    
    
    parsed_html = bs4.BeautifulSoup( html_page_source )
    
    anchor_tag_qtt = len ( parsed_html('a') )
    
    href_link_tmp_list = []
    
    for i in xrange( 0 , anchor_tag_qtt ):
        
        # Some anchors are not related to image links
        # so we need to filter these with correct tags
        
        try :
            
            href_link = parsed_html('a')[i]['href'] 
            
            if '//images.4chan.org' in href_link :
                
                href_link_tmp_list.append( 'http:'+href_link )
        
        except :
        
            continue
                
    return href_link_tmp_list


# ----------------------------------------------------------------------

# function [get_filenames_on_disk]
# 
# The board thread receive, or not, a new image
# so every time we request a new html file related of a thread
# we are in a situation of : scanning the same href links that was downloaded before.
# to avoid downloading a already saved picture we need a name/reference list
# of the saved pictures at disk at the choosen folder.

def get_filenames_on_disk( folder_path ):
    
    filenames_list = []

    directory = os.listdir(folder_path)
    
    # directory is a list of strings where this string are
    # the name of the files on this directory

    for filename in directory :
        
        writelog( 'file : ' , filename )
        
        filenames_list.append( filename )
        
    return filenames_list

def downloader2( thread_url , folder_path ):
    
    global LOG
    global LINK_DB
    
    write_log( 'SCANNING FOLDER : ' + folder_path )
    
    LINK_DB += get_filenames_on_disk( folder_path )
    
    write_log( 'EXTRACTING PICTURES LINKS FROM : ' + thread_url )
    
    image_url_list = extract_links( thread_url )
    
    for link in image_url_list:
        
        now = datetime.datetime.today()

        print 'Running : %i/%i %i:%i:%i ' % ( now.day , now.month, now.hour, now.minute, now.second )
        
        if not get_filename( link ) in LINK_DB :
            
            write_log( '[new link found] [' + link + ']' )
            
            save_image_file_from_web( link , get_filename(link) , folder_path )
            
            LINK_DB.append( get_filename( link ) )
            
        else :
            
            write_log( 'file is already saved' )
            
    print LOG

def downloader( thread_url , folder_path ):

    while True:
        
        try :
            
            # --- getting html source
            
            HTML_SOURCE_SOCKET = urllib2.urlopen( thread_url )
            
            html_page = HTML_SOURCE_SOCKET.read() # return a string
            
            # --- parsing html
            
            parsed_html = bs4.BeautifulSoup(html_page)
            
            anchor_tag_qtt = len( parsed_html('a') )
            
            # --- refreshing db with , possible, new links
            
            for i in xrange(0, anchor_tag_qtt) :
                
                try :
                    
                    #print parsed_html('a')[i]['href']
                    
                    # --- extracting href value com anchor tags
                    
                    href_link_string = parsed_html('a')[i]['href']
                    
                    # --- validating as an address for a image
                    
                    if '//images.4chan.org' in href_link_string :
                        
                        print 'scanning -> ' , href_link_string ,
                        
                        if not href_link_string in LINK_DB :
                            
                            print '[new link found]'
                            
                            LINK_DB.append( href_link_string )
                            
                            # --- generating a name for pic
                            
                            picture_name = href_link_string.split('/')[-1]
                            
                            print '[saving as] ' ,  picture_name
                            
                            # --- downloading content
                            
                            save_image_file_from_web( "http:"+href_string , picture_name , folder_path )
                            print 'penis'
                            #~ img_opener = urllib2.build_opener()
                            #~ page_tmp = img_opener.open("http:"+href_string)
                            #~ 
                            #~ picture = page_tmp.read()
                            
                            # --- persisting
                            
                            #~ fout = open( FOLDER+picture_name , 'wb')
                            #~ fout.write( picture )
                            #~ fout.close
                            
                            print '[picture was saved]'
                            
                        else :
                            
                            print '[link was downloaded]'
            
                except :
                    
                    continue
                    
            HTML_SOURCE_SOCKET.close()
            exit(0)        
            
        except urllib2.URLError:
        
            print '404'
            
            exit(0)
    
if __name__ == "__main__":
    
    
    
    if not len (sys.argv) == 3:
    
        print 'python2 4chan_downloader.py   /folder/path   http://4chan.url.site'
        #print len (sys.argv)
        exit(0)
        
        
    else:
        
        LINK_DB     = []
        
        downloader2( sys.argv[2] , sys.argv[1] )
        
        #get_filenames_from_disk( sys.argv[1] )
        
        
        
