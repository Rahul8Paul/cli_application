import sys
from command_lib.run_command.command import Command
from datetime import datetime
if __name__ == "__main__":
    query_name = sys.argv[1]
    granularity = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    category = sys.argv[5]
    #TODO: conn_url can be taken from a secret file coming from password vault.
    conn_url = "mysql+mysqlconnector://ecom_user:ecom_pass@localhost/ecom_db"
    Command().execute(query_name=query_name, granularity=granularity, start= datetime.strptime(start_date, "%Y-%m-%d"), end= datetime.strptime(end_date, "%Y-%m-%d"), category=category, conn_url=conn_url)