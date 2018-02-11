import unittest
import artcbot
import logging


class MyTest(unittest.TestCase):
    def test_parse_distance_unit(self):
        distance, unit = artcbot.parse_distance_unit("5km")
        self.assertEqual(int(distance), 5)
        self.assertEqual(unit, "km")

    def test_callbot(self):
        reply = artcbot.call_bot(["!pacing", "20:09", "5", "km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km", ""],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km", "km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

if __name__ == '__main__':
    unittest.main()