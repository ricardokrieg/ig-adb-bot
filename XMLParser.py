from dataclasses import dataclass
import re
import logging


@dataclass
class Point:
    x: float
    y: float


@dataclass
class XMLParser:
    xml: object

    def find_node(self, query):
        logging.debug(f'XMLParser#find_node {query}')

        nodes = self.xml.xpath(f'//node[{query}]')

        if len(nodes) == 0:
            raise ValueError(f'Node with query "{query}" not found')

        return nodes[0]

    @staticmethod
    def get_point(node):
        bounds = node.get('bounds')

        m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)

        if m is None:
            raise ValueError(f'Invalid bounds: {bounds}')

        return Point((int(m.group(1)) + int(m.group(3))) / 2, (int(m.group(2)) + int(m.group(4))) / 2)
