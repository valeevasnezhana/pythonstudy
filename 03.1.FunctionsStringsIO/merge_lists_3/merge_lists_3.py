import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    heap: list[tuple[int, int]] = []

    for i, input_stream in enumerate(input_streams):
        line = input_stream.readline().strip()
        if line:
            heapq.heappush(heap, (int(line), i))

    if not heap:
        output_stream.write(b"\n")

    while heap:
        value, i = heapq.heappop(heap)
        output_stream.write(b"%d\n" % value)

        line = input_streams[i].readline().strip()
        if line:
            heapq.heappush(heap, (int(line), i))

