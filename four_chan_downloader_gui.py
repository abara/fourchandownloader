#import four_chan_downloader as fdown
import thread_image_downloader as fdown
import pygtk
import gtk
import multiprocessing as CPU
from multiprocessing import Pool
    
#import 4chan_downloader

class MainWindow(object):

    def eventHandlerButtonGoClick(self, widget, data=None):
        
        thread_url = self.textentry_thread_url.get_text()
        
        folder_path = self.textentry_folder_path.get_text()
        
        if thread_url == '' or folder_path == '':
            
            print 'feels batman!'
        
        else:
            

            print 'URL :: ' ,thread_url
        
            print 'FOLDER :: ', folder_path

            # --- downloading ---

            #fdown.downloader2( thread_url , folder_path )
            p = Pool(processes=2)
            result = p.apply_async( fdown.downloader2 , [thread_url,folder_path] )
            
            print 'is us'

            
    def quit(self, widget, data=None):

        gtk.main_quit()    

    def __init__(self):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        #self.window.set_default_size(400, 300)

        #--- events connectors        

        self.window.connect("delete_event", self.quit)
        
        #--- packing
 
        self.table = gtk.Table(2 , 4, False)

        self.window.add(self.table)
        
        #--- attaching Widgets

        self.label_thread_url = gtk.Label('Thread URL')
        self.textentry_thread_url = gtk.Entry()
        
        self.label_folder_path = gtk.Label('Destiny folder') 
        self.textentry_folder_path = gtk.Entry()


        self.button_go = gtk.Button("Download Nao")
        
        self.button_go.connect("clicked", self.eventHandlerButtonGoClick)

        # --- Log Viewer
        
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        
        self.sw.add(self.textview)


        #--------------------
        
        # table.attach(child, left_attach, right_attach, top_attach, bottom_attach, xoptions=EXPAND|FILL, yoptions=EXPAND|FILL, xpadding=0, ypadding=0)
        
        self.table.attach( self.textentry_thread_url , 1 , 2 , 0 , 1 , yoptions=gtk.FILL , xpadding=5, ypadding=5) #, gtk.FILL, gtk.FILL)
        
        self.table.attach( self.textentry_folder_path , 1 , 2 , 1 , 2, yoptions=gtk.FILL , xpadding=5, ypadding=5) #, gtk.FILL)
        
        self.table.attach( self.label_thread_url , 0 , 1 , 0 , 1 , yoptions=gtk.FILL ,xpadding=5, ypadding=5)  #, gtk.FILL, gtk.FILL)
        
        self.table.attach( self.label_folder_path , 0 , 1 , 1 , 2, yoptions=gtk.FILL , xpadding=5, ypadding=5) #, gtk.FILL)
        
        self.table.attach( self.sw , 0 , 2 , 2 , 3, xoptions=gtk.FILL ,yoptions=gtk.FILL , xpadding=5, ypadding=5) #, gtk.FILL)
        
        self.table.attach( self.button_go , 0 , 2 , 3 , 4, xoptions=gtk.FILL ,yoptions=gtk.FILL , xpadding=5, ypadding=5) #, gtk.FILL)
        
        #self.table.attach( self.list_viewer_frame , 0 , 1 , 2 , 3 )

        

        
        #self.list_viewer_frame.show()
        #self.list_command_frame.show()
        #self.notebook_viewer.show()
        #self.table.show()
        self.window.show_all()
    

    def loop(self):
        
        gtk.main()

if __name__ == '__main__':
    
    hello = MainWindow()

    hello.loop()
