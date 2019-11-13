#!/usr/bin/ python3

import getpass
import os
import sys
import time
from multiprocessing import Process

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from common import gdae_log
from common import globalvar as gl, one_encrypt
from config import gdae_config
from config.eos_config import walletPwd
from core import gdae_constant
from core.gdae_constant import SLEEP_STEP_TIMEOUT
from core.withraw_atom_send import WithdrawAtomSend


def withdraw_atom_send():
    try:
        while True:
            confirm = WithdrawAtomSend()
            confirm.runloop()
            # 休眠指定时间后继续执行
            time.sleep(SLEEP_STEP_TIMEOUT)
    except Exception as e:
        gdae_log.logger.error('Send withdraw return asset failed')
        gdae_log.logger.error('%s' % e)


if __name__ == '__main__':
    # mod by hsp 18 1-25 add aes encrypt
    try:
        input = getpass.getpass('please input password:')
        key = input.strip()
        if key != one_encrypt.decrypt(gdae_config.ENCRYPT_KEY, key).strip():
            print('password error')
            sys.exit(0)
        gl._init()

        gl.set_value('db_password', one_encrypt.decrypt(gdae_config.db_conn['password'], key).strip())
        gl.set_value('walletPwd', one_encrypt.decrypt(walletPwd, key).strip())

    except Exception as e:
        print('encrypt text error')
        sys.exit(0)

    print(int(round(time.time() * gdae_constant.TIME_MULTIPLE)))
    # WithdrawAtomSend()

    process_list = list()
    pc = Process(target=withdraw_atom_send, args=())
    process_list.append(pc)

    for proc in process_list:
        proc.start()
    #
    for proc in process_list:
        proc.join()

    print("all process finished")
