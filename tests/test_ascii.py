import unittest
from unittest.mock import Mock
import tkinter as tk
import pyfiglet
from ascii_app import AsciiApp, InputError, TEXT, available_fonts, render_ascii


class RenderingTests(unittest.TestCase):
    def test_standard_font_is_packaged(self):
        self.assertIn("standard", available_fonts())

    def test_output_matches_figlet_for_all_alignments(self):
        for alignment in ("left", "center", "right"):
            with self.subTest(alignment=alignment):
                self.assertEqual(render_ascii("SWIR", "standard", "100", alignment), pyfiglet.figlet_format("SWIR", font="standard", width=100, justify=alignment))

    def test_width_bounds_and_invalid_values(self):
        for width in ("0", "9", "501", "1000", "-10", "1.5", "²", "１００", "", "NaN"):
            with self.subTest(width=width), self.assertRaisesRegex(InputError, "width_error"):
                render_ascii("A", "standard", width)
        self.assertTrue(render_ascii("A", "standard", "10"))
        self.assertTrue(render_ascii("A", "standard", "500"))

    def test_text_limits(self):
        for text in ("", "  ", "A" * 501):
            with self.assertRaisesRegex(InputError, "empty"):
                render_ascii(text, "standard")

    def test_unknown_font_and_alignment(self):
        with self.assertRaisesRegex(InputError, "font_error"):
            render_ascii("A", "../../missing")
        with self.assertRaisesRegex(InputError, "alignment_error"):
            render_ascii("A", "standard", alignment="sideways")

    def test_missing_glyphs_are_reported(self):
        with self.assertRaisesRegex(InputError, "render_error"):
            render_ascii("\U0001f600", "standard")

    def test_copy_handles_unavailable_clipboard(self):
        app = object.__new__(AsciiApp)
        app.words = TEXT["en"]
        app.output = Mock()
        app.output.get.return_value = "ASCII result\n"
        app.root = Mock()
        app.root.clipboard_clear.side_effect = tk.TclError("unavailable")
        app.status = Mock()
        self.assertFalse(app.copy())
        app.status.set.assert_called_with(TEXT["en"]["clipboard_error"])
        app.root.clipboard_append.assert_not_called()

    def test_empty_result_does_not_replace_clipboard(self):
        app = object.__new__(AsciiApp)
        app.words, app.output, app.root, app.status = TEXT["en"], Mock(), Mock(), Mock()
        app.output.get.return_value = ""
        self.assertFalse(app.copy())
        app.root.clipboard_clear.assert_not_called()

    def test_translation_keys_match(self):
        self.assertEqual(set(TEXT["pl"]), set(TEXT["en"]))


if __name__ == "__main__":
    unittest.main()
