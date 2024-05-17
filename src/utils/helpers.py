def get_database_queries(file: str):
    with open(file, "r") as sql_file:
        sql_script = sql_file.read()
    return sql_script
