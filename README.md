# paperwork-sublime
A plugin for Sublime Text 3 that allows you to create and edit notes on your Paperwork (https://github.com/twostairs/paperwork) note-taking app.

Paperwork for Sublime Text 3 allows you to open and save Paperwork notes via commands in the command palette. Lists of notebooks and notes are displayed in a quick panel.

This works best with notes that are plain text. There is only basic parsing of HTML to convert some formatting tags. 
I'm in the process of improving the HTML parsing, currently it has some flaws due to bad HTML code in the notes.

UPDATE (09-17-20): I am no longer maintaining this, as I no longer use Paperwork. I've found that using Syncthing with Sublime Text on my desktop and the Jotterpad app on my Android phone provides the same functionality I was seeking with Paperwork, and it's far easier to setup, with absolutely nothing in the way of maintenance. I am keeping this here for archival purposes. I found this project very helpful in learning how to create plugins for Sublime Text, so perhaps you will, too.


### To use:
1. Copy the paperwork folder to your ST3-config-folder/Packages/
2. Edit `paperwork.sublime-settings` to fill in your `username`, `password`, `domain`, specify `http` or `https` for `protocol`, and `yes` or `no` for `panel_save`
3. Copy `paperwork.sublime-settings` to ST3-config-folder/Packages/User/
4. Open the command palette in Sublime Text 3 and enter `paperwork` to see the menu options

I recommend saving a new note and editing it a few times, comparing it to what you see on the Android app or the web interface, before editing and saving an existing note.

Menu options: `Open Note`, `Save New Note`, `Save Existing Note`, `Delete Note`. 

`Save New Note` will prompt you to enter a note title. 
The newly-saved note will reload in the current view so you can continue editing without having to reload the note yourself.

`Save Existing Note` will search for the note and save it to the correct notebook, by default. 
If you have a large number of notes and notebooks and/or the server is remote, this may be slow. 
To disable this and use the quick panel menu to select a note instead, set `panel_save` to `yes` in `paperwork.sublime-settings`
With `panel_save` set to `yes`, `Save Existing Note` will only save the note if the title of the note to be saved matches the title of the note selected. 

`Delete Note` will allow you to select a note to delete using quick panels. You will be asked to confirm before the note is deleted.

See the console for errors. You will see confirmation and an API response if save or delete was successful.

### What's new:

- Fixed some bugs when saving from the quick panel and via shortcut keys
- All saved notes will reload in the current view so you can continue editing!
- Keyboard shortcuts: `Alt+Shift+n: Save New Note`, `Alt+Shift+s: Save Existing Note`, `Alt+Shift+o: Open Note`
- Delete notes! New `Delete Note` command palette menu item allows you to select a note to delete (will confirm before deleting)
- Compressed API responses for 50% faster listing and saving of notes and notebooks!
- ~~Newly-saved notes will reload in the current view so you can keep editing without reloading the note yourself.~~
