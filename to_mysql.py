import mysql.connector
import datetime

# Thông tin kết nối cơ sở dữ liệu
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'daovannminnh',
    'database': 'social_media_data'
}

# Kết nối đến MySQL
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Kết nối thành công!")
except mysql.connector.Error as err:
    print(f"Lỗi: {err}")
    
def insert_profile_target(url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos):
    sql = """
    INSERT INTO profile_target (url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos)

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Thêm profile dùng thành công!")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm người dùng: {err}")

def insert_profile_user(url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos):
    sql = """
    INSERT INTO profile_user (url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (url, cover_image, logo_image, num_like, num_follower, num_following, detail, post_photos)

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Thêm người dùng thành công!")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm người dùng: {err}")

# insert_profile_user("url", "cover_image", "logo_image", 8, 7, 6, "detail", "post_photos")

# Gọi hàm để thêm người dùng
# insert_profile_target(1, "https://www.facebook.com/ctsvdhbkdhdn", "https://scontent.fdad1-2.fna.fbcdn.net/v/t39.30808-6/295675637_3129675700629093_2629172712890429347_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeFyc7XLgVrdIthh2iybThWowxlYltUNCWTDGViW1Q0JZObEkYOR30GRXIjjlA_zUF7urwv0sVxy7Ow2Dd7cZ8qn&_nc_ohc=RJLv2wDDna0Q7kNvgERJl3y&_nc_oc=AdibNMmFuivcZTS6WIyc78JnCgGWg0NiG6kGtXbyiw2GK6N33KBwXXaUJL7h6tOIndmcdz9EQ_MjhjYMjs6s8Lsb&_nc_zt=23&_nc_ht=scontent.fdad1-2.fna&_nc_gid=A82gYa5bTedEhKbQkx649T7&oh=00_AYA2DffhsnkzkY2MSs_jfJWwNF51u7xwLNmZFMPdeIHl2w&oe=67700C78", "https://scontent.fdad1-1.fna.fbcdn.net/v/t39.30808-6/298200072_3142268236036506_1359487990849628224_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEODiq3wFEMTBwvDogvGHxp6SO5kpqamk3pI7mSmpqaTfeEloBQXCdH6FFjsOIx2AEidQ0W43WsCBE5iWEHxTBo&_nc_ohc=8JOodf-Nwp8Q7kNvgGi11RP&_nc_oc=AdjQtx7SeFya63tGA7NrkeKRSTxSffiaSOu5zFgCzkwIWIVDkWj98wtX4GYwyVG6ZHmvH6bCIP2-NtZT7hcrNhqK&_nc_zt=23&_nc_ht=scontent.fdad1-1.fna&_nc_gid=APDCHM596oT5_VleELb0bZ9&oh=00_AYA3cIBiFKhpEyzeJ3XN2OquiMCrEdMxbjdA0O58HKNVJg&oe=67702544", 3000, 4500, 2, "Phòng CTSV", None)

def insert_post(post_content, link_post, link_img, likes, comments, shares, collected_time, url_page):
    sql = """
    INSERT INTO posts (post_content, link_post, link_img, likes, comments, shares, collected_time, url_page)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (post_content, link_post, link_img, likes, comments, shares, collected_time, url_page)

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Thêm bài viết thành công!")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm bài viết: {err}")
# insert_post("post_content", "link_post", "link_img", 5, 6, 7, datetime.datetime.now(), "url_page")
# Gọi hàm để thêm bài viết
# insert_post("pfbid0zJWu2RS6SvPRLtWLLAGPwpGSC1E9HgkJNi9kv3P1PDTD7wtto442KZM3vZKJsa7Cl", 1, "Like+Shares", "2024-12-04 14:00:00", 100, 50)



