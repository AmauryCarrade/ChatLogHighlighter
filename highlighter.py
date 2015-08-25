__author__ = 'amaury'

import re, random

def highlight(raw_log: str, remove_dates=True, remove_bots=None, colors=None, actions_italic=True,
              dates_color: str="gray", line_separator: str=None, nick_prefixes=None, nick_prefixes_color="gray",
              output_format="html"):
	"""
	Highlights a chat log.

	:param raw_log: The raw chat log
	:param remove_dates: If True, the date prefixes will be removed.
	:param remove_bots: If non-empty, the nicknames of bots to remove, if a bot transmits the
						chat of some persons. The messages of the bots will be traited as normal
						messages.
	:param colors: The colors to use to highlight the pseudonyms. If not specified, a default set
	               of colors will be used.
	:param actions_italic: If True, the action messages (/me) will be displayed italicized.
	:param line_separator: The separator to use between lines (for the generated output).
	                       If None, deduced from the output format.
	:param nick_prefixes: A list of the nick prefixes, ignored when the nicks are compared and
	                      differently colored, like the operators' “@” or the voiced “+”.
	                      If None, a default set is used with usual IRC prefixes (~, &, @, % and +).
	:param nick_prefixes_color: The color of the nick prefixes. Set to None to color them the
	                            same way as the nickname.
	:param output_format: The output_format type to produce. Supported: "html", "bbcode".
	:return: The highlighted version of the log.
	"""

	nicknames_colors = {}
	used_colors = []

	if not colors or len(colors) == 0:
		colors = ["orange", "green", "lime", "red", "purple", "blue", "yellow"]

	if output_format not in ["html", "bbcode"]:
		output_format = "html"

	if line_separator is None:
		if   output_format == "html":   line_separator = "<br />\n"
		elif output_format == "bbcode": line_separator = "\n"

	if not remove_bots:
		remove_bots = []

	if not nick_prefixes:
		nick_prefixes = ["~", "&", "@", "%", "+"]


	input_lines = raw_log.strip().split("\n")
	output = ""

	regexp_date = re.compile(r"^(\[?([0-9]{1,4}(/|-|\\|\.| )[0-9]{1,2}((/|-|\\|\.| )[0-9]{1,4})( |T)?)?[0-9]{1,2}:[0-9]{1,2}(:[0-9]{1,2})?\]?) ", re.IGNORECASE)
	regexp_nick_message = re.compile(r"^(<|\()([^>)]+)(>|\))", re.IGNORECASE)
	regexp_nick_action  = re.compile(r"^\*+ ?(\S+)", re.IGNORECASE)

	rand = random.Random()


	for line in input_lines:
		line = line.strip()
		no_date_line = regexp_date.sub("", line, 1).strip()

		nick = None
		is_action = False
		date = ""
		message = ""


		# Date extraction

		date_match = regexp_date.match(line)
		if date_match:
			date = date_match.group(1)

		# Nick + message type (message/action) extraction

		nick_match = regexp_nick_message.match(no_date_line)
		if nick_match:
			nick = nick_match.group(2).strip()
			message = regexp_nick_message.sub("", no_date_line, 1)

			if nick in remove_bots:
				nick = None
				no_date_line = regexp_nick_message.sub("", no_date_line, 1).strip()
				nick_match = regexp_nick_message.match(no_date_line)
				if nick_match:
					nick = nick_match.group(2).strip()
					message = regexp_nick_message.sub("", no_date_line, 1)

		if nick is None:
			# Action message maybe?
			nick_match = regexp_nick_action.match(no_date_line)
			if nick_match:
				nick = nick_match.group(1)
				message = regexp_nick_action.sub("", no_date_line, 1)
				is_action = True

		if nick is None:
			# Not a message. Raw addition, and next one.
			if not remove_dates:
				output += _colorize(date, dates_color, output_format) + " "

			output += no_date_line + line_separator
			continue

		# Nick prefixes extraction
		nick_prefix = None

		for prefix in nick_prefixes:
			if nick.startswith(prefix):
				nick_prefix = prefix
				nick = nick.replace(nick_prefix, "", 1)


		# Let's find a color for this nick

		if nick in nicknames_colors:
			nick_color = nicknames_colors[nick]

		else:
			if len(colors) == 0:
				colors = used_colors
				used_colors = []

			nick_color = rand.choice(colors)
			colors.remove(nick_color)
			used_colors.append(nick_color)

			nicknames_colors[nick] = nick_color


		# Assembly

		if not remove_dates:
			output += _colorize(date, dates_color, output_format) + " "

		colored_nick = ""

		if nick_prefix:
			if nick_prefixes_color:
				colored_nick = _colorize(nick_prefix, nick_prefixes_color, output_format)
			else:
				nick = nick_prefix + nick

		colored_nick += _colorize(nick, nick_color, output_format)

		if is_action:
			action_text = "* " + colored_nick + message
			if actions_italic:
				output += _italic(action_text, output_format)
			else:
				output += action_text

		else:
			output += "<" + colored_nick + ">" + message

		output += line_separator

	return output

def _colorize(text, color, output_format):
	"""
	Adds the color tags to the given text.
	"""

	if color is None or color == "":
		return text

	if output_format == "html":
		return '<span style="color: ' + color + ';">' + text + '</span>'
	elif output_format == "bbcode":
		return "[color=" + color + "]" + text + "[/color]"
	else:
		return text

def _italic(text, output_format):
	"""
	Puts the given text in italic.
	"""

	if output_format == "html":
		return '<span style="font-style: italic;">' + text + '</span>'
	elif output_format == "bbcode":
		return '[i]' + text + '[/i]'
	else:
		return text
