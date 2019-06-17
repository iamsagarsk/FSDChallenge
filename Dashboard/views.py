from django.shortcuts import render
import play_scraper
import psycopg2
import psycopg2.extras


def dashboard_view(request):
    connection = psycopg2.connect(user="postgres",
                                  password="root",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor=connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    check_table_query="select exists(select 1 from information_schema.tables where table_name='top_apps')"
    cursor.execute(check_table_query)
    record1=cursor.fetchone()

    if request.method == 'GET':
        if record1['exists'] == True:
            top_apps = "select * from top_apps"
            cursor.execute(top_apps)
            record = cursor.fetchall()
            return render(request, "Dashboard/index.html", record)

        else:
            create_table_query = "create table top_apps(app_id varchar(50) not null, url varchar(150) not null, icon varchar(150) not null, title varchar(50) not null, developer varchar(50) not null, description varchar(150) not null, score varchar(50) not null, primary key(app_id))"
            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL")
            top_free_apps = play_scraper.collection(collection='TOP_FREE')
            for app in top_free_apps:
                insert_query = "insert into top_apps values ($$" + app['app_id'] +"$$, $$" + app['url'] + "$$, $$" + app['icon'] + "$$, $$" + app['title'] + "$$, $$" + app['developer'] + "$$, $$" + app['description'] + "$$, $$" + app['score'] + "$$)"
                cursor.execute(insert_query)
                connection.commit()
            top_apps = "select * from top_apps"
            cursor.execute(top_apps)
            record = cursor.fetchall()
            return render(request, "Dashboard/index.html", record)

    if request.method =='POST':
        top_free_apps = play_scraper.collection(collection='TOP FREE')
        for app in top_free_apps:
            insert_query = "insert into top_apps values ($$" + app['app_id'] +"$$, $$" + app['url'] + "$$, $$" + app['icon'] + "$$, $$" + app['title'] + "$$, $$" + app['developer'] + "$$, $$" + app['description'] + "$$, $$" + app['score'] + "$$) where not exists( select * from top_apps where app_id = " + app['app_id'] +")"
            cursor.execute(insert_query)
            connection.commit()
        top_apps = "select * from top_apps"
        cursor.execute(top_apps)
        record = cursor.fetchall()
        return render(request, "Dashboard/index.html", record)