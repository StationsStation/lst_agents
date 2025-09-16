"""Processing of Ethereum events."""
# ruff: noqa: D105, N815

from typing import Any, Protocol
from collections.abc import Mapping, Iterator, Sequence

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


class AttrAny(Protocol):
    """Type for an object supporting both attribute- and mapping-style access."""

    def __getattr__(self, name: str) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...
    def get(self, key: str, default: Any = ...) -> Any: ...  # noqa: D102
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...


class Event(AttributeDict):
    """TypedDict for an Ethereum event."""

    args: AttrAny
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
    from_block: int
    to_block: int
