import json
import typing as tp

from abc import abstractmethod, ABC
from . import operations as ops
from . import external_sort as exts
from .operations import TRow, TRowsIterable, TRowsGenerator


TNode = tp.Union['Node', 'NodeFromFile', 'NodeFromIter']


class AbstractNode(ABC):
    @abstractmethod
    def __call__(self, sources: tp.Dict[str, tp.Any]) -> tp.Generator[tp.Dict[str, tp.Any], None, None]:
        pass


class Node(AbstractNode):
    """ Node of computational graph.
        @param operation: фабрика типа operations.Operation, создает мапперы, редьюсеры, джоинеры
        @param parents: список родителей данного узла
    """
    def __init__(self, operation: ops.Operation, parents: tp.List[TNode]) -> None:
        self.operation = operation
        self.parents = parents

    def __call__(self, sources: tp.Dict[str, tp.Callable[[TRow], TRowsIterable]]) -> TRowsGenerator:
        """ Starts computation in node, calling parent nodes if necessary."""
        yield from self.operation(*[parent(sources) for parent in self.parents])


class NodeFromFile(AbstractNode):
    """Input node of computational graph which reads from file"""
    def __init__(self, filename: str, parser: tp.Callable[[str], ops.TRow] = json.loads):
        self.filename = filename
        self.operation = ops.ReadFromFile(parser)

    def __call__(self, sources: tp.Dict[str, tp.Callable[[TRow], TRowsIterable]]) -> TRowsGenerator:
        with open(self.filename, 'r') as file:
            for line in file:
                yield from self.operation(line)


class NodeFromIter(AbstractNode):
    """Input node of computational graph which reads from iterator"""
    def __init__(self, iterator_name: str) -> None:
        self.iterator_name = iterator_name

    def __call__(self, sources: tp.Dict[str, tp.Callable[[TRow], TRowsIterable]]) -> TRowsGenerator:
        yield from sources[self.iterator_name]()  # type: ignore


class Graph:
    """Computational graph implementation"""

    def __init__(self, tail: TNode) -> None:
        """ Граф вычислений состоит из объектов класса Graph соединенных ссылками через поля prevs и heads.
        @param tail: последний узел в графе, его output направляется пользователю
        """
        self.tail = tail

    @staticmethod
    def graph_from_iter(iterator: tp.Any) -> 'Graph':
        """Construct new graph which reads data from row iterator (in form of sequence of Rows
        from 'kwargs' passed to 'run' method) or from another graph into graph data-flow
        :param iterator: name of kwarg to use as data source or Graph object
        """
        return Graph(tail=NodeFromIter(iterator))

    @staticmethod
    def graph_from_file(filename: str, parser: tp.Callable[[str], ops.TRow] = json.loads) -> 'Graph':
        """Construct new graph extended with operation for reading rows from file
        :param filename: filename to read from
        :param parser: parser from string to Row
        """
        return Graph(tail=NodeFromFile(filename, parser))

    @staticmethod
    def copy_graph(graph: 'Graph') -> 'Graph':
        return Graph(tail=graph.tail)

    def map(self, mapper: ops.Mapper) -> 'Graph':
        """Construct new graph extended with map operation with particular mapper
        :param mapper: mapper to use
        """
        graph = Graph.copy_graph(self)
        graph.tail = Node(operation=ops.Map(mapper), parents=[self.tail])
        return graph

    def reduce(self, reducer: ops.Reducer, keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with reduce operation with particular reducer
        :param reducer: reducer to use
        :param keys: keys for grouping
        """
        graph = Graph.copy_graph(self)
        graph.tail = Node(operation=ops.Reduce(reducer, keys), parents=[self.tail])
        return graph

    def sort(self, keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with sort operation
        :param keys: sorting keys (typical is tuple of strings)
        """
        graph = Graph.copy_graph(self)
        graph.tail = Node(operation=exts.ExternalSort(keys), parents=[self.tail])
        return graph

    def join(self, joiner: ops.Joiner, join_graph: 'Graph', keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with join operation with another graph
        :param joiner: join strategy to use
        :param join_graph: other graph to join with
        :param keys: keys for grouping
        """
        graph = Graph.copy_graph(self)
        graph.tail = Node(operation=ops.Join(joiner, keys), parents=[self.tail, join_graph.tail])
        return graph

    def run(self, **sources: tp.Any) -> tp.List[ops.TRow]:
        """Single method to start execution; data sources passed as kwargs"""
        return list(self.tail(sources))
