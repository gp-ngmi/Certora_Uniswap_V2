
#!/bin/sh

certoraRun \
    contracts/UniswapV2Pair.sol                    \
    --verify UniswapV2Pair:certora/specs/UniswapV2Pair.spec \
    --solc solc-0.5.16                     \
    --msg "UniswapV2Pair verification"             \
    $*

