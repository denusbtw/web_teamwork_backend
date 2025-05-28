import pytest


@pytest.mark.django_db
class TestHackathonFactory:

    def test_start_datetime_at_this_month(self, hackathon_factory, now):
        this_month = now.month
        hackathon = hackathon_factory()
        assert hackathon.start_datetime.month == this_month

    def test_end_datetime_at_this_month(self, hackathon_factory, now):
        this_month = now.month
        hackathon = hackathon_factory()
        assert hackathon.end_datetime.month == this_month

    def test_winner_is_none_if_hackathon_is_active(
        self, hackathon_factory, now, future_date
    ):
        hackathon = hackathon_factory(start_datetime=now, end_datetime=future_date)
        assert hackathon.winner is None

    def test_winner_is_set_if_hackathon_ended(self, hackathon_factory, now, past_date):
        hackathon = hackathon_factory(start_datetime=past_date, end_datetime=now)
        assert hackathon.winner is not None
