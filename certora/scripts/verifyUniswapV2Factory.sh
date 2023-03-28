#!/bin/sh

certoraRun \
    contracts/UniswapV2Factory.sol                    \
    --verify UniswapV2Factory:certora/specs/UniswapV2Factory.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2Factory verification"             \
    $*

