import MySQLdb
import sys
import pandas as pd

connection = MySQLdb.connect(host = "localhost" , user = "root", passwd = "enixta@123", db = "production")
cursor = connection.cursor()

brand = pd.read_sql('select p.id as number_of_products, b.brand_name as brand_name from product p join brand b on b.id=p.brand_id where p.id<2000', con=connection)
html = brand.groupby(['brand_name']).count()

Battery = pd.read_sql('select b.brand_name as Brand_name, ps.colval_23 as capacity, s.score5 as Avg_score from product p join brand b on b.id=p.brand_id join product_spec_map ps on ps.product_id=p.id join product_score s on s.product_id=ps.product_id where s.score_type="Total score" and p.id<2000', con=connection)
Battery.capacity = Battery.capacity.str.extract('([0-9.]+)',flags=0).astype(float)
Battery = Battery.fillna(value=0)
html_avg = Battery.groupby(['Brand_name']).mean()

cm_table = pd.merge(html_avg, html, left_index=True, right_index=True, how='inner')
cm_table = cm_table.sort(['Avg_score'], ascending=[True]).to_html()
fp = open('pr_battery_average.html','w')
fp.write(cm_table)
