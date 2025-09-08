"""Module for performing transactions."""

from typing import Any, NamedTuple, cast

from aea_ledger_ethereum import (
    HexBytes,
    EthereumApi,
    SignedTransaction,
    try_decorator,
)


def _getitem(self, index):
    """Private get attribute by index or name."""
    try:
        return tuple.__getitem__(self, index)  # noqa: PLC2801
    except TypeError:
        return getattr(self, index)


class NewStyleSignedTransaction(NamedTuple):
    """New style SignedTransaction."""

    raw_transaction: HexBytes
    hash: HexBytes
    r: int
    s: int
    v: int

    def __getitem__(self, index):
        """Get attribute by index or name."""
        return _getitem(self, index)


def signed_tx_to_dict(signed_transaction: SignedTransaction) -> dict[str, str | int]:
    """Write SignedTransaction to dict."""
    signed_transaction_dict: dict[str, str | int] = {
        "raw_transaction": cast(str, signed_transaction.rawTransaction.hex()),
        "hash": cast(str, signed_transaction.hash.hex()),
        "r": cast(int, signed_transaction.r),
        "s": cast(int, signed_transaction.s),
        "v": cast(int, signed_transaction.v),
    }
    return signed_transaction_dict


@try_decorator("Unable to send transaction: {}", logger_method="warning")
def try_send_signed_transaction(
    ethereum_api: EthereumApi, tx_signed: dict[str, str | int], **_kwargs: Any
) -> HexBytes | None:
    """Try send a raw signed transaction."""
    signed_transaction = SignedTransactionTranslator.from_dict(tx_signed)
    hex_value = ethereum_api.api.eth.send_raw_transaction(  # pylint: disable=no-member
        signed_transaction.raw_transaction
    )
    tx_digest = hex_value.hex()
    if not tx_digest.startswith("0x"):
        tx_digest = "0x" + tx_digest
    return cast(HexBytes, HexBytes(tx_digest))


class SignedTransactionTranslator:
    """Translator for SignedTransaction."""

    @staticmethod
    def to_dict(signed_transaction: NewStyleSignedTransaction) -> dict[str, str | int]:
        """Write SignedTransaction to dict."""
        signed_transaction_dict: dict[str, str | int] = {
            "raw_transaction": cast(str, signed_transaction.raw_transaction.hex()),
            "hash": cast(str, signed_transaction.hash.hex()),
            "r": cast(int, signed_transaction.r),
            "s": cast(int, signed_transaction.s),
            "v": cast(int, signed_transaction.v),
        }
        return signed_transaction_dict

    @staticmethod
    def from_dict(signed_transaction_dict: dict[str, str | int]) -> NewStyleSignedTransaction:
        """Get SignedTransaction from dict."""
        if not isinstance(signed_transaction_dict, dict) and len(signed_transaction_dict) == 5:
            msg = f"Invalid for conversion. Found object: {signed_transaction_dict}."
            raise ValueError(  # pragma: nocover
                msg
            )
        return NewStyleSignedTransaction(
            raw_transaction=HexBytes(cast(str, signed_transaction_dict["raw_transaction"])),
            hash=HexBytes(cast(str, signed_transaction_dict["hash"])),
            r=cast(int, signed_transaction_dict["r"]),
            s=cast(int, signed_transaction_dict["s"]),
            v=cast(int, signed_transaction_dict["v"]),
        )
