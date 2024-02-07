from app.calculations import add, sub,mul,div,InsufficientFunds,BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("creating 50rs bank account")
    return BankAccount(50)


@pytest.mark.parametrize("x,y,expected",[(3,2,5),(1,4,5),(1,6,7),(12,4,16)])
def testing_add(x,y,expected):
    print("testing add function")
    assert add(x,y) == expected
    
def testingg_sub():
    print("testing sub function")
    assert sub(5,3) == 2
    
def testingg_mul():
    print("testing sub function")
    assert mul(5,3) == 15
    
def testingg_div():
    print("testing sub function")
    assert div(1,2) == 0.5
    
def testing_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
    
def testing_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0   
    
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

@pytest.mark.parametrize("dep,wit,expected",[
    (200,100,100),(50,10000,40),(60,20,40),(12,4,8)])
  
def test_bank_trans(zero_bank_account,dep,wit,expected):
    zero_bank_account.deposit(dep)
    zero_bank_account.withdraw(wit)
    assert zero_bank_account.balance == expected
    
def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
     bank_account.withdraw(200)
    
    

    