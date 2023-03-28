methods {
    balanceOf(address)         returns(uint) envfree
    allowance(address,address) returns(uint) envfree
    totalSupply()              returns(uint) envfree
    transferFrom(address,address,uint) envfree
}





/// Transfer must move `amount` tokens from the caller's account to `recipient`
rule transferSpec {
    address sender; address recip; uint amount;
    env e;
    require e.msg.sender == sender;
    mathint balance_sender_before = balanceOf(sender);
    mathint balance_recip_before = balanceOf(recip);
    transfer(e, recip, amount);
    mathint balance_sender_after = balanceOf(sender);
    mathint balance_recip_after = balanceOf(recip);
    require sender != recip;
    assert balance_sender_after == balance_sender_before - amount,
        "transfer must decrease sender's balance by amount";
    assert balance_recip_after == balance_recip_before + amount,
        "transfer must increase recipient's balance by amount";
}
/// Transfer must revert if the sender's balance is too small
rule transferReverts {
    env e; address recip; uint amount;

    require balanceOf(e.msg.sender) < amount;

    transfer@withrevert(e, recip, amount);

    assert lastReverted,
        "transfer(recip,amount) must revert if sender's balance is less than `amount`";
}


/// Transfer must not revert unless
///    - sender doesn't have enough funds,
///    - or the message value is nonzero,
///    - or the recipient's balance would overflow,
///
/// @title Transfer doesn't revert
rule transferDoesntRevert {
    env e; address recipient; uint amount;
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;
    require recipient != 0;
    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

////// TransferFrom must move `amount` tokens from the sender's account to `recipient`
rule transferFromSpec {
    address sender; address recip; uint amount;
    env e;

    require approve(sender, amountAllowance) >= amount;
    mathint balance_sender_before = balanceOf(sender);
    mathint balance_recip_before = balanceOf(recip);
    transferFrom(sender, recip, amount);
    mathint balance_sender_after = balanceOf(sender);
    mathint balance_recip_after = balanceOf(recip);
    require sender != recip;
    assert balance_sender_after == balance_sender_before - amount,
        "transfer must decrease sender's balance by amount";
    assert balance_recip_after == balance_recip_before + amount,
        "transfer must increase recipient's balance by amount"
}


rule transferFromRevertsAmounts {
    env e; address sender; address recip; uint amount; uint amountAllowance;

    require balanceOf(e.msg.sender) < amount;
    require approve(sender, amountAllowance) >= amount;

    transferFrom@withrevert(sender, recip, amount);

    assert lastReverted,
        "transferFrom(from, to, value) must revert if from's balance is less than `amount`";
}

rule transferFromRevertsAllowance {
    env e; address sender; address recip; uint amount; uint amountAllowance;

    require balanceOf(e.msg.sender) > amount;
    require approve(sender, amountAllowance) < amount;

    transferFrom@withrevert(sender, recip, amount);

    assert lastReverted,
        "transferFrom(from, to, value) must revert if from's allowance is less than `amount`";
}

/// Transfer must not revert unless
///    - sender doesn't have enough funds,
///    - sender doesn't have enough allowance,
///    - or the message value is nonzero,
///    - or the recipient's balance would overflow,
///    - or the message sender is 0
///
/// @title transferFrom doesn't revert
rule transferFromDoesntRevert {
    env e; address sender; address recipient; uint amount; uint amountAllowance;
    require balanceOf(e.msg.sender) > amount;
    require approve(sender, amountAllowance) >= amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    transferFrom@withrevert(sender, recipient, amount);
    assert !lastReverted;
}

//// Part 2: parametric rules //////////////////////////////////////////////////

/// If `approve` changes a holder's allowance, then it was called by the holder
rule onlyHolderCanChangeAllowance {
    address holder; address spender;
    mathint allowance_before = allowance(holder, spender);
    method f; env e; calldataarg args; // was: env e; uint256 amount;
    f(e, args);                        // was: approve(e, spender, amount);
    mathint allowance_after = allowance(holder, spender);
    assert allowance_after > allowance_before => e.msg.sender == holder,
        "approve must only change the sender's allowance";
    assert allowance_after > allowance_before =>
        (f.selector == approve(address,uint).selector || f.selector == increaseAllowance(address,uint).selector),
        "only approve and increaseAllowance can increase allowances";
}

//// Part 3: invariants ////////////////////////////////////////////////////////

/// @dev This rule is unsound!
invariant balancesBoundedByTotalSupply(address alice, address bob)
    balanceOf(alice) + balanceOf(bob) <= totalSupply()
{
    preserved transfer(address recip, uint256 amount) with (env e) {
        require recip        == alice || recip        == bob;
        require e.msg.sender == alice || e.msg.sender == bob;
    }

    preserved transferFrom(address from, address to, uint256 amount) {
        require from == alice || from == bob;
        require to   == alice || to   == bob;
    }
}

//// Part 4: ghosts and hooks //////////////////////////////////////////////////

ghost mathint sum_of_balances {
    init_state axiom sum_of_balances == 0;
}

hook Sstore balanceOf[KEY address a] uint new_value (uint old_value) STORAGE {
    // when balance changes, update ghost
    sum_of_balances = sum_of_balances + new_value - old_value;
}

invariant totalSupplyIsSumOfBalances()
    totalSupply() == sum_of_balances

