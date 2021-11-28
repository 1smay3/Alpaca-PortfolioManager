from dataclasses import dataclass
import datetime as dt

from app.main import alpaca


def __get_pretty_timestamp__(time: dt.datetime) -> str:
    return time.strftime('%d %B %Y at %H:%M')


@dataclass
class MarketStatus:
    # FIXME: This timestamp is using some whack timezone, fix it
    timestamp: dt.datetime
    is_open: bool
    next_open: dt.datetime
    next_close: dt.datetime

    def __str__(self) -> str:
        # TODO: Use string comprehension
        pretty_timestamp = "Currently it is " + __get_pretty_timestamp__(self.timestamp)
        # FIXME: Is there a nicer way of doing this? It's butters.
        if self.is_open:
            formatted_next = "The market is currently open, but will close at " + __get_pretty_timestamp__(
                self.next_close)
        else:
            formatted_next = "The market is currently closed, but will open at " + __get_pretty_timestamp__(
                self.next_open)

        return pretty_timestamp + ".\n" + formatted_next + "."


def print_market_status(clock):
    # TODO: Why does this not know what the properties are despite the type hint?
    mapped = MarketStatus(clock.timestamp, clock.is_open, clock.next_open, clock.next_close)
    print(mapped)


def print_current_market_status():
    clock_observable = alpaca.get_clock()
    clock_observable.subscribe(lambda clock: print_market_status(clock))