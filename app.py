
from flask import Flask, render_template, redirect, jsonify
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_tolzmank"
app.config["MYSQL_PASSWORD"] = "1874"
app.config["MYSQL_DB"] = "cs340_tolzmank"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Routes
@app.route('/', defaults={'user_id': None})
@app.route('/<int:user_id>', methods=['GET'])
def root(user_id):
        try:
            query = "SELECT * FROM users"
            cur = mysql.connection.cursor()
            cur.execute(query)
            users = cur.fetchall()
        except Exception as e:
            print(f"MySQL connect FAILED: {e}")
            return "<h1>Failed to connect to MySQL</h1>"
        
        if user_id is None:
            return render_template('index.j2', 
                                users = users,
                                user_id = None
                                )
        else:
            query = "SELECT * FROM users WHERE user_id = %s" % (user_id)
            cur = mysql.connection.cursor()
            cur.execute(query)
            user = cur.fetchall()

            query2 = """
                    SELECT location_name FROM locations WHERE location_id IN 
                    (SELECT location_id FROM users_locations WHERE user_id = %s)
                    """ % (user_id)
            cur = mysql.connection.cursor()
            cur.execute(query2)
            locations = cur.fetchall()

            query3 = """
                    SELECT
                        l.location_name,
                        sc.condition_reading,
                        c.condition_type,
                        c.measurement_unit,
                        sc.wind_direction,
                        sc.date_refreshed
                    FROM users_locations ul
                    JOIN locations l ON ul.location_id = l.location_id
                    JOIN locations_stations ls ON l.location_id = ls.location_id
                    JOIN stations_conditions sc ON ls.station_id = sc.station_id
                    JOIN conditions c ON sc.condition_id = c.condition_id
                    WHERE ul.user_id = %s
                    """ % (user_id)
            cur = mysql.connection.cursor()
            cur.execute(query3)
            report = cur.fetchall()


            return render_template('index.j2',
                                    users = users,
                                    user_id = user_id,
                                    user = user[0],
                                    locations = locations,
                                    display_names = {
                                        'Condition Type': 'condition_type',
                                        'Condition Reading': 'condition_reading',
                                        'Measurement Unit': 'measurement_unit',
                                        'Wind Direction': 'wind_direction',
                                        'Date Refreshed': 'date_refreshed',
                                    },
                                    report = report

                                   )



# -- GET REPORT for USER --
@app.route('/report', methods=['POST'])
def get_report():
    if request.form.get("Get_Report"):
        user_id = request.form["user_id"]
        query = """
                SELECT
                    l.location_name,
                    sc.condition_reading,
                    c.condition_type,
                    c.measurement_unit,
                    sc.wind_direction
                FROM users_locations ul
                JOIN locations l ON ul.location_id = l.location_id
                JOIN locations_stations ls ON l.location_id = ls.location_id
                JOIN stations_conditions sc ON ls.station_id = sc.station_id
                JOIN conditions c ON sc.condition_id = c.condition_id
                WHERE ul.user_id = %s
                """
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        surf_report = cur.fetchall()
        print(surf_report)
        return render_template('report.j2', surf_report = surf_report)


# MAIN TABLES
# -- CRUD: users --
@app.route('/users', methods=['GET'])
def show_users():
    query = "SELECT * FROM users"
    cur = mysql.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()
    return render_template('table.j2', 
                            data = users,
                            table_name = 'Users',
                            obj_name = 'user',
                            Obj_Name = 'User',
                            id = 'user_id',
                            main_name = 'username',
                            display_names = {
                                'ID': 'user_id',
                                'Username': 'username',
                                'Email': 'email'
                                }
                           )


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        if request.form.get("Add_User"):
            username = request.form['username']
            email = request.form['email']
            query = "INSERT INTO users (username, email) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (username, email))
            mysql.connection.commit()
        return redirect("/users")


@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
def update_user(user_id):
    if request.method == "GET":
        query = "SELECT * FROM users WHERE user_id = %s" % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        user = cur.fetchall()
        return render_template("table_update.j2", 
                                item_data = user,
                                table_name = 'Users',
                                obj_name = 'user',
                                Obj_Name = 'User',
                                obj_names = 'users',
                                ID = 'ID',
                                id = 'user_id',
                                display_names = {
                                    'ID': 'user_id',
                                    'Username': 'username',
                                    'Email': 'email'
                                    }
                               )

    if request.method == "POST":
        if request.form.get("Update_User"):
            user_id = request.form["user_id"]
            username = request.form["username"]
            email = request.form["email"]

            query = "UPDATE users SET users.username = %s, users.email = %s WHERE users.user_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (username, email, user_id))
            mysql.connection.commit()

            return redirect("/users")


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == "GET":
        query = "DELETE FROM users WHERE user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        mysql.connection.commit()

        return redirect("/users")



# -- CRUD: locations --
@app.route('/locations', methods=['GET'])
def show_locations():
    query = "SELECT * FROM locations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    locations = cur.fetchall()
    return render_template('table.j2', 
                            data=locations,
                            table_name = 'Locations',
                            obj_name = 'location',
                            Obj_Name = 'Location',
                            id = 'location_id',
                            main_name = 'location_name',
                            display_names = {
                                'ID': 'location_id',
                                'Location Name': 'location_name', 
                                'Coordinates': 'coordinates'
                            }
                           )


@app.route('/add_location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        if request.form.get("Add_Location"):
            location_name = request.form['location_name']
            coordinates = request.form['coordinates']
            query = "INSERT INTO locations (location_name, coordinates) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location_name, coordinates))
            mysql.connection.commit()
        return redirect("/locations")


@app.route('/update_location/<int:location_id>', methods=['POST', 'GET'])
def update_location(location_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM locations WHERE location_id = %s" % (location_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        location = cur.fetchall()
        return render_template("table_update.j2", 
                                item_data = location,
                                table_name = 'Locations',
                                obj_name = 'location',
                                Obj_Name = 'Location',
                                obj_names = 'locations',
                                id = 'location_id',
                                display_names = {
                                    'ID': 'location_id',
                                    'Location Name': 'location_name',
                                    'Coordinates': 'coordinates'
                                    }
                               )


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_Location"):
            # grab user form inputs
            location_id = request.form["location_id"]
            location_name = request.form["location_name"]
            coordinates = request.form["coordinates"]

            # no null inputs
            query = "UPDATE locations SET locations.location_name = %s, locations.coordinates = %s WHERE locations.location_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (location_name, coordinates, location_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/locations")


@app.route('/delete_location/<int:location_id>', methods=['GET', 'POST'])
def delete_location(location_id):
    if request.method == "GET":
        query = "DELETE FROM locations WHERE location_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (location_id,))
        mysql.connection.commit()
        return redirect("/locations")


# -- CRUD: stations --
@app.route('/stations', methods=['GET'])
def show_stations():
    query = "SELECT * FROM stations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    stations = cur.fetchall()
    return render_template('table.j2', 
                            data = stations,
                            table_name = 'Stations',
                            obj_name = 'station',
                            Obj_Name = 'Station',
                            id = 'station_id',
                            main_name = 'station_name',
                            display_names = {
                                'ID': 'station_id',
                                'Station Code': 'station_code',
                                'Station Name': 'station_name',
                                'Station URL': 'station_url'
                            }
                           )


@app.route('/add_station', methods=['POST'])
def add_station():
    if request.method == 'POST':
        if request.form.get("Add_Station"):
            station_code = request.form['station_code']
            station_name = request.form['station_name']
            station_url = request.form['station_url']
            date_refreshed = request.form['date_refreshed']
            query = "INSERT INTO stations (station_code, station_name, station_url, date_refreshed) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (station_code, station_name, station_url, date_refreshed))
            mysql.connection.commit()
        return redirect("/stations")


@app.route('/update_station/<int:station_id>', methods=['POST', 'GET'])
def update_station(station_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM stations WHERE station_id = %s" % (station_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        station = cur.fetchall()
        return render_template("table_update.j2", 
                            item_data = station,
                            table_name = 'Stations',
                            obj_name = 'station',
                            Obj_Name = 'Station',
                            id = 'station_id',
                            main_name = 'station_name',
                            display_names = {
                                'ID': 'station_id',
                                'Station Code': 'station_code',
                                'Station Name': 'station_name',
                                'Station URL': 'station_url'
                            }
                               )


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_Station"):
            # grab user form inputs
            station_id = request.form["station_id"]
            station_code = request.form["station_code"]
            station_name = request.form["station_name"]
            station_url = request.form["station_url"]
            date_refreshed = request.form["date_refreshed"]

            # no null inputs
            query = "UPDATE stations SET stations.station_code = %s, stations.station_name = %s, stations.station_url = %s, stations.date_refreshed = %s WHERE stations.station_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (station_code, station_name, station_url, date_refreshed, station_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/stations")


@app.route('/delete_station/<int:station_id>', methods=['GET', 'POST'])
def delete_station(station_id):
    if request.method == "GET":
        query = "DELETE FROM stations WHERE station_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (station_id,))
        mysql.connection.commit()
        return redirect("/stations")


# -- CRUD: conditions --
@app.route('/conditions', methods=['GET'])
def show_conditions():
    query = "SELECT * FROM conditions"
    cur = mysql.connection.cursor()
    cur.execute(query)
    conditions = cur.fetchall()
    return render_template('table.j2', 
                            data = conditions,
                            table_name = 'Conditions',
                            obj_name = 'condition',
                            Obj_Name = 'Condition',
                            id = 'condition_id',
                            main_name = 'condition_type',
                            display_names = {
                                'ID': 'condition_id',
                                'Condition Type': 'condition_type',
                                'Measurement Unit': 'measurement_unit',
                            }
                           )


@app.route('/add_condition', methods=['POST'])
def add_condition():
    if request.method == 'POST':
        if request.form.get("Add_Condition"):
            condition_type = request.form['condition_type']
            measurement_unit = request.form['measurement_unit']
            query = "INSERT INTO conditions (condition_type, measurement_unit) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (condition_type, measurement_unit))
            mysql.connection.commit()
        return redirect("/conditions")


@app.route('/update_condition/<int:condition_id>', methods=['POST', 'GET'])
def update_condition(condition_id):
    if request.method == "GET":
        query = "SELECT * FROM conditions WHERE condition_id = %s" % (condition_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        condition = cur.fetchall()
        return render_template("table_update.j2",                             
                                item_data = condition,
                                table_name = 'Conditions',
                                obj_name = 'condition',
                                Obj_Name = 'Condition',
                                id = 'condition_id',
                                main_name = 'condition_type',
                                display_names = {
                                    'ID': 'condition_id',
                                    'Condition Type': 'condition_type',
                                    'Measurement Unit': 'measurement_unit',
                            })


    if request.method == "POST":
        if request.form.get("Update_Condition"):
            condition_id = request.form["condition_id"]
            condition_type = request.form["condition_type"]
            measurement_unit = request.form["measurement_unit"]
            query = "UPDATE conditions SET conditions.condition_type = %s, conditions.measurement_unit = %s WHERE conditions.condition_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (condition_type, measurement_unit, condition_id))
            mysql.connection.commit()
            return redirect("/conditions")


@app.route('/delete_condition/<int:condition_id>', methods=['GET', 'POST'])
def delete_condition(condition_id):
    if request.method == "GET":
        query = "DELETE FROM conditions WHERE condition_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (condition_id,))
        mysql.connection.commit()

        return redirect("/conditions")


# INTERSECTION TABLES
# -- CRUD: locations_stations --
@app.route('/locations_stations/', defaults={'location_id': None})
@app.route('/locations_stations/<int:location_id>', methods=['GET'])
def show_locations_stations(location_id):
    query = "SELECT * FROM locations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    locations = cur.fetchall()
    if location_id is None:
        return render_template('intersect_table.j2', 
                                data = locations,
                                coverage = {},
                                table_name = 'Locations-Stations',
                                obj_name = 'locations_stations',
                                main_name = '',
                                main_id = 'location_id',
                                db_main_name = 'location_name',
                                view_select_name = 'Location',
                                view_label = 'Station Coverage'
                            )
    
    else:
        query = """
                SELECT s.station_id, s.station_code, s.station_name, s.station_url
                FROM locations_stations ls
                JOIN locations l ON ls.location_id = l.location_id
                JOIN stations s ON ls.station_id = s.station_id
                WHERE l.location_id = %s
                """ % (location_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        station_coverage = cur.fetchall()

        query2 = "SELECT location_name FROM locations WHERE location_id = %s" % (location_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        location_name = cur.fetchall()

        query3 = "SELECT * FROM stations"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_stations = cur.fetchall()

        return render_template('intersect_table.j2', 
                                data = locations,
                                coverage = station_coverage,
                                table_name = 'Locations-Stations',
                                obj_name = 'locations_stations',
                                main_name = location_name,
                                main_id = 'location_id',
                                db_main_name = 'location_name',
                                view_select_name = 'Location',
                                view_label = 'Station Coverage',

                                Obj_Name = 'Location-Station',
                                assoc_id = 'station_id',
                                ref_id = location_id,
                                display_names = {
                                    'Station ID': 'station_id',
                                    'Station Code': 'station_code',
                                    'Station Name': 'station_name',
                                    'URL': 'station_url'
                                },
                                assoc_name = 'Station',
                                db_assoc_name = ['station_code', 'station_name'],
                                all_assoc = all_stations
                            )


@app.route('/add_locations_stations', methods=['POST'])
def add_locations_stations():
    if request.method == 'POST':
        if request.form.get("Add"):
            location_id = request.form['location_id']
            station_id = request.form['station_id']
            query = "INSERT INTO locations_stations (location_id, station_id) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location_id, station_id))
            mysql.connection.commit()
            return redirect(f"/locations_stations/{location_id}")


@app.route('/delete_locations_stations/<int:location_id>/<int:station_id>', methods=['GET'])
def delete_locations_stations(location_id, station_id):
    if request.method == 'GET':
        query = "DELETE FROM locations_stations WHERE location_id = %s AND station_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (location_id, station_id))
        mysql.connection.commit()
        return redirect(f"/locations_stations/{location_id}")



# -- CRUD: users_locations --
@app.route('/users_locations/', defaults={'user_id': None})
@app.route('/users_locations/<int:user_id>', methods=['GET'])
def show_users_locations(user_id):
    query = "SELECT * FROM users"
    cur = mysql.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()
    if user_id is None:
        return render_template('intersect_table.j2', 
                                data = users,
                                coverage = {},
                                table_name = 'Users-Locations',
                                obj_name = 'users_locations',
                                main_name = '',
                                main_id = 'user_id',
                                db_main_name = 'username',
                                view_select_name = 'User',
                                view_label = 'Locations'
                            )
    
    else:
        query = """
                SELECT l.location_id, l.location_name, l.coordinates
                FROM users_locations ul
                JOIN users u ON ul.user_id = u.user_id
                JOIN locations l ON ul.location_id = l.location_id
                WHERE u.user_id = %s
                """ % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        selected_locations = cur.fetchall()

        query2 = "SELECT username FROM users WHERE user_id = %s" % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        username = cur.fetchall()

        query3 = "SELECT * FROM locations"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_locations = cur.fetchall()

        return render_template('intersect_table.j2', 
                                data = users,
                                coverage = selected_locations,
                                table_name = 'Users-Locations',
                                obj_name = 'users_locations',
                                main_name = username,
                                main_id = 'user_id',
                                db_main_name = 'username',
                                view_select_name = 'User',
                                view_label = 'Locations',

                                Obj_Name = 'User-Location',
                                assoc_id = 'location_id',
                                ref_id = user_id,
                                display_names = {
                                    'Location ID': 'location_id',
                                    'Location Name': 'location_name',
                                    'Coordinates': 'coordinates'
                                },
                                assoc_name = 'Location',
                                db_assoc_name = ['location_name'],
                                all_assoc = all_locations
                            )


@app.route('/add_users_locations', methods=['POST'])
def add_users_locations():
    if request.method == 'POST':
        if request.form.get("Add"):
            user_id = request.form['user_id']
            location_id = request.form['location_id']
            query = "INSERT INTO users_locations (user_id, location_id) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (user_id, location_id))
            mysql.connection.commit()
            return redirect(f"/users_locations/{user_id}")


@app.route('/delete_users_locations/<int:user_id>/<int:location_id>', methods=['GET'])
def delete_users_locations(user_id, location_id):
    if request.method == 'GET':
        query = "DELETE FROM users_locations WHERE user_id = %s AND location_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id, location_id))
        mysql.connection.commit()
        return redirect(f"/users_locations/{user_id}")


# -- CRUD: users_conditions --
@app.route('/users_conditions/', defaults={'user_id': None})
@app.route('/users_conditions/<int:user_id>', methods=['GET'])
def show_users_conditions(user_id):
    query = "SELECT * FROM users"
    cur = mysql.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()
    if user_id is None:
        return render_template('intersect_table.j2', 
                                data = users,
                                coverage = {},
                                table_name = 'Users-Conditions',
                                obj_name = 'users_conditions',
                                main_name = '',
                                main_id = 'user_id',
                                db_main_name = 'username',
                                view_select_name = 'User',
                                view_label = 'Conditions'
                            )
    
    else:
        query = """
                SELECT c.condition_id, c.condition_type, c.measurement_unit
                FROM users_conditions uc
                JOIN users u ON uc.user_id = u.user_id
                JOIN conditions c ON uc.condition_id = c.condition_id
                WHERE u.user_id = %s;
                """ % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        selected_conditions = cur.fetchall()

        query2 = "SELECT username FROM users WHERE user_id = %s" % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        username = cur.fetchall()

        query3 = "SELECT * FROM conditions"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_conditions = cur.fetchall()

        return render_template('intersect_table.j2', 
                                data = users,
                                coverage = selected_conditions,
                                table_name = 'Users-Conditions',
                                obj_name = 'users_conditions',
                                main_name = username,
                                main_id = 'user_id',
                                db_main_name = 'username',
                                view_select_name = 'User',
                                view_label = 'Conditions for User',

                                Obj_Name = 'User-Condition',
                                assoc_id = 'condition_id',
                                ref_id = user_id,
                                display_names = {
                                    'Condition ID': 'condition_id',
                                    'Condition Type': 'condition_type',
                                    'Measurement Unit': 'measurement_unit'
                                },
                                assoc_name = 'Condition',
                                db_assoc_name = ['condition_type'],
                                all_assoc = all_conditions
                            )


@app.route('/add_users_conditions', methods=['POST'])
def add_users_conditions():
    if request.method == 'POST':
        if request.form.get("Add"):
            user_id = request.form['user_id']
            condition_id = request.form['condition_id']
            query = "INSERT INTO users_conditions (user_id, condition_id) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (user_id, condition_id))
            mysql.connection.commit()
            return redirect(f"/users_conditions/{user_id}")


@app.route('/delete_users_conditions/<int:user_id>/<int:condition_id>', methods=['GET'])
def delete_users_conditions(user_id, condition_id):
    if request.method == 'GET':
        query = "DELETE FROM users_conditions WHERE user_id = %s AND condition_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id, condition_id))
        mysql.connection.commit()
        return redirect(f"/users_conditions/{user_id}")


# -- CRUD: stations_conditions --
@app.route('/stations_conditions/', defaults={'station_id': None})
@app.route('/stations_conditions/<int:station_id>', methods=['GET'])
def show_stations_conditions(station_id):
    query = "SELECT * FROM stations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    stations = cur.fetchall()
    if station_id is None:
        return render_template('intersect_table.j2', 
                                data = stations,
                                coverage = {},
                                table_name = 'Stations-Conditions',
                                obj_name = 'stations_conditions',
                                main_name = '',
                                main_id = 'station_id',
                                db_main_name = 'station_name',
                                view_select_name = 'Station',
                                view_label = 'Conditions'
                            )
    
    else:
        query = """
                SELECT sc.reading_id, c.condition_type, sc.condition_reading, c.measurement_unit, sc.wind_direction, sc.date_refreshed
                FROM stations_conditions sc
                JOIN stations s ON sc.station_id = s.station_id
                JOIN conditions c ON sc.condition_id = c.condition_id
                WHERE s.station_id = %s 
                """ % (station_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        readings = cur.fetchall()

        query2 = "SELECT station_name FROM stations WHERE station_id = %s" % (station_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        station_name = cur.fetchall()

        query3 = "SELECT * FROM conditions"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_conditions = cur.fetchall()

        return render_template('intersect_table.j2', 
                                data = stations,
                                coverage = readings,
                                table_name = 'Stations-Conditions',
                                obj_name = 'stations_conditions',
                                main_name = station_name,
                                main_id = 'station_id',
                                db_main_name = 'station_name',
                                view_select_name = 'Station',
                                view_label = 'Conditions',

                                Obj_Name = 'Station-Condition',
                                assoc_id = 'reading_id',
                                ref_id = station_id,
                                display_names = {
                                    'Reading ID': 'reading_id',
                                    'Condition Type': 'condition_type',
                                    'Condition Reading': 'condition_reading',
                                    'Measurement Unit': 'measurement_unit',
                                    'Wind Direction': 'wind_direction',
                                    'Date Refreshed': 'date_refreshed',
                                },
                                assoc_name = 'Reading',
                                db_assoc_name = ['condition_type'],
                                all_assoc = {},
                                all_conditions = all_conditions,
                                wind_compass = [
                                    'N', 'NNE', 'NE', 'ENE',
                                    'E', 'ESE', 'SE', 'SSE',
                                    'S', 'SSW', 'SW', 'WSW',
                                    'W', 'WNW', 'NW', 'NNW'
                                ]
                            )


@app.route('/add_stations_conditions', methods=['POST'])
def add_stations_conditions():
    if request.method == 'POST':
        if request.form.get("Add"):
            station_id = request.form['station_id']
            condition_id = request.form['condition_id']
            condition_reading = request.form['condition_reading']
            wind_direction = request.form['wind_direction']
            date_refreshed = request.form['date_refreshed']
            query = "INSERT INTO stations_conditions (station_id, condition_id, condition_reading, wind_direction, date_refreshed) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (station_id, condition_id, condition_reading, wind_direction, date_refreshed))
            mysql.connection.commit()
            return redirect(f"/stations_conditions/{station_id}")


@app.route('/delete_stations_conditions/<int:station_id>/<int:reading_id>', methods=['GET'])
def delete_stations_conditions(station_id, reading_id):
    if request.method == 'GET':
        query = "DELETE FROM stations_conditions WHERE reading_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (reading_id,))
        mysql.connection.commit()
        return redirect(f"/stations_conditions/{station_id}")


@app.route('/update_stations_conditions/<int:reading_id>/<int:station_id>', methods=['POST', 'GET'])
def update_stations_conditions(reading_id, station_id):
    if request.method == "GET":
        query = "SELECT * FROM stations_conditions WHERE reading_id = %s" % (reading_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        reading = cur.fetchall()

        query2 = "SELECT * FROM stations WHERE station_id = %s" % (station_id)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        station = cur.fetchall()

        query3 = "SELECT * FROM conditions"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_conditions = cur.fetchall()

        query4 = "SELECT condition_type FROM conditions WHERE condition_id = %s" % (reading[0]['condition_id'])
        cur = mysql.connection.cursor()
        cur.execute(query4)
        current_condition_type = cur.fetchall()
        

        return render_template("intersect_table_update.j2", 
                                reading=reading,
                                station_id = station_id,
                                station = station,
                                current_condition_type = current_condition_type[0]['condition_type'],
                                all_conditions = all_conditions,
                                display_names = {
                                    'Condition Type': 'condition_type',
                                    'Condition Reading': 'condition_reading',
                                    'Wind Direction': 'wind_direction',
                                    'Date Refreshed': 'date_refreshed'
                                },
                                wind_compass = [
                                    'N', 'NNE', 'NE', 'ENE',
                                    'E', 'ESE', 'SE', 'SSE',
                                    'S', 'SSW', 'SW', 'WSW',
                                    'W', 'WNW', 'NW', 'NNW'
                                ]
                               )


    if request.method == "POST":
        if request.form.get("Update"):
            condition_id = request.form['condition_id']
            condition_reading = request.form['condition_reading']
            wind_direction = request.form['wind_direction']
            date_refreshed = request.form['date_refreshed']
            query = """
                UPDATE stations_conditions 
                SET stations_conditions.condition_id = %s, 
                    stations_conditions.condition_reading = %s,
                    stations_conditions.wind_direction = %s,
                    stations_conditions.date_refreshed = %s
                WHERE stations_conditions.reading_id = %s
                """
            cur = mysql.connection.cursor()
            cur.execute(query, (condition_id, condition_reading, wind_direction, date_refreshed, reading_id))
            mysql.connection.commit()
            return redirect(f"/stations_conditions/{station_id}")




# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3181)) 
    app.run(port=port, debug=True)