import json
import time

from common import gdae_log
from common import globalvar as gl
from model import gdae_db
from . import gdae_constant
from config.eos_config import *
from eosapi.cliapi.cleos import Cleos


def construct_withdrawOffchainTransactionRecord(withdrawRequestRecord):
    timeStamp = int(round(time.time() * gdae_constant.TIME_MULTIPLE))

    transactionRecord = {}
    transactionRecord['request_uuid'] = withdrawRequestRecord['uni_uuid']
    transactionRecord['like_d_account'] = withdrawRequestRecord['user_id']
    transactionRecord['to_eos_account'] = withdrawRequestRecord['to_account']
    transactionRecord['from_eos_account'] = agent
    transactionRecord['fee_amount'] = 0
    transactionRecord['fee_asset'] = 'EOS'
    transactionRecord['amount'] = withdrawRequestRecord['amount']
    transactionRecord['asset_code'] = withdrawRequestRecord['asset_code']
    transactionRecord['block_num'] = withdrawRequestRecord['block_num']
    transactionRecord['block_time'] = withdrawRequestRecord['block_time']
    transactionRecord['create_time'] = timeStamp
    transactionRecord['update_time'] = 0
    return transactionRecord


def construct_account_record(record):
    time_stamp = int(round(time.time() * gdae_constant.TIME_MULTIPLE))

    rec = dict()
    rec['from_user_id'] = 0
    rec['to_user_id'] = record['user_id']
    rec['amount'] = record['amount']
    rec['asset_code'] = record['asset_code']
    rec['operation_type'] = 4
    rec['deposit_withdraw_id'] = record['id']
    rec['remark'] = ''
    rec['create_time'] = time_stamp
    rec['update_time'] = 0
    return rec


class WithdrawAtomSend(object):

    def __init__(self):
        super().__init__()
        self.db = gdae_db.DbManage()

    # 确认提现请求记录
    def ConfirmWithdrawRequest(self, cleos, recordList):
        for record in recordList[::-1]:
            try:
                # 检查提现请求是否已经完成
                exist_record = self.db.select_whithdrawOffchainTransactionRecord(record['uni_uuid'])
                if exist_record:
                    gdae_log.logger.error("Operate already, uni_uuid:{}".format(record['uni_uuid']))
                    continue
                # 检查提现金额是否有效
                if record['amount'] <= 0:
                    gdae_log.logger.error('amount is less than 0,like_d_account:{}, to_eos_account:{}'.format(
                        record['user_id'], record['to_account']))
                    continue
                # 检查是否需要审核
                if record['need_audit'] == 'YES':
                    # 检查审核是否通过
                    if record['audit_status'] == 'INIT' or record['audit_status'] == 'FAIL':
                        gdae_log.logger.error(
                            'audit status is init or fail,account_id:{}, account_name{}'.format(record['user_id'],
                                                                                                record['to_account']))
                        continue
                # transfer
                self.transferAndRecord(cleos, record)
            except Exception as e:
                gdae_log.logger.error('Confirm withdraw record fail, error: {}'.format(e))
                continue

    # 构造提现记录表的数据

    # 对交易做原子操作
    def transferAndRecord(self, cleos, record):
        # transaction begin
        try:
            result = cleos.getInfo()
            if result['code'] == api_code['FAIL']:
                gdae_log.logger.error('Get block info fail, result:{}'.format(result))
                raise Exception('Get block Info fail')
            head_block_info = json.loads(result['data'])
            record['block_num'] = str(head_block_info['head_block_num'])
            record['block_time'] = head_block_info['head_block_time']
            newTransactionRecord = construct_withdrawOffchainTransactionRecord(record)
            # 插入提现记录表
            self.db.insert_withdrawOffchainTransactionRecord(newTransactionRecord)
            # 更新请求表中请求状态
            record['status'] = 'SUCCESS'
            self.db.update_withdrawRequestStatus(record)
            self.db.update_offchainAmountFrozen(record)

            account_record = construct_account_record(record)
            self.db.insert_account_record(account_record)

            # memo = record['uni_uuid'] + ':' + str(record['user_id'])
            memo = str(record['memo'])
            contract = "eosio.token" if record['asset_code'] == "EOS" else "dgvtoken1533"
            result = cleos.transfer2(record['to_account'], record['amount'],
                                     record['asset_code'],
                                     contract, memo, min_precision)
            if not result:
                gdae_log.logger.error('transfer fail ,transfer return result null')
                raise Exception('transfer return null')

            if result.get('message') and str(result['message']).__contains__('Locked wallet'):
                cleos.openWallet()
                gdae_log.logger.error('wallet lock at this time, wait next for withdraw')
                time.sleep(gdae_constant.SLEEP_STEP_TIMEOUT)
                return

            if result['code'] != api_code['SUCCESS']:
                gdae_log.logger.error("transfer fail, result:{}".format(result))
                raise Exception('transfer error')

            self.db.dbconn.commit()

            gdae_log.logger.info(
                "transfer finish:account_name:{}, asset_code:{}, amount:{}".format(record['to_account'],
                                                                                   record['asset_code'],
                                                                                   record['amount']))

        except Exception as e:
            self.db.dbconn.rollback()
            gdae_log.logger.error('transfer fail,request:{0},stack trace:{1}'.format(record, e))
            try:
                record['status'] = 'FAIL'
                self.db.update_withdrawRequestStatus(record)
                self.db.update_offchainAmountAvailable(record)
                self.db.dbconn.commit()
            except Exception as err:
                self.db.dbconn.rollback()
                gdae_log.logger.error(
                    'fail,  check log and program!!!!,request:{}, error: {}'.format(record, err))

    def runloop(self):

        walletPwd = gl.get_value('walletPwd')
        cleos = Cleos(agent=agent, basePath=basePath, walletUrl=walletUrl, walletPwd=walletPwd, nodeUrl=nodeUrl)

        try:

            while True:
                noAuditList = self.db.select_withdraw_request_noaudit(gdae_constant.PAGE_SIZE)

                auditPassList = self.db.select_withdraw_request_audit(gdae_constant.PAGE_SIZE)
                resultList = []
                if noAuditList:
                    resultList += noAuditList

                if auditPassList:
                    resultList += auditPassList

                if not resultList:
                    time.sleep(gdae_constant.SLEEP_STEP_TIMEOUT)
                else:
                    self.ConfirmWithdrawRequest(cleos, resultList)

        except Exception as e:
            gdae_log.logger.error('runloop failed')
            gdae_log.logger.error(e)
