__author__ = 'Amaury Carrade'

import unittest
import highlighter
import re

h = highlighter.Highlighter()

class DatesDetectionTestCase(unittest.TestCase):
	def test_dates_removed(self):
		log = """
		[08:19:06] <Jenjeur> Un message
		08:19:06 <Amaury> Un message
		[08:19] <Jenjeur> Un message
		08:19 <Amaury> Un message
		[01-04-2016 08:18:27] <Jenjeur> Un message
		[01/04/2016 08:18:27] <Jenjeur> Un message
		[1/4/16 08:18:27] <Jenjeur> Un message
		[2016-04-01T08:18:27] <Jenjeur> Un message
		[01.4.16 08:18:27] <Jenjeur> Un message
		"""
		h.remove_dates = True
		highlighted =h.highlight(log)

		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			self.assertFalse("08:19" in line)
			self.assertFalse("08:19:06" in line)
			self.assertFalse("01-04-2016" in line)
			self.assertFalse("01/04/2016" in line)
			self.assertFalse("1/4/16" in line)
			self.assertFalse("2016-04-01T" in line)
			self.assertFalse("01.4.16" in line)

	def test_dates_highlighted(self):
		log = """
		[08:19:06] <Jenjeur> Un message
		08:19:06 <Amaury> Un messageeee
		[08:19] <Jenjeur> Un messageeeeeeee
		08:19 <Amaury> Un messageeeeeee
		"""
		h.remove_dates = False
		h.dates_color = "gray"
		h.output_format = "html"
		highlighted = h.highlight(log)

		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			self.assertTrue(line.strip().startswith('<span style="color: gray;">'), "Date color not found")
			self.assertTrue("08:19" in line, "Date not found in the highlighted log")


class BotsRemovalTestCase(unittest.TestCase):
	def test_bot_removed(self):
		log = """
		<Jenjeur> Un message
		<Anna> <Amaury> Un message
		<Jenjeur> Un toast
		< Anna> <Amaury> Un message
		< Anna > <Amaury> Un message
		<Anna > <Amaury> Un message
		"""
		h.remove_bots = ["Anna"]
		highlighted = h.highlight(log)

		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			self.assertFalse("Anna" in line, "Bot not removed from the log: '" + line + "'")


class PrefixExtractorTestCase(unittest.TestCase):
	def test_prefix_highlighted(self):
		log = """
		<@Jenjeur> Un message
		<@Amaury> Un message
		<@Jenjeur> Un toast
		<@Amaury> Un message
		<@Amaury> Un message
		<@Amaury> Un message
		"""
		h.output_format = "bbcode"
		highlighted = h.highlight(log)

		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			self.assertTrue(line.strip().startswith('<[color=gray]@[/color][color='))

	def test_prefixed_nicks_with_same_color(self):
		log = """
		<Jenjeur> Un message
		<Amaury> Un message
		<~Jenjeur> Un toast
		<%Amaury> Un message
		<@Amaury> Un message
		<@Jenjeur> Un message
		"""
		h.nick_prefixes_color = None
		highlighted = h.highlight(log)

		nicks_colors = {}
		regexp_nick = re.compile(r"^<\[color=([^\]])\]([^\[\]])", re.IGNORECASE)
		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			nick_and_color = regexp_nick.match(line)
			if nick_and_color:
				nick  = nick_and_color.group(2)
				color = nick_and_color.group(1)

				if nick not in nicks_colors:
					nicks_colors[nick] = color
				else:
					self.assertTrue(nicks_colors[nick] == color, "Color not kept for nick " + nick + ": " + nicks_colors[nick] + " vs " + color)


if __name__ == '__main__':
	unittest.main()
