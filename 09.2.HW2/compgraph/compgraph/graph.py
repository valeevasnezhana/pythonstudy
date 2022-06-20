import typing as tp
from . import operations as ops, external_sort as sort


Operations = tp.Union[ops.Operation, tp.Callable[[ops.TRowsGenerator, tp.Any], ops.TRowsGenerator]]


class Graph:
    """Computational graph implementation"""

    __slots__ = (
        "source_type",
        "source",
        "parser",
        "fabric",
        "operations",
        "return_list"
    )

    def __init__(self, operations: tp.List[Operations]) -> None:
        self.operations = operations

    # ----

    @staticmethod
    def graph_from_iter(name: str) -> 'Graph':
        """Construct new graph which reads data from row iterator (in form of sequence of Rows
        from 'kwargs' passed to 'run' method) into graph data-flow
        Use ops.ReadIterFactory
        :param name: name of kwarg to use as data source
        """
        graph = Graph([])
        graph.return_list = True
        graph.source_type = "generator"
        graph.source = name
        return graph

    @staticmethod
    def graph_from_file(filename: str, parser: tp.Callable[[str], ops.TRow]) -> 'Graph':
        """Construct new graph extended with operation for reading rows from file
        Use ops.Read
        :param filename: filename to read from
        :param parser: parser from string to Row
        """

        def fabric() -> tp.Callable[[str, tp.Callable[[str], ops.TRow]], ops.TRowsGenerator]:
            def generator(filename: str, parser: tp.Callable[[str], ops.TRow]) -> ops.TRowsGenerator:
                with open(filename, "r") as file:
                    for string in file:
                        yield parser(string)

            return generator

        graph = Graph([])
        graph.source_type = "file"
        graph.source = filename
        graph.parser = parser
        graph.fabric = fabric
        return graph

    def map(self, mapper: ops.Mapper) -> 'Graph':
        """Construct new graph extended with map operation with particular mapper
        :param mapper: mapper to use
        """
        self.operations.append(ops.Map(mapper))
        return self

    def reduce(self, reducer: ops.Reducer, keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with reduce operation with particular reducer
        :param reducer: reducer to use
        :param keys: keys for grouping
        """
        self.operations.append(ops.Reduce(reducer, tuple(keys)))
        return self

    def sort(self, keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with sort operation
        :param keys: sorting keys (typical is tuple of strings)
        """
        self.operations.append(sort.ExternalSort(keys))
        return self

    def join(self, joiner: ops.Joiner, join_graph: 'Graph', keys: tp.Sequence[str]) -> 'Graph':
        """Construct new graph extended with join operation with another graph
        :param joiner: join strategy to use
        :param join_graph: other graph to join with
        :param keys: keys for grouping
        """

        def join_op(left_generator: ops.TRowsGenerator, **right_kwargs: tp.Any) -> ops.TRowsGenerator:
            right_generator = join_graph.run(**right_kwargs)
            return ops.Join(joiner, keys=keys)(left_generator, right_generator)

        self.operations.append(join_op)
        return self

    def run(self, **kwargs: tp.Any) -> ops.TRowsIterable:
        """Single method to start execution; data sources passed as kwargs"""

        current_generator = kwargs[
            self.source]() if self.source_type == "generator" \
            else self.fabric()(self.source, self.parser)

        for operation in self.operations:
            new_kwargs = kwargs.copy()
            current_generator = operation(current_generator, **new_kwargs)
        return list(current_generator)
