---
name: desktop-ui-check
description: Review the screens of a Windows desktop program (tkinter, ttk, WinForms, WPF) for clear wording, readable colours, keyboard use, screen states and regressions. Use when asked to check a desktop interface, when colours, texts or windows change, or before a release. Not for websites.
---

# Desktop UI Check

A review for desktop programs, based on measuring and not on guessing. It works in T3 Code, Claude, Gemini, Antigravity, ChatGPT and Codex.

The ideas come from [jakubkrehel/skills](https://github.com/jakubkrehel/skills) by Jakub Krehel (MIT license). Those skills are written for websites, so this one was rewritten for desktop programs. For a website, use web skills instead.

## How to Use This Skill

- This is a review: read and report only. Change code only after the user says so.
- Follow the project's own rules first. They may forbid reading personal files, clicking in other windows, or using the clipboard.
- Use sample data for screenshots. Never show the user's own data.
- Say what was measured and what was only read in the code. Never claim that a screen was checked when it was not seen.
- Tell the user before anything needs them to leave the mouse and keyboard alone.

## Part 1: Words

Check every label, button, notification, error and confirmation.

1. **An error says what happened and what to do next.** "No microphone was found. Connect one or choose another in Settings." Not "Error -9996".
2. **A button says what it does.** Prefer "Delete history" over "OK". Windows' own Yes and No buttons are fine when a custom window would be too much work; then the question must be clear by itself.
3. **Say what cannot be undone,** and before it happens.
4. **Use one word for one thing everywhere:** in the program, the manual and the screenshots.
5. **Keep it short and plain.** Name no technical cause when the user cannot act on it; keep such detail for the log.

## Part 2: Colours

Measure the contrast with the WCAG formula. The minimum is 4.5:1 for normal text, 3:1 for large or bold text of at least 18.66 pixels, and 3:1 for a border or icon that is the only sign of a control.

1. **Check every theme and every background.** A program looks right in the theme the developer uses; the fault is often in the other one. A colour can also sit on both the window and a lighter panel.
2. **Find how each colour is really used.** A colour meant for large text may also be used for small text. Use the rule for its smallest use.
3. **Measure real pixels in a screenshot.** The theme file is not enough: a colour can come from somewhere else, such as a tray icon colour used as text. Take the darkest pixel of the letters on a light background, or the lightest on a dark one, as the edges of letters are blended.
4. **Keep a colour test in the project,** at 4.5:1, for all colours of text in all themes. A lower limit lets the fault stay.
5. **Colour is never the only signal.** A state also has a word or a shape, such as "● Stopped".

## Part 3: Keyboard

1. Every control can be reached with Tab, in a logical order.
2. Focus can be seen on every control, in every theme.
3. Enter does the main action and Esc closes or cancels, where the user expects that. Scrolling areas work with the keyboard and the mouse wheel.
4. A small window that appears does not steal focus from the program the user types in, unless it is meant to.

Record each control that fails, with the window and the tab it is on.

## Part 4: States and Stress

Show each window in each of these conditions, without changing the user's real data. In tkinter, build the window from the project's own code with sample data, and keep it behind other windows or off the screen.

1. **States:** empty, loading, working, finished, error, and with the service stopped.
2. **Long text:** the longest real message, a long file path, and a long name.
3. **Small window:** the minimum size and a low screen. Buttons must stay visible, and the part that shrinks must be the part that can.
4. **Scale:** 100%, 125% and 150%, as text and controls can overlap at some scales.
5. **Themes:** light and dark for every window.
6. **Missing parts:** no microphone, no speaker, no graphics card, or a missing file. The program must say what is wrong and keep working where it can.

## Part 5: Check per Release

Compare the screens with the last release, and ask: did this change make anything worse?

Give every finding one label:

- **New:** comes from this change.
- **Regression:** worked before, and is broken now.
- **Existing:** was already there, and is not caused by this change.

Regressions come first, then new findings. Existing findings are listed, but do not hold up the release.

## Report

Start with one or two sentences: is the screen ready or not? Then one table:

| Severity | Label | Window | Finding | Measured | Suggested fix |
|---|---|---|---|---|---|

- **High:** the user cannot do the task, or loses data.
- **Medium:** text cannot be read, or a control cannot be reached.
- **Low:** wording or a small inconsistency.

End with what was not checked, such as other screens, or scales that were not tried.
