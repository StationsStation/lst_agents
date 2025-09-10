#!/usr/bin/env bash

function generate_contracts() {
    local abi_path=$1
    local contract_name=$2
    local contract_author=lstolas

    echo removing old contract at packages/${contract_author}/contracts/${contract_name}
    rm -rf packages/${contract_author}/contracts/${contract_name}
    adev scaffold contract --from-abi "$abi_path" "${contract_author}/${contract_name}"
}

generate_contracts ../olas-lst/out/StakingTokenLocked.sol/StakingTokenLocked.json lst_staking_token_locked
generate_contracts ../olas-lst/out/Collector.sol/Collector.json lst_collector
generate_contracts ../olas-lst/out/ActivityModule.sol/ActivityModule.json lst_activity_module
generate_contracts ../olas-lst/out/Distributor.sol/Distributor.json lst_distributor
generate_contracts ../olas-lst/out/UnstakeRelayer.sol/UnstakeRelayer.json lst_unstake_relayer
generate_contracts ../olas-lst/out/DefaultStakingProcessorL2.sol/DefaultStakingProcessorL2.json lst_staking_processor_l2
generate_contracts ../olas-lst/out/StakingManager.sol/StakingManager.json lst_staking_manager
