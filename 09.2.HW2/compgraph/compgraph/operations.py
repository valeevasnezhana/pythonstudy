import heapq
from abc import abstractmethod, ABC
import typing as tp
import itertools
from operator import itemgetter
from string import punctuation
from copy import deepcopy
import math
from dateutil import parser as dateutil_parser


TRow = dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass


# Operations


class Mapper(ABC):
    """Base class for mappers"""
    @abstractmethod
    def __call__(self, row: TRow) -> TRowsGenerator:
        """
        :param row: one table row
        """
        pass


class Map(Operation):
    def __init__(self, mapper: Mapper) -> None:
        self.mapper = mapper

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in rows:
            yield from self.mapper(row)


class Reducer(ABC):
    """Base class for reducers"""
    @abstractmethod
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        """
        :param rows: table rows
        """
        pass


class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: tp.Sequence[str]) -> None:
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        if len(self.keys):
            for _key, group in itertools.groupby(rows, key=itemgetter(*self.keys)):
                yield from self.reducer(tuple(self.keys), group)
        else:
            yield from self.reducer(tuple(), rows)


class Joiner(ABC):
    """Base class for joiners"""
    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2') -> None:
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    def _merge_rows(self, keys: tp.Sequence[str], row_a: TRow, row_b: TRow) -> TRow:
        common_keys = {key for key in row_a.keys() if key in row_b.keys() and key not in set(keys)}

        new_row: TRow = {}

        for key, value in row_a.items():
            if key in common_keys:
                new_row[key + self._a_suffix] = value
            else:
                new_row[key] = value

        for key, value in row_b.items():
            if key in common_keys:
                new_row[key + self._b_suffix] = value
            else:
                new_row[key] = value
        return new_row

    @abstractmethod
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        """
        :param keys: join keys
        :param rows_a: left table rows
        :param rows_b: right table rows
        """
        pass


class Join(Operation):
    def __init__(self, joiner: Joiner, keys: tp.Sequence[str]):
        self.keys = keys
        self.joiner = joiner

    def grouper(self, rows: TRowsIterable) ->\
            tp.Generator[tuple[tp.Optional[tuple[tp.Any, ...]], TRowsIterable], None, None]:
        if len(self.keys):
            for key, group in itertools.groupby(rows, key=itemgetter(*self.keys)):
                yield key, group
            yield None, []
        else:
            yield tuple(), rows
            yield None, []

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        first_grouper = self.grouper(rows)
        second_grouper = self.grouper(args[0])
        first_key, first_group = next(first_grouper)
        second_key, second_group = next(second_grouper)
        while first_key is not None and second_key is not None:
            if first_key < second_key:
                for row in self.joiner(self.keys, first_group, []):
                    yield row
                first_key, first_group = next(first_grouper)
            elif first_key == second_key:
                for row in self.joiner(self.keys, first_group, second_group):
                    yield row
                first_key, first_group = next(first_grouper)
                second_key, second_group = next(second_grouper)
            else:
                for row in self.joiner(self.keys, [], second_group):
                    yield row
                second_key, second_group = next(second_grouper)

        while first_key is not None:
            for row in self.joiner(self.keys, first_group, []):
                yield row
            first_key, first_group = next(first_grouper)

        while second_key is not None:
            for row in self.joiner(self.keys, [], second_group):
                yield row
            second_key, second_group = next(second_grouper)





# Dummy operators


class DummyMapper(Mapper):
    """Yield exactly the row passed"""
    def __call__(self, row: TRow) -> TRowsGenerator:
        yield row


class FirstReducer(Reducer):
    """Yield only first row from passed ones"""
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            yield row
            break


# Mappers


class FilterPunctuation(Mapper):
    """Left only non-punctuation symbols"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _filter_punctuation(txt: str):
        punctuation_set = set(punctuation + '“”‘')

        return "".join(symbol for symbol in txt if symbol not in punctuation_set)

    def __call__(self, row: TRow) -> TRowsGenerator:
        new_row = deepcopy(row)
        new_row[self.column] = self._filter_punctuation(row[self.column])
        yield new_row



class ToASCII(Mapper):
    """Left only non-punctuation symbols"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _to_ascii(txt: str):
        result = ''
        for symbol in txt:
            if symbol.isascii():
                result += symbol
            else:
                result += " "
        return result

    def __call__(self, row: TRow) -> TRowsGenerator:
        new_row = deepcopy(row)
        new_row[self.column] = self._to_ascii(row[self.column])
        yield new_row



class LowerCase(Mapper):
    """Replace column value with value in lower case"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _lower_case(txt: str):
        return txt.lower()

    def __call__(self, row: TRow) -> TRowsGenerator:
        new_row = deepcopy(row)
        new_row[self.column] = self._lower_case(row[self.column])
        yield new_row


class Split(Mapper):
    """Split row on multiple rows by separator"""
    def __init__(self, column: str, separator: tp.Optional[str] = None) -> None:
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    def __call__(self, row: TRow) -> TRowsGenerator:
        for field in row[self.column].split(self.separator):
            new_row = deepcopy(row)
            new_row[self.column] = field
            yield new_row


class Split_remove_s(Mapper):
    """Split row on multiple rows by separator"""
    def __init__(self, column: str, separator: tp.Optional[str] = None) -> None:
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    def __call__(self, row: TRow) -> TRowsGenerator:
        for field in row[self.column].split(self.separator):
            new_row = deepcopy(row)
            new_row[self.column] = field
            if field == "s":
                continue
            else:
                yield new_row


class Product(Mapper):
    """Calculates product of multiple columns"""
    def __init__(self, columns: tp.Sequence[str], result_column: str = 'product') -> None:
        """
        :param columns: column names to product
        :param result_column: column name to save product in
        """
        self.columns = columns
        self.result_column = result_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        product = 1
        for column in self.columns:
            product *= row[column]
        row[self.result_column] = product
        yield row


class Filter(Mapper):
    """Remove records that don't satisfy some condition"""
    def __init__(self, condition: tp.Callable[[TRow], bool]) -> None:
        """
        :param condition: if condition is not true - remove record
        """
        self.condition = condition

    def __call__(self, row: TRow) -> TRowsGenerator:
        if self.condition(row):
            yield row



class Project(Mapper):
    """Leave only mentioned columns"""
    def __init__(self, columns: tp.Sequence[str]) -> None:
        """
        :param columns: names of columns
        """
        self.columns = columns

    def __call__(self, row: TRow) -> TRowsGenerator:
        yield {key: row[key] for key in self.columns}


class AddField(Mapper):
    """add useless field column"""

    def __init__(self, column: str, def_value: tp.Any = None):
        """
        :param column: name of column to process
        """
        self.column = column
        self.def_value = def_value

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = self.def_value
        yield row


class RemoveField(Mapper):
    """add useless field column"""

    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row.pop(self.column)
        yield row






class Idf(Mapper):
    """Count idf metrics based on number of docs and \
            number of docs containing the word"""

    def __init__(self, doc_count: str, num_word_entries: str, text_column: str, result_column: str) -> None:
        """
        :param doc_count: name of doc_count column
        :param num_word_entries: name of word entries number column
        :param text_column: name of column with word
        :param result_colum: name of column for idf
        """
        self.doc_count = doc_count
        self.num_word_entries = num_word_entries
        self.text_column = text_column
        self.result_column = result_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        total_doc = row[self.doc_count]
        entries_count = row[self.num_word_entries]
        word = row[self.text_column]

        result = dict()
        result[self.text_column] = word
        result[self.result_column] = math.log(total_doc / entries_count)
        yield result


class TFIDF(Mapper):
    """Calculate IDF"""

    def __init__(self, tf_column: str, idf_column: str, tfidf_column: str = "tfidf") -> None:
        """TFIDF(word_i, doc_i) = (frequency of word_i in doc_i) *
        log((total number of docs) / (docs where word_i is present))
        @param tf_column: имя столбца содержащего tf
        @param idf_column: имя столбца содержащего idf
        @param tfidf_column: имя столбца, в который записывается результат
        """
        self.tf_column = tf_column
        self.idf_column = idf_column
        self.tfidf_column = tfidf_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.tfidf_column] = row[self.tf_column] * row[self.idf_column]
        yield row


class PMI(Mapper):
    """Count pmi metrics based on frequency of word in docs and total"""
    def __init__(self, tf_column: str, cf_column: str, pmi_column: str = "pmi") -> None:
        """pmi(word_i, doc_i) = log((frequency of word_i in doc_i) / (frequency of word_i in all documents combined))
        @param tf_column: frequency of word_i in doc_i
        @param cf_column: frequency of word_i in all documents combined
        @param pmi_column: result column
        """
        self.tf_column = tf_column
        self.cf_column = cf_column
        self.pmi_column = pmi_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.pmi_column] = math.log(row[self.tf_column] / row[self.cf_column])
        yield row



class ProcessLength(Mapper):
    """Get edge length"""

    def __init__(self, start_coord_column: str, end_coord_column: str, length_column: str) -> None:
        """
        :param start_coord_column: name of start column
        :param end_coord_column: name of end column
        :param length_column: name of column for length
        """
        self.start = start_coord_column
        self.end = end_coord_column
        self.length = length_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        b1, a1 = row[self.start]
        b2, a2 = row[self.end]
        a1 = math.radians(a1)
        a2 = math.radians(a2)
        b1 = math.radians(b1)
        b2 = math.radians(b2)
        row[self.length] = round(6373 * 2 * math.asin(
            math.sqrt(math.sin(a2 / 2 - a1 / 2) ** 2 + math.cos(a1) * math.cos(a2) * (math.sin(b2 / 2 - b1 / 2) ** 2))
        ), 5)
        yield row


class ProcessTime(Mapper):
    """Get edge length"""

    def __init__(self, enter_time_column: str, leave_time_column: str, time_column: str, weekday_column: str,
                 hour_column: str) -> None:
        """
        :param enter_time_column: name of enter time column
        :param leave_time_column: name of leave time column
        :param time_column: name of column for time
        :param weekday_column: name of column for week day
        :param hour_column: name of column for hour
        """
        self.enter = enter_time_column
        self.leave = leave_time_column
        self.time = time_column
        self.day = weekday_column
        self.hour = hour_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        date1 = dateutil_parser.parse(row[self.enter])
        date2 = dateutil_parser.parse(row[self.leave])

        row[self.day] = date1.strftime('%a')
        row[self.hour] = date1.hour
        row[self.time] = (date2 - date1).total_seconds()
        yield row



class ProcessSpeed(Mapper):
    """Get speed based on length and time"""

    def __init__(self, length_column: str, time_column: str, speed_column: str) -> None:
        """
        :param length_column: column for total length
        :param time_column: column for total time
        :param speed_column: column for redult speed
        """
        self.length = length_column
        self.time = time_column
        self.speed = speed_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.speed] = round(row[self.length] / row[self.time] * 3600, 4)
        yield row







# Reducers



class MultipleSum(Reducer):
    """Sum values in columns passed and yield single row as a result"""

    def __init__(self, columns: tp.Iterable[str]) -> None:
        """
        :param column: name of columns to sum
        """
        self.columns = columns

    def __call__(self, group_key: tp.Tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        start: bool = True
        new_row: TRow = {}
        for column in self.columns:
            new_row[column] = 0
        for row in rows:
            if start:
                for key in group_key:
                    new_row[key] = row[key]
                start = False
            for column in self.columns:
                new_row[column] += row[column]
        yield new_row




class TopN(Reducer):
    """Calculate top N by value"""
    def __init__(self, column: str, n: int) -> None:
        """
        :param column: column name to get top by
        :param n: number of top values to extract
        """
        self.column_max = column
        self.n = n

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in heapq.nlargest(self.n, rows, key=itemgetter(self.column_max)):
            yield row



class TermFrequency(Reducer):
    """Calculate frequency of values in column"""
    def __init__(self, words_column: str, result_column: str = 'tf') -> None:
        """
        :param words_column: name for column with words
        :param result_column: name for result column
        """
        self.words_column = words_column
        self.result_column = result_column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        words: tp.Dict[str, int] = {}
        new_row: TRow = {}
        start: bool = True
        group_size = 0
        for row in rows:
            group_size += 1
            if start:
                for key in group_key:
                    new_row[key] = row[key]
                start = False
            field = row[self.words_column]
            if field not in words.keys():
                words[field] = 1
            else:
                words[field] += 1
        for key, value in words.items():
            result_row = deepcopy(new_row)
            result_row[self.words_column] = key
            result_row[self.result_column] = value / group_size
            yield result_row





class Count(Reducer):
    """
    Count records by key
    Example for group_key=('a',) and column='d'
        {'a': 1, 'b': 5, 'c': 2}
        {'a': 1, 'b': 6, 'c': 1}
        =>
        {'a': 1, 'd': 2}
    """
    def __init__(self, column: str) -> None:
        """
        :param column: name for result column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        start: bool = True
        new_row: TRow = {}
        for row in rows:
            if start:
                for key in group_key:
                    new_row[key] = row[key]
                new_row[self.column] = 1
                start = False
            else:
                new_row[self.column] += 1
        yield new_row




class SafeCount(Reducer):
    """Count rows passed and yield multiple row as a result"""

    def __init__(self, column: str) -> None:
        """
        :param column: name of column to count
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        start: bool = True
        new_row: TRow = {}
        count = 0
        for row in rows:
            if start:
                for key in group_key:
                    new_row[key] = row[key]
                count = 1
                start = False
            else:
                count += 1
        new_row[self.column] = count
        for i in range(count):
            yield deepcopy(new_row)




class Sum(Reducer):
    """
    Sum values aggregated by key
    Example for key=('a',) and column='b'
        {'a': 1, 'b': 2, 'c': 4}
        {'a': 1, 'b': 3, 'c': 5}
        =>
        {'a': 1, 'b': 5}
    """
    def __init__(self, column: str) -> None:
        """
        :param column: name for sum column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        start: bool = True
        new_row: TRow = {}
        for row in rows:
            if start:
                for key in group_key:
                    new_row[key] = row[key]
                new_row[self.column] = row[self.column]
                start = False
            else:
                new_row[self.column] += row[self.column]
        yield new_row





# Joiners


class InnerJoiner(Joiner):
    """Join with inner strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_a = list(rows_a)
        for row_b in rows_b:
            for row_a in cache_a:
                yield self._merge_rows(keys, row_a, row_b)


class OuterJoiner(Joiner):
    """Join with outer strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_a = list(rows_a)
        if not cache_a:
            for row_b in rows_b:
                yield row_b

        cache_b = list(rows_b)
        if not cache_b:
            for row_a in cache_a:
                yield row_a

        for row_a in cache_a:
            for row_b in cache_b:
                yield self._merge_rows(keys, row_a, row_b)


class LeftJoiner(Joiner):
    """Join with left strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_b = list(rows_b)
        for row_a in rows_a:
            if not cache_b:
                yield row_a
            for row_b in cache_b:
                yield self._merge_rows(keys, row_a, row_b)


class RightJoiner(Joiner):
    """Join with right strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_a = list(rows_a)
        for row_b in rows_b:
            if not cache_a:
                yield row_b
            for row_a in cache_a:
                yield self._merge_rows(keys, row_a, row_b)


class ReadFromFile(Mapper):
    """Read from filename line-by-line and process every string using parser"""

    def __init__(self, parser: tp.Callable[[str], TRow]) -> None:
        """
        @param parser: функция преобразующая строку в TRow
        """
        self.parser = parser

    def __call__(self, row: str) -> TRowsGenerator:
        yield self.parser(row)
