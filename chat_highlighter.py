__author__ = 'Amaury Carrade'

import re, random, html

class ChatHighlighter:

	def __init__(self, remove_dates=True, remove_bots: set=None, colors: set=None, actions_italic=True,
	              dates_color="gray", lines_separator: str=None, nick_prefixes: set=None,
	              nick_prefixes_color="gray", output_format="html"):
		"""
		Initializes a new chat log highlighter.

		:param remove_dates:
			If True, the date prefixes will be removed.

		:param remove_bots:
			If non-empty, the nicknames of bots to remove, if a bot transmits the chat of some persons.
			The messages of the bots will be parsed as normal messages.

		:param colors:
			The colors to use to highlight the pseudonyms. If not specified, a default set of colors
			will be used. Use HTML colors here.

		:param actions_italic:
			If True, the action messages (/me) will be displayed italicized.

		:param dates_color:
			The color to use to highlight the dates. Use HTML colors here.

		:param lines_separator:
			The separator to use between lines (for the generated output).
		    If None, deduced from the output format.

		:param nick_prefixes:
			A list of the nick prefixes, ignored when the nicks are compared and differently colored,
			like the operators' “@” or the voiced “+”.
		    If None, a default set is used with usual IRC prefixes (~, &, @, % and +).

		:param nick_prefixes_color:
			The color of the nick prefixes. Set to None to color them the same way as the nicknames.
			Use HTML colors here.

		:param output_format:
			The output format type to produce. Supported: "html", "bbcode".
			Fallbacks to "html" if the given format is invalid.
		"""

		if not colors or len(colors) == 0:
			colors = ["orange", "green", "lime", "red", "purple", "blue"]

		if output_format not in ["html", "bbcode"]:
			output_format = "html"

		if lines_separator is None:
			if   output_format == "html":   lines_separator = "<br />\n"
			elif output_format == "bbcode": lines_separator = "\n"

		if not remove_bots:
			remove_bots = []

		if not nick_prefixes:
			nick_prefixes = ["~", "&", "@", "%", "+"]


		self.remove_dates = remove_dates
		self.remove_bots = remove_bots

		self.colors = colors
		self.actions_italic = actions_italic
		self.dates_color = dates_color

		self.lines_separator = lines_separator

		self.nick_prefixes = nick_prefixes
		self.nick_prefixes_color = nick_prefixes_color

		self.output_format = output_format


		self._regexp_date = re.compile(r"^(\[?([0-9]{1,4}(/|-|\\|\.| )[0-9]{1,2}((/|-|\\|\.| )[0-9]{1,4})( |T)?)?[0-9]{1,2}:[0-9]{1,2}(:[0-9]{1,2})?\]?) ", re.IGNORECASE)
		self._regexp_nick_message = re.compile(r"^(<|\()([^>)]+)(>|\))", re.IGNORECASE)
		self._regexp_nick_action  = re.compile(r"^(\*+) ?(\S+)", re.IGNORECASE)

		self._rand = random.Random()


	def highlight(self, raw_log: str):
		"""
		Highlights a chat log.

		:param raw_log:
			The raw chat log.

		:return:
			The highlighted version of the log.
		"""

		nicknames_colors = {}
		used_colors = []

		# The colors are copied because this set will be modified to remove used
		# colors, avoiding duplicates.
		base_colors = self.colors.copy()

		input_lines = raw_log.strip().split("\n")
		output = ""


		for line in input_lines:
			line = line.strip()
			no_date_line = self._regexp_date.sub("", line, 1).strip()

			nick = None
			nick_prefix_char = "<"
			nick_suffix_char = ">"

			is_action = False
			action_prefix_char = "*"

			date = ""
			message = ""


			# Date extraction

			date_match = self._regexp_date.match(line)
			if date_match:
				date = date_match.group(1)


			# Nick + message type (message/action) extraction

			nick_match = self._regexp_nick_message.match(no_date_line)
			if nick_match:
				nick = nick_match.group(2).strip()
				nick_prefix_char = nick_match.group(1)
				nick_suffix_char = nick_match.group(3)
				message = self._regexp_nick_message.sub("", no_date_line, 1)

				if nick in self.remove_bots:
					nick = None
					no_date_line = self._regexp_nick_message.sub("", no_date_line, 1).strip()
					nick_match = self._regexp_nick_message.match(no_date_line)
					if nick_match:
						nick = nick_match.group(2).strip()
						nick_prefix_char = nick_match.group(1)
						nick_suffix_char = nick_match.group(3)
						message = self._regexp_nick_message.sub("", no_date_line, 1)

			if nick is None:
				# Action message maybe?
				nick_match = self._regexp_nick_action.match(no_date_line)
				if nick_match:
					nick = nick_match.group(2)
					action_prefix_char = nick_match.group(1)
					message = self._regexp_nick_action.sub("", no_date_line, 1)
					is_action = True

			if nick is None:
				# Not a message. Raw addition, and next one.
				if not self.remove_dates:
					output += self._colorize(date, self.dates_color) + " "

				output += no_date_line + self.lines_separator
				continue


			# Nick prefixes extraction

			nick_prefix = None

			for prefix in self.nick_prefixes:
				if nick.startswith(prefix):
					nick_prefix = prefix
					nick = nick.replace(nick_prefix, "", 1)


			# Let's find a color for this nick

			if nick in nicknames_colors:
				nick_color = nicknames_colors[nick]

			else:
				if len(base_colors) == 0:
					base_colors = used_colors
					used_colors = []

				nick_color = self._rand.choice(base_colors)
				base_colors.remove(nick_color)
				used_colors.append(nick_color)

				nicknames_colors[nick] = nick_color


			# Assembly

			if not self.remove_dates:
				output += self._colorize(date, self.dates_color) + " "

			colored_nick = ""

			if nick_prefix:
				if self.nick_prefixes_color:
					colored_nick = self._colorize(nick_prefix, self.nick_prefixes_color)
				else:
					nick = nick_prefix + nick

			colored_nick += self._colorize(nick, nick_color)

			if is_action:
				action_text = self._escape(action_prefix_char) + " " + colored_nick + self._escape(message)
				if self.actions_italic:
					output += self._italic(action_text)
				else:
					output += action_text

			else:
				output += self._escape(nick_prefix_char) + colored_nick + self._escape(nick_suffix_char + message)

			output += self.lines_separator

		return output


	def _colorize(self, text: str, color: str):
		"""
		Adds the color tags to the given text.
		"""

		if color is None or color == "":
			return text

		if self.output_format == "html":
			return '<span style="color: ' + color + ';">' + text + '</span>'
		elif self.output_format == "bbcode":
			return "[color=" + color + "]" + text + "[/color]"
		else:
			return text

	def _italic(self, text: str):
		"""
		Puts the given text in italic.
		"""

		if self.output_format == "html":
			return '<span style="font-style: italic;">' + text + '</span>'
		elif self.output_format == "bbcode":
			return '[i]' + text + '[/i]'
		else:
			return text

	def _escape(self, text: str):
		"""
		Escapes the HTML entities of the given text, if the output type is HTML.
		"""

		if self.output_format == "html":
			return html.escape(text)
		else:
			return text
