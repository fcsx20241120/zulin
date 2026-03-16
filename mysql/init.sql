-- MySQL 初始化脚本
-- 创建用户（如果不存在）
CREATE USER IF NOT EXISTS 'zulin'@'%' IDENTIFIED BY 'Zulin@2026!';
GRANT ALL PRIVILEGES ON zulin.* TO 'zulin'@'%';
FLUSH PRIVILEGES;

-- 设置时区
SET GLOBAL time_zone = '+08:00';
