## 1.1.0 — 2026-10-19

- Use one maintained implementation for the Polish and English applications.
- Validate text length, font selection, alignment and widths from 10 to 500 before rendering.
- Report missing glyphs and font/rendering errors without leaving stale output.
- Use Tk's clipboard integration and handle unavailable or empty clipboard operations.
- Make the result area resize with the window and retain horizontal/vertical scrolling.
- Add regression coverage and frozen PL/EN runtime tests that verify the bundled FIGlet fonts before publication.

## Windows downloads

Choose the standalone EXE or portable Windows x64 ZIP. Verify it with `SHA256SUMS.txt`. `BUILD_INFO.json` records the exact source commit and build dependencies. Regression tests, hidden-window frozen application tests and a freshly downloaded draft package must pass before publication.
