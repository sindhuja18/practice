import MySQLdb
import sys
import pandas as pd

minprice = int(raw_input('Enter min price: '))
maxprice = int(raw_input('Enter max price: '))
connection = MySQLdb.connect(host = "localhost" , user = "root", passwd = "enixta@123", db = "production")
cursor = connection.cursor()
# query = "select id, brand_name from brand"
# cursor.execute(query)
# brand = cursor.fetchall()
# for a in brand:
# 	brand_id, brand_name = a
# 	print brand_id, brand_name
# 	


products = pd.read_sql('select p.id as number_of_products, b.brand_name as brand_name from product p join brand b on b.id=p.brand_id where p.id in (select product_id from store_product_hist where product_id<2000 group by product_id having min(price) between {} and {})'.format(minprice, maxprice), con=connection)
html = products.groupby(['brand_name']).count()
pr_ids = ', '.join(map(str, list(products.number_of_products)))
# fp = open('pr_list.html','w')
# fp.write(html)

products = pd.read_sql('select b.brand_name as brand_name, sp.colval_14 as primary_camera, sp.colval_15 as secondary_camera, sc.score5 as Avg_score from product p join brand b on b.id=p.brand_id join product_spec_map sp on sp.product_id=p.id join product_score sc on sc.product_id=sp.product_id where sc.score_type="Total Score" and p.id in ({})'.format(pr_ids), con=connection)
products.primary_camera = products.primary_camera.str.extract('([0-9.]+)').astype(float)
products.secondary_camera = products.secondary_camera.str.extract('([0-9.]+)').astype(float)
html_average = products.groupby(['brand_name']).mean()

cm_table = pd.merge(html_average, html, left_index=True, right_index=True, how='inner')
cm_table = cm_table.sort(['Avg_score'], ascending=[True]).to_html()
fp = open('pr_Camera_average.html','w')
fp.write(cm_table)


