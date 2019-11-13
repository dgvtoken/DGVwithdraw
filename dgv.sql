use dgv;

-- 验证码
DROP TABLE IF EXISTS `dgv_verification_code`;
CREATE TABLE `dgv_verification_code` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `mobile` varchar(16) NOT NULL COMMENT '用户账号name',
  `code` char(6) NOT NULL COMMENT '验证码',
  `type` tinyint(4) unsigned NOT NULL COMMENT '1注册,2修改登录密码,3修改安全码密码,4忘记密码',
  `used` tinyint(4) unsigned DEFAULT '0' COMMENT '是否使用, 1=使用,2=过期',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_mobile_type_used` (`mobile`, `type`, `used`),
  KEY `idx_mobile_used` (`mobile`, `used`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='验证码';

-- --------------------------------------------
-- 用户信息表
-- --------------------------------------------

DROP TABLE IF EXISTS `dgv_user`;
CREATE TABLE `dgv_user` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `mobile` varchar(16) NOT NULL COMMENT '用户账号name',
  `login_password` varchar(64) NOT NULL COMMENT '登录密码',
  `login_salt` char(32) NOT NULL COMMENT '登录密码加盐',
  `user_code_invite` varchar(8) DEFAULT NULL COMMENT '用户邀请码',
  `code_invite` varchar(8)  DEFAULT NULL COMMENT '别人的邀请码',
  `safety_password` varchar(64) NOT NULL COMMENT '交易安全码,需加密',
  `safety_salt` char(32) NOT NULL COMMENT '安全码加盐',
  `auth_level` tinyint(4) unsigned DEFAULT 100 NOT NULL COMMENT '100普通用户,1是群主(满足邀请的条件)',
  `email` varchar(70) DEFAULT NULL COMMENT '邮箱',
  `sex` tinyint(4) DEFAULT NULL COMMENT '性别 1男 2女 3未知',
  `nickname` varchar(70) DEFAULT NULL COMMENT '昵称',
  `avatar_url`  varchar(256) DEFAULT '' COMMENT '头像url',
  `intro`  varchar(512) DEFAULT NULL COMMENT '个人简介',
  `create_vip_time` bigint(20) DEFAULT NULL COMMENT '开通会员时间',
  `user_status` tinyint(4) DEFAULT 1 COMMENT '用户是否有效 1=有效,0=禁止',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `idx_mobile` (`mobile`),
  UNIQUE KEY `idx_user_code_invite` (`user_code_invite`),
  KEY `idx_code_invite` (`code_invite`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 用户账户表
DROP TABLE IF EXISTS `dgv_user_account`;
CREATE TABLE `dgv_user_account` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户id',
  `asset_code` varchar(16) NOT NULL COMMENT '资产类型',
  `amount_available` decimal(35,4) unsigned NOT NULL COMMENT '可用资产',
  `amount_frozen` decimal(35,4) unsigned NOT NULL COMMENT '冻结资产',
  `account_status` enum('OK','BAN') DEFAULT 'OK' COMMENT '账户状态：冻结：BAN，正常，OK',
  `enough_money` tinyint(4) DEFAULT 0 COMMENT '资产是否达到过5w,1=达到(只针对DG币)',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_id_asset_code` (`user_id`, `asset_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='用户账户表';


-- ----------------------------
-- Table structure for `user_offchain_account_record`
-- ----------------------------
-- 闪电转账记录表(内部转账)
-- （这一块操作资金的时候必须用sql来做加减，不要用程序获取之后再加减）

DROP TABLE IF EXISTS `dgv_account_record`;
CREATE TABLE `dgv_account_record` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `from_user_id` bigint(20) NOT NULL COMMENT '转账的人',
  `to_user_id` bigint(20) NOT NULL COMMENT '收款的人,0=官方收款账号',
  `amount` decimal(30,4) NOT NULL DEFAULT '0.00' COMMENT '转账金额',
  `asset_code` varchar(16) NOT NULL COMMENT '资产类型',
  `operation_type` tinyint(4) unsigned DEFAULT 1 COMMENT '1是闪电转账,2=认购,3=充值,4=提现,5=注册推荐奖励,6=注册奖励,7=1级好友奖励,8=2级好友奖励,9=DGV兑换DG币(消耗dgv),10=DGV兑换DG币(获取dg),11=每天凌晨释放',
  -- `subscribe_type` tinyint(4) unsigned DEFAULT NULL COMMENT '认购状态, 1=未释放,2=释放,当operation_type=2时',
  `deposit_withdraw_id` bigint(20) unsigned DEFAULT NULL COMMENT '提现/充值请求的id,当operation_type=3/4时',
  `remark` varchar(1024) DEFAULT '' COMMENT '备注',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_from_user_id_asset_code` (`from_user_id`, `asset_code`),
  KEY `idx_to_user_id_asset_code` (`to_user_id`, `asset_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='中心转账记录表';

-- ----------------------------
-- Table structure for `deposit_eos_record`
-- ----------------------------
-- 充值请求
DROP TABLE IF EXISTS `dgv_deposit_request`;
CREATE TABLE `dgv_deposit_request` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `eos_trx_id` VARCHAR(128) NOT NULL COMMENT 'eos交易id',
  `from_account` varchar(16) NOT NULL COMMENT '充值用户',
  `to_account` varchar(16) NOT NULL COMMENT 'dgv官方-接收账户',
  `user_id`bigint(20) NOT NULL COMMENT 'user_id',
  `amount` DECIMAL(30,4) NOT NULL  COMMENT '交易数量',
  `asset_code` varchar(16) DEFAULT 'DGV' COMMENT 'eos币种',
  `block_num` bigint(20) NOT NULL  COMMENT '区块编号',
  `deposit_status` enum('INIT', 'CONFIRMED', 'SUCCESS', 'FAIL') NOT NULL  COMMENT '充值状态',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_eos_trx_id` (`eos_trx_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_deposit_status` (`deposit_status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='EOS链上充值请求表';


-- 充值记录
DROP TABLE IF EXISTS `dgv_deposit_record`;
CREATE TABLE `dgv_deposit_record` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `out_trx_id` VARCHAR(70) NOT NULL COMMENT '外部的交易id',
  `from_account` varchar(16) NOT NULL COMMENT 'eos充值用户',
  `user_id` bigint(20) NOT NULL COMMENT 'user_id',
  `amount` DECIMAL(30,4) NOT NULL  COMMENT '交易数量',
  `asset_code` varchar(16) DEFAULT 'DGV' COMMENT '币种',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_out_trx_id` (`out_trx_id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='充值eos记录表';


-- ----------------------------
-- Table structure for `withdraw_eos_request`
-- ----------------------------
-- 提现请求表
DROP TABLE IF EXISTS `dgv_withdraw_request`;
CREATE TABLE `dgv_withdraw_request` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `uni_uuid` char(32) NOT NULL COMMENT '唯一id',
  `user_id` bigint(20) NOT NULL COMMENT '用户id',
  `to_account` varchar(16) NOT NULL COMMENT '提现到的eos账户名',
  `amount` DECIMAL(30,4) NOT NULL COMMENT '提现数量',
  `asset_code` varchar(40) DEFAULT 'DGV' COMMENT '币种类型',
  `memo` varchar(1024) DEFAULT NULL COMMENT 'memo信息',
  `need_audit` enum('YES','NO') NOT NULL COMMENT '是否需要审核 :YES是 NO否',
  `audit_status` enum('INIT','PASS','FAIL') NOT NULL COMMENT '审核状态 :INIT初始化 PASS通过 FAIL不通过',
  `withdraw_status` enum('INIT','SUCCESS', 'FAIL') NOT NULL COMMENT '体现状态 :INIT初始化 SUCCESS提现成功 FAIL 提现失败',
  `fail_message` varchar(1024) DEFAULT NULL COMMENT '失败消息',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  UNIQUE KEY `idx_uni_uuid` (`uni_uuid`),
  KEY `idx_withdraw_status_need_audit_audit_status` (`withdraw_status`, `need_audit`, `audit_status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='eos提现请求表';

-- ----------------------------
-- Table structure for `withdraw_eos_record`
-- ----------------------------
-- eos提现记录表

DROP TABLE IF EXISTS `dgv_withdraw_record`;
CREATE TABLE `dgv_withdraw_record` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `request_uuid` varchar(70) NOT NULL COMMENT '对应请求记录表的uni_uuid',
  `user_id` bigint(20) NOT NULL COMMENT '提现用户id',
  `to_account` varchar(16) NOT NULL COMMENT '提现到的eos账户名',
  `from_account` varchar(16) NOT NULL COMMENT '来源地址',
  `fee_amount` DECIMAL(30,4) NOT NULL COMMENT '手续费数量',
  `amount` DECIMAL(30,4) NOT NULL COMMENT '交易数量',
  `asset_code` varchar(16) DEFAULT 'DGV'  COMMENT '币种类型',
  `block_num` bigint(20) NOT NULL COMMENT '区块编号',
  `block_time` varchar(40) NOT NULL COMMENT '区块时间',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_request_uuid` (`request_uuid`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='eos提现记录表';

-- 联系我们
DROP TABLE IF EXISTS `dgv_contact_us`;
CREATE TABLE `dgv_contact_us` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) NOT NULL COMMENT '用户名',
  `title` varchar(256) NOT NULL COMMENT '标题',
  `content` varchar(1024) DEFAULT NULL COMMENT '内容',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='联系我们';

-- 推荐奖励（一级）：币权认购奖励
-- DROP TABLE IF EXISTS `dgv_recommend_awards`;
-- CREATE TABLE `dgv_recommend_awards` (
--   `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
--   `recommend_user_id` bigint(20) NOT NULL COMMENT '推荐用户id',
--   `user_id` bigint(20) NOT NULL COMMENT '被推荐用户id,花钱的人',
--   `is_send` tinyint(4) NOT NULL DEFAULT 1 COMMENT '发放奖励,1=未发,2=发',
--   `eos_amount` decimal(30,4) NOT NULL COMMENT '认购数量',
--   `dgv_amount` decimal(30,4) NOT NULL COMMENT '需要发放的dgv数量',
--   `create_time` bigint(20) NOT NULL COMMENT '创建时间',
--   `update_time` bigint(20) NOT NULL COMMENT '更新时间',
--   PRIMARY KEY (`id`),
--   KEY `idx_user_id` (`user_id`),
--   KEY `idx_create_time` (`create_time`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='推荐奖励（一级）';

-- 常见问题/消息通知
DROP TABLE IF EXISTS `dgv_problem_message`;
CREATE TABLE `dgv_problem_message` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `title` varchar(256) NOT NULL COMMENT '标题',
  `content` varchar(2048) DEFAULT NULL COMMENT '内容',
  `content_type` tinyint(4) NOT NULL DEFAULT 1 COMMENT '1=常见问题,2=消息通知',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) NOT NULL COMMENT '更新时间',
  `type` tinyint(4) NOT NULL DEFAULT 1 COMMENT '是否有效,1=有效,2=删除',
  PRIMARY KEY (`id`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='常见问题/消息通知';


-- 系统配置表,可以存 勾兑比例,兑换比例等
DROP TABLE IF EXISTS `dgv_profile`;
CREATE TABLE `dgv_profile` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `profile_key` varchar(64) NOT NULL COMMENT '配置关键字',
  `profile_value` varchar(32) NOT NULL COMMENT '配置的值',
  `profile_index` tinyint(4) DEFAULT 1 COMMENT '配置序号',
  `profile_type` varchar(32) NOT NULL COMMENT '数据类型',
  `create_time` bigint(20) NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_profile_key_profile_index` (`profile_key`, `profile_index`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
INSERT INTO `dgv`.`dgv_profile` (`id`, `profile_key`, `profile_value`, `profile_index`, `profile_type`, `create_time`, `update_time`) VALUES ('1', 'release_rate', '0.01', '1', 'int', '0', NULL);

-- 每天释放dg
DROP TABLE IF EXISTS `dgv_release_dg`;
CREATE TABLE `dgv_release_dg` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) NOT NULL COMMENT '用户id',
  `amount` decimal(30,4) NOT NULL COMMENT '发放的金额',
  `create_time` bigint(20) NOT NULL COMMENT '发送时间',
  `create_date` date NOT NULL COMMENT '发布日期',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='每天释放dg';