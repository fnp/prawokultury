from textile import Textile


class TextilePL(Textile):
    """Polish version of Textile.

    Changes opening quote to Polish lower-double.
    """
    glyph_defaults = [(name, repl) 
        for (name, repl) in Textile.glyph_defaults
        if name != 'txt_quote_double_open']
    glyph_defaults.append(('txt_quote_double_open', '&#8222;'))


def textile_pl(text):
    return TextilePL().textile(text)


def textile_restricted_pl(text):
    return TextilePL(restricted=True, lite=True,
                   noimage=True, auto_link=False).textile(
                        text, rel='nofollow')
