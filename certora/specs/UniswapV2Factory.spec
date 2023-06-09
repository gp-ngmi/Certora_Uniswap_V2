
methods {
    createPair(address,address)         returns(uint) envfree
    allPairsLength()              returns(uint) envfree
    setFeeToSetter(address)
    setFeeTo(address)
    feeTo() envfree
    feeToSetter() envfree
    getPair(address,address) envfree
    allPair(uint) envfree
}

function isContract(address _pair) returns bool {
  uint32 size;
    assembly {
        size := extcodesize(a)
    }
    return (size > 0);
}



/// setFeeTo must set  `_feeTo` as the new value of 'feeTo'
rule setFeeToSpec {
    address _feeTo; 
    env e;
    require e.msg.sender == feeToSetter();
    setFeeTo(e,_feeTo);
    assert _feeTo == feeTo(),"setFeeTo must update the variable";
}

/// setFeeTo must revert  if msg.sender != feeToSetter
rule setFeeToRevert {
    address _feeTo; 
    env e;
    require e.msg.sender != feeToSetter();
    require _feeTo != feeTo();
    setFeeTo@withrevert(e,_feeTo);
    assert _feeTo != feeTo(),"setFeeTo must NOT update the variable";
    ssert lastReverted,
        " setFeeTo must revert  if msg.sender != feeToSetter";
    
}

/// setFeeTo must not revert unless
///    - msg.sender is not the feeToSetter
/// @title setFeeTo doesn't revert
rule setFeeToDoesntRevert {
    address _feeTo; 
    env e;
    require e.msg.sender == feeToSetter();
    setFeeTo@withrevert(e,_feeTo);
    assert !lastReverted;
}

/// setFeeToSetter must set  `_feeToSetter` as the new value of 'feeToSetter'
rule setFeeToSetterSpec {
    address _feeToSetter;
    env e;
    require e.msg.sender == feeToSetter();
    setFeeToSetter(e,_feeToSetter);
    assert _feeToSetter == feeToSetter(),"setFeeToSetter must update the variable";
}

/// setFeeToSetter must revert  if msg.sender != feeToSetter
rule setFeeToSetterRevert {
    address _feeToSetter;
    env e;
    require e.msg.sender != feeToSetter();
    require _feeToSetter != feeToSetter();
    setFeeToSetter@withrevert(e,_feeToSetter);
    assert _feeToSetter != feeToSetter(),"setFeeToSetter must NOT update the variable";
    ssert lastReverted,
        " setFeeToSetter must revert  if msg.sender != feeToSetter";
    
}

/// setFeeToSetter must not revert unless
///    - msg.sender is not the feeToSetter
/// @title setFeeToSetter doesn't revert
rule setFeeToSetterDoesntRevert {
    address _feeToSetter; 
    env e;
    require e.msg.sender == feeToSetter();
    setFeeToSetter@withrevert(e,_feeToSetter);
    assert !lastReverted;
}

////// createPair create a new Pool
rule createPairSpec {
    address tokenA; address tokenB;
    require tokenA != tokenB;
    //require getPair(tokenA,tokenB) == address(0);
    require tokenA != address(0);
    require tokenB != address(0);
    address _pair = createPair(tokenA, tokenB);

    //assert address(_pair).code.length >0,""; KO
    //assert isContract(address(pair)) == true,"not a deloyed contract; KO
    assert _pair == getPair(tokenA,tokenB),
        "";
    assert _pair == getPair(tokenB,tokenA),
        "";
    
}

/// createPair must revert
rule createPairReverts1 {
    address tokenA; address tokenB;
    require tokenA == tokenB;
    //require getPair(tokenA,tokenB) == address(0);
    require tokenA != address(0);
    require tokenB != address(0);
    createPair@withrevert(tokenA, tokenB);

    assert lastReverted,
        "";
}

/// createPair must revert
rule createPairReverts2 {
    address tokenA; address tokenB;
    require tokenA != tokenB;
    //require getPair(tokenA,tokenB) == address(0);
    require tokenA == address(0);
    require tokenB != address(0);
    createPair@withrevert(tokenA, tokenB);

    assert lastReverted,
        "";
}

/// createPair must revert
rule createPairReverts3 {
    address tokenA; address tokenB;
    require tokenA != tokenB;
    //require getPair(tokenA,tokenB) == address(0);
    require tokenA != address(0);
    require tokenB == address(0);
    createPair@withrevert(tokenA, tokenB);

    assert lastReverted,
        "";
}

/// createPair must revert
rule createPairReverts4 {
    address tokenA; address tokenB;
    require tokenA != tokenB;
    require tokenA != address(0);
    require tokenB != address(0);
    //require getPair(tokenA,tokenB) != address(0);
    
    createPair@withrevert(tokenA, tokenB);

    assert lastReverted,
        "";
}


/// createPair must not revert unless
///    - tokenA or tokenB is equal to 0x0,
///    - tokenA == tokenB 
///    - The pair is not created,
///
/// @title createPair doesn't revert
rule createPairDoesntRevert {
    address tokenA; address tokenB;
    require tokenA != tokenB;
    //require getPair(tokenA,tokenB) == address(0);
    require tokenA != address(0);
    require tokenB != address(0);
    createPair@withrevert(tokenA, tokenB);
    assert !lastReverted;
}


//// Part 4: ghosts and hooks //////////////////////////////////////////////////

ghost mathint sum_of_pairs {
    init_state axiom sum_of_pairs == 0;
}

hook Sstore allPairs[KEY uint a] address new_value (address old_value) STORAGE {
    // when a new pair is created, update ghost
    sum_of_pairs = sum_of_pairs + 1;
}

invariant totalAllPairsIsSumOfPairs()
    allPairsLength() == sum_of_pairs

