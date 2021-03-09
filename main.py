import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ds_messenger import *

#https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only
#https://stackoverflow.com/questions/10020885/creating-a-popup-message-box-with-an-entry-field

class Body(tk.Frame):
    def __init__(self, root, directMessenger=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.directMessenger = directMessenger
        self.sender = None

        self.messages = self.directMessenger.retrieve_all()
        self._users = []
        self._draw()
        self.set_users()


    def node_select(self, event):
        #adds new messages received every time a user clicks on another user (kind of like a refresh)
        if self.messages != self.messages + self.directMessenger.retrieve_new():
            self.messages += self.directMessenger.retrieve_new()
        
        if self.user_tree.selection():
            index = int(self.user_tree.selection()[0])-1
            self.sender = self._users[index]

            self.reset_main()
            self.populate_msg(self.sender)

    def populate_msg(self, user:str):
        """populates the messages_frame with all the messages from that user"""
        self.message_frame.configure(state='normal')
        
        for dm1 in self.messages:
            if dm1.get_recipient() == user:
                self.message_frame.insert('end', dm1.get_message() + '\n')
        self.message_frame.configure(state='disabled')


    def reset_main(self):
        """resets the main_frame for another user's direct messages"""
        self.message_frame.configure(state='normal')
        self.message_frame.delete('1.0', 'end')
        self.message_frame.configure(state='disabled')


    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()


    def set_text_entry(self, text:str):
        self.entry_editor.delete('1.0', 'end')
        self.entry_editor.insert('1.0', text)


    def set_users(self):
        for dm in self.messages:
            if dm.get_recipient() not in self._users:
                self.insert_user(dm.get_recipient())
        print(self._users)


    def insert_user(self, user:str):
        self._users.append(user)
        self._insert_user_tree(len(self._users), user)

        
    def _insert_user_tree(self, id, user:str):
        shortenName = user
        if len(shortenName) > 25:
            shortenName = user[:24] + "..."

        self.user_tree.insert('', id, id, text=shortenName)


    def _draw(self):
        users_frame = tk.Frame(master=self, width=250)
        users_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.user_tree = ttk.Treeview(users_frame)
        self.user_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.user_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        main_frame = tk.Frame(master=self, bg="white")
        main_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

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

        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        message_scrollbar = tk.Scrollbar(master=scroll_frame2, command=self.message_frame.yview)
        self.message_frame['yscrollcommand'] = message_scrollbar.set
        message_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
    

class Footer(tk.Frame):
    def __init__(self, root, addUser_callback=None, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._addUser_callback = addUser_callback
        self._send_callback = send_callback

        self._draw()


    def add_click(self):
        if self._addUser_callback is not None:
            self._addUser_callback()


    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()


    def _draw(self):
        send_button = tk.Button(master=self, text="Send", width=10)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.new_user = tk.Button(master=self, text="Add User", width=10)
        self.new_user.configure(command=self.add_click)
        self.new_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)


class popupWindow:
    def __init__(self, root):
        window = self.window = tk.Toplevel(root)
        self.l = tk.Label(window, text="Add User")
        self.l.pack()
        self.e = tk.Entry(window)
        self.e.pack()
        self.b = tk.Button(window, text="Ok", command=self.cleanup)
        self.b.pack()
        self.value = None

    def cleanup(self):
        if self.e is not None:
            self.value = self.e.get()
        self.window.destroy()
        

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        try:
            self.dm = DirectMessenger('168.235.86.101', 'abigail99999999', '123')
            self._draw()
        except DSUProtocolError as dse:
            print('sorry mate, looks like ya broke it :)')
            self._errorMessage() #pop-up window telling user the error from server


    def add_user(self):
        self.w = popupWindow(self.root)
        self.footer.new_user.configure(state='disabled')
        self.root.wait_window(self.w.window)
        self.footer.new_user.configure(state='normal')

        if self.w.value is not None:
            self.body.insert_user(self.w.value)

        
    def send_message(self) -> None:
        if self.body.sender is not None: #makes sure a node is selected (recipient)
            message = self.body.get_text_entry()
            self.dm.send(message, self.body.sender)


    def _errorMessage(self):
        messagebox.showinfo(title='Heads up', message=self.dm.resp_msg["response"]["message"])
            

    def _draw(self):
        self.body = Body(self.root, self.dm)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, addUser_callback=self.add_user, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Messenger")

    main.geometry("600x500")
    main.option_add('*tearOff', False)

    MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()
