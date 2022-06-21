from compgraph import algorithms

resources_path = 'C:\\Users\\valee\\anaconda3\\envs\\public-2021-fall-master\\09.2.HW2\\compgraph\\resources\\'


def word_count_from_file() -> None:
    """ Cчитает количество вхождений для каждого слова в файле из ресурсов
        и печатает результат в stdout.
    """
    filename = resources_path + 'text_corpus.txt'

    graph = algorithms.word_count_graph_from_file(filename)

    result = graph.run()

    for row in result:
        print(row)


def yandex_maps_from_file() -> None:
    """ По двум файлам из ресурсов считает среднюю скорость движения в каждый час каждого дня недели
        и печатает результат в stdout.
    """
    input_stream_name_time = resources_path + 'travel_times.txt'
    input_stream_name_length = resources_path + 'road_graph_data.txt'
    graph = algorithms.yandex_maps_graph_from_file(input_stream_name_time, input_stream_name_length,
                                                   enter_time_column='enter_time', leave_time_column='leave_time',
                                                   edge_id_column='edge_id',
                                                   start_coord_column='start', end_coord_column='end',
                                                   weekday_result_column='weekday', hour_result_column='hour',
                                                   speed_result_column='speed'
                                                   )

    result = graph.run()

    for row in result:
        print(row)


if __name__ == "__main__":
    yandex_maps_from_file()
