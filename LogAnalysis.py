import psycopg2  # Import posgreSQL python module
"""
This code is aimed to answer 3 questions from newsdata.sql database.
The questions are:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
"""
"""
3 Views are created in the newsdata.sql at the code makes
use of them. The views are:
- popular_articles
- total_log
- failed_log
"""


def top_3_articles(db):
    cursor = db.cursor()
    cursor.execute('select * from popular_articles')
    results = cursor.fetchall()
    return results


def most_popular_author(db):
    cursor = db.cursor()
    cursor.execute('''select name,SUM(views) as views from (select authors.name,
                      articles.slug, popular_articles.views from
                      popular_articles, articles,
                      authors where authors.id = articles.author and
                      popular_articles.slug = articles.slug)
                      as best_authors group by name order by views desc''')
    results = cursor.fetchall()
    return results


def day_request_error(db):
    cursor = db.cursor()
    cursor.execute('''select failed_log.date,
                      100.0 * (failed_log.failed_views::real/
                      total_log.total_views::real) as failure_percentage
                      from failed_log,total_log
                      where failed_log.date = total_log.date
                      order by failure_percentage desc''')
    results = cursor.fetchall()
    return results


def answer(value1, value2, value3):
    print('The most popular 3 articles are: {0}, {1}, {2}'.format(
           value1[0][0], value1[1][0], value1[2][0]))
    print('The most popular author is: {}'.format(value2[0][0]))
    print('The day that had more than 1 percent of error is: {}'.format(
          value3[0][0]))
    print(type(value3[0][0]))


def main():
    db = psycopg2.connect('dbname = news')
    top_articles = (top_3_articles(db))
    top_author = most_popular_author(db)
    worst_day = day_request_error(db)
    answer(top_articles, top_author, worst_day)
    db.close()
main()
