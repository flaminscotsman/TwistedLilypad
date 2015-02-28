from unittest import main, TestCase
from twistedlilypad.Utilities.EncoderUtilities import varIntEncoder, varIntPrefixedStringEncoder, \
    booleanEncoder


class TestVarIntEncoder(TestCase):
    def test_varIntEncoder_short(self):
        self.assertEquals(varIntEncoder(1), "\x01")

    def test_varIntEncoder_long(self):
        self.assertEquals(varIntEncoder(300), "\xAC\x02")


class TestVarIntPrefixedStringEncoder(TestCase):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed convallis interdum suscipit. In nec " \
            "hendrerit nibh. Nunc eget vestibulum ex. Nullam pellentesque ac eros eu sagittis. Pellentesque erat " \
            "neque, egestas ac blandit pulvinar, eleifend a urna. Vestibulum fermentum interdum vehicula. Duis amet."

    def test_varIntPrefixedStringEncoder_short(self):
        self.assertEquals(varIntPrefixedStringEncoder("Hello, World!"), "\x0DHello, World!")

    def test_varIntPrefixedStringEncoder_long(self):
        self.assertEquals(varIntPrefixedStringEncoder(self.lorem), "\xAC\x02" + self.lorem)


class TestBooleanEncoder(TestCase):
    def test_booleanEncoder_true(self):
        self.assertEquals(booleanEncoder(True), "\x01")
    def test_booleanEncoder_false(self):
        self.assertEquals(booleanEncoder(False), "\x00")

if __name__ == "__main__":
    main()
