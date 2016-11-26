import MySQLdb
import sys
import pandas as pd
import re


minprice = int(raw_input('Enter Min Price Value: '))
maxprice = int(raw_input('Enter Max Price Value: '))
connection = MySQLdb.connect(host = "localhost" , user = "root", passwd = "enixta@123", db = "production")
cursor = connection.cursor()

products = pd.read_sql('select p.id as number_of_products, b.brand_name as brand_name from product p join brand b on b.id=p.brand_id where p.id in (select product_id from store_product_hist where product_id<2000 group by product_id having min(price) between {} and {})'.format(minprice, maxprice), con=connection)
html = products.groupby(['brand_name']).count()
pr_ids = ', '.join(map(str, list(products.number_of_products)))
# fp = open('pr_list.html','w')
# fp.write(html)
products = pd.read_sql('select b.brand_name as brand_name, sp.colval_11 as inches, sp.colval_55 as ppi, sc.score5 as total_score from product p join brand b on b.id=p.brand_id join product_spec_map sp on sp.product_id=p.id join product_score sc on sc.product_id=sp.product_id where sc.score_type="Total Score" and p.id in ({})'.format(pr_ids), con=connection)
# products['colval_55'] = map(replace_empty, products['colval_55'])
products.inches = products.inches.str.extract('([0-9.]+)').astype(float)
products.ppi = products.ppi.str.extract('([0-9.]+)',flags=0).astype(float)
products = products.fillna(value=0)
html_average = products.groupby(['brand_name']).mean()

cm_table = pd.merge(html_average, html, left_index=True, right_index=True, how='inner')
cm_table = cm_table.sort(['total_score'], ascending=[True]).to_html()
fp = open('pr_display_average.html','w')
fp.write(cm_table)
