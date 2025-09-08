"""FinalizeBridgedTokensRound class module."""

from typing import Any, TypedDict
from collections.abc import Mapping, Sequence

from eth_typing import HexStr
from eth_utils.abi import event_abi_to_log_topic
from web3._utils.events import get_event_data  # noqa: PLC2701
from aea_ledger_ethereum import HexBytes
from web3.datastructures import AttributeDict
from eth_utils.conversions import to_hex

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


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


class FinalizeBridgedTokensRound(BaseState):
    """This class implements the behaviour of the state FinalizeBridgedTokensRound."""

    _state = LstabciappStates.FINALIZEBRIDGEDTOKENSROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Finalizing bridged tokens...")
        self._is_done = True
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check if the state is triggered."""
        # we check if there are bridged tokens to be finalised here;

        events = EventsPayload(
            dictionary=self.strategy.lst_collector_contract.get_tokens_relayed_events(
                self.strategy.layer_2_api, self.strategy.lst_collector_address, from_block=17590111
            ),
        )
        l2_to_l1_events = []
        for event in events.events:
            l2_to_l1_events += self._decode_event_data(event)

        # we now check if there are any events to be processed
        self.log.info(f"Found {len(l2_to_l1_events)} L2 to L1 events.")
        self.log.info("Checking for any events to be finalized...")
        finalised_events, pending_events = [], []
        for decoded_event in l2_to_l1_events:
            # check if the event has been processed on the layer 1
            # we search for events on the l1 for the same message id
            l1_events = EventsPayload(
                dictionary=self.strategy.amb_mainnet_contract.get_relayed_message_events(
                    self.strategy.layer_1_api,
                    self.strategy.layer_1_amb_home,
                    from_block=9123229,
                    message_id=decoded_event.args.messageId,
                ),
            )
            for event in l1_events.events:
                decoded_l1_event = hexify(event)
                if decoded_l1_event.args.status:  # pyright: ignore
                    finalised_events.append(decoded_event)
                else:
                    self.log.info(f"Event with message id {decoded_event.args.messageId} is pending.")
                    pending_events.append(decoded_event)
        self.log.info(f"Found {len(finalised_events)} finalised events.")
        self.log.info(f"Found {len(pending_events)} pending events.")

        return len(pending_events) > 0

    def _decode_event_data(self, event: Event) -> list:
        """Decode the events data.
        1. get the transaction receipt.
        2. get the message hash from the event.

        """
        receipt = self.strategy.layer_2_api.api.eth.get_transaction_receipt(event["transactionHash"])
        amb_abi = self.load_abi(self.strategy.layer_2_amb_home_contract)
        event_abis = [a for a in amb_abi if a.get("type") == "event"]
        topic_to_eventabi = {to_hex(event_abi_to_log_topic(e)): e for e in event_abis}  # pyright: ignore
        raw_logs = [log for log in receipt["logs"] if log["address"].lower() == self.strategy.layer_2_amb_home.lower()]
        decoded_events = []
        for raw_log in raw_logs:
            event_abi = topic_to_eventabi[raw_log["topics"][0].hex()]  # pyright: ignore
            decoded = get_event_data(self.strategy.layer_2_api.api.codec, event_abi, raw_log)
            decoded_events.append(hexify(decoded))
        return decoded_events
