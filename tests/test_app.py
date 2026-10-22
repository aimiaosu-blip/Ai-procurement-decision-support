import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
class AppTests(unittest.TestCase):
    def test_dashboard_starts(self):
        app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py').run(timeout=30)
        self.assertEqual(len(app.exception),0,str(app.exception))

    def test_scenario_controls(self):
        app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py').run()
        app.slider[0].set_value(.8).run()
        app.slider[1].set_value(.25).run()
        app.slider[2].set_value(.5).run()
        self.assertEqual(len(app.exception),0)
