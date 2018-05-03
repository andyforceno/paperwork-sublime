#! /usr/bin/python3
# -*- coding: utf-8 -*-#
import sublime, sublime_plugin
import json, urllib.request, http.client, re, sys
from urllib.request import Request, urlopen
from base64 import b64encode

global settings
settings = sublime.load_settings('paperwork.sublime-settings')
settings.add_on_change('reload', sublime.load_settings('paperwork.sublime-settings'))

class ShowNotePanelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        notebooklist = paper.list_notebooks()
        sublime.active_window().show_quick_panel(sorted(notebooklist), self.notes_panel)

    def notes_panel(self, index):
        if index == -1:
                return

        notebooklist = sorted(paper.list_notebooks())
        notebooktitle = notebooklist[index]
        ShowNotePanelCommand.notebookid = paper.notebook_to_id(notebooktitle)
        self.notelist = paper.list_notes(self.notebookid)
        sublime.active_window().show_quick_panel(sorted(self.notelist), self.run_open)

    def run_open(self, index):
        if index == -1:
                return

        notelist = sorted(paper.list_notes(self.notebookid))
        ShowNotePanelCommand.notetitle = notelist[index]
        noteid = paper.note_to_id(self.notetitle)
        self.view.run_command("open_note")

class OpenNoteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        notelist = sorted(paper.list_notes(ShowNotePanelCommand.notebookid))
        noteid = paper.note_to_id(ShowNotePanelCommand.notetitle)
        note = paper.get_note(ShowNotePanelCommand.notebookid, noteid)
        note = paper.html2text(note)
        self.view = sublime.active_window().new_file()
        notetitle = paper.get_note_title(ShowNotePanelCommand.notebookid, noteid)
        self.view.set_name(notetitle)
        self.view.insert(edit, self.view.sel()[0].begin(), note)

class SaveExistingNoteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        notebooklist = paper.list_notebooks()
        panel_save = settings.get("panel_save", "no")
        # Autosave setting in Paperwork-sublime.settings
        if panel_save == "yes":
            sublime.active_window().show_quick_panel(sorted(notebooklist), self.notes_panel)
        else:
            self.autosave_note()

    def notes_panel(self, index):
        if index == -1:
                return

        notebooklist = sorted(paper.list_notebooks())
        notebooktitle = notebooklist[index]
        ShowNotePanelCommand.notebookid = paper.notebook_to_id(notebooktitle)
        self.notelist = paper.list_notes(ShowNotePanelCommand.notebookid)
        sublime.active_window().show_quick_panel(sorted(self.notelist), self.run_save)

    def run_save(self, index):
        notelist = sorted(paper.list_notes(ShowNotePanelCommand.notebookid))
        ShowNotePanelCommand.notetitle = notelist[index]
        self.view.run_command("save_existing")

    def autosave_note(self):
        notetitle = self.view.name()
        notebookid, noteid = paper.search_notes(notetitle)
        self.note = self.view.substr(sublime.Region(0, self.view.size()))
        content_preview = self.note[:40]
        self.note = paper.text2html(self.note)
        content_preview = paper.text2html(content_preview)

        try:
            editnote = paper.edit_note(notebookid, noteid, notetitle, self.note, content_preview)
            print(editnote)
        except:
            print("An error occured. Unable to save existing note.")
        else:
            print("Successfully saved existing note!")

class SaveExisting(sublime_plugin.TextCommand):
    def run(self, edit):
        noteid = paper.note_to_id(ShowNotePanelCommand.notetitle)
        notetitle = self.view.name()
        self.note = self.view.substr(sublime.Region(0, self.view.size()))
        content_preview = self.note[:40]
        self.note = paper.text2html(self.note)
        content_preview = paper.text2html(content_preview)

        if ShowNotePanelCommand.notetitle == notetitle:
            try:
                editnote = paper.edit_note(ShowNotePanelCommand.notebookid, noteid, notetitle, self.note, content_preview)
                print(editnote)
            except:
                print("An errror occured. Unable to save existing note.")
            else:
                print("Successfully saved existing note!")
        else:
            print("Note title mismatch! Save aborted.")

class SaveNewNoteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.notebooklist = paper.list_notebooks()
        # Display list of notebooks
        sublime.active_window().show_quick_panel(sorted(self.notebooklist), self.input_title)

    def input_title(self, index):
        if index == -1:
                return

        notebooklist = sorted(paper.list_notebooks())
        notebooktitle = notebooklist[index]
        self.notebookid = paper.notebook_to_id(notebooktitle)
        caption = "Enter a title for this note: "
        initial = ""
        self.view.window().show_input_panel(caption, initial, self.save_new_note, None, None)

    def save_new_note(self, notetitle):
        self.note = self.view.substr(sublime.Region(0, self.view.size()))
        content_preview = self.note[:40]
        self.note = paper.text2html(self.note)
        content_preview = paper.text2html(content_preview)
        try:
            postnote = paper.create_note(self.notebookid, notetitle, self.note, self.note[:40])
            print(postnote)
        except:
            print("An error occured. Unable to save new note")

class PaperworkAPI(object):
    def get_request(self):
        """ GET request template for gettinG
            notes and notebooks
        """
        username = settings.get("username", "")
        password = settings.get("password", "")
        authstring="%s:%s" % (username, password)
        auth = b64encode(authstring.encode()).decode("ascii")

        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic %s' % auth
        }

        request = urllib.request.Request(self.endpoint, headers=headers)
        json_response = json.loads(urlopen(request).read().decode())
        response = json_response['response']
        return response

    def post_request(self):
        """ POST request template for creating, editing,
            deleting of notes & notebooks
        """
        username = settings.get("username", "")
        password = settings.get("password", "")
        authstring="%s:%s" % (username, password)
        auth = b64encode(authstring.encode()).decode("ascii")

        headers = {
                  'Content-Type': 'application/json',
                  'Authorization': 'Basic %s' % auth
                }

        body = self.body.encode('utf-8')
        request = urllib.request.Request(self.endpoint, data=body, headers=headers)
        if self.putreq == 1:
            request.get_method = lambda: 'PUT'
        try:
            json_response = json.loads(urlopen(request).read().decode())
            response = json_response['response']
            return response
        except urllib.error.HTTPError as err:
            if err.code == 400:
                print("Error 400 - Bad request")
            elif err.code == 404:
                print("Error 404 - Note or notebook ID not found")
            elif err.code == 500:
                print("Error 500 - Server did not understand API request")
            else:
                raise

    def list_notebooks(self):
        """ Returns all notebook titles
        """
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks" % (protocol, domain)
        response = self.get_request()
        # Print title of each notebook
        self.notebook_titles = [response[x]['title'] for x in range(0,(len(response)-1))]
        self.notebook_ids = [response[x]['id'] for x in range(0,(len(response)-1))]
        return self.notebook_titles

    def list_notes(self, notebookid):
        """ Display note titles from a given notebook
        """
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks/%s/notes/" % (protocol, domain, notebookid)
        response = self.get_request()
        # Print title of every note in notebookid
        self.note_titles = []
        self.note_ids = []
        self.note_titles = [response[x]['version']['title'] for x in range(0,(len(response)-1))]
        self.notebook_ids = [response[x]['notebook_id'] for x in range(0,(len(response)-1))]
        self.note_ids = [response[x]['id'] for x in range(0,(len(response)-1))]
        return self.note_titles

    def get_note(self, notebookid, noteid):
        """ Display a note's content given a notebookid and noteid
        """
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks/%s/notes/%s" % (protocol, domain, notebookid, noteid)
        response = self.get_request()
        # Get content of note
        note = response['version']['content']
        self.notebookid = response['notebook_id']
        return note

    def get_note_title(self, notebookid, noteid):
        """ Display a note's content given a noteid
        """
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks/%s/notes/%s" % (protocol, domain, notebookid, noteid)
        response = self.get_request()
        # Print title of every note in notebookid
        notetitle = response['version']['title']
        return notetitle

    ##
    ## POST & PUT requests
    def create_note(self, notebookid, title, content, content_preview):
        """ Save a new note by supplying notebookid,
            title, content, and content_preview
        """
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.body = """ { "title": "%s", "content": "%s", "content_preview": "%s" } """ % (title, content, content_preview)
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks/%s/notes/" % (protocol, domain, notebookid)
        self.putreq = 0
        response = self.post_request()
        return response

    def edit_note(self, notebookid, noteid, title, content, content_preview):
        """ Save an existing note by supplying notebookid,
            noteid, content, and content_preview
        """
        self.putreq = 1
        protocol = settings.get("protocol", "https")
        domain = settings.get("domain", "")
        self.body = """ { "title": "%s", "content": "%s", "content_preview": "%s" } """ % (title, content, content_preview)
        self.endpoint = "%s://%s/paperwork/api/v1/notebooks/%s/notes/%s" % (protocol, domain, notebookid, noteid)
        response = self.post_request()
        return response

    ##
    ## Utility functions
    def notebook_to_id(self, title):
        """ Returns the notebookid of a notebook title
            Use list_notebooks() to get notebook_titles
        """
        titleindex = self.notebook_titles.index(title)
        notebookid = self.notebook_ids[titleindex]
        return notebookid

    def note_to_id(self, title):
        """ Returns the noteid of a note title
            Use list_notes() to get note_titles
        """
        titleindex = self.note_titles.index(title)
        noteid = self.note_ids[titleindex]
        return noteid

    def search_notes(self, notetitle):
        """ Search All Notes notebook for notetitle
            Returns corresponding notebookid and noteid
        """
        # All Notes notebook
        notebookid = '00000000-0000-0000-0000-000000000000'
        notelist = self.list_notes(notebookid)
        noteid = self.note_to_id(notetitle)
        titleindex = self.note_titles.index(notetitle)
        notebookid = self.notebook_ids[titleindex]

        return notebookid, noteid

    def text2html(self, note):
       """ Convert plain text from an ST3 file view,
           Returns HTML formatted for Paperwork
       """
       note = re.sub('&','&amp;', note)
       # Substitute < and > before adding html tags
       note = re.sub('<','&lt;', note)
       note = re.sub('>','&gt;', note)
       # Add paragraph tags around paragraphs
       # From: https://www.djangosnippets.org/snippets/143/
       note = re.split(r'[\r\n]+', note)
       note = ['<p>%s</p>' % p.strip() for p in note]
       note = '\n'.join(note)
       # Formatting to match original from Paperwork
       note = re.sub('<p>','<p><br/>', note)
       note = re.sub('\n', '', note)
       note = re.sub('"', '&quot;', note)
       return note

    def html2text(self, note):
        """ Strips HTML from response body,
            Returns plaintext
        """
        note = re.sub('</p>','\n\n', note)
        note = re.sub('<p>','', note)
        note = re.sub('<br/>','', note)
        note = re.sub('&amp;','&', note)
        note = re.sub('&lt;','<', note)
        note = re.sub('&gt;','>', note)
        note = re.sub('<p dir="ltr">','', note)
        note = re.sub('<br clear="none">', '\n', note)
        note = re.sub('</div><div>', '\n', note)
        note = re.sub('&quot;', '"', note)
        return note

paper = PaperworkAPI()

# Main
if __name__ == '__main__':
    paper = PaperworkAPI()