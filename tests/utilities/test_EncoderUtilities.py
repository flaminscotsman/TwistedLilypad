from unittest import main, TestCase
from twistedlilypad.utilities.encoder_utilities import varint_encoder, varint_prefixed_string_encoder, \
    boolean_encoder


class TestVarIntEncoder(TestCase):
    def test_varIntEncoder_short(self):
        self.assertEqual(varint_encoder(1), b"\x01")

    def test_varIntEncoder_long(self):
        self.assertEqual(varint_encoder(300), b"\xAC\x02")


class TestVarIntPrefixedStringEncoder(TestCase):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed convallis interdum suscipit. In nec " \
            "hendrerit nibh. Nunc eget vestibulum ex. Nullam pellentesque ac eros eu sagittis. Pellentesque erat " \
            "neque, egestas ac blandit pulvinar, eleifend a urna. Vestibulum fermentum interdum vehicula. Duis amet."

    def test_varIntPrefixedStringEncoder_short(self):
        self.assertEqual(varint_prefixed_string_encoder("Hello, World!"), b"\x0DHello, World!")

    def test_varIntPrefixedStringEncoder_long(self):
        self.assertEqual(varint_prefixed_string_encoder(self.lorem), b"\xAC\x02" + self.lorem.encode('utf-8'))


class TestBooleanEncoder(TestCase):
    def test_booleanEncoder_true(self):
        self.assertEqual(boolean_encoder(True), b"\x01")

    def test_booleanEncoder_false(self):
        self.assertEqual(boolean_encoder(False), b"\x00")


if __name__ == "__main__":
    main()
