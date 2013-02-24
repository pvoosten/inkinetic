#!/usr/bin/env python
import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *
from textwrap import dedent
from math import sqrt, acos

def _elem_id(el):
    return el.attrib['id'].replace('-', '_')

def get_layers(effect):
    return effect.document.xpath("/*[local-name()='svg']/*[local-name()='g']")

def kinetic_js_script(effect):
    root = effect.document.getroot()
    yield """var stage = new Kinetic.Stage({{
        container:'container',
        width:{0},
        height:{1}
        }});
    """.format(root.attrib['width'], root.attrib['height'])
    # get all layers (top level group elements, bottom layer first, top
    # layer last)
    for line in (line for layer in get_layers(effect) for line in add_layer(layer)):
        yield line

def create_canvas_js_file(svg_filename, canvas_js_filename):
    effect = inkex.Effect()
    effect.parse(svg_filename)
    with open(canvas_js_filename, 'w') as f:
        f.writelines(dedent(line) for line in kinetic_js_script(effect))

def add_layer(layer):
    layer_id = _elem_id(layer)
    yield """
    // Create a new layer
    var {0} = new Kinetic.Layer();
    """.format(layer_id)

    for child in layer.getchildren():
        for line in paint_element(child):
            yield line
        yield """{0}.add({1}); // add {1} to layer
        """.format(layer_id, _elem_id(child))
    if "transform" in layer.attrib:
        for line in transform_element(layer):
            yield line
    yield """stage.add({0}); // add the layer to the stage
    """.format(layer_id)

def paint_group(group):
    group_id = _elem_id(group)
    yield """var {0} = new Kinetic.Group();
    """.format(group_id)
    for child_element in group.getchildren():
        for line in paint_element(child_element):
            yield line
        yield """{0}.add({1}); // add to the {0} group
        """.format(group_id, _elem_id(child_element))

def paint_path(path):
    yield """var {0} = new Kinetic.Path({{
        x: {x},
        y: {y},
        data: "{data}",
        }});
    """.format(_elem_id(path), data = path.attrib['d'], x=0, y=0)

def paint_rect(rect):
    x, y, width, height = (float(rect.attrib[s]) for s in ('x', 'y', 'width', 'height'))
    yield """var {0} = new Kinetic.Rect({{
        x: {x},
        y: {y},
        width: {width},
        height: {height},
        }});
    """.format(_elem_id(rect),x=x, y=y, width=width, height=height)

def paint_text(text):
    yield """var {0} = new Kinetic.Text({{
        x:10,
        y:10,
        text:"Hello",
        fontSize:20
        }});
    """.format(_elem_id(text))

def transform_element(element):
    tf_string = element.attrib['transform']
    if tf_string.startswith("matrix("):
        return matrix_transform_element(element)
    elif tf_string.startswith("translate("):
        return translate_transform_element(element)

def translate_transform_element(element):
    tf_string = element.attrib['transform'][10:-1]
    tx, ty = (float(x) for x in tf_string.split(','))
    yield """{id}.setAbsolutePosition({tx}, {ty});
    """.format(id=_elem_id(element), tx=tx, ty=ty)

def matrix_transform_element(element):
    tf_string = element.attrib['transform'][7:-1]
    m = [float(x) for x in tf_string.split(',')]
    translate_x = m[4]
    translate_y = m[5]
    scale_x = sqrt(m[0]*m[0] + m[1]*m[1])
    scale_y = sqrt(m[2]*m[2] + m[3]*m[3])
    if m[0]*m[3] - m[1]*m[2] < 0:
        scale_y = -scale_y
    if m[0] < 0:
        scale_x = -scale_x
        scale_y = -scale_y
    angle = acos(m[3] / scale_y)
    if m[2]/scale_y > 0:
        angle = -angle

    yield """{id}.setAbsolutePosition({tx}, {ty});
    {id}.setRotation({angle});
    {id}.setScale({sx}, {sy});
    """.format(id=_elem_id(element), tx=translate_x, ty=translate_y,
         angle=angle, sx=scale_x, sy=scale_y)

_group_tag = '{http://www.w3.org/2000/svg}g'
_painter_by_tagname = {
    _group_tag: paint_group,
    '{http://www.w3.org/2000/svg}path': paint_path,
    '{http://www.w3.org/2000/svg}rect': paint_rect,
    '{http://www.w3.org/2000/svg}text': paint_text,
    }
def paint_element(element):
    for line in _painter_by_tagname[element.tag](element):
        yield line
    if 'style' in element.attrib:
        for line in apply_style(element):
            yield line
    if "transform" in element.attrib:
        for line in transform_element(element):
            yield line

def apply_style(element):
    id = _elem_id(element)
    style = parseStyle(element.attrib['style'])
    if element.tag != _group_tag:
        if 'fill' in style:
            yield """{id}.setFill('{fill_color}');
            """.format(id=id, fill_color=style['fill'])
        if 'stroke' in style and style['stroke'] != 'none':
            yield """{id}.setStroke('{stroke_color}');
            """.format(id=id, stroke_color=style['stroke'])
    if 'opacity' in style:
        yield"""{id}.setOpacity({opacity});
        """.format(id=id, opacity=style['opacity'])

if __name__ == '__main__':
    svg_filename='drawing.svg'
    canvas_js_filename = 'canvas.js'
    create_canvas_js_file(svg_filename, canvas_js_filename)

