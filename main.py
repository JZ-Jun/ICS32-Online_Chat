# main.py
#
# Tkinter Program used to create a GUI for ICS 32 Direct Messenger
# Final Project
#
# Authors: Carlos Lim, Jun Zhu
# 17 March 2021

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ds_messenger import *


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, directMessenger=None):
        """
        Constructs all the necessary attributes for Body object.

        :param root: tk.Menu
        :param directMessenger: DirectMessenger object created by MainApp
        :type root: tk.main.root
        :type directMessenger: DirectMessenger object
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.directMessenger = directMessenger
        #determines if there is a sender (uses to send message)
        self.sender = None
        #retrieves all the messages
        self.messages = self.directMessenger.retrieve_all()
        #list of users to populate the tree
        self._users = []
        self._draw()
        self.set_users()


    def node_select(self, event) -> None:
        """
        Updates the message_frame with all the messages from self.sender when
        the corresponding node is selected.

        :param event: not used
        """
        #adds new messages received every time a user clicks on another user (kind of like a refresh)
        if self.messages != self.messages + self.directMessenger.retrieve_new():
            self.messages = self.directMessenger.retrieve_all()
            print('retrieving new...')
    
        if self.user_tree.selection():
            #selections are not 0-based, so subtarct one.
            index = int(self.user_tree.selection()[0])-1
            self.sender = self._users[index]
            #empties the main message frame for senders messages (via populate_msg)
            self.reset_main()
            self.populate_msg(self.sender)

    def populate_msg(self, user:str) -> None:
        """
        Populates the messages_frame with all the messages from that user.

        :param user: person clicked on by node_select
        :type user: str
        """
        #adopted from stackoverflow (check README for citation)
        #configures message_frame to 'normal' so we can edit the Text frame
        self.message_frame.configure(state='normal')
        
        for dm1 in self.messages:
            if dm1.get_recipient() == user:
                self.message_frame.insert('end', dm1.get_message() + '\n')
        self.message_frame.configure(state='disabled')


    def reset_main(self) -> None:
        """
        Resets the main_frame for another user's direct messages.
        """
        self.message_frame.configure(state='normal')
        #deletes all the text in the message_frame
        self.message_frame.delete('1.0', 'end')
        self.message_frame.configure(state='disabled')


    def get_text_entry(self) -> str:
        """
        Getter method that returns the text in entry_editor (this is where you send msgs from).

        :return: the text currently displayed in the entry_editor widget
        :rtype: str
        """
        return self.entry_editor.get('1.0', 'end').rstrip()


    def set_text_entry(self, text:str) -> None:
        """
        Sets the text to be displayed in teh entry_editor widget

        :param text: string of entry
        :type text: str

        .. note:: This method is usefull for clearing the widget
        """
        self.entry_editor.delete('1.0', 'end')
        self.entry_editor.insert('1.0', text)


    def set_users(self) -> None:
        """
        Sets the user into the user_tree.
        """
        for dm in self.messages:
            if dm.get_recipient() not in self._users:
                self.insert_user(dm.get_recipient())


    def insert_user(self, user:str) -> None:
        """
        Inserts the user into the user_tree.

        :param user: individual recipient received from set_user
        :type user: str
        """
        self._users.append(user)
        self._insert_user_tree(len(self._users), user)

        
    def _insert_user_tree(self, id, user:str) -> None:
        """
        Inserts a user into the user_tree widget.

        :param id: length of ._users list (for next insert)
        :param user: individual recipient received from insert_user
        :type user: str
        :type id: int
        """
        shortenName = user
        #shortens the name if the name length is too long
        if len(shortenName) > 25:
            shortenName = user[:24] + "..."

        self.user_tree.insert('', id, id, text=shortenName)


    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame.
        """
        users_frame = tk.Frame(master=self, width=250)
        users_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        #Tree widget
        self.user_tree = ttk.Treeview(users_frame)
        self.user_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.user_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        #main widget
        main_frame = tk.Frame(master=self, bg="white")
        main_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        #message frame for all the messages received from certain user (based on node_select)
        self.message_frame = tk.Text(main_frame, width=0, state='disabled')
        self.message_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        editor_frame = tk.Frame(master=self, bg="", height=100)
        editor_frame.pack_propagate(0)
        editor_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        #for the editing frame
        scroll_frame = tk.Frame(master=editor_frame, bg="", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        #for message frame
        scroll_frame2 = tk.Frame(master=main_frame, bg="", width=10)
        scroll_frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)
        # frame for writing messages to send to node_selected user
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        message_scrollbar = tk.Scrollbar(master=scroll_frame2, command=self.message_frame.yview)
        self.message_frame['yscrollcommand'] = message_scrollbar.set
        message_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
    

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the foorer portion of the root frame.
    """
    def __init__(self, root, addUser_callback=None, send_callback=None):
        """
        Constructs all the necessary attributes for Footer object.

        :param root: master root from MainApp
        :param addUser_callback: Calls the callback function specified in addUser_callback
        :param send_callback: Calls the callback function specified in send_callback
        :type root: tk.Menu
        :type addUser_callback: function
        :type send_callback: function
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._addUser_callback = addUser_callback
        self._send_callback = send_callback
        #packs widgets into the Footer instance
        self._draw()


    def add_click(self) -> None:
        """
        Calls the callback function specified in add_click class attribute, if
        available, when add user button has been clicked.
        """
        if self._addUser_callback is not None:
            self._addUser_callback()


    def send_click(self) -> None:
        """
        Calls the callback function specified in the send_click attribute, if
        available, when the send button has been clicked.
        """
        if self._send_callback is not None:
            self._send_callback()


    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame.
        """
        #send button
        send_button = tk.Button(master=self, text="Send", width=10)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        #add user button
        self.new_user = tk.Button(master=self, text="Add User", width=10)
        self.new_user.configure(command=self.add_click)
        self.new_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)


class popupWindow:
    """
    The popupWindow class generates a Toplevel pop-up window that allows
    users to add new people to direct message.
    """
    #adopted from stackoverflow (check README for citation)
    def __init__(self, root):
        """
        Constructs all the necessary attributes for popupWindow object

        :param root: master root from MainApp
        :type root: tk.main.root
        """
        window = self.window = tk.Toplevel(root)
        self.l = tk.Label(window, text="Add User")
        self.l.pack()
        #entry allows people to enter new user
        self.e = tk.Entry(window)
        self.e.pack()
        self.b = tk.Button(window, text="Ok", command=self.cleanup)
        self.b.pack()
        self.value = None


    def cleanup(self) -> None:
        """
        Destroy's popupWindow once the person clicks "Ok"
        """
        if self.e is not None:
            self.value = self.e.get()
        self.window.destroy()
        

class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all the method calls
    for DirectMessenger class.
    """
    def __init__(self, root):
        """
        :param root: master root for MainApp
        :type root: tk.main.root
        """
        tk.Frame.__init__(self, root)
        self.root = root
        #ensure that person is able to connect before packing (drawing all the widgets)
        try:
            self.dm = DirectMessenger('168.235.86.101', 'abigail9009', '123')
            self._draw()
        except DSUProtocolError as dse:
            print('sorry mate, looks like ya broke it :)')
            self._errorMessage() #pop-up window telling user the error from server.
        except Exception as e:
            print(e)


    def add_user(self) -> None:
        """
        Adds users to the window. This is triggered by clicking the "Add user" button
        on the GUI.
        """
        #popup is prompted
        self.w = popupWindow(self.root)
        self.footer.new_user.configure(state='disabled')
        self.root.wait_window(self.w.window)
        self.footer.new_user.configure(state='normal')

        if self.w.value is not None and self.w.value !="":
            self.body.insert_user(self.w.value)

        
    def send_message(self) -> None:
        """
        Sends message to the server (received from self.body.entry_editor).
        """
        if self.body.sender is not None: #makes sure a node is selected (recipient)
            message = self.body.get_text_entry()
            if message != "": #checks if user put something into the entry_editor
                if not self.dm.send(message, self.body.sender):
                    self._errorMessage() #pop-up window telling user the error from server.
            

    def _errorMessage(self) -> None:
        """
        Generates a messagebox form the server telling user the error that occured.
        """
        messagebox.showinfo(title='Heads up', message=self.dm.resp_msg["response"]["message"])
            

    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame.
        """
        #The Body and Footer classes must be initialized and packed into root window.
        self.body = Body(self.root, self.dm)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, addUser_callback=self.add_user, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # Root window and title
    main = tk.Tk()
    main.title("ICS 32 Messenger")

    # Starting default size
    main.geometry("600x500")
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)
    main.update()

    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()
