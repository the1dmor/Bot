import sqlite3
from datetime import datetime
from difflib import SequenceMatcher

# ===================================================================
# Baza bilan ulanish
conn = sqlite3.connect('app/database/database.db', check_same_thread=False)
cursor = conn.cursor()

# ===================================================================
# Jadvallarni yaratish (agar hali mavjud bo'lmasa)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    lang TEXT DEFAULT 'uz',
    is_admin BOOLEAN DEFAULT 0,
    is_staff BOOLEAN DEFAULT 0,
    is_anipass TEXT DEFAULT 0,
    is_lux TEXT DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS media (
    media_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trailer_id TEXT,
    name TEXT,
    genre TEXT,
    tag TEXT,
    dub TEXT,
    series INTEGER DEFAULT 0,
    status TEXT DEFAULT 'loading',
    views INTEGER DEFAULT 0,
    msg_id INTEGER DEFAULT 0,
    type TEXT DEFAULT 'anime',
    is_vip BOOLEAN DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS episodes (
    episode_id TEXT PRIMARY KEY,
    which_media INTEGER,
    episode_num INTEGER,
    msg_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sponsors (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT,
    channel_link TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS statistics (
    bot TEXT PRIMARY KEY,
    users_count INTEGER DEFAULT 0,
    anime_count INTEGER DEFAULT 0
)
""")

# Default statistika qatori
cursor.execute('INSERT OR IGNORE INTO statistics (bot, users_count, anime_count) VALUES ("bot", 0, 0)')

conn.commit()

# ===================================================================
# USER FUNKSIYALARI
def add_user_base(user_id , username , lang = "uz" , is_admin = False , is_staff = False):
    cursor.execute(
        'INSERT INTO users (user_id , username , lang , is_admin , is_staff) VALUES (?, ?, ?, ?, ?);', 
        (user_id , username , lang , is_admin , is_staff)
    )
    update_statistics_user_count_base()
    conn.commit()

def get_user_base(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchone()
    return dict(zip(columns, data)) if data else None

def get_all_user_id_base():
    cursor.execute("SELECT user_id FROM users")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def get_all_staff_base():
    cursor.execute("SELECT * FROM users WHERE is_staff = 1")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def update_statistics_user_count_base():
    cursor.execute("""UPDATE statistics SET users_count = users_count + 1 WHERE bot = "bot" """)
    conn.commit()

def update_user_staff_base(user_id, value):
    cursor.execute(f"""UPDATE users SET is_staff = {value} WHERE user_id = {user_id} """)
    conn.commit()

# ===================================================================
# MEDIA FUNKSIYALARI
def add_media_base(trailer_id , name , genre , tag , dub , series = 0 , status = "loading", views = 0, msg_id = 0, type = "anime"):
    cursor.execute(
        'INSERT INTO media (trailer_id , name , genre , tag , dub , series , status , views , msg_id , type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', 
        (trailer_id , name , genre , tag , dub , series , status , views , msg_id , type)
    )
    if type == "anime":
        cursor.execute("""UPDATE statistics SET anime_count = anime_count + 1 WHERE bot = "bot" """)
    conn.commit()
    return cursor.lastrowid

def get_media_base(media_id):
    cursor.execute("SELECT * FROM media WHERE media_id = ?", (media_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchone()
    return dict(zip(columns, data)) if data else None

def get_all_media_base(type):
    cursor.execute(f"SELECT * FROM media WHERE type = ?", (type,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def get_all_ongoing_media_base():
    cursor.execute("SELECT * FROM media WHERE status = 'loading'")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def search_media_base(name, type="any"):
    if type == "any":
        cursor.execute("SELECT * FROM media WHERE name LIKE ?", (f"%{name}%",))
    else:
        cursor.execute("SELECT * FROM media WHERE name LIKE ? AND type = ?", (f"%{name}%", type))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    if not data:
        cursor.execute("SELECT * FROM media")
        all_data = cursor.fetchall()
        media = [dict(zip(columns, row)) for row in all_data]

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        new_data = []
        for i in media:
            similarity = similar(i["name"], name)
            if similarity >= 0.4:
                new_data.append([similarity, i])
            else:
                try:
                    tags = i["tag"].split(",")
                    for tag in tags:
                        tag_similarity = similar(tag, name)
                        if tag_similarity >= 0.5:
                            new_data.append([tag_similarity, i])
                            break
                except KeyError:
                    pass
        new_data.sort(reverse=True, key=lambda x: x[0])
        return [i[1] for i in new_data]
    else:
        return [dict(zip(columns, row)) for row in data]

# ===================================================================
# EPISODES FUNKSIYALARI
def add_episode_base(which_media , episode_id , episode_num, msg_id):
    cursor.execute('INSERT INTO episodes (which_media , episode_id , episode_num, msg_id) VALUES (?, ?, ?, ?);', (which_media , episode_id , episode_num, msg_id))
    conn.commit()
    return cursor.lastrowid

def get_media_episodes_base(media_id):
    cursor.execute("SELECT * FROM episodes WHERE which_media = ? ORDER BY episode_num ASC", (media_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def update_media_episodes_count_plus_base(media_id):
    cursor.execute(f"UPDATE media SET series = series + 1 WHERE media_id = ?", (media_id,))
    conn.commit()

def update_media_episodes_count_minus_base(media_id):
    cursor.execute(f"UPDATE media SET series = series - 1 WHERE media_id = ?", (media_id,))
    conn.commit()

def delete_episode_base(media_id, episode_num):
    cursor.execute(f"DELETE FROM episodes WHERE which_media = ? AND episode_num = ?", (media_id, episode_num))
    conn.commit()

# ===================================================================
# SPONSORS FUNKSIYALARI
def add_sponsor_base(channel_id , channel_name , channel_link):
    cursor.execute('INSERT INTO sponsors (channel_id , channel_name , channel_link) VALUES (?, ?, ?);', (channel_id , channel_name , channel_link))
    conn.commit()
    return cursor.lastrowid

def get_all_sponsors_base():
    cursor.execute("SELECT * FROM sponsors")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return [dict(zip(columns, row)) for row in data] if data else []

def get_sponsors_base(channel_id):
    cursor.execute("SELECT * FROM sponsors WHERE channel_id = ?", (channel_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchone()
    return dict(zip(columns, data)) if data else None

def delete_sponsor_base(channel_id):
    cursor.execute("DELETE FROM sponsors WHERE channel_id = ?", (channel_id,))
    conn.commit()

# ===================================================================
# STATISTICS FUNKSIYALARI
def get_statistics_base():
    cursor.execute("SELECT * FROM statistics WHERE bot = 'bot'")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchone()
    return dict(zip(columns, data)) if data else None

# ===================================================================
# ADDITIONAL UPDATES
def update_media_name_base(media_id,name):
    cursor.execute("UPDATE media SET name = ? WHERE media_id = ?", (name, media_id))
    conn.commit()

def update_media_genre_base(media_id,genre):
    cursor.execute("UPDATE media SET genre = ? WHERE media_id = ?", (genre, media_id))
    conn.commit()

def update_media_tag_base(media_id,tag):
    cursor.execute("UPDATE media SET tag = ? WHERE media_id = ?", (tag, media_id))
    conn.commit()

def update_media_dub_base(media_id,dub):
    cursor.execute("UPDATE media SET dub = ? WHERE media_id = ?", (dub, media_id))
    conn.commit()

def update_media_vip_base(media_id,is_vip):
    cursor.execute("UPDATE media SET is_vip = ? WHERE media_id = ?", (is_vip, media_id))
    conn.commit()

def update_media_status_base(media_id,status):
    cursor.execute("UPDATE media SET status = ? WHERE media_id = ?", (status, media_id))
    conn.commit()

def update_episode_base(media_id,episode_num,episode_id):
    cursor.execute("UPDATE episodes SET episode_id = ? WHERE which_media = ? AND episode_num = ?", (episode_id, media_id, episode_num))
    conn.commit()

# ===================================================================
# ANIPASS & LUX UPDATES
def update_anipass_data_base():
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT user_id FROM users WHERE is_anipass < ? AND is_anipass != 0", (current_date,))
    data = cursor.fetchall()
    cursor.execute("UPDATE users SET is_anipass = 0 WHERE is_anipass < ? AND is_anipass != 0", (current_date,))
    conn.commit()
    return data

def update_lux_data_base():
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT user_id FROM users WHERE is_lux < ? AND is_lux != 0", (current_date,))
    data = cursor.fetchall()
    cursor.execute("UPDATE users SET is_lux = 0 WHERE is_lux < ? AND is_lux != 0", (current_date,))
    conn.commit()
    return data
  
