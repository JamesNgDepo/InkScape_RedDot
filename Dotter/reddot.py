#!/usr/bin/env python3
import inkex
from lxml import etree as ET

class RedDotExtension(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--dot_size", type=float, default=1.0, help="Size of the red dot in mm")

    def effect(self):
        if not self.svg.selection:
            inkex.errormsg("Please select at least one object.")
            return

        for _, element in self.svg.selection.items():
            center = self.get_center(element)
            self.create_red_dot(center)

    def get_center(self, element):
        transformation = self.calculate_nested_transformation(element)
        bbox = element.bounding_box(transformation)
        return ((bbox.left + bbox.right) / 2, (bbox.top + bbox.bottom) / 2)

    def calculate_nested_transformation(self, element):
        transformation = inkex.Transform()
        while element.getparent() is not None:
            if isinstance(element.getparent(), inkex.Group):
                transformation = element.getparent().transform @ transformation
            element = element.getparent()
        return transformation

    def create_red_dot(self, center):
        dot_size_mm = self.options.dot_size
        dot_attribs = {
            'style': f'fill:red;stroke:none',
            'cx': str(center[0]),
            'cy': str(center[1]),
            'r': str(dot_size_mm / 2)  # radius is half of the diameter
        }
        dot = ET.SubElement(self.svg.get_current_layer(), 'circle', attrib=dot_attribs)

if __name__ == '__main__':
    RedDotExtension().run()
