import re
import urllib.request

xkcd_colors_url = 'https://xkcd.com/color/rgb.txt'
pattern = re.compile('([a-zA-Z0-9 /]+)\s+\#([a-fA-F0-9]+)');

# csharp
target_filename = 'colors.cs'
color_entry_format = 'public static readonly Color %s = new Color(%s);\n'
color_hex_format = '0x%sFF'

print('> Requesting color list from \'%s\'...' % xkcd_colors_url)
with urllib.request.urlopen(xkcd_colors_url) as response:
    colors_data = response.read()
    colors = str(colors_data, 'utf-8')

    print('> Looking for colors...')
    items_found = 0
    color_result = []
    for match in pattern.findall(colors):
        name = match[0]
        hex_value = match[1]
        color_result.append((name, hex_value))
        items_found += 1

    if items_found > 0:
        print('> %d color entr%s was found!' % (items_found, 'ies' if items_found != 1 else 'y'))
    else:
        print('> No color entry was found')
        exit

    # write as c-sharp fields
    print('> Writing to target file \'%s\'...' % target_filename)
    with open(target_filename, 'w') as output_file:
        for (color_name, color_hex) in color_result:

            # handle color name
            color_name = color_name.title().replace('/', 'And')
            splitted_color_name = str.split(color_name, ' ')
            color_name = ''

            for word in splitted_color_name:
                color_name += word


            # handle color hex value
            color_hex = color_hex_format % color_hex.upper()

            output_file.write(color_entry_format % (color_name, color_hex))

print('> Everything has been done!')



