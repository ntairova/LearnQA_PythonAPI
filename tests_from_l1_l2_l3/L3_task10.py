import pytest

class TestLenght:


    def test_len_text(self):
        phrase = input("Set a phrase: ")
        expected_len = 14
        assert len(phrase) <= expected_len, f"Phrase lenght = {len(phrase)}. More than expected {expected_len} characters"


