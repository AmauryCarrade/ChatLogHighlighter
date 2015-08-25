# Simple chat log highlighter

I used to highlight chat logs by hand before, to share them on a dedicated topic of a community's forum.

I wrote this tool to do that automatically. With unit tests because why not?

### Features

 - highlights chat log, with a random color per user (the colors can be changed);
 - removes bot prefixes if you are, as example, in a channel with a bot reporting the chat of a Minecraft server with PurpleIRC;
 - removes the dates and times, or highlights them in the color of your choice (default gray);
 - puts action texts (`/me`) in italic, or not;
 - extracts nicks prefixes (like `%` or `@`, you can set your own prefixes), highlighting them in a different color (except if disabled) and the nicknames with and without with the same one;
 - generates HTML or BBCode (other formats can be added too).

### Example

```python
import highlighter

# Chat log from http://bash.org/?4281 (a bit modified to serve the demo)
log = """
<Zybl0re> get up
<Zybl0re> get on up
<Zybl0re> get up
<Zybl0re> get on up
<@phxl|paper> and DANCE
* nmp3bot dances :D-<
* nmp3bot dances :D|-<
* nmp3bot dances :D/-<
* phxl|paper dances :D\-<
<[HB]HatfulOfHollow> i'm going to become rich and famous after i invent a device that allows you to stab people in the face over the internet
"""

print(highlighter.highlight(log, output_format="bbcode"))

# Output
"""
<[color=green]Zybl0re[/color]> get up
<[color=green]Zybl0re[/color]> get on up
<[color=green]Zybl0re[/color]> get up
<[color=green]Zybl0re[/color]> get on up
<[color=gray]@[/color][color=blue]phxl|paper[/color]> and DANCE
[i]* [color=lime]nmp3bot[/color] dances :D-<[/i]
[i]* [color=lime]nmp3bot[/color] dances :D|-<[/i]
[i]* [color=lime]nmp3bot[/color] dances :D/-<[/i]
[i]* [color=blue]phxl|paper[/color] dances :D\-<[/i]
<[color=gray][HB][/color][color=purple]HatfulOfHollow[/color]> i'm going to become rich and famous after i invent a device that allows you to stab people in the face over the internet
"""
```

See options directly inside the `highlighter.py` file (documented there).

### Licence

This small piece of work is published under the CeCILL-B licence (see `LICENCE` file).