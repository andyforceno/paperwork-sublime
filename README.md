# paperwork-sublime
A plugin for Sublime Text 3 that allows you to create and edit notes on your Paperwork (https://github.com/twostairs/paperwork) note-taking app.

Paperwork for Sublime Text 3 allows you to open and save Paperwork notes via commands in the command palette. Lists of notebooks and notes are displayed in a quick panel.

This works best with notes that are plain text. There is only basic parsing of HTML to convert some formatting tags (and ST3's Python doesn't include html2text).

### To use:
1. Copy paperwork.py, Default.sublime-commands, and paperwork.sublime-settings your ST3-config-folder/Packages/User/
2. Edit paperwork.sublime-settings to fill in your username, password, domain, specify http or https for protocol, and yes or no for panel_save
3. Open the command palette in Sublime Text 3 and enter 'paperwork' to see the menu options

I recommend saving a new note and editing it a few times, comparing it to what you see on the Android app or the web interface, before editing and saving an existing note.

Menu options: `Open Note`, `Save New Note`, and `Save Existing Note`. 

`Save New Note` will prompt you to enter a note title.

`Save Existing Note` will search for the note and save it to the correct notebook, by default. If you have a large number of notes and notebooks, this will be slow. It may also be buggy, sometimes failing to save. To disable this and use the quick panel menu to select a note instead, set `panel_save` to `yes` in `Paperwork.sublime-settings`

With `panel_save` set to `yes`, `Save Existing Note` will only save the note if the title of the note to be saved matches the title of the note selected. 

See the console for errors. You will see confirmation and an API response if save was successful.
