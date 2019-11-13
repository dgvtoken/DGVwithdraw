import uuid

import gdae_db
import gdae_log

if __name__ == "__main__":
    record = {}
    record['uni_uuid'] = uuid.uuid1()
    # record['out_tx_id'] = '1.2.35'
    record['account_id'] = '1.2.5515'
    record['account_name'] = 'testhsp875'
    record['asset_code'] = 'IOUBTS'
    record['amount'] = 1.0
    # record['category'] = 'ceshi'
    # record['from_address'] = 'ceshidizhi'
    # record['to_address'] = 'ceshidizhi'
    # record['contract_address'] = 'ceshidizhi'
    # record['block_height'] = '0'
    # record['last_block_height'] = '0'
    # record['block_time'] = '0'
    # record['confirmations'] = '0'
    # record['deposit_status'] = 'CONFIRMED'
    # record['fail_message'] = ''
    record['need_audit'] = 1
    record['audit_status'] = 3
    record['request_status'] = 1
    record['create_time'] = 0
    record['update_time'] = 0
    gdae_db.DbManage().insert_withdrawOffchainRequest(record)