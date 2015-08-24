__author__ = 'amaury'

import unittest
import highlighter


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
		highlighted = highlighter.highlight(log, remove_dates=True)

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
		highlighted = highlighter.highlight(log, remove_dates=False, dates_color="gray", output_format="html")

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
		highlighted = highlighter.highlight(log, remove_bots=["Anna"])

		for line in highlighted.split("\n"):
			if len(line) == 0: continue

			self.assertFalse("Anna" in line, "Bot not removed from the log: '" + line + "'")

if __name__ == '__main__':
	unittest.main()
