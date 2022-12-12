#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide the interface class
"""

import logging
from tkinter import Tk, IntVar, StringVar, Spinbox
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror, askyesno, showwarning
from os.path import basename


def choose_dir(old_dir):
    """!@brief
        Generic function to choose a directory

        @param old_dir (str)
            Old path of directory

        @return (str)
            Path of choose directory
    """
    temp_str = askdirectory()

    # https://stackoverflow.com/questions/15010461/askopenfilename-handling-cancel-on-dialogue
    if not temp_str:
        temp_str = old_dir
    return temp_str


def choose_file(old_file, **args):
    """!@brief
        Generic function to choose a file

        @param old_file (str)
            Old path of file

        @param args (**)
            Parameters of askopenfilename

        @return (str)
            Path of choose file
    """
    temp_str = askopenfilename(**args)

    # Verify if click on cancel
    if not temp_str:
        temp_str = old_file
    return temp_str


def disable_elemens(part):
    """!@brief
        disable all element of part

        @param part (tk object)
            graphical part
    """
    for child in part.winfo_children():
        # we can't disable scrollbar and frame
        if ('scrollbar' not in child._name and
            'frame' not in child._name):
            child.configure(state='disabled')


def enable_elemens(part):
    """!@brief
        enable all element of part

        @param part (tk object)
            graphical part
    """
    for child in part.winfo_children():
        # we can't enable scrollbar and frame
        if ('scrollbar' not in child._name and
            'frame' not in child._name):
            child.configure(state='normal')


def reduce_path(path):
    """!@brief
       reduce path of directory to keep only name of directory
       
       @param path (str)
           complete path
    """
    return '... ' + basename(path)
    
    
    
class CabInterface (Tk):
    """!@brief
        define global windows
    """
    # Class of global windows

    def __init__(self, argument, send_pipe=None, recv_pipe=None, parent=None):
        """!@brief
            constructor

            @param argument (namespace)
                namespace of arguments
            @param send_pipe
                sender of argument to execution
            @param recv_pipe
                reciever of result from execution
            @param parent : object
                whose called
        """
        logging.debug("IN")
        # Create Windows
        Tk.__init__(self, parent)
        self.option_add("*background", "white", 100)
        self.parent = parent
        self.args = argument
        self.send_pipe = send_pipe
        self.recv_pipe = recv_pipe
        # State of interface
        self.execute = False
        self.advice = False
        row = 0

        # Input directory
        ttk.Label(self, text="Input Directory").\
            grid(column=0, row=row, columnspan=2, sticky='W')
        row += 1

        ttk.Button(self, text="...", command=self.choose_dir_i).\
                   grid(column=0, row=row, sticky='W')
        self.input = StringVar(value=".")
        self.input_show = StringVar(value=self.input.get())
        ttk.Label(self, textvariable=self.input_show,
                  wraplength=1200, style='path.TLabel').\
            grid(column=1, row=row, columnspan=5, sticky="W")
        row += 1

        # Output directory
        ttk.Label(self, text="Output Directory").\
            grid(column=0, row=row, columnspan=2, sticky='W')
        row += 1

        ttk.Button(self, text="...", command=self.choose_dir_o).\
                   grid(column=0, row=row, sticky='W')
        self.output = StringVar(value=self.input.get())
        self.output_show = StringVar(value=self.input.get())
        ttk.Label(self, textvariable=self.output_show,
                  wraplength=1200, style='path.TLabel').\
            grid(column=1, row=row, columnspan=5, sticky="W")
        row += 1

        # Number by image
        ttk.Label(self, text="Number by image").\
            grid(column=0, row=row, columnspan=1, sticky='W')

        self.max = StringVar(value="1")
        Spinbox(self, from_=1, to=10, textvariable=self.max,
                width=4).\
            grid(column=1, row=row, sticky='E')
        
        row += 1

        # Validation
        self.validation = IntVar(value=1)
        ttk.Checkbutton(self, text="Validation",
                        variable=self.validation,
                        command=self.change_valid).grid(column=0,
                                                        row=row,
                                                        columnspan=2,
                                                        sticky='W')
        row += 1

        self.valid_title = ttk.Label(self, text="Validation file")
        self.valid_title.grid(column=0, row=row, columnspan=2)
        
        row += 1
        self.valid_but = ttk.Button(self, text="...", width=5,
                                    command=self.choose_valid_file)
        self.valid_but.grid(column=0, row=row, columnspan=1, sticky="E")
        self.valid = StringVar(value="./validation.csv")
        self.valid_show = StringVar(value=self.valid.get())
        self.valid_lab = ttk.Label(self, textvariable=self.valid_show,
                                   style='path.TLabel')
        self.valid_lab.grid(column=1, row=row, sticky="W")

        row += 1

        # type of output
        self.csv = IntVar(value=1)
        ttk.Checkbutton(self, text="Export csv",
                        variable=self.csv,).grid(column=0,row=row,
                                                 columnspan=2, sticky='W')
        row += 1
        
        self.barcode = IntVar(value=0)
        ttk.Checkbutton(self, text="Barcode only",
                        variable=self.barcode,).grid(column=0,row=row,
                                                     columnspan=2, sticky='W')
        row += 1
        
        self.pref = IntVar(value=1)
        ttk.Checkbutton(self, text="Barcode_ImageName",
                        variable=self.pref,).grid(column=0,row=row,
                                                  columnspan=2, sticky='W')
        row += 1

        self.suf = IntVar(value=0)
        ttk.Checkbutton(self, text="ImageName_Barcode",
                        variable=self.suf,).grid(column=0,row=row,
                                                 columnspan=2, sticky='W')
        row += 1

        # Create Launcher part
        self.launch = ttk.Frame(self.parent)
        self.launch.grid(column=0, row=row, sticky="N", columnspan=9)
        self.gowait = ttk.Button(self.launch, text="GO",
                                 command=self.star_execute)
        self.gowait.grid(column=4, row=row, columnspan=2)

        # Capture closed windows
        self.protocol("WM_DELETE_WINDOW", self.close)
        logging.info("OUT")

        # launch function whose verify end of execution
        self.after(20, self.maj)


    def choose_dir_i(self):
        """!@brief
            Take directory for input
        """
        logging.debug("IN")
        logging.debug(self.input.get())

        self.input.set(choose_dir(self.input.get()))
        self.input_show.set(reduce_path(self.input.get()))
        
        # TODO : while output not modify use value of input 

        logging.debug("OUT")

    def choose_dir_o(self):
        """!@brief
            Take directory for output
        """
        logging.debug("IN")
        logging.debug(self.output.get())

        self.output.set(choose_dir(self.output.get()))
        self.output_show.set(reduce_path(self.output.get()))

        logging.debug("OUT")

    def advise(self):
        """!@brief
            warn risked to work without validation file if maximum of barcode
            by images > 1 
        """
        if (not self.advice and
            int(self.max.get())>1 and
            self.validation.get() == 0):
            # set flag for message not appear every time 
            self.advice = True
            showwarning("Advice","Used validation file when there are more one\
                         barcode by images")
        
    def choose_valid_file(self):
        """!@brief
            Take path of validation file
        """
        self.valid.set(choose_file(old_file=self.valid.get(),
                                   title="validation file",
                                   filetypes=[('csv files', '.csv')],
                                   initialdir=self.input.get()))
        self.valid_show.set(reduce_path(self.valid.get()))

    def change_valid(self):
        """!@brief
            Enable or disable validation file
        """
        if self.validation.get() == 1:
            self.valid_title.configure(state='normal')
            self.valid_but.configure(state='normal')
            self.valid_lab.configure(state='normal')
        else:
            self.valid_title.configure(state='disabled')
            self.valid_but.configure(state='disabled')
            self.valid_lab.configure(state='disabled')


    def star_execute(self):
        """!@brief
            all actions when click on button GO
            disable all elements
            launch waiting bar
            take all configuration parameters
            launch execution
        """
        logging.debug("IN")
        # Take size of windows
        width_win = self.winfo_width()
        # Delete GO Button
        self.gowait.destroy()
        # Create progessbar
        self.gowait = ttk.Progressbar(self.launch, mode='indeterminate',
                                      length=width_win)
        self.gowait.grid(column=0, row=18, columnspan=8)
        self.gowait.start(20)
        
        # Indicate start of execution
        self.execute = True
        
        # Disable all configuration part
        disable_elemens(self)

        # Affect all parameters
        args = self.args
        args.input = self.input.get()
        args.output = self.output.get()
        args.nb_bc = int(self.max.get())
        # Take value of validation file only activate validation
        if self.validation.get():
            args.valid = self.valid.get()
        else:
            args.valid = None
        args.csv = self.csv.get() == 1
        args.barcode = self.barcode.get() == 1
        args.prefix = self.pref.get() == 1
        args.suffix = self.suf.get() == 1
        

        # send all parameters
        self.send_pipe.send(args)

        logging.debug("OUT")

    def maj(self):
        """!@brief
            Manage activation of identification file
            Verify if execution finished
        """
        self.update()

        if self.execute == False:
            self.verify_all_disable()
            self.advise()
        else:
            # verify if execution sent the result
            if self.recv_pipe.poll(0.01) is True:
                logging.info("it captured end execution")
                # take result of execute
                val = self.recv_pipe.recv()
                # show the result
                if val[0] == "Done":
                    showinfo(val[0], val[1])
                else:
                    showerror(val[0], val[1])
                # Put interface in configuration state
                self.finish_execute()

        # restart in 20ms the verification
        self.after(20, self.maj)
            

    def finish_execute(self):
        """!@brief
            Put interface in configuration state
        """
        logging.debug("IN")

        # Delete ProgressBar
        self.gowait.destroy()
        # Put GO Button
        self.gowait = ttk.Button(self.launch, text="GO",
                                 command=self.star_execute)
        self.gowait.grid(column=4, row=18, columnspan=2)
        self.update()
        # Enable all configuration part
        enable_elemens(self)
        self.change_valid()
        
        # Indicate end of execution
        self.execute = False

        logging.debug("OUT")

    def close(self):
        """!@brief
            close application
        """
        logging.debug("IN")

        # Ask confirmation
        if askyesno("Quit", "Do you really wish to quit?"):
            # Kill the execution if it is running
            if hasattr(self, "thread"):
                if self.thread.isAlive():
                    self.thread._Thread__stop()
            # Close all
            self.destroy()

        logging.debug("OUT")

    def verify_all_disable(self):
        """!@brief
            disable GO button if not output type selected
        """
        if (self.csv.get() == 0 and
            self.barcode.get() == 0 and
            self.pref.get() == 0 and 
            self.suf.get() == 0):

            disable_elemens(self.launch)
        else:
            enable_elemens(self.launch)


