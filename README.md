# paperwork-sublime
A plugin for Sublime Text 3 that allows you to create and edit notes on your Paperwork note-taking app

Paperwork for Sublime Text 3 allows you to open and save Paperwork notes via commands in the command palette. Lists of notebooks and notes are displayed in a quick panel.

This works best with notes that are plain text. There is only basic parsing of HTML to convert some formatting tags (and ST3's Python doesn't include html2text).

This is potentially buggy. It works well enough for me to use, but I make no guarantees that it won't crash. I have some safeguards in place so you (probably) won't overwrite the wrong note. 

To use:
Copy paperwork.py, Default.sublime-commands, and paperwork.sublime-settings your ST3-config-folder/Packages/User/
Edit paperwork.sublime-settings to fill in your username, password, domain, and specify http or https.
Open the command palette in Sublime Text 3 and enter 'paperwork' to see the menu options.
See the console for errors and confirmation of successful saves
