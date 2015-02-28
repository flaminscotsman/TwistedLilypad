from unittest import TestCase, main
from twistedlilypad.Utilities.DecoderUtilities import varIntParser, varIntParserWithLength, varIntPrefixedStringParser


class TestVarIntParser(TestCase):
    def test_varIntParser_short(self):
        self.assertEquals(varIntParser("\x01"), (1, ""))

    def test_varIntParser_long(self):
        self.assertEquals(varIntParser("\xAC\x02"), (300, ""))

    def test_varIntParser_overflow(self):
        self.assertRaises(OverflowError, varIntParser, "\x90\x90\x90\x90\x90\x09")


class TestVarIntWithLengthParser(TestCase):
    def test_varIntParserWithLength_short(self):
        self.assertEquals(varIntParserWithLength("\x01"), (1, "", 1))

    def test_varIntParserWithLength_long(self):
        self.assertEquals(varIntParserWithLength("\xAC\x02"), (300, "", 2))

    def test_varIntParserWithLength_overflow(self):
        self.assertRaises(OverflowError, varIntParserWithLength, "\x90\x90\x90\x90\x90\x09")


class TestVarIntPrefixedStringParser(TestCase):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed convallis interdum suscipit. In nec " \
            "hendrerit nibh. Nunc eget vestibulum ex. Nullam pellentesque ac eros eu sagittis. Pellentesque erat " \
            "neque, egestas ac blandit pulvinar, eleifend a urna. Vestibulum fermentum interdum vehicula. Duis amet."

    def test_varIntPrefixedStringParser_short(self):
        self.assertEquals(varIntPrefixedStringParser("\x0DHello, World!"), ("Hello, World!", ""))

    def test_varIntPrefixedStringParser_long(self):
        self.assertEquals(varIntPrefixedStringParser("\xAC\x02" + self.lorem), (self.lorem, ""))

if __name__ == "__main__":
    main()