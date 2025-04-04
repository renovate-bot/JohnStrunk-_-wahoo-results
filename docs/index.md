---
hide:
  - navigation  # Left navigation
  - toc         # Right TOC
  - footer      # Prev, next page links
title: Wahoo! Results swimming scoreboard
---
<!-- markdownlint-disable-next-line MD041 -->
<style>
  body {
    background: linear-gradient(135deg, white, var(--md-accent-bg-color));
    background-attachment: fixed;
  }
</style>
<div class="mycard" markdown>

<!-- markdownlint-disable-next-line MD025 -->
# Wahoo! Results

![Example scoreboard](images/demo1.png){ width=1280 height=720 .rfloat }

{{ WR }} is a free swimming scoreboard to display race results at your meets.
It combines start list data from your meet management software (e.g., {{ HMM
}} or {{ SMM }}) with timing data from your timing system to produce an
attractive scoreboard that keeps swimmers, coaches, and spectators informed of
race results in real-time.

{{ WR }} currently supports receiving race data from either a {{ CD }} or any
system that uses the "{{ GEN }}".[^1]

The scoreboard is transmitted to Chromecast devices, allowing the results to be
available on many displays at your facility.

<!-- markdownlint-capture -->
<!-- markdownlint-disable -->
<div style="text-align:center" markdown>
[:material-download:{style="vertical-align:middle"} Download](download.md){ .md-button .md-button--primary style="margin:1em"}
[:material-rocket-launch:{style="vertical-align:middle"} Get started](quickstart.md){ .md-button  style="margin:1em"}
</div>
<!-- markdownlint-restore -->

{{ CLEARFLOAT }}

<div style="text-align:right" markdown>
[Latest news on the {{ WR }} blog
:material-chevron-right:{ style="vertical-align:middle"}](blog/index.md)
</div>

</div>

<div class="mygrid" markdown>
<div class="mycard" markdown>

## Features

The {{ WR }} scoreboard is customizable to meet the needs of your swim team.

- Configurable number of lanes (6 &ndash; 10)
- Use custom text fonts, sizes, and colors plus a background image or solid
  color to fit your team's theme
- Final times are calculated based on multiple Dolphin watches or pad + backup
  times
- Results are transmitted to your {{ CC }} devices

</div>
<div class="mycard" markdown>

## Requirements

- {{ CD }} or a timing system that can generate "{{ GEN }}" files[^1]
- {{ HMM }}, {{ SMM }}, or other meet management software that can generate
  scoreboard "CTS start list" files
- Windows 10/11 PC to run {{ WR }} (It can be shared with either of the above.)
- One or more {{ CC }} devices to display the scoreboard

</div>

</div>

[^1]:
  The {{ GEN }} is used by a number of different timing systems. This is the
  same file format used by {{ HMM }} when "Generic Network File Sharing" is
  selected as the timing system. These files typically have a `*.gen`
  extension.

## Contributing

Interested in contributing? [Check out the project's repository on
GitHub](https://github.com/JohnStrunk/wahoo-results):

:material-floppy: [View the latest
releases](https://github.com/JohnStrunk/wahoo-results/releases)

:material-chat-question: [Ask
questions](https://github.com/JohnStrunk/wahoo-results/discussions)

:material-bug: [File bug
reports](https://github.com/JohnStrunk/wahoo-results/issues)

:material-download: [Download the source
code](https://github.com/JohnStrunk/wahoo-results)

:material-account-hard-hat: [Contribute
enhancements](https://github.com/JohnStrunk/wahoo-results/pulls)

## License

{{ WR }} is free, open-source software that you can download, use, and modify.
It is licensed under the [GNU Affero General Public License, version
3](https://www.gnu.org/licenses/agpl-3.0.en.html).  
The documentation &copy; 2020 &ndash; 2025 by John Strunk is licensed under
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA
4.0)](http://creativecommons.org/licenses/by-sa/4.0/)
