import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("src_dicts, state, filter_dicts", [
    ([
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ],
     "EXECUTED",
     [
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
     ]),
    ([
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ],
     "CANCELED",
     [
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
     ]),
])
def test_filter_dict_by_state_key(src_dicts, state, filter_dicts):
    assert filter_by_state(src_dicts, state) == filter_dicts


@pytest.mark.parametrize("src_dicts, state, notice", [
    ([
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ],
     "NEXT",
     "Нет словарей со значением state"),
])
def test_note_have_value_state_in_dicts(src_dicts, state, notice):
    assert filter_by_state(src_dicts, state) == notice


@pytest.mark.parametrize("src_dicts, state, notice", [
    ([
         {'id': 41428829, 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'date': '2018-10-14T08:21:33.419441'}
     ],
     "EXECUTED",
     "В словарях нет ключа 'state'"),
    ([
         {'id': 41428829, 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'date': '2018-10-14T08:21:33.419441'}
     ],
     "CANCELED",
     "В словарях нет ключа 'state'"),
])
def test_state_key_not_in_dicts(src_dicts, state, notice):
    assert filter_by_state(src_dicts, state) == notice


@pytest.mark.parametrize("src_dicts, notice", [
    (None, "Не указан список словарей"),
])
def test_none_list_dicts(src_dicts, notice):
    assert filter_by_state(src_dicts) == notice


@pytest.mark.parametrize("src_dicts, reverse_, sort_dicts", [
    ([
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ],
     "True",
     [
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
     ]),
    ([
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ],
     "False",
     [
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
         {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
     ]),
    ])
def test_sort_dict_by_date_key(src_dicts, reverse_, sort_dicts):
    assert sort_by_date(src_dicts, reverse_) == sort_dicts


@pytest.mark.parametrize("src_dicts, notice", [
    ([
         {'id': 41428829, 'state': 'EXECUTED'},
         {'id': 939719570, 'state': 'EXECUTED'},
         {'id': 594226727, 'state': 'CANCELED'},
         {'id': 615064591, 'state': 'CANCELED'}
     ],
     "В словарях нет ключа 'date'")
])
def test_not_have_date_key_in_dict(src_dicts, notice):
    assert sort_by_date(src_dicts) == notice