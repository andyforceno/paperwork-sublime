# paperwork-sublime
A plugin for Sublime Text 3 that allows you to create and edit notes on your Paperwork (https://github.com/twostairs/paperwork) note-taking app.

Paperwork for Sublime Text 3 allows you to open and save Paperwork notes via commands in the command palette. Lists of notebooks and notes are displayed in a quick panel.

This works best with notes that are plain text. There is only basic parsing of HTML to convert some formatting tags (and ST3's Python doesn't include html2text).

### To use:
1. Copy paperwork.py, Default.sublime-commands, and paperwork.sublime-settings your ST3-config-folder/Packages/User/  
2. Edit paperwork.sublime-settings to fill in your username, password, domain, and specify http or https.
3. Open the command palette in Sublime Text 3 and enter 'paperwork' to see the menu options

Menu options: Open Note, Save New Note, and Save Existing Note. Save Existing will only save the note if the title of the note to be saved matches the title of the note selected. 
When saving a new note, the note will be uploaded with the first line of text as the title. 

See the console for errors. You will see an API response with the note data if a save was successful.
