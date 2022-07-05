import typing

import pytest
import random

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EpsilonGreedyBannerEngine, EmptyBannerStorageError, NoBannerError
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> typing.List[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
        Banner("b5", cost=2, stat=BannerStat(15, 35)),
        Banner("b6", cost=350, stat=BannerStat(20, 25)),
        Banner("b7", cost=200, stat=BannerStat(0, 50)),
        Banner("b8", cost=200, stat=BannerStat(1, 100)),
    ]


UNKNOWN_BANNER_ID = "huinya"


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05), (4, 16, 0.25)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    assert BannerStat(clicks, shows).compute_ctr(TEST_DEFAULT_CTR) == pytest.approx(expected_ctr)


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    assert BannerStat().compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    banner_stat = BannerStat(1, 1)
    for i in range(10):
        banner_stat_ctr = banner_stat.compute_ctr(TEST_DEFAULT_CTR)
        banner_stat.add_show()
        assert banner_stat.compute_ctr(TEST_DEFAULT_CTR) < banner_stat_ctr


def test_banner_stat_add_click_increases_ctr() -> None:
    banner_stat = BannerStat(1, 100)
    for i in range(10):
        banner_stat_ctr = banner_stat.compute_ctr(TEST_DEFAULT_CTR)
        banner_stat.add_click()
        assert banner_stat.compute_ctr(TEST_DEFAULT_CTR) > banner_stat_ctr


def _cpc(banner: Banner):
    return banner.stat.compute_ctr(TEST_DEFAULT_CTR) * banner.cost


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: typing.List[Banner]) -> None:
    selected_banner = BannerStorage(test_banners, TEST_DEFAULT_CTR).banner_with_highest_cpc()
    banner_with_highest_cpc = max(test_banners, key=_cpc)
    assert _cpc(selected_banner) == _cpc(banner_with_highest_cpc)


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    with pytest.raises(EmptyBannerStorageError):
        EpsilonGreedyBannerEngine(BannerStorage([], TEST_DEFAULT_CTR), 1.0)
        EpsilonGreedyBannerEngine(BannerStorage([], TEST_DEFAULT_CTR), 0.5)
        EpsilonGreedyBannerEngine(BannerStorage([], TEST_DEFAULT_CTR), 0.0)


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: typing.List[Banner]) -> None:
    banner_storage = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    banner_engine = EpsilonGreedyBannerEngine(banner_storage, 1.0)
    try:
        banner_engine.send_click(UNKNOWN_BANNER_ID)
    except NoBannerError as e:
        pytest.fail("Banner Engine mustn't fail on unknown banner with{}".format(e))


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: typing.List[Banner]) -> None:
    banner_with_highest_cpc = max(test_banners, key=_cpc)
    showed_banner_id = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 0.0).show_banner()
    banner_storage = BannerStorage(test_banners)
    showed_banner = banner_storage.get_banner(showed_banner_id)
    assert _cpc(banner_with_highest_cpc) == _cpc(showed_banner)


@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: typing.List[Banner],
        monkeypatch: typing.Any
        ) -> None:

    banner_storage = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    banner_engine = EpsilonGreedyBannerEngine(banner_storage, 1.0)
    monkeypatch.setattr(random, "choice", lambda _: expected_random_banner)
    banner_show = banner_engine.show_banner()
    assert banner_show == expected_random_banner


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: typing.List[Banner]) -> None:
    banner_storage = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    banner_engine = EpsilonGreedyBannerEngine(banner_storage, 1.0)
    cost_of_clicked = 0
    for i in range(100):
        banner_id = banner_engine.show_banner()
        banner_engine.send_click(banner_id)
        banner = banner_storage.get_banner(banner_id)
        cost_of_clicked += banner.cost
    total_cost = banner_engine.total_cost
    assert total_cost == pytest.approx(cost_of_clicked)


def test_engine_show_increases_banner_show_stat(test_banners: typing.List[Banner]) -> None:
    banner_storage = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    banner_engine = EpsilonGreedyBannerEngine(banner_storage, 1.0)
    banners_shows = {}
    for banner in test_banners:
        banners_shows[banner.banner_id] = banner.stat.shows
    for i in range(100):
        banner_id = banner_engine.show_banner()
        banner = banner_storage.get_banner(banner_id)
        new_banner_shows = banner.stat.shows
        assert new_banner_shows > banners_shows[banner_id]


def test_engine_click_increases_banner_click_stat(test_banners: typing.List[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 1.0)
    for banner in test_banners:
        banner_click = banner.stat.clicks
        banner_engine.send_click(banner.banner_id)
        assert banner.stat.clicks > banner_click
