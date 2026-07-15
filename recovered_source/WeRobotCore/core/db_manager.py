# Decompiled from: db_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import sqlite3
import os
import sys
from datetime import datetime
from WeRobotCore.utils.data_manager import DataManager
class WeChatDBManager:
    """WeChatDBManager"""

    _instance = None
    def __new__(cls, db_path):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self, db_path):
        self.db_path = os.path.join(DataManager.get_data_dir_str(), db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        sqlite3.register_converter("TEXT", lambda x: x.decode("utf-8"))
        self.init_db()
        self._initialized = True
    def init_db(self):
        """初始化数据库表"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        conn.text_factory = str
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS wechat_accounts (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        nickname TEXT NOT NULL,\n                        account_id TEXT UNIQUE,\n                        last_updated DATETIME,\n                        UNIQUE(nickname, account_id)\n                    )\n                ")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS friends (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        account_id TEXT NOT NULL,\n                        wxid TEXT NOT NULL,\n                        name TEXT NOT NULL,\n                        nickname TEXT,\n                        remark TEXT,\n                        tag TEXT,\n                        is_new INTEGER DEFAULT 0,\n                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n                        last_updated DATETIME,\n                        FOREIGN KEY (account_id) REFERENCES wechat_accounts(account_id),\n                        UNIQUE(account_id, wxid, tag)\n                    )\n                ")
        cursor.execute("ALTER TABLE friends ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS groups (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        account_id TEXT NOT NULL,\n                        name TEXT NOT NULL,\n                        tag TEXT DEFAULT '',\n                        last_updated DATETIME,\n                        FOREIGN KEY (account_id) REFERENCES wechat_accounts(account_id),\n                        UNIQUE(account_id, name)\n                    )\n                ")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS contacts (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        account_id TEXT,\n                        name TEXT NOT NULL,\n                        tag TEXT,\n                        type TEXT CHECK(type IN ('friend', 'group')),\n                        last_updated DATETIME,\n                        FOREIGN KEY (account_id) REFERENCES wechat_accounts(account_id),\n                        UNIQUE(account_id, name, tag, type)\n                    )\n                ")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS group_members (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        group_name TEXT NOT NULL,\n                        nickname TEXT NOT NULL,\n                        gender TEXT,\n                        wx_id TEXT,\n                        region TEXT,\n                        is_friend INTEGER DEFAULT 0,\n                        last_updated DATETIME,\n                        UNIQUE(group_name, nickname)\n                    )\n                ")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS friend_list (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        wxid TEXT NOT NULL,\n                        remark TEXT,\n                        tags TEXT,\n                        nickname TEXT,\n                        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'added', 'failed', 'unknown', 'already')),\n                        error TEXT,\n                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n                        UNIQUE(wxid)\n                    )\n                ")
        cursor.execute("ALTER TABLE friend_list ADD COLUMN account_id TEXT")
        cursor.execute("\n                    CREATE TABLE IF NOT EXISTS contact_tags (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        account_id TEXT NOT NULL,\n                        tag_name TEXT NOT NULL,\n                        contact_count INTEGER DEFAULT 0,\n                        last_updated DATETIME,\n                        FOREIGN KEY (account_id) REFERENCES wechat_accounts(account_id),\n                        UNIQUE(account_id, tag_name)\n                    )\n                ")
        conn.commit()
        None(None, None)
    def update_tag_statistics(self, account_id, contact_type):
        """更新标签统计信息"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        now = datetime.now()
        contacts = self.get_contacts_with_tags(account_id, contact_type)
        tag_stats = {}
        untagged_count = 0
        cursor.execute("\n                SELECT tag_name FROM contact_tags WHERE account_id = ?\n            ", (account_id,))
        existing_tags = cursor.fetchall()
        row = set()
        cursor.execute("\n                    INSERT INTO contact_tags (account_id, tag_name, contact_count, last_updated)\n                    VALUES (?, ?, ?, ?)\n                ", (account_id, "未分组", untagged_count, now))
        conn.commit()
        tag_stats.items()(None, None, None)
        tag = existing_tags[0]
        count = existing_tags[1]
        cursor.execute("\n                        INSERT INTO contact_tags (account_id, tag_name, contact_count, last_updated)\n                        VALUES (?, ?, ?, ?)\n                    ", (account_id, tag, count, now))
        cursor.execute("\n                        UPDATE contact_tags \n                        SET contact_count = ?, last_updated = ? \n                        WHERE account_id = ? AND tag_name = ?\n                    ", (count, now, account_id, tag))
        cursor.execute("\n                    UPDATE contact_tags \n                    SET contact_count = ?, last_updated = ? \n                    WHERE account_id = ? AND tag_name = ?\n                ", (untagged_count, now, account_id, "未分组"))
        tag = row
        cursor.execute("\n                        DELETE FROM contact_tags WHERE account_id = ? AND tag_name = ?\n                    ", (account_id, tag))
        row = contacts
        contact = row[0]
        tags = []
        tag = tags
        tag = tag.strip()
        tag_stats[tag] = tag_stats.get(tag, 0) + 1
        untagged_count = untagged_count + 1
    def save_friends(self, account_id, friends_data, is_incremental):
        """保存好友列表到friends表（采用旧版contacts表的存储方式）

                Args:
                    account_id: 微信账号ID
                    friends_data: 好友数据列表
                    is_incremental: 是否为增量更新，True表示增量更新不删除现有数据，False表示全量更新先删除再插入
                """

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        now = datetime.now()
        friend_tags = {}
        saved_count = 0
        updated_count = 0
        conn.commit()
        print("好友数据全量保存完成 - 保存: ", f'{saved_count}')
        None(None, None)
        self.update_tag_statistics(account_id)
        return {"inserted": saved_count, "updated": 0, "deleted": 0, "total_synced": saved_count}
        f'{saved_count}'(", 更新: ", f'{updated_count}')
        wxid = "好友数据增量更新完成 - 新增: "[0]
        friend_info = "好友数据增量更新完成 - 新增: "[1]
        tag_str = ""
        cursor.execute("\n                            INSERT INTO friends (account_id, wxid, name, nickname, remark, tag, is_new, created_at, last_updated)\n                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n                        ", (str(account_id), friend_info["wxid"], friend_info["name"], friend_info["nickname"], friend_info["remark"], tag_str, 1, now, now))
        saved_count = saved_count + 1
        cursor.execute("SELECT COUNT(*) FROM friends WHERE account_id = ? AND wxid = ?", (str(account_id), wxid))
        exists = cursor.fetchone()[0] > 0
        cursor.execute("\n                                INSERT INTO friends (account_id, wxid, name, nickname, remark, tag, is_new, created_at, last_updated)\n                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n                            ", (str(account_id), friend_info["wxid"], friend_info["name"], friend_info["nickname"], friend_info["remark"], tag_str, 0, now, now))
        saved_count = saved_count + 1
        cursor.execute("\n                                UPDATE friends \n                                SET name = ?, nickname = ?, remark = ?, tag = ?, last_updated = ?\n                                WHERE account_id = ? AND wxid = ?\n                            ", (friend_info["name"], friend_info["nickname"], friend_info["remark"], tag_str, now, str(account_id), wxid))
        updated_count = updated_count + 1
        friend = ",".join(sorted(friend_info["tags"]))
        wxid = friend.get("wxid", "")
        name = friend.get("name", "").strip()
        nickname = friend.get("nickname", "").strip()
        remark = friend.get("remark", "").strip()
        tags = friend.get("tags", [])
        name = ""
        name = name.encode("utf-16", "surrogatepass").decode("utf-16")
        friend_tags[wxid]["tags"].add(str(tags))
        friend_tags[wxid]["tags"].add(tags)
        friend_tags[wxid]["tags"].update((t for t in _iter)(tags))
        friend_tags[wxid] = {"wxid": wxid, "name": name, "nickname": nickname, "remark": remark, "tags": set()}
        wxid = wxid.strip()
        str(name)
        cursor.execute("DELETE FROM friends WHERE account_id = ?", (account_id,))
    def save_groups(self, account_id, groups_data):
        """保存群聊列表到新的groups表"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        now = datetime.now()
        normalized_groups = {}
        cursor.execute("SELECT name, tag FROM groups WHERE account_id = ?", (account_id,))
        existing_rows = cursor.fetchall()
        existing_names = existing_rows
        row = set()
        latest_names = set(normalized_groups.keys())
        names_to_insert = latest_names - existing_names
        names_to_delete = existing_names - latest_names
        names_to_update = latest_names & existing_names
        cursor.execute("BEGIN")
        deleted_count = 0
        inserted_count = 0
        updated_count = 0
        conn.commit()
        f'{deleted_count}'(", 更新: ", f'{updated_count}')
        ", 删除: "(None, None, None)
        name = f'{inserted_count}'
        tag = normalized_groups.get(name, "")
        cursor.execute("INSERT INTO groups (account_id, name, tag, last_updated) VALUES (?, ?, ?, ?)", (account_id, name, tag, now))
        inserted_count = inserted_count + 1
        name = "群聊增量同步完成 - 新增: "
        cursor.execute("DELETE FROM groups WHERE account_id = ? AND name = ?", (account_id, name))
        deleted_count = deleted_count + 1
        row = print
        group = row[0]
        name = ""
        tag = ""
        name = str(group).strip()
        tag = ""
        normalized_groups[name] = tag
        normalized_groups[name] = tag
        name = group.strip()
        tag = ""
        tag = ""
        name = group[0]
        name = ""
        tag = ""
        tag = group[1]
        name = group[0]
        name = group.get("name").strip()
        tag = group.get("tag").strip()
        tag = group.get("type").strip()
        str(name).strip()
    def update_groups_tag_batch(self, account_id, group_names, tag):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        now = datetime.now()
        {"success": False, "updated": 0, "not_found": []}(None, None, None)
        return "???"
        names = group_names
        n = []
        cursor.execute("SELECT name FROM groups WHERE account_id = ?", (account_id,))
        existing = cursor.fetchall()
        row = set()
        to_update = names
        n = []
        not_found = names
        n = []
        cursor.execute("BEGIN")
        updated = 0
        conn.commit()
        to_update(None, None, None)
        return {"success": True, "updated": updated, "not_found": not_found}
        cursor.execute("UPDATE groups SET tag = ?, last_updated = ? WHERE account_id = ? AND name = ?", (tag, now, account_id, n))
        updated = updated + 1
        row = n
        row[0](None, None, None)
        return {"success": False, "updated": 0, "not_found": []}
        n = row
    def get_group_tag(self, account_id, group_name):
        """根据群名称查询对应标签"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT tag FROM groups\n                    WHERE account_id = ? AND name = ?\n                    LIMIT 1\n                ", (account_id, group_name))
        row = cursor.fetchone()
        tag = row[0].strip()
        ""(None, None, None)
        return "???"
        ""(None, None, None)
    def get_friends(self, account_id, tag):
        """获取好友列表（从新的friends表）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT DISTINCT wxid, name, nickname, remark, tag, is_new, last_updated, created_at\n                    FROM friends \n                    WHERE account_id = ?\n                    ORDER BY name\n                ", (account_id,))
        cursor.fetchall()(None, None, None)
        return "???"
        cursor.execute("\n                    SELECT DISTINCT wxid, name, nickname, remark, tag, is_new, last_updated, created_at\n                    FROM friends \n                    WHERE account_id = ? AND tag = ?\n                    ORDER BY name\n                ", (account_id, tag))
    def get_contact_names(self, account_id, contact_type):
        """
                直接获取联系人名称列表，更高效的实现

                Args:
                    account_id: 微信账号ID
                    contact_type: 联系人类型，'friend'表示好友，'group'表示群聊，None表示所有

                Returns:
                    list: 联系人名称列表
                """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT DISTINCT name\n                    FROM (\n                        SELECT name FROM friends WHERE account_id = ? AND name IS NOT NULL\n                        UNION\n                        SELECT name FROM groups WHERE account_id = ? AND name IS NOT NULL\n                    )\n                    ORDER BY name\n                ", (account_id, account_id))
        row = []
        row(None, None, None)
        return cursor.fetchall()
        cursor.execute("\n                    SELECT DISTINCT name\n                    FROM groups \n                    WHERE account_id = ? AND name IS NOT NULL\n                    ORDER BY name\n                ", (account_id,))
        cursor.execute("\n                    SELECT DISTINCT name\n                    FROM friends \n                    WHERE account_id = ? AND name IS NOT NULL\n                    ORDER BY name\n                ", (account_id,))
    def get_groups(self, account_id, tag):
        """获取群聊列表（从新的groups表）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT name, tag, last_updated\n                    FROM groups \n                    WHERE account_id = ?\n                    ORDER BY name\n                ", (account_id,))
        cursor.fetchall()(None, None, None)
        return "???"
        cursor.execute("\n                    SELECT name, tag, last_updated\n                    FROM groups \n                    WHERE account_id = ? AND tag = ?\n                    ORDER BY name\n                ", (account_id, tag))
    def get_friend_by_wxid(self, account_id, wxid):
        """根据wxid获取好友信息"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                SELECT wxid, name, nickname, remark, tag, is_new, last_updated\n                FROM friends \n                WHERE account_id = ? AND wxid = ?\n                LIMIT 1\n            ", (account_id, wxid))
        cursor.fetchone()(None, None, None)
        return "???"
    def update_friend_is_new_status(self, account_id, wxid, is_new):
        """更新好友的is_new状态"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                UPDATE friends \n                SET is_new = ?, last_updated = ?\n                WHERE account_id = ? AND wxid = ?\n            ", (is_new, datetime.now(), account_id, wxid))
        conn.commit()
        cursor.rowcount > 0(None, None, None)
        return "???"
    def get_friend_created_time(self, account_id, wxid):
        """获取好友的创建时间"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                SELECT created_at FROM friends \n                WHERE account_id = ? AND wxid = ?\n                LIMIT 1\n            ", (account_id, wxid))
        result = cursor.fetchone()
        None(None, None, None)
        return "???"
    def is_new_friend(self, account_id, wxid, days_threshold):
        """判断是否为新用户（基于创建时间）

                Args:
                    account_id: 微信账号ID
                    wxid: 好友微信ID
                    days_threshold: 天数阈值，默认7天内算新用户

                Returns:
                    bool: True表示是新用户，False表示老用户，None表示用户不存在
                """

        created_time = self.get_friend_created_time(account_id, wxid)
        time_diff = datetime.now() - created_time
        return time_diff.days <= days_threshold
        created_time = datetime.fromisoformat(created_time)
    def get_new_friends_by_date(self, account_id, start_date, end_date):
        """获取指定时间范围内新增的好友

                Args:
                    account_id: 微信账号ID
                    start_date: 开始日期（datetime对象或字符串）
                    end_date: 结束日期（datetime对象或字符串）

                Returns:
                    list: 好友列表
                """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "\n                SELECT DISTINCT wxid, name, nickname, remark, created_at, last_updated\n                FROM friends \n                WHERE account_id = ?\n            "
        params = [account_id]
        query = query + " ORDER BY created_at DESC"
        cursor.execute(query, params)
        cursor.fetchall()(None, None, None)
        return "???"
        query = query + " AND created_at <= ?"
        params.append(end_date)
        query = query + " AND created_at >= ?"
        params.append(start_date)
    def get_friend_count(self, account_id):
        """获取指定账号的好友数量（兼容方法，优先使用新表）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                SELECT COUNT(DISTINCT wxid) FROM friends \n                WHERE account_id = ?\n            ", (account_id,))
        count = cursor.fetchone()[0]
        count(None, None, None)
        return "???"
        cursor.execute("\n                    SELECT COUNT(DISTINCT name) FROM contacts \n                    WHERE account_id = ? AND type = 'friend'\n                ", (account_id,))
        count = cursor.fetchone()[0]
    def get_contact_counts(self, account_id):
        """一次性获取好友和群聊数量（兼容方法，优先使用新表）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        counts = {"friend_count": 0, "group_count": 0}
        cursor.execute("\n                SELECT COUNT(DISTINCT wxid) FROM friends \n                WHERE account_id = ?\n            ", (account_id,))
        friend_count = cursor.fetchone()[0]
        cursor.execute("\n                SELECT COUNT(DISTINCT name) FROM groups \n                WHERE account_id = ?\n            ", (account_id,))
        group_count = cursor.fetchone()[0]
        counts["friend_count"] = friend_count
        counts["group_count"] = group_count
        counts(None, None, None)
        return "???"
    def add_friend_list(self, friend_list):
        """批量添加好友名单"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        valid_count = 0
        friend_list(None, None, None)
        return True
        wxid = friend.get("wxid", "").strip()
        print("跳过wxid为空的好友数据: ", f'{friend}')
        cursor.execute("\n                            INSERT OR REPLACE INTO friend_list \n                            (wxid, remark, tags, status) \n                            VALUES (?, ?, ?, 'pending')\n                        ", (friend.get("wxid", ""), friend.get("remark", ""), friend.get("tags", "")))
        valid_count = valid_count + 1
    def update_friend_status(self, wxid, status, nickname, error, account_id):
        """
                更新好友添加状态

                Args:
                    wxid: 微信号
                    status: 状态 ('added' 或 'failed')
                    nickname: 用户昵称
                    error: 失败原因
                """

        f'{error}'(", ", f'{account_id}')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    UPDATE friend_list \n                    SET status = ?, \n                        nickname = COALESCE(?, nickname),\n                        error = ?,\n                        account_id = COALESCE(?, account_id),\n                        updated_at = CURRENT_TIMESTAMP\n                    WHERE wxid = ?\n                ", (status, nickname, error, account_id, wxid))
        conn.commit()
        ", "(None, None, None)
        return True
    def get_friend_list(self, limit):
        """获取好友名单列表"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT wxid, remark, tags, status \n                    FROM friend_list \n                    ORDER BY created_at DESC\n                    LIMIT ?\n                ", (limit,))
        results = cursor.fetchall()
        row = []
        row(None, None, None)
        return results
    def delete_friend_from_list(self, wxid):
        """从名单中删除指定好友"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM friend_list WHERE wxid = ?", (wxid,))
        conn.commit()
        None(None, None)
        return True
    def batch_delete_friend_list(self, wxids):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        w = []
        cursor.executemany("DELETE FROM friend_list WHERE wxid = ?", w, wxids)
        conn.commit()
        None(None, None)
        return True
        return True
    def filter_friend_list(self, status, tag, limit):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        base_sql = "SELECT wxid, remark, tags, status,error,nickname,account_id FROM friend_list"
        where = []
        params = []
        base_sql = base_sql + " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        cursor.execute(base_sql, tuple(params))
        results = cursor.fetchall()
        row = []
        row(None, None, None)
        return results
        base_sql = base_sql + " WHERE " + " AND ".join(where)
        where.append("(tags = ? OR tags LIKE ? OR tags LIKE ? OR tags LIKE ?)")
        ",%"("%,", [f'{tag}', ",%", "%,", f'{tag}'])
        where.append("status = ?")
        params.append(status)
    def get_pending_friends(self, limit):
        """
                获取指定数量的待添加好友

                Args:
                    limit: 获取数量

                Returns:
                    list: 待添加好友列表 [{'wxid': str, 'remark': str, 'tags': str}]
                """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT wxid, remark, tags \n                    FROM friend_list \n                    WHERE status = 'pending'\n                    LIMIT ?\n                ", (limit,))
        results = cursor.fetchall()
        row = []
        row(None, None, None)
        return results
    def get_pending_friend_count(self):
        """获取待添加好友数量"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM friend_list WHERE status = \"pending\"")
        cursor.fetchone()[0](None, None, None)
        return "???"
    def save_account(self, nickname, account_id):
        """保存或更新微信账号信息"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                INSERT OR REPLACE INTO wechat_accounts (nickname, account_id, last_updated)\n                VALUES (?, ?, ?)\n            ", (nickname, account_id, datetime.now()))
        conn.commit()
        cursor.lastrowid(None, None, None)
        return "???"
    def get_all_contact_tags(self, account_id):
        """获取指定账号的标签列表及其统计"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("\n                SELECT tag_name, contact_count FROM contact_tags \n                WHERE account_id = ? \n                ORDER BY contact_count DESC, tag_name\n            ", (account_id,))
        results = cursor.fetchall()
        results(None, None, None)
        return "???"
        print("标签数据为空，正在初始化标签统计信息...")
        self.update_tag_statistics(account_id)
        cursor.execute("\n                    SELECT tag_name, contact_count FROM contact_tags \n                    WHERE account_id = ? \n                    ORDER BY contact_count DESC, tag_name\n                ", (account_id,))
        results = cursor.fetchall()
    def get_group_tags_statistics(self, account_id):
        """获取指定账号的群聊标签列表及其统计"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("\n                SELECT tag, COUNT(*) FROM groups \n                WHERE account_id = ?\n                GROUP BY tag\n                ORDER BY COUNT(*) DESC\n            ", (account_id,))
        results = cursor.fetchall()
        results(None, None, None)
        return "???"
    def add_friend_if_not_exists(self, account_id, nickname, tag):
        """添加好友到通讯录（如果不存在）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT COUNT(*) FROM contacts \n                    WHERE account_id = ? AND name = ? AND type = 'friend'\n                ", (account_id, nickname))
        "数据库已存在好友"(f'{nickname}', "，跳过添加")
        print(None, None, None)
        return False
        cursor.execute("\n                        INSERT INTO contacts (account_id, name, tag, type, last_updated)\n                        VALUES (?, ?, ?, 'friend', ?)\n                    ", (account_id, nickname, tag, datetime.now()))
        conn.commit()
        f'{nickname}'(", 标签: ", f'{"无"}')
        "新好友已添加到通讯录: "(None, None, None)
        return True
    def save_or_update_friend_info(self, account_id, friend_info, is_new):
        """保存或更新好友信息到数据库（采用旧版contacts表的存储方式）

                参数:
                - account_id: 微信账号ID
                - friend_info: 好友信息字典，包含nickname, wechat_id, remark_name, tags等
                - is_new: 是否为新好友，None表示自动判断，True表示强制设为新好友，False表示强制设为非新好友

                返回:
                - bool: 是否成功保存/更新
                """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        nickname = friend_info.get("nickname", "")
        wechat_id = friend_info.get("wechat_id", "")
        remark_name = friend_info.get("remark_name", "")
        tags = friend_info.get("tags", [])
        display_name = wechat_id
        tag_str = ""
        now = datetime.now()
        print("警告: 好友信息缺少微信ID，无法保存: ", f'{nickname}')
        None(None, None)
        return False
        cursor.execute("\n                        SELECT created_at FROM friends \n                        WHERE account_id = ? AND wxid = ?\n                        LIMIT 1\n                    ", (account_id, wechat_id))
        existing = cursor.fetchone()
        is_new_value = 1
        cursor.execute("\n                            INSERT INTO friends \n                            (account_id, wxid, name, nickname, remark, tag, is_new, created_at, last_updated)\n                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n                        ", (account_id, wechat_id, display_name, nickname, remark_name, tag_str, is_new_value, now, now))
        " (昵称: "(f'{nickname}', ")")
        conn.commit()
        self.update_tag_statistics(account_id)
        f'{wechat_id}'(None, None, None)
        return True
        is_new_value = 0
        created_at = existing[0]
        cursor.execute("\n                            UPDATE friends \n                            SET name = ?, nickname = ?, remark = ?, tag = ?, is_new = 0, last_updated = ?\n                            WHERE account_id = ? AND wxid = ?\n                        ", (display_name, nickname, remark_name, tag_str, now, account_id, wechat_id))
        tag_str = tags
        tag_str = ",".join((tag for tag in _iter)(tags))
    def get_contacts(self, account_id, contact_type):
        """获取指定账号的联系人列表"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT name, type FROM contacts \n                    WHERE account_id = ?\n                    ORDER BY type, name\n                ", (account_id,))
        cursor.fetchall()(None, None, None)
        return "???"
        cursor.execute("\n                    SELECT name FROM contacts \n                    WHERE account_id = ? AND type = ?\n                    ORDER BY name\n                ", (account_id, contact_type))
    def get_contacts_with_tags(self, account_id, contact_type):
        """获取指定账号的联系人列表及其标签（从friends表获取）"""

        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT name, tag FROM contacts \n                    WHERE account_id = ? AND type = ?\n                    ORDER BY name\n                ", (account_id, contact_type))
        cursor.fetchall()(None, None, None)
        return "???"
        cursor.execute("\n                    SELECT name, tag FROM friends \n                    WHERE account_id = ?\n                    ORDER BY name\n                ", (account_id,))
    def get_contact_tags(self, account_id, contact_name):
        """获取指定联系人的标签信息

                参数:
                - account_id: 微信账号ID
                - contact_name: 联系人名称（优先匹配备注名，如果没有备注名则匹配昵称）

                返回:
                - 包含联系人名称和标签的元组列表 [(name, tag)]
                """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                SELECT name, tag FROM friends \n                WHERE account_id = ? \n                AND (\n                    (remark IS NOT NULL AND remark != '' AND remark = ?) \n                    OR (remark IS NULL OR remark = '') AND nickname = ?\n                )\n                LIMIT 1\n            ", (account_id, contact_name, contact_name))
        result = cursor.fetchall()
        result(None, None, None)
        return "???"
        name = result[0][0]
        tags = result[0][1].split(",")
        tag = []
        tag = []
        tag(None, None, None)
        return tags
        tag = (name, tag)
    def save_contact_tags(self, account_id, tags):
        """
                保存联系人标签信息

                参数:
                - account_id: 微信账号ID
                - tags: 标签字典，格式为 {tag_name: [contact_names]}
                """

        cursor = self.conn.cursor()
        cursor.execute("\n            CREATE TABLE IF NOT EXISTS contact_tags (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                account_id TEXT NOT NULL,\n                contact_name TEXT NOT NULL,\n                tag_name TEXT NOT NULL,\n                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n                UNIQUE(account_id, contact_name, tag_name)\n            )\n            ")
        cursor.execute("DELETE FROM contact_tags WHERE account_id = ?", (account_id,))
        self.conn.commit()
        "成功保存 "(f'{len(tags)}', " 个标签的信息")
        tag_name = print[0]
        contacts = print[1]
        contact_name = contacts
        cursor.execute("\n                    INSERT OR REPLACE INTO contact_tags (account_id, contact_name, tag_name)\n                    VALUES (?, ?, ?)\n                    ", (account_id, contact_name, tag_name))
    def save_group_members(self, group_name, members):
        """保存群成员信息"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now()
        conn.commit()
        members(None, None, None)
        cursor.execute("\n                    INSERT OR REPLACE INTO group_members \n                    (group_name, nickname, gender, wx_id, region, is_friend, last_updated)\n                    VALUES (?, ?, ?, ?, ?, ?, ?)\n                ", (group_name, member["nickname"], member.get("gender", ""), member.get("wx_id", ""), member.get("region", ""), member.get("is_friend", 0), now))
    def add_group_if_not_exists(self, account_id, group_name):
        """添加群聊到通讯录（如果不存在）"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                    SELECT COUNT(*) FROM groups \n                    WHERE account_id = ? AND name = ?\n                ", (account_id, group_name))
        None(None, None)
        cursor.execute("\n                        INSERT INTO groups (account_id, name, tag, last_updated)\n                        VALUES (?, ?, '', ?)\n                    ", (account_id, group_name, datetime.now()))
        conn.commit()
        print("新群聊已添加到通讯录: ", f'{group_name}')
    def get_group_members(self, group_name):
        """获取群成员列表"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("\n                SELECT nickname, gender, wx_id, region, is_friend\n                FROM group_members\n                WHERE group_name = ?\n                ORDER BY nickname\n            ", (group_name,))
        members = []
        cursor.fetchall()(None, None, None)
        return members
        members.append({"nickname": row[0], "gender": row[1], "wx_id": row[2], "region": row[3], "is_friend": bool(row[4])})
    def get_users_by_tag(self, account_id, tag_id):
        """
                根据标签ID获取用户列表

                参数:
                - account_id: 微信账号ID
                - tag_id: 标签ID

                返回:
                - 包含用户名称的列表
                """

        conn = sqlite3.connect(self.db_path)
        conn.text_factory = str
        cursor = conn.cursor()
        tag_id(f'{tag_id}', ",%", ("%,", f'{tag_id}', ",%", "%,", f'{tag_id}'))
        results = cursor.fetchall()
        account_id(None, None, None)
        return []
        result = []
        result = results
    __classcell__ = __class__
    return __class__
