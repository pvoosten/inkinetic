#!/usr/bin/env python
"""
Inkinetic. Convert SVG to HTML5 canvas.
Copyright (C) 2013 Philip van Oosten

This file is part of Inkinetic.

Inkinetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Inkinetic.  If not, see <http://www.gnu.org/licenses/>.

@author: Philip van Oosten (@pvoosten)

"""
import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
from simplestyle import *
from textwrap import dedent
from math import sqrt, acos
import json

def _elem_id(el):
    return el.attrib['id'].replace('-', '_')

def inkscape(localname):
    return '{{http://www.inkscape.org/namespaces/inkscape}}{}'.format(localname)

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
    conf = {'id': layer_id,}
    set_transform(layer, conf)
    yield """
    // Create a new layer
    var {0} = new Kinetic.Layer({1});
    """.format(layer_id, json.dumps(conf))

    for child in layer.getchildren():
        for line in paint_element(child):
            yield line
        yield """{0}.add({1}); // add {1} to layer
        """.format(layer_id, _elem_id(child))
    yield """stage.add({0}); // add the layer to the stage
    """.format(layer_id)

def paint_group(group, conf):
    group_id = _elem_id(group)
    yield """var {0} = new Kinetic.Group({1});
    """.format(group_id, json.dumps(conf))
    for child_element in group.getchildren():
        for line in paint_element(child_element):
            yield line
        yield """{0}.add({1}); // add to the {0} group
        """.format(group_id, _elem_id(child_element))

def paint_path(path, conf):
    conf['data'] = path.attrib['d']
    yield """var {0} = new Kinetic.Path({1});
    """.format(_elem_id(path), json.dumps(conf))

def paint_rect(rect, conf):
    for s in ('x', 'y', 'width', 'height'):
        conf[s] = float(rect.attrib[s])
    yield """var {0} = new Kinetic.Rect({1});
    """.format(_elem_id(rect), json.dumps(conf))

def paint_text(text, conf):
    conf.update(x = 10, y=10, fontSize=20, text='Hello')
    yield """var {0} = new Kinetic.Text({1});
    """.format(_elem_id(text), json.dumps(conf))

def set_transform(element, conf):
    if 'transform' not in element.attrib:
        return
    tf_string = element.attrib['transform']
    if tf_string.startswith("matrix("):
        set_matrix_transform(element, conf)
    elif tf_string.startswith("translate("):
        set_translate_transform(element, conf)

def set_translate_transform(element, conf):
    tf_string = element.attrib['transform'][10:-1]
    conf['x'], conf['y'] = (float(x) for x in tf_string.split(','))

def set_matrix_transform(element, conf):
    tf_string = element.attrib['transform'][7:-1]
    m = [float(x) for x in tf_string.split(',')]
    conf['x'], conf['y'] = m[4], m[5]
    conf['scale'] = {}
    scale_x = sqrt(m[0]*m[0] + m[1]*m[1])
    scale_y = sqrt(m[2]*m[2] + m[3]*m[3])
    if m[0]*m[3] - m[1]*m[2] < 0:
        scale_y = -scale_y
    if m[0] < 0:
        scale_x = -scale_x
        scale_y = -scale_y
    conf['scale'] = {'x': scale_x, 'y': scale_y}
    angle = acos(m[3] / scale_y)
    if m[2]/scale_y > 0:
        angle = -angle
    conf['rotation'] = angle

_group_tag = '{http://www.w3.org/2000/svg}g'
_painter_by_tagname = {
    _group_tag: paint_group,
    '{http://www.w3.org/2000/svg}path': paint_path,
    '{http://www.w3.org/2000/svg}rect': paint_rect,
    '{http://www.w3.org/2000/svg}text': paint_text,
    }

def paint_element(element):
    conf = {'id':_elem_id(element)}
    if 'style' in element.attrib:
        apply_style(element, conf)
    if 'transform' in element.attrib:
        set_transform(element, conf)
    for line in _painter_by_tagname[element.tag](element, conf):
        yield line

def gradient_fill(element, conf):
    if 'fill' in conf and conf['fill'].startswith('url('):
        # get the linear or radial gradient fill element
        gradient_id = conf['fill'][5:-1]
        gradient_el = element.xpath("//*[@id='{}']".format(gradient_id))[0]
        if gradient_el.tag == '{http://www.w3.org/2000/svg}radialGradient':
            radial_gradient_fill(gradient_el, conf)
        elif gradient_el.tag == '{http://www.w3.org/2000/svg}linearGradient':
            linear_gradient_fill(gradient_el, conf)

def radial_gradient_fill(gradient_el, conf):
    cx, cy, fx, fy, r, href = (gradient_el.attrib[nm]
        for nm in ('cx', 'cy', 'fx', 'fy', 'r',
            '{http://www.w3.org/1999/xlink}href'))
    conf.update({
        "fillPriority": "radial-gradient",
        "fill": "#FFFFFF",
        "fillRadialGradientStartPoint" : {"x": cx, "y": cy},
        "fillRadialGradientEndPoint" : {"x": fx, "y": fy},
        "fillRadialGradientStartRadius" : 0,
        "fillRadialGradientEndRadius" : r,
        "fillRadialGradientColorStops": color_stops(gradient_el, href)
      })

def color_stops(gradient_el, href = None):
    colors_el = gradient_el
    if href:
        colors_el = gradient_el.xpath("//*[@id='{}']".format(href[1:]))[0]
    color_list = []
    stops = colors_el.xpath("*[local-name()='stop']")
    for stop in stops:
        style = parseStyle(stop.attrib['style'])
        r, g, b = parseColor(style['stop-color'])
        a = style['stop-opacity']
        color_list.append(stop.attrib['offset'])
        color_list.append('rgba({},{},{},{})'.format(r, g, b, a))
    return color_list

def linear_gradient_fill(gradient_el, conf):
    pass

def apply_style(element, conf):
    def copy_style(conf_att, style_prop,
        style_type=unicode, condition=lambda x:True):
        if style_prop in style and condition(style[style_prop]):
            st = style_type(style[style_prop])
            conf[conf_att] = style[style_prop]
    id = _elem_id(element)
    style = parseStyle(element.attrib['style'])
    if element.tag != _group_tag:
        copy_style('fill', 'fill')
        gradient_fill(element, conf)
        copy_style('lineJoin', 'stroke-linejoin')
        copy_style('lineCap', 'stroke-linecap')
        copy_style('stroke', 'stroke', condition = lambda x: x != 'none')
        if 'stroke-width' in style:
            sw = style['stroke-width']
            sw = sw[:-2] if sw.endswith('px') else sw
            conf['strokeWidth'] = float(sw)
    copy_style('opacity', 'opacity', float)

if __name__ == '__main__':
    import shutil
    import os.path
    j = lambda f: os.path.join(os.getcwd(), f)
    k = lambda f: os.path.join(os.path.dirname(os.path.realpath(__file__)), f)
    svg = j('drawing.svg')
    if len(sys.argv) == 2:
        orig_svg = sys.argv[1]
        shutil.copy(orig_svg, svg)	
    js = j('canvas.js')
    if not os.path.exists(j('motion.js')):
        with open(j('motion.js'), 'w') as mjs:
            mjs.write("// Make things move in this file.")
    create_canvas_js_file(svg, js)
    # copy boilerplate files
    def copy_from_installdir(filename):
        if not os.path.exists(j(filename)):
            shutil.copy(k(filename), j(filename))
    copy_from_installdir('canvas.html')
    copy_from_installdir('kinetic-v4.3.3.min.js')

