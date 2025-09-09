"""Processing of Ethereum events."""

from typing import Any, TypedDict
from collections.abc import Mapping, Sequence

from eth_typing import HexStr
from aea_ledger_ethereum import HexBytes
from web3.datastructures import AttributeDict
from eth_utils.conversions import to_hex


def hexify(obj):
    """Convert bytes in the given object to hex strings."""
    if isinstance(obj, bytes | bytearray | HexBytes):
        return to_hex(obj)  # always 0x-prefixed
    if isinstance(obj, AttributeDict):
        return AttributeDict({k: hexify(v) for k, v in obj.items()})
    if isinstance(obj, Mapping):
        return {k: hexify(v) for k, v in obj.items()}
    if isinstance(obj, tuple):
        return tuple(hexify(v) for v in obj)
    if isinstance(obj, Sequence) and not isinstance(obj, str | bytes | bytearray):
        return [hexify(v) for v in obj]
    return obj


class Event(TypedDict):
    """TypedDict for an Ethereum event."""

    args: dict[str, Any]
    event: str
    logIndex: int
    transactionIndex: int
    transactionHash: HexBytes | HexStr
    address: str
    blockHash: str | bytes
    blockNumber: int


class EventsPayload(AttributeDict):
    """TypedDict for a payload containing a list of events."""

    events: list[Event] = []
