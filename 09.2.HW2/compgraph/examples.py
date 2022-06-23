from compgraph import algorithms

resources_path = 'C:\\Users\\valee\\anaconda3\\envs\\public-2021-fall-master\\09.2.HW2\\compgraph\\resources\\'
results_path = 'C:\\Users\\valee\\anaconda3\\envs\\public-2021-fall-master\\09.2.HW2\\compgraph\\results\\'


def word_count_from_file() -> None:
    """ Считает количество вхождений для каждого слова в файле из ресурсов
        и печатает результат в stdout.
    """
    filename = resources_path + 'text_corpus.txt'
    result = results_path + 'word_count_result.txt'

    graph = algorithms.word_count_graph_from_file(filename)
    with open(result, "w") as file:
        for row in graph.run():
            print(row, file=file)


def pmi_graph_from_file() -> None:
    filename = resources_path + 'text_corpus.txt'
    result = results_path + 'pmi_result.txt'

    graph = algorithms.pmi_graph_from_file(filename)

    with open(result, "w") as file:
        for row in graph.run():
            print(row, file=file)


def inverted_index_graph_from_file() -> None:
    filename = resources_path + 'text_corpus.txt'
    result = results_path + 'tf_idf_result_new.txt'
    graph = algorithms.inverted_index_graph_from_file(filename)
    with open(result, "w") as file:
        for row in graph.run():
            print(row, file=file)



def yandex_maps_from_file() -> None:
    """ По двум файлам из ресурсов считает среднюю скорость движения в каждый час каждого дня недели
        и печатает результат в stdout.
    """
    input_stream_name_time = resources_path + 'travel_times.txt'
    input_stream_name_length = resources_path + 'road_graph_data.txt'
    graph = algorithms.yandex_maps_graph_from_file(input_stream_name_time, input_stream_name_length)
    result = results_path + 'yandex_maps_result.txt'

    with open(result, "w") as file:
        for row in graph.run():
            print(row, file=file)


