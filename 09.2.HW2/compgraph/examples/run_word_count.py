import itertools
import json
import os

from compgraph import algorithms as graphs
from compgraph import operations as ops


def parser(line: str) -> ops.TRow:
    return json.loads(line)


dir_path = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(os.path.split(dir_path)[0], 'resources')


def word_count() -> None:
    graph = graphs.word_count_graph('docs', text_column='text', count_column='count')
    filename = os.path.join(resource_path, "text_corpus.txt")
    graph = graph.graph_from_file(filename=filename, parser=parser)

    result = graph.run()
    for res in itertools.islice(result, 5):
        print(res)
