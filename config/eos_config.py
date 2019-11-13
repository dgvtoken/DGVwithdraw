# -*- coding:utf-8 -*-

basePath = "cleos"

walletUrl = "http://127.0.0.1:port"

nodeUrl = "http://47.52.127.232:80"

# walletPwd = b'u98w\xa0\xc5\xe3\xac)\x8e\xda\x83F\xa8\t\x96\xea\x95%\x86\xb0\x07~\xdc\x7f:\x9cmN[\xc7\x16,\xbf\xd8\x19\xec\xf3zi\x9d\xb1\x07t\x11\xfc\t\xcd\x17sV\xe4\x80\x82\xe8\xa6\x07w\x0cZ\xef\xe5\xe3\x9d'
walletPwd = b'\xc5aP\xeb<\xe8\x11\xfb\xa3\x1f4\x1aY\xc5(\xa9\x8a8_?\x93\rl\x00\xd1f&\xf5\xca\x03?\nPC\x93\xac\xe0\x04<\x89\xe9\xb2YP\xdd\xb8$\xfb\x89\x04\xe4\x080X\\Dm(b\xb5\x9aqn\x0e'

agent = "*****"

contract_name = 'eosio.token'
min_precision = 4

act = [
    'onblock',
    'transfer'
]

chain_id = "****"

# account_name = 'onechaindapp'

api_code = {
    'SUCCESS': '100200',
    'FAIL': '100500'
}

FEE_AMOUNT = '0.1'

WITHDRAW_MIN = 0.1