from Tkinter import * 
from tkSimpleDialog import *
from tkFileDialog   import *
from tkMessageBox import *
class QuitMe(Frame):                        
    def __init__(self, parent=None):          
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Confirm exit', "Sure you want to Quit?")
        if ans: Frame.quit(self)


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)           
        sbar.pack(side=RIGHT, fill=Y)                   
        text.pack(side=LEFT, expand=YES, fill=BOTH)     
        self.text = text
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')              
        self.text.focus()                                
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')         



class SimpleEditor(ScrolledText):                        
    def __init__(self, parent=None, file=None): 
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, text='Cut',   command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find',  command=self.onFind).pack(side=LEFT)
        QuitMe(frm).pack(side=LEFT)
	Button(frm, text='+',  command=self.up).pack(side=LEFT)
	Button(frm, text='-',  command=self.down).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file) 
        self.text.config(font=('consolas', 14, 'normal'))
    def onSave(self):
	self.file_opt = options = {}
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        options['initialfile'] = 'textfile.txt'
        options['parent'] = root
        filename = asksaveasfilename(**self.file_opt)
        if filename:
            alltext = self.gettext()                      
            open(filename, 'w').write(alltext)          
    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)        
        self.text.delete(SEL_FIRST, SEL_LAST)           
        self.clipboard_clear()              
        self.clipboard_append(text)
    def up(self):
        size2 = self.text.config()["font"][4].split(" ")
	size = int(size2[1])
	self.text.config(font=('consolas', size + 1, 'normal'))
    def down(self):
        dsize2 = self.text.config()["font"][4].split(" ")
	dsize = int(dsize2[1])
	self.text.config(font=('consolas', dsize - 1, 'normal'))
    def onPaste(self):                                    
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass                                      
    def onFind(self):
	print "1"
        target = askstring('Find', 'Find: ')
        if target:
	    print "2"
            where = self.text.search(target, INSERT, END)  
            #if where:
	    print "3"                                    
            print where
            pastit = where + ('+%dc' % len(target))   
            self.text.tag_remove(SEL, '1.0', END)    
            self.text.tag_add(SEL, where, pastit)     
            self.text.mark_set(INSERT, pastit)         
            self.text.see(INSERT)                    
            self.text.focus()                        

#if there are no cmdline arguments, open a new file.
if len(sys.argv) > 1:
	root = Tk()
	root.attributes('-zoomed', True)
	#root.iconbitmap("main.gif")
	root.resizable(0, 0)
    	root.title("Text Editor")
	img = Image("photo", file="main.gif")
	root.tk.call('wm','iconphoto',root._w,img)
	SimpleEditor(file=sys.argv[1]).mainloop()                
else:
	root = Tk()
	root.attributes('-zoomed', True)
	#root.iconbitmap("main.gif")
	root.resizable(0, 0)
    	root.title("Text Editor")
	img = Image("photo", file="main.gif")
	root.tk.call('wm','iconphoto',root._w,img)
	SimpleEditor().mainloop()
