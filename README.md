Carlos Lim & Jun Zhu\
Team: Chris P Bacon\
ICS 32 Baldwin\
17 March, 2021


Our main entry point [GUI code] is main.py
---------------------------------------------

> The additional class is popupWindow inside the main.py\
> The custom exception is DSUProtocolError inside ds_messenger.py\
> We ARE NOT using encryption (port 3021)

*Note* you can edit the user on line 296 in main.py\
*Note* if you are sending a message to yourself, click the node on the tree to refresh

Work Cited
----------
"Is there a way to make the Tkinter text widget read only?"
> We used the second answer by renzowesterbeek\
> allowed us to disable editing of the messages frame (text box really)\
> used in lines 61-85 in main.py\
> link: https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only

"Creating a popup message box with an Entry field"
> We used the first answer by mgilson\
> allowed us to create a pop-up window for inputting a new user\
> used in lines 248-278 in main.py\
> link: https://stackoverflow.com/questions/10020885/creating-a-popup-message-box-with-an-entry-field
