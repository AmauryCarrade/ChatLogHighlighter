import argparse

from chat_highlighter import ChatHighlighter

parser = argparse.ArgumentParser(description='Highlights quotes')

parser.add_argument('--remove-dates', help='Remove the dates from the log.', action='store_true')
parser.add_argument('--remove-bots', help='Remove the bots from the log. Comma-separated list of nicks.', metavar='nick1,nick2')
parser.add_argument('--colors', help='HTML colors to use for the nicks. Comma-separated list of HTML colors.', metavar='color1,color2')
parser.add_argument('--color-date', help='HTML color to use for the dates.', metavar='color')
parser.add_argument('--italic-actions', help='Displays actions messages (/me) italicized', action='store_true')
parser.add_argument('--lines-separator', help='The separator to use between lines (for the generated output).', metavar='separator')
parser.add_argument('--nick-prefixes', help='A list of the nick prefixes, ignored when the nicks are compared and differently colored, like the operators\' “@” or the voiced\' “+”. Comma-separated list.', metavar='prefix1,prefix2')
parser.add_argument('--nick-prefixes-color', help='The HTML color of the nick prefixes. Set to None to color them the same way as the nicknames.', metavar='color')
parser.add_argument('--output-format', help='The output format', choices=['html', 'bbcode'], default='html')

parser.add_argument('quote', help='The quote. Lines separated using \\n.')


args = parser.parse_args()

h = ChatHighlighter(
    remove_dates=args.remove_dates,
    remove_bots=args.remove_bots.split(',') if args.remove_bots else None,
    colors=args.colors.split(',') if args.colors else None,
    actions_italic=args.italic_actions,
    dates_color=args.color_date if args.color_date else 'gray',
    lines_separator=args.lines_separator,
    nick_prefixes=args.nick_prefixes.split(',') if args.nick_prefixes else None,
    nick_prefixes_color=args.nick_prefixes_color if args.nick_prefixes_color else 'gray',
    output_format=args.output_format
)

print(h.highlight(args.quote.replace('\\n', '\n')))
