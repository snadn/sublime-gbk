#coding: utf8

import sublime, sublime_plugin
import os, re
import urllib

TEMP_PATH = os.path.join(os.getcwd(), 'tmp')
SEPERATOR = '                '
OPEN_WITH_GBK = True

def gbk2utf8(view):
	try:
		reg_all = sublime.Region(0, view.size())
		gbk = view.substr(reg_all).encode('gbk')
	except:
		gbk = file(view.file_name()).read()
		text = gbk.decode('gbk')
		file_name = view.file_name().encode('utf-8')

		tmp_file_name = urllib.quote_plus(os.path.basename(file_name))  + SEPERATOR + urllib.quote_plus(file_name)
		tmp_file = os.path.join(TEMP_PATH, tmp_file_name)

		window = sublime.active_window()
		view_index = window.get_view_index(view)
		is_pre_view = view_index[1] == -1
		
		if(True):
			f = file(tmp_file, 'w')
			f.write(text.encode('utf8'))
			f.close()

		if (is_pre_view):
			v = window.open_file(tmp_file,sublime.TRANSIENT)
		else:
			window.focus_view(view)
			window.run_command('close')
			v = window.open_file(tmp_file)

		sublime.status_message('gbk encoding detected, open with utf8.')

def saveWithEncoding(view, file_name = None, encoding = 'gbk'):
	if(not file_name):
		file_name = view.file_name()
	reg_all = sublime.Region(0, view.size())
	text = view.substr(reg_all).encode(encoding)
	gbk = file(file_name, 'w')
	gbk.write(text)
	gbk.close()	

def toggleEncode(view):
	global OPEN_WITH_GBK
	file_name = view.file_name()

	if(not file_name):
		return

	parts = file_name.split(SEPERATOR)

	if(file_name.startswith(TEMP_PATH) and len(parts) > 1):
		file_name = urllib.unquote_plus(parts[1].encode('utf-8')).decode('utf-8')
		sublime.active_window().run_command('close')
		OPEN_WITH_GBK= False
		sublime.active_window().open_file(file_name)
	else:
		OPEN_WITH_GBK = True
		window = sublime.active_window()
		window.run_command('close')
		window.open_file(file_name)

class EventListener(sublime_plugin.EventListener):
	def on_load(self, view):
		global OPEN_WITH_GBK 
		if (OPEN_WITH_GBK):
			gbk2utf8(view)
		OPEN_WITH_GBK = True

	def on_post_save(self, view):
		parts = view.file_name().split(SEPERATOR)
		if(view.file_name().startswith(TEMP_PATH) and len(parts) > 1):
			file_name = urllib.unquote_plus(parts[1].encode('utf-8')).decode('utf-8')
			saveWithEncoding(view, file_name)

class SaveWithGbkCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		parts = file_name.split(SEPERATOR)
		if(not file_name.startswith(TEMP_PATH) and len(parts) <= 1):
			saveWithEncoding(self.view)
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(self.view.file_name())
		else:
			sublime.active_window().run_command('save')

class SaveWithUtf8Command(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		parts = file_name.split(SEPERATOR)

		if(file_name.startswith(TEMP_PATH) and len(parts) > 1):
			file_name = urllib.unquote_plus(parts[1].encode('utf-8')).decode('utf-8')
			saveWithEncoding(self.view, file_name, 'utf-8')
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(file_name)
		else:
			sublime.active_window().run_command('save')
			
class ToggleEncodeCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		toggleEncode(self.view)