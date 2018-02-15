import unittest
import artcbot

class MyTest(unittest.TestCase):
    def test_parse_distance_unit(self):
        distance, unit = artcbot.parse_distance_unit("5.1km")
        self.assertEqual(5.1, float(distance))
        self.assertEqual(unit, "km")

        distance, unit = artcbot.parse_distance_unit("5.0km")
        self.assertEqual(5.0, float(distance))
        self.assertEqual(unit, "km")

        distance, unit = artcbot.parse_distance_unit("5m")
        self.assertEqual(5, float(distance))
        self.assertEqual(unit, "m")

        distance, unit = artcbot.parse_distance_unit("5.0 km")
        self.assertEqual(5.0, float(distance))
        self.assertEqual(unit, "km")

        distance, unit = artcbot.parse_distance_unit("5.0 miles")
        self.assertEqual(5.0, float(distance))
        self.assertEqual(unit, "miles")

    def test_callbot(self):
        reply = artcbot.call_bot(["!pacing", "20:09", "5", "km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km", ""],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km", "km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5km"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "20:09", "5kilometers"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        #I'm funny
        reply = artcbot.call_bot(["!pacing", "20:09", "5kilograms"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 kilometer(s) in 20:09 you need to run each kilometer in 4:01, or each mile in 6:30.")

        reply = artcbot.call_bot(["!pacing", "50:00", "5miles"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 mile(s) in 50:00 you need to run each mile in 10:00, or each kilometer in 6:15.")

        reply = artcbot.call_bot(["!pacing", "50:00", "5.0miles"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 mile(s) in 50:00 you need to run each mile in 10:00, or each kilometer in 6:15.")

        reply = artcbot.call_bot(["!pacing", "50:00", "5.0 miles"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 mile(s) in 50:00 you need to run each mile in 10:00, or each kilometer in 6:15.")

        reply = artcbot.call_bot(["!pacing", "50:00", "5 miles"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 mile(s) in 50:00 you need to run each mile in 10:00, or each kilometer in 6:15.")

        reply = artcbot.call_bot(["!pacing", "50:00", "5 m"],"","")
        self.assertEqual(reply, "\n\nTo run 5.0 mile(s) in 50:00 you need to run each mile in 10:00, or each kilometer in 6:15.")

if __name__ == '__main__':
    unittest.main()