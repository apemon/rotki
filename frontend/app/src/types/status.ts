export enum Status {
  NONE,
  LOADING,
  REFRESHING,
  PARTIALLY_LOADED,
  LOADED
}

export enum Section {
  NONE,
  ASSET_MOVEMENT,
  TRADES,
  TX,
  BLOCKCHAIN_BTC,
  BLOCKCHAIN_BCH,
  BLOCKCHAIN_ETH,
  BLOCKCHAIN_ETH2,
  BLOCKCHAIN_KSM,
  BLOCKCHAIN_DOT,
  BLOCKCHAIN_AVAX,
  STAKING_ETH2,
  STAKING_ETH2_DEPOSITS,
  STAKING_ETH2_STATS,
  STAKING_KRAKEN,
  LEDGER_ACTIONS,
  PRICES,
  EXCHANGES,
  MANUAL_BALANCES,
  L2_LOOPRING_BALANCES,
  DEFI_COMPOUND_BALANCES,
  DEFI_COMPOUND_HISTORY,
  DEFI_OVERVIEW,
  DEFI_AAVE_BALANCES,
  DEFI_AAVE_HISTORY,
  DEFI_BORROWING_HISTORY,
  DEFI_LENDING,
  DEFI_LENDING_HISTORY,
  DEFI_BORROWING,
  DEFI_BALANCES,
  DEFI_DSR_BALANCES,
  DEFI_DSR_HISTORY,
  DEFI_MAKERDAO_VAULT_DETAILS,
  DEFI_MAKERDAO_VAULTS,
  DEFI_YEARN_VAULTS_HISTORY,
  DEFI_YEARN_VAULTS_BALANCES,
  DEFI_AIRDROPS,
  DEFI_UNISWAP_V2_BALANCES,
  DEFI_UNISWAP_V3_BALANCES,
  DEFI_UNISWAP_EVENTS,
  DEFI_BALANCER_BALANCES,
  DEFI_BALANCER_EVENTS,
  DEFI_YEARN_VAULTS_V2_HISTORY,
  DEFI_YEARN_VAULTS_V2_BALANCES,
  DEFI_SUSHISWAP_BALANCES,
  DEFI_SUSHISWAP_EVENTS,
  DEFI_LIQUITY_BALANCES,
  DEFI_LIQUITY_EVENTS,
  DEFI_LIQUITY_STAKING,
  DEFI_LIQUITY_STAKING_POOLS,
  NON_FUNGIBLE_BALANCES,
  REPORTS
}

export const defiSections: Section[] = [
  Section.DEFI_COMPOUND_BALANCES,
  Section.DEFI_COMPOUND_HISTORY,
  Section.DEFI_OVERVIEW,
  Section.DEFI_AAVE_BALANCES,
  Section.DEFI_AAVE_HISTORY,
  Section.DEFI_BORROWING_HISTORY,
  Section.DEFI_LENDING,
  Section.DEFI_LENDING_HISTORY,
  Section.DEFI_BORROWING,
  Section.DEFI_BALANCES,
  Section.DEFI_DSR_BALANCES,
  Section.DEFI_DSR_HISTORY,
  Section.DEFI_MAKERDAO_VAULT_DETAILS,
  Section.DEFI_MAKERDAO_VAULTS,
  Section.DEFI_YEARN_VAULTS_BALANCES,
  Section.DEFI_YEARN_VAULTS_HISTORY,
  Section.DEFI_YEARN_VAULTS_V2_BALANCES,
  Section.DEFI_YEARN_VAULTS_V2_HISTORY,
  Section.DEFI_LIQUITY_BALANCES,
  Section.DEFI_LIQUITY_EVENTS,
  Section.DEFI_UNISWAP_V2_BALANCES,
  Section.DEFI_UNISWAP_V3_BALANCES,
  Section.DEFI_UNISWAP_EVENTS,
  Section.DEFI_SUSHISWAP_BALANCES,
  Section.DEFI_SUSHISWAP_EVENTS,
  Section.DEFI_AIRDROPS
];
