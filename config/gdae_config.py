import os

db_conn = {
    'host': '127.0.0.1',
    # 'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    # 'password': "omJrdJRowQDLX8B8",
    # 'password': b"<+'\xd7\x12\xe9\xf0\xc4N\xe0\xc1\xdc\xfd5\xe1\xf4n\n\xc5\xb0\x86\xf3\xd3\xda\x8a\xe3\x17\xf6\x8aS\xab*",
    'password': b'\xd0\xf8lr\x14\x9c\xa6\xcf\x190-\xc7\xe7\xd0\x00\xd8_\xbb"_\x81]V\xc85\xae\x10\xe4*M\xdb\xc9',
    'db': 'dgv'
}
logger_config = {
    'level': 40,  # debug 10,info 20, warning 30, error 40
    'format': '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    'datefmt': '%a, %d %b %Y %H:%M:%S',
    'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/gaegae2_transfer_exchange.log'),
    'filemode': 'a'
}

COIN_WITHDRAW_CONFIG = {
    'ATOMLTC': {
        'audit_min_amount': 100,
    },
    'ATOMETH': {
        'audit_min_amount': 100,
    },
    'ATOMEOS': {
        'audit_min_amount': 100,
    },
}
# the private_key
ENCRYPT_KEY = b'3\xc4\x8c"\xe2\xbb\x82\x12["\xb5\x1b\xa6+\xb9n'
