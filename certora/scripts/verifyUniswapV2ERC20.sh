#!/bin/sh

certoraRun \
    contracts/UniswapV2ERC20.sol                    \
    --verify UniswapV2ERC20:certora/specs/UniswapV2ERC20.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2ERC20 verification"             \
    $*
