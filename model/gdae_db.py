import time

import pymysql

from common import gdae_log
from config import gdae_config
from core import gdae_constant
from common import globalvar as gl


class DbManage:
    def __init__(self):
        gdae_config.db_conn['password'] = gl.get_value('db_password')
        self.dbconn = pymysql.connect(**gdae_config.db_conn)

    def __del__(self):
        self.dbconn.close()

    # 查询不需要审核的体现请求
    def select_withdraw_request_noaudit(self, page_size):
        sql = "select * from dgv_withdraw_request where withdraw_status = 'INIT' and need_audit = 'NO' order by create_time asc limit {}".format(
            page_size)
        self.dbconn.connect()
        cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
        record = None
        if cursor.execute(sql) > 0:
            record = cursor.fetchall()
        self.dbconn.close()

        return record

    # 查询审核通过的体现请求
    def select_withdraw_request_audit(self, page_size):
        sql = "select * from dgv_withdraw_request where withdraw_status = 'INIT' and need_audit = 'YES' and audit_status = 'PASS' order by create_time asc limit {}".format(
            page_size)
        self.dbconn.connect()
        cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
        record = None
        if cursor.execute(sql) > 0:
            record = cursor.fetchall()
        self.dbconn.close()

        return record

    # get withdraw_request for confirm
    def select_withdrawRequest(self, start, pageSize):
        record = {}
        try:
            firstSQL = "SELECT * FROM dgv_withdraw_request WHERE audit_status ='INIT' and withdraw_status = 'INIT' " \
                       "limit %s,%s" % (start, pageSize)
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchall()
            cursor.close()
        except Exception as e:
            gdae_log.logger.error('%s' % e)
        return record

    # add by heshipeng
    # check whether transfer already
    def select_whithdrawOffchainTransactionRecord(self, request_uuid):
        record = None
        try:
            firstSQL = "SELECT * FROM dgv_withdraw_record WHERE " \
                       "request_uuid='%s' " % request_uuid
            self.dbconn.connect()
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute(firstSQL) > 0:
                record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            gdae_log.logger.error('%s' % e)

    # add transaction record
    def insert_withdrawOffchainTransactionRecord(self, record):

        cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)

        secondSQL = "INSERT INTO dgv_withdraw_record(request_uuid, user_id, \
                        to_account, fee_amount, amount, asset_code, from_account,  \
                        block_num,block_time, create_time, update_time) " \
                    "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                        record['request_uuid'], record['like_d_account'],
                        record['to_eos_account'],
                        record['fee_amount'],  record['amount'],
                        record['asset_code'], record['from_eos_account'], record['block_num'],
                        record['block_time'], record['create_time'], record['update_time'])
        cursor.execute(secondSQL)

    # 更新请求状态
    def update_withdrawRequestStatus(self, record):
        cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
        timeStamp = int(round(time.time() * gdae_constant.TIME_MULTIPLE))
        thirdSQL = "update dgv_withdraw_request set withdraw_status = '%s', update_time = '%s' " \
                   "where uni_uuid = '%s'" % (record['status'], timeStamp, record['uni_uuid'])
        cursor.execute(thirdSQL)

    # 提现请求成功直接扣掉冻结账户
    def update_offchainAmountFrozen(self, record):
        cursor = self.dbconn.cursor()
        timeStamp = int(round(time.time() * gdae_constant.TIME_MULTIPLE))
        SQL = "update dgv_user_account set amount_frozen = amount_frozen-'%s', update_time = '%s' " \
              "where user_id = '%s' and asset_code = '%s'" % (record['amount'], timeStamp, record['user_id'], record['asset_code'])
        cursor.execute(SQL)

    # 提现请求失败扣掉冻结账户的资金,加回到可用账户中
    def update_offchainAmountAvailable(self, record):
        cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)
        timeStamp = int(round(time.time() * gdae_constant.TIME_MULTIPLE))
        SQL = "update dgv_user_account set amount_available = amount_available+'%s', amount_frozen = amount_frozen-'%s', update_time = '%s' " \
              "where user_id = '%s' and asset_code = '%s'" % (record['amount'], record['amount'], timeStamp, record['user_id'], record['asset_code'])
        cursor.execute(SQL)

    def insert_account_record(self, record):
        try:
            cursor = self.dbconn.cursor(pymysql.cursors.DictCursor)

            secondSQL = "INSERT INTO dgv_account_record(from_user_id, to_user_id, \
                                    amount,asset_code, operation_type, deposit_withdraw_id,remark, create_time, update_time) " \
                        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                            record['from_user_id'], record['to_user_id'],
                            record['amount'],
                            record['asset_code'], record['operation_type'], record['deposit_withdraw_id'],
                            record['remark'], record['create_time'], record['update_time'])
            cursor.execute(secondSQL)
        except Exception as err:
            gdae_log.logger.error('insert_account_record failed. error:{}, record:{}'.format(err, record))



