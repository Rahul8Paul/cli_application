from command_lib.dataset_io.mysql_io import MySqlIO
import pandas as pd


df = pd.read_csv("db/data.csv", encoding= 'utf-8')
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
conn_url = "mysql+mysqlconnector://ecom_user:ecom_pass@localhost/ecom_db"
mysql_operator = MySqlIO()
#mysql_operator.write_dataset(df, conn_url=conn_url, table_name="sales_table")
#df_read = mysql_operator.query_table("select sum(Quantity), Description, Country from sales_table  where date(InvoiceDate) = '2010-12-10' group by Description, Country", conn_url=conn_url)
#print(df_read)

