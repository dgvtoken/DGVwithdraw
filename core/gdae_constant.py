# bitshares
nobroadcast = False  # Safety mode
witness_url = "ws://47.92.108.254:31201"
send_account = "reverve-fund"
send_address = "ONE8Sgjb5po5RKKGx7fSSRYMBsT3vAkMRRZUtLy7PCaSstLf1mXge"
wif = b'g\xd7V\x13\xffA:\xea\x16\x05\x8e\xddrO\x92\x86pFK\xdb\xe0\xa5\xedu\xa1\xfb_\x994\xdf\x1f\x9d\xd83\xdf\xc6H\x9a\xfa\xbb\xe9\xd0\x17\x8b_\xe2\xf9\xc7Au\xc0\nu\xb9\xa3\x1f\x94d\xe1\xb7\x96\xe7"\xe7'

# sleep time setting
SLEEP_STEP_TIMEOUT = 5

#

# mortgage status
MORTGAGE_RETURN_STATUS = {
    'NEW': 'NEW',
    'SUCCESS': 'SUCCESS',
    'FAIL': 'FAIL'
}

AUDIT_STATUS = {
    'INIT': 'INIT',
    'PASS': 'PASS',
    'NOPASS': 'NOPASS'
}

# mortgage_transaction_record status
ASSET_STATUS = {
    'INIT': 'INIT',
    'SUCCESS': 'SUCCESS',
    'FAILURE': 'FAILURE'
}

PAGE_START = 0

PAGE_SIZE = 50
# 转账的查询页数
PAGE_SIZE_SEND = 1

# time stamp multiple
TIME_MULTIPLE = 1000
# 抵押命令
CMD_MORTGAGE = "MORTGAGE"
# 归还命令
CMD_MORTGAGE_RETURN = "RETURN"
