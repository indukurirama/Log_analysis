#!/usr/bin/env python2

# importing Postgresql library
import psycopg2

''' Database query to print top 3 articles '''

cateChize_1 = '      $$$ Most popular three articles of all time $$$ '
report_articles = """
SELECT articles.title, COUNT (*) as views FROM
articles JOIN log ON articles.slug = SUBSTRING(path, 10)
GROUP BY path, articles.title
ORDER BY views  desc LIMIT 3;
"""

''' Database query to print top authors of all time '''

cateChize_2 = '     $$$ Top most popular article authors of all time $$$ '
report_authors = """
SELECT authors.name, count(log.path) as views FROM\
                 articles, log, authors\
                 WHERE log.path=('/article/'||articles.slug)\
                 AND articles.author = authors.id \
                 GROUP BY authors.name ORDER BY views desc
"""

''' Database query to display day more than 1% of requests lead to errors '''

cateChize_3 = '      $$$ Days more than 1% of requests lead to errors $$$ '
report_errors = """
select * from (
    select a.day,
    round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
    as errp from
        (select date(time) as day, count(*) as hits from log group by day) as a
        inner join
        (select date(time) as day, count(*) as hits from log where status
        like '%404%' group by day) as b
    on a.day = b.day)
as t where errp > 1.0;
"""


class Analysis:
    def __init__(auto):
        try:
            auto.database = psycopg2.connect('dbname=news')
            auto.cursor = auto.database.cursor()
        except Exception as e:
            print e

    def report_query(auto, query):
        auto.cursor.execute(query)
        return auto.cursor.fetchall()

    def report(auto, pro, query, data='views'):
        query = query.replace('\n', ' ')
        output = auto.report_query(query)
        print pro
        for s in range(len(output)):
            print '\n', '\t', '*',  output[s][0], '--->', output[s][1], data

    def exit(auto):
        auto.database.close()

if __name__ == '__main__':
    Request = Analysis()
    Request.report(cateChize_1, report_articles)
    Request.report(cateChize_2, report_authors)
    Request.report(cateChize_3, report_errors, '% error')
    Request.exit()
