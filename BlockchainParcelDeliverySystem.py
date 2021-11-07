import I2C_LCD_driver #Import the I2C_LCD_driver package for displaying strings onto the LCD 
import RPi.GPIO as GPIO #Import the package used for controlling the GPIO pins of the RPi
from time import * #Import the time package for creating delays
import random #Import the random package to create unique passwords
import web3 #Import the web3 package to interact with Ethereum and the Ethereum Blockchain
from web3 import Web3

#connect to the Ethereum network through a node created via an Infura account
web3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/86c2e4bace77460da7f8e690b3c51215'))
#declare the Smart Contract Application Binary Interface for interaction with the smart contract
abi = '[{"constant":true,"inputs":[],"name":"ContractCompleted","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"ContractTerminated","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"CorrectCustomersPasswordEntered","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"CorrectSellersPasswordEntered","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"created_customers_password","type":"string"}],"name":"CustomersPassword","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"price","type":"string"},{"internalType":"string","name":"product","type":"string"}],"name":"DefineContract","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"IncorrectCustomersPasswordEntered","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"IncorrectSellersPasswordEntered","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"scanned_barcode","type":"string"}],"name":"ScannedBarcode","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"ScannedBarcodeIsCorrect","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"ScannedBarcodeIsIncorrect","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"created_sellers_password","type":"string"}],"name":"SellersPassword","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"created_barcode","type":"string"}],"name":"StoreBarcode","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[],"name":"receiveEth","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}]'
#store the Smart Contracts address, but make sure the format is correct, using a function called toChecksumAddress
addr = web3.toChecksumAddress('0x89d68d660998b8fBFB0859DeC892BBeAa8ecf426')
#communicate with the smart contract
contract = web3.eth.contract(address=addr, abi=abi) 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #Sets the pins to be referred to by the GPIO number rather than pin number
GPIO.setup(18, GPIO.OUT) #sets the GPIO 18 pin to an output pin (this is where the relay is connected)

#define the function to complete a payment from the customers ETH wallet to the sellers ETH wallet
def EthPayment(product_price):
    web3 = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/86c2e4bace77460da7f8e690b3c51215'))
    address1 = '0xc51D409f3e8089301dD98B0B882Cc5E9F4d8780d'
    address2 = '0x56e682255E39260a8BaB6381eBF14f246Efc7e23'

    private_key = 'b96f8f1dbfd9a6b22328bafb7a3abc181502bd9753c5b0ffda7120e9c7341aea'

    customer_address = Web3.toChecksumAddress(address1)
    seller_address = Web3.toChecksumAddress(address2)

    nonce = web3.eth.getTransactionCount(address1)

    tx = {
        'nonce': nonce,
        'to': seller_address,
        'value': web3.toWei(product_price, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei(40, 'gwei'),
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)

    tx_hash =  web3.eth.sendRawTransaction(signed_tx.rawTransaction)
 

screen = I2C_LCD_driver.lcd()
screen.lcd_clear()
price = input("Declare product price (in ETH):\n")
product = input("Enter the name/type of product:\n")
a = contract.functions.DefineContract(price, product).call()
print(a) #prints a return string from the smart contract function declaring the contract


#create product barcode
product_barcode = random.randint(11111,99999)
b = contract.functions.StoreBarcode(str(product_barcode)).call()
print(b)


#create password for seller to open box
correct_seller_password = random.randint(1111,9999)
correct_seller_password = int(correct_seller_password)
c = contract.functions.SellersPassword(str(correct_seller_password)).call()
print(c)


screen.lcd_display_string("Unlock with code,", 1)
screen.lcd_display_string("and scan parcel.", 2)

#receive input password from seller
seller_password = input("Enter password:\n")
seller_password = int(seller_password)

def Check_Seller_Code(password_entered, correct_password):
    while password_entered != correct_password:
        screen.lcd_clear()
        screen.lcd_display_string("Incorrect code!", 1)
        screen.lcd_display_string("Try again!", 2)
        d = contract.functions.IncorrectSellersPasswordEntered().call()
        print(d)
        password_entered = input("Enter password:\n")
        password_entered = int(password_entered)
    return password_entered

def Check_Customers_Code(password_entered, correct_password):
    while password_entered != correct_password:
        screen.lcd_clear()
        screen.lcd_display_string("Incorrect code!", 1)
        screen.lcd_display_string("Try again!", 2)
        i = contract.functions.IncorrectCustomersPasswordEntered().call()
        print(i)
        password_entered = input("Enter password:\n")
        password_entered = int(password_entered)
    return password_entered

seller_password = Check_Seller_Code(seller_password, correct_seller_password)

if seller_password == correct_seller_password:
    e = contract.functions.CorrectSellersPasswordEntered().call()
    print(e)
    screen.lcd_clear()
    screen.lcd_display_string("Correct code!", 1)
    screen.lcd_display_string("Scan parcel.", 2)
    sleep(2)
    GPIO.output(18, 1)
    screen.lcd_clear()
    screen.lcd_display_string("Opened", 1)
    sleep(0.9)
    GPIO.output(18, 0)
    screen.lcd_clear()
    screen.lcd_display_string("Please close box", 1)
    screen.lcd_display_string("after delivery.", 2)
    scanned_barcode = input("Scan Code: \n")
    scanned_barcode = int(scanned_barcode)
    f = contract.functions.ScannedBarcode(str(scanned_barcode)).call()
    print(f)
    
    
    if scanned_barcode == product_barcode:
        #create password for customer to open box
        correct_customer_password = random.randint(1111,9999)
        correct_customer_password = int(correct_customer_password)
        h = contract.functions.CustomersPassword(str(correct_customer_password)).call()
        print(h)
        g = contract.functions.ScannedBarcodeIsCorrect().call()
        print(g)
        screen.lcd_clear()
        screen.lcd_display_string("Enter password", 1)
        customer_password = int(input("Enter password: \n"))
        
        customer_password = Check_Customers_Code(customer_password, correct_customer_password)
        
        if customer_password == correct_customer_password:
            j = contract.functions.CorrectCustomersPasswordEntered().call()
            print(j)
            EthPayment(price)
            screen.lcd_clear()
            screen.lcd_display_string("Correct code!", 1)
            screen.lcd_display_string("Take your item.", 2)
            sleep(2)
            GPIO.output(18, 1)
            screen.lcd_clear()
            screen.lcd_display_string("Opened", 1)
            sleep(0.9)
            GPIO.output(18, 0)
            screen.lcd_clear()
            screen.lcd_display_string("Please close box", 1)
            l = contract.functions.ContractCompleted().call()
            print(l)

    else:
        k = contract.functions.ScannedBarcodeIsIncorrect().call()
        print(k)
        z = contract.functions.ContractTerminated().call()
        print(z)
        screen.lcd_clear()
        screen.lcd_display_string("Parcel is incorrect", 1)
        screen.lcd_display_string("Enter password", 2)
        correct_seller_password2 = random.randint(1111,9999)
        correct_seller_password2 = int(correct_seller_password)
        c2 = contract.functions.SellersPassword(str(correct_seller_password)).call()
        print(c2)
        seller_password2 = input("Enter password:\n")
        seller_password2 = int(seller_password)
        seller_password = Check_Seller_Code(seller_password2, correct_seller_password2)
        if seller_password == correct_seller_password:
            print("Seller has entered the correct password, the box will unlock and the incorrect package may be taken.")
            screen.lcd_clear()
            screen.lcd_display_string("Correct code!", 1)
            screen.lcd_display_string("Take parcel", 2)
            sleep(2)
            GPIO.output(18, 1)
            screen.lcd_clear()
            screen.lcd_display_string("Opened", 1)
            sleep(0.9)
            GPIO.output(18, 0)
            screen.lcd_clear()
            screen.lcd_display_string("Please close box", 1)eU
