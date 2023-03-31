#!/bin/sh

certoraRun \
     contracts/UniswapV2ERC20.sol                    \
    --verify UniswapV2ERC20:certora/specs/sanity.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2ERC20 sanity"             \
    $*

certoraRun \
    contracts/UniswapV2Factory.sol                    \
    --verify UniswapV2Factory:certora/specs/sanity.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2Factory sanity"             \
    $*

certoraRun \
    contracts/UniswapV2Pair.sol                    \
    --verify UniswapV2Pair:certora/specs/sanity.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2Pair sanity"             \
    $*
