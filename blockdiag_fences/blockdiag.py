from __future__ import absolute_import, unicode_literals
import base64
from urllib.parse import quote as url_quote
from blockdiag import (
    nw_parser,
    nw_builder,
    nw_drawer,
    seq_parser,
    seq_builder,
    seq_drawer,
    act_parser,
    act_builder,
    act_drawer,
    block_parser,
    block_builder,
    block_drawer,
    rack_parser,
    rack_builder,
    rack_drawer,
    packet_parser,
    packet_builder,
    packet_drawer,
    FontMap
)

DIAG_MODULES = {
    "nwdiag": (nw_parser, nw_builder, nw_drawer),
    "seqdiag": (seq_parser, seq_builder, seq_drawer),
    "actdiag": (act_parser, act_builder, act_drawer),
    "blockdiag": (block_parser, block_builder, block_drawer),
    "rackdiag": (rack_parser, rack_builder, rack_drawer),
    "packetdiag": (packet_parser, packet_builder, packet_drawer),
}


def draw_blockdiag(
    content,
    diag_type,
    filename=None,
    font_path=None,
    font_antialias=True,
    output_fmt="png",
):
    header, content = content.split(" ", 1)
    parser, builder, drawer = DIAG_MODULES[diag_type.strip()]
    tree = parser.parse_string(content)
    diagram = builder.ScreenNodeBuilder.build(tree)

    fontmap = FontMap()

    if font_path:
        fontmap.set_default_font(font_path)

    draw = drawer.DiagramDraw(
        output_fmt,
        diagram,
        filename=filename,
        font_alias=font_antialias,
        fontmap=fontmap,
    )
    draw.draw()

    return draw.save()


def fence_img_format(source, language, class_name, options, md, **kwargs):
    output_fmt = "svg"
    diagram = draw_blockdiag(
        source,
        language,
        output_fmt=output_fmt,
    )

    if output_fmt == "png":
        src_data = f'data:image/png;base64,{base64.b64encode(diagram).decode("ascii")}'
    else:
        src_data = f"data:image/svg+xml;charset=utf-8,{url_quote(diagram)}"

    classes = kwargs.get('classes', [])
    id_value = kwargs.get('id_value', '')
    attrs = kwargs.get('attrs', {})

    if class_name:
        classes.insert(0, class_name)

    id_attr = f' id="{id_value}"' if id_value else ''
    class_attr = f' class="{" ".join(classes)}"' if classes else ''
    extra_attrs = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs.items()) if attrs else ''

    code = f'<img src="{src_data}"{id_attr}{class_attr}{extra_attrs}>'
    return code
