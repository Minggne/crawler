from to_mysql import db_config, conn, cursor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. In ra danh sách bài viết
# 2. Lọc bài viết nhiều (ít) likes, shares, comments nhất
# 3. Lọc bài viết nhiều (ít) tương tác nhất
# 4. Lọc bài viết theo từ khóa (những bài viết nào có từ khóa..)
# 5. Vẽ biểu đồ tương tác (likes, shares, comments, tương tác)
# 6. Phân tích xu hướng..

def return_profile_user():
    query = f"SELECT url, num_follower FROM profile_user ORDER BY profile_id DESC LIMIT 1"
    cursor.execute(query)
    data = cursor.fetchall()
    # cursor.close()
    return data
def get_post_info(url_page):
    query = f"SELECT post_id, post_content, likes, shares, comments, collected_time FROM posts WHERE url_page LIKE '%{url_page}%'"
    cursor.execute(query)
    data = cursor.fetchall()
    # cursor.close()
    return data

# print(get_post_info("https://www.facebook.com/ctsvdhbkdhdn"))
def filter_keyword(field, option, limit, keyword):
    query = f"SELECT post_id, post_content, likes, shares, comments, collected_time FROM posts WHERE post_content LIKE '%{keyword}%' ORDER BY {field} {option} LIMIT {limit}"
    cursor.execute(query)
    data = cursor.fetchall()
    return data


# filter_keyword("likes", "DESC", "3", "")

# field = likes, shares, comments
# option = ASC, DESC
# limit = int
# keyword = str

def analysis_count_reaction():
    cursor.execute("SELECT COUNT(*) FROM posts")
    num_posts = cursor.fetchone()[0]

    cursor.execute("SELECT post_content, likes, shares, comments FROM posts")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["Post Content", "Likes", "Shares", "Comments"])

    cursor.close()
    conn.close()

    totals = df[["Likes", "Shares", "Comments"]].sum()

    plt.figure(figsize=(8, 5))
    totals.plot(kind="bar", color=["skyblue", "orange", "lightgreen"])
    plt.title(f"Tổng số Likes, Shares, và Comments của {num_posts} bài viết gần nhất")
    plt.ylabel("Số lượng")
    plt.xlabel("Chỉ số")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def compare_post():
    cursor.execute("SELECT COUNT(*) FROM posts")
    num_posts = cursor.fetchone()[0]

    cursor.execute("SELECT post_content, likes, shares, comments FROM posts")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["Post Content", "Likes", "Shares", "Comments"])

    top_posts = df.head(num_posts)  

    x = range(len(top_posts))
    width = 0.25

    plt.figure(figsize=(12, 6))
    plt.bar([p - width for p in x], top_posts["Likes"], width=width, label="Likes", color="skyblue")
    plt.bar(x, top_posts["Shares"], width=width, label="Shares", color="orange")
    plt.bar([p + width for p in x], top_posts["Comments"], width=width, label="Comments", color="lightgreen")

    plt.xticks(x, top_posts["Post Content"], rotation=45, ha="right")
    plt.title("Phân tích Likes, Shares, và Comments từng bài viết")
    plt.ylabel("Số lượng")
    plt.xlabel("Bài viết")
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def compare_reaction():
    cursor.execute("SELECT post_content, likes, shares, comments FROM posts")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["Post Content", "Likes", "Shares", "Comments"])
    
    sns.pairplot(df[["Likes", "Shares", "Comments"]])
    plt.suptitle("Mối quan hệ giữa Likes, Shares, và Comments", y=1.02)
    plt.show()
