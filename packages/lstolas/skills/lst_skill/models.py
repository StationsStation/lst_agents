"""Strategy for the lst agent."""

from typing import Any, cast
from pathlib import Path
from functools import cached_property

from aea.skills.base import Model
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import Address, EthereumApi, EthereumCrypto
from aea.configurations.base import ContractConfig
from aea.configurations.loader import load_component_configuration
from aea.configurations.data_types import ComponentType

from packages.eightballer.contracts.erc_20 import PUBLIC_ID as ERC20_PUBLIC_ID
from packages.lstolas.contracts.lst_collector import PUBLIC_ID as LST_COLLECTOR_PUBLIC_ID
from packages.eightballer.contracts.amb_gnosis import PUBLIC_ID as AMB_LAYER_2_PUBLIC_ID
from packages.eightballer.contracts.amb_mainnet import PUBLIC_ID as AMB_MAINNET_PUBLIC_ID
from packages.eightballer.contracts.erc_20.contract import Erc20
from packages.lstolas.contracts.lst_unstake_relayer import PUBLIC_ID as LST_UNSTAKE_RELAYER_PUBLIC_ID
from packages.eightballer.contracts.amb_gnosis_helper import PUBLIC_ID as AMB_GNOSIS_HELPER_PUBLIC_ID
from packages.lstolas.contracts.lst_collector.contract import LstCollector
from packages.eightballer.contracts.amb_gnosis.contract import AmbGnosis as AmbLayer2
from packages.eightballer.contracts.amb_mainnet.contract import AmbMainnet
from packages.lstolas.contracts.lst_unstake_relayer.contract import LstUnstakeRelayer
from packages.eightballer.contracts.amb_gnosis_helper.contract import AmbGnosisHelper


ROOT = Path(__file__).parent.parent.parent.parent

GAS_PREMIUM = 1.2  # multiplier to add to the gas price


def load_contract(contract_path: Path) -> Contract:
    """Helper function to load a contract."""
    configuration = cast(ContractConfig, load_component_configuration(ComponentType.CONTRACT, contract_path))
    configuration._directory = contract_path  # noqa
    if str(configuration.public_id) not in contract_registry.specs:
        # load contract into sys modules
        Contract.from_config(configuration)
    return contract_registry.make(str(configuration.public_id))


class LstStrategy(Model):
    """This class implements the strategy of the lst agent."""

    layer_1_api: EthereumApi
    layer_2_api: EthereumApi

    # lst contract addresses
    lst_collector_address: Address
    lst_unstake_relayer_address: Address
    lst_distributor_address: Address

    # bridge contract addresses
    layer_2_amb_home: Address
    layer_1_amb_home: Address
    layer_2_amb_helper: Address
    # token contract address
    layer_1_olas_token_address: Address

    def __init__(self, **kwargs):
        """Initialize the strategy of the lst agent."""
        self.layer_1_api = EthereumApi(address=kwargs.pop("layer_1_rpc_endpoint"))
        self.layer_2_api = EthereumApi(address=kwargs.pop("layer_2_rpc_endpoint"))

        self.lst_collector_address = kwargs.pop("lst_collector_address")
        self.lst_unstake_relayer_address = kwargs.pop("lst_unstake_relayer_address")
        self.lst_distributor_address = kwargs.pop("lst_distributor_address")

        self.layer_2_amb_home = kwargs.pop("layer_2_amb_home")
        self.layer_1_amb_home = kwargs.pop("layer_1_amb_home")
        self.layer_2_amb_helper = kwargs.pop("layer_2_amb_helper")

        self.layer_1_olas_token_address = kwargs.pop("layer_1_olas_address")

        super().__init__(**kwargs)

    @cached_property
    def lst_collector_contract(self) -> LstCollector:
        """Get the LST Collector contract."""
        return cast(
            LstCollector,
            load_contract(ROOT / LST_COLLECTOR_PUBLIC_ID.author / "contracts" / LST_COLLECTOR_PUBLIC_ID.name),
        )

    @cached_property
    def amb_mainnet_contract(self) -> AmbMainnet:
        """Get the AMB Mainnet contract."""
        return cast(
            AmbMainnet, load_contract(ROOT / AMB_MAINNET_PUBLIC_ID.author / "contracts" / AMB_MAINNET_PUBLIC_ID.name)
        )

    @cached_property
    def layer_2_amb_home_contract(self) -> AmbLayer2:
        """Get the AMB Layer 2 contract."""
        return cast(
            AmbLayer2, load_contract(ROOT / AMB_LAYER_2_PUBLIC_ID.author / "contracts" / AMB_LAYER_2_PUBLIC_ID.name)
        )

    @cached_property
    def layer_2_amb_helper_contract(self) -> AmbGnosisHelper:
        """Get the AMB Gnosis Helper contract."""
        return cast(
            AmbGnosisHelper,
            load_contract(ROOT / AMB_GNOSIS_HELPER_PUBLIC_ID.author / "contracts" / AMB_GNOSIS_HELPER_PUBLIC_ID.name),
        )

    @cached_property
    def lst_unstake_relayer_contract(self) -> LstUnstakeRelayer:
        """Get the LST Unstake Relayer contract."""
        return cast(
            LstUnstakeRelayer,
            load_contract(
                ROOT / LST_UNSTAKE_RELAYER_PUBLIC_ID.author / "contracts" / LST_UNSTAKE_RELAYER_PUBLIC_ID.name
            ),
        )

    @cached_property
    def layer_1_olas_contract(self) -> Erc20:
        """Get the OLAS token contract."""
        return cast(Erc20, load_contract(ROOT / ERC20_PUBLIC_ID.author / "contracts" / ERC20_PUBLIC_ID.name))

    def build_transaction(self, ledger: EthereumApi, func: Any, value: int = 0):
        """Build the transaction."""

        nonce = ledger._try_get_transaction_count(self.sender_address)  # noqa: SLF001

        return func.build_transaction(
            {
                "from": self.crypto.address,
                "nonce": nonce,
                "gas": func.estimate_gas({"from": self.crypto.address, "value": value}),
                "gasPrice": int(ledger.api.eth.gas_price * GAS_PREMIUM),
                "value": value,
            }
        )

    @cached_property
    def crypto(self) -> EthereumCrypto:
        """Get EthereumCrypto."""
        return EthereumCrypto(private_key_path="ethereum_private_key.txt")

    @property
    def sender_address(self) -> Address:
        """Get the sender address."""
        return cast(Address, self.crypto.address)
