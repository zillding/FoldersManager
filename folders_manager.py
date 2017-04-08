import os
import subprocess
import sublime
import sublime_plugin

def subl(args=[]):
	# learnt from SideBarEnhancements
	executable_path = sublime.executable_path()
	if sublime.platform() == 'osx':
		app_path = executable_path[:executable_path.rfind('.app/') + 5]
		executable_path = app_path + 'Contents/SharedSupport/bin/subl'
	subprocess.Popen([executable_path] + args)
	if sublime.platform() == 'windows':
		def fix_focus():
			window = sublime.active_window()
			view = window.active_view()
			window.run_command('focus_neighboring_group')
			window.focus_view(view)
		sublime.set_timeout(fix_focus, 300)

def dont_close_windows_when_empty(func):
	def f(*args, **kwargs):
		s = sublime.load_settings('Preferences.sublime-settings')
		close_windows_when_empty = s.get('close_windows_when_empty')
		s.set('close_windows_when_empty', False)
		func(*args, **kwargs)
		if close_windows_when_empty:
			s.set('close_windows_when_empty', close_windows_when_empty)
	return f

class FoldersManagerCommand(sublime_plugin.WindowCommand):
	@dont_close_windows_when_empty
	def close_project_by_window(self, window):
		window.run_command('close_project')
		window.run_command('close_window')

	def on_select(self, index):
		if (index >= 0):
			self.close_project_by_window(self.window)
			subl([self.items[index][1]])

	def run(self):
		settings = sublime.load_settings('folders_manager.sublime-settings')
		self.roots = settings.get('root_dirs', ['/'])
		self.items = []
		for root in self.roots:
			for f in os.listdir(root):
				full_path = os.path.join(root, f)
				if (os.path.isdir(full_path)):
					self.items.append([f, full_path])

		self.window.show_quick_panel(self.items, self.on_select)
