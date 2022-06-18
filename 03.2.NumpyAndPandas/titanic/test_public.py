import os

import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from .titanic import male_age, nan_columns, class_distribution, \
    families_count, mean_price, max_size_group, dead_lucky

FILE_PATH = os.path.join(os.path.dirname(__file__), 'titanic.csv')


def test_all() -> None:
    df = pd.read_csv(FILE_PATH, sep='\t')

    np.testing.assert_allclose(male_age(df), 30.)

    assert set(nan_columns(df)) == {'Age', 'Cabin', 'Embarked'}

    class_distr_ans = pd.Series(data=[0.192308, 0.192308, 0.615385], index=[1, 2, 3], name='Pclass')
    assert_series_equal(class_distribution(df).sort_index(), class_distr_ans)

    assert families_count(df, 0) == 141
    assert families_count(df, 1) == 13
    assert families_count(df, 2) == 1
    assert families_count(df, 3) == 1
    assert families_count(df, 4) == 0

    np.testing.assert_allclose(mean_price(df, df['Ticket'].unique()), df['Fare'].mean())

    for i, row in df.iterrows():
        np.testing.assert_allclose(mean_price(df, [row['Ticket']]), row['Fare'])

    value = 26.0
    tickets = df[np.isclose(df['Fare'], value)]['Ticket']
    np.testing.assert_allclose(mean_price(df, tickets), value)

    assert max_size_group(df, ['Survived', 'Sex']) == (0, 'male')
    assert max_size_group(df, ['Survived', 'Sex', 'Cabin']) == (0, 'male', 'D26')
    assert max_size_group(df, ['Embarked', 'Pclass']) == ('S', 3)
    assert max_size_group(df, ['Age']) == (21.00, )

    np.testing.assert_allclose(dead_lucky(df), 0.75)
