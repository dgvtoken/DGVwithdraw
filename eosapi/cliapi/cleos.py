# -*- coding:utf-8 -*-

import subprocess
import json
from config.eos_config import *
# from util import decimal


class Cleos():

    """
    EOS相关操作类
    """

    def __init__(self, agent=agent,
                 basePath=basePath, walletUrl=walletUrl,
                 walletPwd=walletPwd, nodeUrl=nodeUrl):
        self.agent = agent
        self.basePath = basePath
        self.walletUrl = walletUrl
        self.walletPwd = walletPwd
        self.nodeUrl = nodeUrl

    def exec(self, cmd=None):
        childPs = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = childPs.communicate()
        return self.execResult(out)

    def openWallet(self):
        cmd = self.basePath + ' --wallet-url ' + self.walletUrl + ' --url ' + self.nodeUrl + ' wallet unlock -n default ' \
              '--password ' + self.walletPwd
        out = self.exec(cmd=cmd)
        return out

    def transfer(self, to, amount, asset_code, memo):
        cmd = self.basePath + ' --wallet-url ' + self.walletUrl + ' --url ' + self.nodeUrl + ' transfer ' + self.agent + \
              ' ' + to + ' "' + self.moneyFormat(str(amount), 4) + ' ' + asset_code + '" "' + memo + '" -j'
        print(cmd)
        out = self.exec(cmd)
        return out

    def transfer2(self, to, amount, asset_code, contract, memo, min_precision):
        money = self.moneyFormat(str(amount), min_precision) + ' ' + asset_code
        action = self.action_of( self.agent, to, money, memo)
        cmd = self.basePath + ' --wallet-url ' + self.walletUrl + ' --url ' + self.nodeUrl + ' push action ' + contract + ' transfer \'' + \
              action + '\' --permission ' + self.agent + '@active'
        print(cmd)
        out = self.exec(cmd)
        return out

    def getHistory(self, account, position=0, offset=10):
        cmd = self.basePath + ' --wallet-url ' + self.walletUrl + ' --url ' + self.nodeUrl + ' get actions ' + account + \
              ' ' + position + ' ' + offset + ' -j'
        out = self.exec(cmd)
        return out

    def getBlock(self, block_num_or_id):
        cmd = self.basePath + ' get block ' + block_num_or_id
        out = self.exec(cmd)
        return out

    def getInfo(self):
        cmd = self.basePath + ' --wallet-url ' + self.walletUrl + ' --url ' + self.nodeUrl + ' get info'
        out = self.exec(cmd)
        return out

    def execResult(self, out):
        result = {}
        if out[1] and str(out[1]).__contains__("Error"):
            result['code'] = api_code['FAIL']
            result['message'] = out[1].decode('utf-8')
        else:
            result['code'] = api_code['SUCCESS']

        if out[0]:
            result['data'] = out[0].decode('utf-8')
        else:
            result['data'] = ''

        return result

    def moneyFormat(self, money, presion):
        data = str(money).split('.')
        i = data[0]
        f = data[1]
        presion = int(presion)
        if len(f) < presion:
           for a in range((presion - len(f))):
               f = f + '0'
        else:
           f = f[:presion]

        if f:
            return i + '.' + f
        else:
            # 精度为0的情况
            return i

    def action_of(self, payer, to, amount, memo):
        action = {"from": payer, "to": to, "quantity": amount, "memo": memo}
        return json.dumps(action)

if __name__ == '__main__':
    from config.common_config import *
    cleos = Cleos(agent=agent, basePath=basePath, walletUrl=walletUrl, walletPwd=walletPwd, nodeUrl=nodeUrl)
    # out = cleos.getInfo()
    # out = cleos.transfer('onechaintttt', '10', 'EOS', 'test')

    out = cleos.moneyFormat('0.1111111111', 4)
    import json
    print(out)