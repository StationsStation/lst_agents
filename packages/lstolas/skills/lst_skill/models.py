"""Strategy for the lst agent."""

from pathlib import Path
from functools import cached_property

from aea.skills.base import Model
from aea.contracts.base import Contract, contract_registry
from aea_ledger_ethereum import Address, EthereumApi
from aea.configurations.loader import ComponentType, load_component_configuration

from packages.lstolas.contracts.lst_collector import PUBLIC_ID as LST_COLLECTOR_PUBLIC_ID
from packages.eightballer.contracts.amb_gnosis import PUBLIC_ID as AMB_LAYER_2_PUBLIC_ID
from packages.eightballer.contracts.amb_mainnet import PUBLIC_ID as AMB_MAINNET_PUBLIC_ID
from packages.lstolas.contracts.lst_collector.contract import LstCollector
from packages.eightballer.contracts.amb_gnosis.contract import AmbGnosis as AmbLayer2
from packages.eightballer.contracts.amb_mainnet.contract import AmbMainnet


ROOT = Path(__file__).parent.parent.parent.parent


def load_contract(contract_path: Path) -> Contract:
    """Helper function to load a contract."""
    configuration = load_component_configuration(ComponentType.CONTRACT, contract_path)
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

    # bridge contract addresses
    layer_2_amb_home: Address
    layer_1_amb_home: Address

    def __init__(self, **kwargs):
        """Initialize the strategy of the lst agent."""
        self.layer_1_api = EthereumApi(address=kwargs.pop("layer_1_rpc_endpoint"))
        self.layer_2_api = EthereumApi(address=kwargs.pop("layer_2_rpc_endpoint"))

        self.lst_collector_address = kwargs.pop("lst_collector_address")

        self.layer_2_amb_home = kwargs.pop("layer_2_amb_home")
        self.layer_1_amb_home = kwargs.pop("layer_1_amb_home")

        super().__init__(**kwargs)

    @cached_property
    def lst_collector_contract(self) -> LstCollector:
        """Get the LST Collector contract."""
        return load_contract(ROOT / LST_COLLECTOR_PUBLIC_ID.author / "contracts" / LST_COLLECTOR_PUBLIC_ID.name)

    @cached_property
    def amb_mainnet_contract(self) -> AmbMainnet:
        """Get the AMB Mainnet contract."""
        return load_contract(ROOT / AMB_MAINNET_PUBLIC_ID.author / "contracts" / AMB_MAINNET_PUBLIC_ID.name)

    @cached_property
    def layer_2_amb_home_contract(self) -> AmbLayer2:
        """Get the AMB Layer 2 contract."""
        return load_contract(ROOT / AMB_LAYER_2_PUBLIC_ID.author / "contracts" / AMB_LAYER_2_PUBLIC_ID.name)
