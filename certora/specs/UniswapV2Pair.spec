using ERC20A as ERC20a
using ERC20B as ERC20b

methods {
    mint(address) returns(uint) envfree
    burn(address) returns(uint) envfree
    swap(uint,uint,address,bytes) envfree
    balanceOf(address)         returns(uint) envfree
    totalSupply()              returns(uint) envfree
    getReserve()               returns(uint112) envfree
}

/*
rule swap k / ?
*/


/// mint must sends token to the user
rule mintSpec {
    address user; 
    env e;
    /*
    Try to send token
    uint amount0; uint amount1;
    uint reserve0; uint reserve1;
    (reserve0,reserve1)=getReserves();
    Send token ?
    maybe mint is not envfree
    */
    uint amount = mint(user);
    minimum = Math.min(amount0.mul(totalSupply()  ) / _reserve0, amount1.mul(totalSupply()) / _reserve1);
    assert amount != 0,"no token is minted";
    assert amount >= minimum,"not enough token is minted";
}

/// mint must revert  if liquidity amount0 or amount 1 is equal to 0
rule mintRevert {
    address user; 
    env e;
    /*
    Try to send token
    uint amount0; uint amount1;
    uint reserve0; uint reserve1;
    (reserve0,reserve1)=getReserves();
    Send token ?
    maybe mint is not envfree
    */
    require amount0=0;
    mint@withrevert(to);
    assert lastReverted,
        "";
    
}

/// mint must not revert unless
///    - amount0 or amount 1 is equal to 0
rule mintDoesntRevert {
    address user; 
    env e;
    /*
    Try to send token
    uint amount0; uint amount1;
    uint reserve0; uint reserve1;
    (reserve0,reserve1)=getReserves();
    require amount0!=0;
    require amount1!=0;
    Send token ?
    maybe mint is not envfree
    */
    mint@withrevert(to);
    assert !lastReverted,
        "";
}

/*
rules for burn :
    - burnSpec, where we assert user get both tokens
    - burnRevert, where no lp token is sending
    - burnDoesntRevert, unless no lp token is send
*/

/*
rules for swap :
    - swapSpec, where user get tokens
    - swapRevert1, where amount0Out and amount1Out are 0
    - swapRevert2, where reserves are not enough
    - swapRevert3, where we are sending token to contract token of the pool
    - swapRevert4, where user doesn't get back token
    - swapRevert5, where invariant K is break
    - swapDoesntRevert, if we sent a minimum amount 

invariant for swap :
    - K = balance0*balance1 >= reserve0*reserve1
*/

//// Part 4: ghosts and hooks //////////////////////////////////////////////////

//reserves is always less are equal to balances
invariant reservesLESBalances()
    (reserve0,reserve1)=getReserves();
    reserve0<=ERC20a.balanceOf(address(this))
    reserve1<=ERC20b.balanceOf(address(this))

