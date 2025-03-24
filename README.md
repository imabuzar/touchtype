# TouchType - Terminal-based Typing Practice App

A Python-based typing practice application that runs in the terminal, designed to help users improve their typing speed and accuracy through progressive difficulty levels.

## Features

- Multiple difficulty modes from novice to expert
- Custom mode with user-defined character sets
- Real-time accuracy checking with color feedback
- WPM (Words Per Minute) calculation
- Accuracy percentage tracking
- Progressive learning system
- Terminal-based user interface
- Custom word lists support

## Requirements

- Python 3.6 or higher
- curses (included in standard library for Unix/Linux/macOS)
- For Windows users: windows-curses package

## Installation

1. Clone the repository:
```bash
git clone https://github.com/imabuzar/touchtype.git
cd touchtype
```

2. For Windows users only, install windows-curses:
```bash
pip install windows-curses
```

3. Ensure you have a `words.txt` file in the same directory as the script, containing one word per line.

## Usage

1. Run the application:
```bash
python main.py
```

2. Select a difficulty mode:
   - Novice: Home row keys (asdfghjkl;)
   - Beginner: Home row + easy reach keys
   - Intermediate: Adding bottom row
   - Advanced: Full keyboard
   - Expert: Special characters
   - Custom: Create your own practice set

3. Type the displayed text as accurately as possible
4. View your results including WPM and accuracy
5. Choose to retry or return to the main menu

## Controls

- Type the displayed text
- Backspace: Delete previous character
- Escape: Exit current session
- Y/N: Yes/No in result screen
- 0-6: Menu selection

## Modes

1. Novice Mode
   - Focus: Home row keys
   - Word Count: 15 words
   - Perfect for: Complete beginners

2. Beginner Mode
   - Focus: Home row + easy reach keys
   - Word Count: 20 words
   - Perfect for: Learning basic finger placement

3. Intermediate Mode
   - Focus: Adding bottom row keys
   - Word Count: 30 words
   - Perfect for: Building speed with more keys

4. Advanced Mode
   - Focus: Full keyboard including capitals
   - Word Count: 50 words
   - Perfect for: Comprehensive typing practice

5. Expert Mode
   - Focus: Special characters and symbols
   - Word Count: 75 words
   - Perfect for: Professional typing skills

6. Custom Mode
   - Focus: User-defined character set
   - Word Count: User-defined
   - Perfect for: Targeting specific characters or practicing problem areas

## Terminal Requirements

- Minimum terminal size: 80x20 characters
- Supports color display

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by various typing tutors and practice applications