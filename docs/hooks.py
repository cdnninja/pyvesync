import re
import urllib.request


def replacer(match):
    filename = f'{match.group(3)}.{match.group(4)}'
    url = f'https://raw.githubusercontent.com/{match.group(1)}/{match.group(2)}/{filename}'
    code = urllib.request.urlopen(url).read().decode('utf-8')
    extension = 'js' if match.group(4) == 'vue' else match.group(4)
    return '\n'.join(
        [f'``` {extension} title="{filename}"'] +
        code.split('\n')[int(match.group(5)) - 1:int(match.group(6))] +
        ['```', f'View at [GitHub]({match.group(0)})']
    )


def on_page_markdown(markdown, **kwargs):
    return re.sub(
        re.compile(
            r'^https://github.com/([\w/\-]+)/blob/([0-9a-f]+)/([\w\d\-/\.]+)\.(\w+)#L(\d+)-L(\d+)$',
            re.MULTILINE,
        ),
        replacer,
        markdown,
    )
