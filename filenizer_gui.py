#!/usr/bin/python
#
# Copyright (C) 2017 Łukasz Kopacz
#
# This file is part of Filenizer.
#
# Filenizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Filenizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Filenizer. If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.1"

import tkinter
from tkinter import filedialog
import sys
import subprocess
import os
import webbrowser
import filenizer
from tkinter import ttk
import data_file


class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)

        self.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        self.master.title('Filenizer')

        self.create_menu_bar()

        # variables
        self.tv_input = None  # text variable for input folder
        self.tv_output = None  # text variable for output folder
        self.recursive_output = None  # boolean variable for recursive setting
        self.tv_title = None  # text variable for title setting
        self.text_ignored_folders = None  # text field for ignored folders
        self.text_ignored_files = None  # text field for ignored files
        self.label_info = None  # label for user output
        self.frame_replace_in_text_list = None  # frame for replace input entry list
        self.frame_replace_out_text_list = None  # frame for replace output entry list
        self.replace_inout = []  # list for values of in/out replace entries

        self.create_widgets()

    def create_menu_bar(self):
        menu_bar = tkinter.Menu(self)

        menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Quit", command=self.master.quit)

        menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=menu)
        menu.add_command(label="Help", command=self.help)
        menu.add_command(label="About", comman=self.about)

        self.master.config(menu=menu_bar)

    def create_widgets(self):
        # todo icon
        # img_icon = tkinter.PhotoImage(data=data_file.icon)
        # root.tk.call('wm', 'iconphoto', root._w, img_icon)

        # input
        frame_input = tkinter.Frame(self)
        frame_input.pack(fill=tkinter.X, expand=False, padx=5, pady=5)

        button_input = tkinter.Button(frame_input, text="Input directory:", command=self.action_input)
        button_input.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        self.tv_input = tkinter.StringVar()
        entry_input = tkinter.Entry(frame_input, textvariable=self.tv_input)
        entry_input.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)
        self.tv_input.set(os.getcwd())

        # output
        frame_output = tkinter.Frame(self)
        frame_output.pack(fill=tkinter.X, expand=False, padx=5, pady=5)

        button_output = tkinter.Button(frame_output, text="Output directory:", command=self.action_output)
        button_output.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        self.tv_output = tkinter.StringVar()
        entry_output = tkinter.Entry(frame_output, textvariable=self.tv_output)
        entry_output.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)
        self.tv_output.set(os.path.join(os.getcwd(), 'output'))

        # settings
        frame_settings = tkinter.LabelFrame(self, text='Settings')
        frame_settings.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        tabs_settings = ttk.Notebook(frame_settings)
        tab_general = ttk.Frame(tabs_settings)  # general tab
        tabs_settings.add(tab_general, text='General')
        tab_ignore = ttk.Frame(tabs_settings)  # ignored folders tab
        tabs_settings.add(tab_ignore, text='Ignored folders')
        tab_ignore_files = ttk.Frame(tabs_settings)  # ignored files tab
        tabs_settings.add(tab_ignore_files, text='Ignored files')
        tab_replace = ttk.Frame(tabs_settings)  # replace string tab
        tabs_settings.add(tab_replace, text='Replace string')
        tabs_settings.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        # settings - general tab
        # settings - general tab - recursive check button
        self.recursive_output = tkinter.BooleanVar()
        check_recursive = tkinter.Checkbutton(tab_general, text="Recursive output", variable=self.recursive_output)
        check_recursive.pack(fill=tkinter.X, expand=False, padx=5, pady=5)

        # settings - general tab - title
        frame_title = tkinter.Frame(tab_general)
        frame_title.pack(fill=tkinter.X, expand=False, padx=5, pady=5)

        label_title = tkinter.Label(frame_title, text="Title: ")
        label_title.pack(fill=tkinter.X, expand=False, side=tkinter.LEFT, padx=5, pady=5)

        self.tv_title = tkinter.StringVar()
        entry_title = tkinter.Entry(frame_title, textvariable=self.tv_title)
        entry_title.pack(fill=tkinter.X, expand=True, side=tkinter.LEFT, padx=5, pady=5)

        # settings - ignored folders tab
        scrollbar_ignored_folders = tkinter.Scrollbar(tab_ignore)

        self.text_ignored_folders = tkinter.Text(tab_ignore, height=2, width=60)
        self.text_ignored_folders.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True, padx=5, pady=5)

        scrollbar_ignored_folders.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_ignored_folders.config(command=self.text_ignored_folders.yview)

        self.text_ignored_folders.config(yscrollcommand=scrollbar_ignored_folders.set)

        # settings - ignored files tab
        scrollbar_ignored_files = tkinter.Scrollbar(tab_ignore_files)

        self.text_ignored_files = tkinter.Text(tab_ignore_files, height=2, width=60)
        self.text_ignored_files.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True, padx=5, pady=5)

        scrollbar_ignored_files.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_ignored_files.config(command=self.text_ignored_files.yview)

        self.text_ignored_files.config(yscrollcommand=scrollbar_ignored_files.set)

        # settings - replace string

        frame_replace = VerticalScrolledFrame(tab_replace)
        frame_replace.pack(fill=tkinter.BOTH, expand=True, side=tkinter.TOP, padx=5, pady=5)

        # settings - replace string - input
        frame_replace_inout = tkinter.Frame(frame_replace.interior)
        frame_replace_inout.pack(fill=tkinter.X, expand=True, side=tkinter.TOP, padx=5, pady=5)

        frame_replace_in = tkinter.Frame(frame_replace_inout)
        frame_replace_in.pack(fill=tkinter.X, expand=True, side=tkinter.LEFT, padx=5, pady=5)
        frame_replace_out = tkinter.Frame(frame_replace_inout)
        frame_replace_out.pack(fill=tkinter.X, expand=True, side=tkinter.LEFT, padx=5, pady=5)

        label_replace_input = tkinter.Label(frame_replace_in, text="Replace:")
        label_replace_input.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        label_replace_input = tkinter.Label(frame_replace_out, text="with:")
        label_replace_input.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        self.frame_replace_in_text_list = tkinter.Frame(frame_replace_in)
        self.frame_replace_in_text_list.pack(fill=tkinter.X, expand=True, side=tkinter.RIGHT, padx=5, pady=5)
        self.frame_replace_out_text_list = tkinter.Frame(frame_replace_out)
        self.frame_replace_out_text_list.pack(fill=tkinter.X, expand=True, side=tkinter.RIGHT, padx=5, pady=5)

        self.add_replace_inout()

        # settings - replace string - buttons
        frame_more_less = tkinter.Frame(frame_replace.interior)
        frame_more_less.pack(fill=tkinter.X, expand=True, side=tkinter.RIGHT, padx=5, pady=5)

        button_more = tkinter.Button(frame_more_less, text="+", command=self.add_replace_inout)
        button_more.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True, padx=5, pady=5)
        button_less = tkinter.Button(frame_more_less, text="-", command=self.remove_replace_inout)
        button_less.pack(fill=tkinter.BOTH, side=tkinter.LEFT, expand=True, padx=5, pady=5)

        # start
        frame_start = tkinter.Frame(self)
        frame_start.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        self.label_info = tkinter.Label(frame_start, text="Ready.")
        self.label_info.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True, padx=5, pady=5)

        start_button = tkinter.Button(frame_start, text="Start", command=self.action_start)
        start_button.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True, padx=5, pady=5)

    def action_start(self):
        try:
            replace_transform = ("{}:{}".format(self.replace_inout[0][0].get(), self.replace_inout[0][1].get()))
            for (a, b) in self.replace_inout[1:]:
                replace_transform = ("{},{}:{}".format(replace_transform, a.get(), b.get()))
        except IndexError:
            replace_transform = None
            
        par = {'input': self.tv_input.get(),
               'output': self.tv_output.get(),
               'ignore': self.ignore(self.text_ignored_folders.get('1.0', tkinter.END).splitlines()),
               'ignore_file': self.ignore(self.text_ignored_files.get('1.0', tkinter.END).splitlines()),
               'recursive': self.recursive_output.get(),
               'replace_string': replace_transform,
               'title': self.tv_title.get()}
        self.label_info['text'] = filenizer.modifynizer(par)

    def add_replace_inout(self):
        entry_in = tkinter.Entry(self.frame_replace_in_text_list)
        entry_in.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        entry_out = tkinter.Entry(self.frame_replace_out_text_list)
        entry_out.pack(fill=tkinter.X, side=tkinter.TOP, padx=5, pady=5)

        self.replace_inout.append((entry_in, entry_out))

    def remove_replace_inout(self):
        try:
            self.frame_replace_in_text_list.pack_slaves()[-1].destroy()
            self.frame_replace_out_text_list.pack_slaves()[-1].destroy()

            self.replace_inout.pop()
        except IndexError:
            pass

    @staticmethod
    def ignore(ign_list):
        ign_s = ign_list[0]
        for ign in ign_list[1:]:
            ign_s += (',{}'.format(ign))
        return ign_s

    def action_input(self):
        directory = self.choose_dir()
        if directory:
            self.tv_input.set(directory)

    def action_output(self):
        directory = self.choose_dir()
        if directory:
            self.tv_output.set(directory)

    @staticmethod
    def choose_dir():
        input_dir = tkinter.filedialog.askdirectory(initialdir=".", title='Select a directory')
        if len(input_dir) > 0:
            return input_dir

    # todo opening file browser
    def open_file_browser(self):
        d = os.path.split(self.res_file)[0]
        if sys.platform == 'win32':
            #subprocess.Popen(['start', d], shell=True)
            os.startfile(d)

        elif sys.platform == 'darwin':
            subprocess.Popen(['open', d])

        else:
            try:
                subprocess.Popen(['xdg-open', d])
            except OSError:
                pass

    # todo help
    def help(self):
        pass
        """"
        top_help = tkinter.Toplevel(self)
        top_help.wm_title('Help')
        top_help.geometry("800x650")

        self.label_help_text = tkinter.Label(top_help, text=data_file.img_description[0])
        self.label_help_text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        self.label_help_text.config(font='-size 14')

        button_exit_help = tkinter.Button(top_help, text='Close', command=top_help.destroy)
        button_exit_help.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=5, pady=5)
        """

    def about(self):
        top_about = tkinter.Toplevel(self)
        top_about.wm_title('About')

        # todo icon
        #img_icon = tkinter.PhotoImage(data=data_file.icon)
        #top_about.tk.call('wm', 'iconphoto', top_about._w, img_icon)

        text_about_text = ('Filenizer\n Version {}\n\n '
                           'License\nGNU General Public License v3.0'
                           .format(__version__))

        label_help_text = tkinter.Label(top_about, text=text_about_text)
        label_help_text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        link_github = 'https://github.com/spasiva/filenizer'
        link_src = tkinter.Label(top_about, text='Source', fg="blue", cursor="hand2")
        link_src.pack()
        link_src.bind("<Button-1>", self.click_link(link_github))

        label_help_text2 = tkinter.Label(top_about, text='Copyright © 2017 Łukasz Kopacz')
        label_help_text2.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        button_license = tkinter.Button(top_about, text='License', command=self.license)
        button_license.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=5, pady=5)

        button_exit_about = tkinter.Button(top_about, text='Close', command=top_about.destroy)
        button_exit_about.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=5, pady=5)

    def license(self):
        top_license = tkinter.Toplevel(self)
        top_license.wm_title('License')
        #top_license.geometry("400x400")

        # todo icon
        #img_icon = tkinter.PhotoImage(data=data_file.icon)
        #top_license.tk.call('wm', 'iconphoto', top_license._w, img_icon)

        frame_license = tkinter.Frame(top_license)

        scrollbar_license = tkinter.Scrollbar(frame_license)

        text_license = tkinter.Text(frame_license, height=20, width=52)
        text_license.pack(fill=tkinter.Y, side=tkinter.LEFT, expand=True, padx=5, pady=5)

        scrollbar_license.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_license.config(command=text_license.yview)

        # todo display link if data file not found
        text_license.insert(tkinter.END, data_file.license_txt)
        text_license.config(state=tkinter.DISABLED, yscrollcommand=scrollbar_license.set)

        frame_license.pack(expand=True, fill=tkinter.BOTH)
        button_exit_license = tkinter.Button(top_license, text='Close', command=top_license.destroy)
        button_exit_license.pack(fill=tkinter.X, side=tkinter.BOTTOM, padx=5, pady=5)

    def click_link(self, addr):
        def click(self):
            webbrowser.open_new_tab(r"{}".format(addr))
        return click


class VerticalScrolledFrame(tkinter.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        tkinter.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        vscrollbar.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=tkinter.FALSE)
        canvas = tkinter.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tkinter.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tkinter.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


root = tkinter.Tk()
root.geometry("600x600")

app = Application(root)

app.mainloop()
