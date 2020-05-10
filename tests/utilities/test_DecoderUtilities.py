from unittest import TestCase, main
from twistedlilypad.utilities.decoder_utilities import varint_parser, varint_parser_with_length, varint_prefixed_string_parser


class TestVarIntParser(TestCase):
    def test_varIntParser_short(self):
        self.assertEqual(varint_parser(b"\x01"), (1, b""))

    def test_varIntParser_long(self):
        self.assertEqual(varint_parser(b"\xAC\x02"), (300, b""))

    def test_varIntParser_overflow(self):
        self.assertRaises(OverflowError, varint_parser, b"\x90\x90\x90\x90\x90\x09")


class TestVarIntWithLengthParser(TestCase):
    def test_varIntParserWithLength_short(self):
        self.assertEqual(varint_parser_with_length(b"\x01"), (1, b"", 1))

    def test_varIntParserWithLength_long(self):
        self.assertEqual(varint_parser_with_length(b"\xAC\x02"), (300, b"", 2))

    def test_varIntParserWithLength_overflow(self):
        self.assertRaises(OverflowError, varint_parser_with_length, b"\x90\x90\x90\x90\x90\x09")


class TestVarIntPrefixedStringParser(TestCase):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed convallis interdum suscipit. In nec " \
            "hendrerit nibh. Nunc eget vestibulum ex. Nullam pellentesque ac eros eu sagittis. Pellentesque erat " \
            "neque, egestas ac blandit pulvinar, eleifend a urna. Vestibulum fermentum interdum vehicula. Duis amet."

    def test_varIntPrefixedStringParser_short(self):
        self.assertEqual(varint_prefixed_string_parser(b"\x0DHello, World!"), ("Hello, World!", b""))

    def test_varIntPrefixedStringParser_long(self):
        self.assertEqual(varint_prefixed_string_parser(b"\xAC\x02" + self.lorem.encode('utf-8')), (self.lorem, b""))

if __name__ == "__main__":
    main()
