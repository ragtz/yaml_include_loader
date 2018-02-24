import yaml
import os

# Base on https://davidchall.github.io/yaml-includes.html

class YAMLIncludeLoader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YAMLIncludeLoader, self).__init__(stream)
        YAMLIncludeLoader.add_constructor('!include', YAMLIncludeLoader.include)

    def include(self, node):
        if isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result += self.extractFile(filename)
            return result

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for key, filename in self.construct_mapping(node).iteritems():
                result[key] = self.extractFile(filename)
            return result

        else:
            raise yaml.constructor.ConstructorError

    def extractFile(self, filename):
        filepath = os.path.join(self._root, filename)
        with open(filepath, 'r') as f:
            return yaml.load(f, YAMLIncludeLoader)

