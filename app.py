from flask import Flask, render_template, request, jsonify
from DatabaseConnection import DatabaseConnectionClass
import random
import os

template_dir = os.path.abspath('templates')
app = Flask(__name__, 
            static_url_path='/static', 
            template_folder=template_dir)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account.html')
def account():
    return render_template('account.html')

@app.route('/user.html')
def user():
    return render_template('user.html')

@app.route('/process-request', methods=['POST'])
def process_request(): # this method processes all data taken in
    data = request.json
    print('Received Data: ', data)
    # Execute Functions based on input
    request_type = data['request_type']
    if request_type == 'login':
        return login_user(data)
    elif request_type == 'register':
        return register_user(data)
    elif request_type == 'form':
        return populate_table(data)
    elif (request_type == 'update_user_table') or (request_type == 'store_rating') or (request_type == 'update_allergen') or (request_type == 'delete_user'):
        return user_data(data)
    else:
        return jsonify({'message': 'Invalid request type'}), 400
  
@app.route('/restaurant_count', methods=['POST'])  
def restaurant_count():
    # aggregate function 
    count_restaurants_query = """
        SELECT COUNT(r.restaurant_id)
        FROM Restaurant r;
    """
    with DatabaseConnectionClass() as db:
        db.cursor.execute(count_restaurants_query)
        results = db.cursor.fetchall()
        row = results[0][0]
        
    successMessage = 'Restaurant Count has been collected'
    user_data = {
        'restaurant_count': row,
        'table': 'Empty',
        'success': successMessage
    }
    
    return user_data
    
@app.route('/populate_table', methods=['POST'])
def populate_table(data): # Table will contain the entire Restaurant table, filtered by the allergen and restaurant type
    food_type = data.get('form_food_type', 'Unknown')
    allergens = data.get('form_allergens', ['None'])
    print('Restaurant Type: ',food_type)
    print('Allergens: ', allergens)
    
    with DatabaseConnectionClass() as db:
        # filter for restaurant type and allergens
        allergens_str = ', '.join([f"'{a}'" for a in allergens])

        # filter for restaurant type and allergens
        filter_query = f"""
            SELECT DISTINCT r.name, r.address, r.distance_miles, r.restaurant_type, r.average_price_score
            FROM Restaurant r
            LEFT JOIN Menu m ON r.restaurant_id = m.restaurant_id
            WHERE r.restaurant_type = '{food_type}' AND m.allergens NOT IN ({allergens_str});
        """
        db.cursor.execute(filter_query)
        table = db.cursor.fetchall()
        print('Table: ', table)
    
        response = {
            'request_type':'table',
            'table': table,
            'user_info': 'Empty',
            'user_data': 'Empty'
        }
        return jsonify(response)
  
@app.route('/login_user', methods=['POST'])  
def login_user(data):
    user_email = data.get('user_email', 'Unknown')
    user_password = data.get('user_password', 'Unknown')
    with DatabaseConnectionClass() as db:
        validate_login_query = f"""
        SELECT name, email, password, allergens
        FROM User
        WHERE email='{user_email}' and password='{user_password}' and (user_id IS NOT NULL);
        """
        db.cursor.execute(validate_login_query) # check if email and password match anything 
        results = db.cursor.fetchall() # returns the row with that user
        success = False
        
        for row in results:
            print(row)
            name, email, password, allergens = row
            if name:
                success = True # if success, suggestions display based on allergens
                user_info = {
                    'success': success,
                    'name': name, 
                    'allergens': allergens
                }   
                user_table_query = f"""
                    SELECT r.name, r.address, r.distance_miles, r.restaurant_type, r.average_price_score, s.rating
                    FROM Restaurant r
                    LEFT JOIN Menu m ON r.restaurant_id = m.restaurant_id
                    JOIN Serves s ON r.restaurant_id = s.restaurant_id
                    WHERE m.allergens NOT IN ('{allergens}');  
                """
                db.cursor.execute(user_table_query)
                results = db.cursor.fetchall()
                
                response = {
                    'request_type':'login',
                    'table': results,
                    'user_info': user_info,
                    'user_data': restaurant_count()
                }

        return jsonify(response)

@app.route('/register_user', methods=['POST'])  
def register_user(data):
    user_name = data.get('user_name', 'Unknown')
    user_email = data.get('user_email', 'Unknown')
    user_password = data.get('user_password', 'Unknown')
    user_allergens = data.get('user_allergens', 'None')
    user_id = random.randint(4, 100)
    
    with DatabaseConnectionClass() as db:
        change_user_id = db.checkUserId(user_id)
        while change_user_id:
            print('in loop')
            user_id += 1
            change_user_id = db.checkUserId(user_id)
        
        create_account_query = f"""
        INSERT INTO User(user_id, name, email, password, isAdmin, allergens) VALUES ('{user_id}', '{user_name}', '{user_email}', '{user_password}', 0, '{user_allergens}');
        """
        db.cursor.execute(create_account_query)
        db.db.commit()        
        print('User has been inserted')
        
        user_table_query = f"""
            SELECT r.name, r.address, r.distance_miles, r.restaurant_type, r.average_price_score, s.rating
            FROM Restaurant r
            LEFT JOIN Menu m ON r.restaurant_id = m.restaurant_id
            JOIN Serves s ON r.restaurant_id = s.restaurant_id
            WHERE m.allergens NOT IN ('{user_allergens}');        
        """
        db.cursor.execute(user_table_query)
        results = db.cursor.fetchall()
        
        user_info = {
            'success': True,
            'name': user_name, 
            'allergens': user_allergens
        }   
        response = {
            'request_type':'register',
            'table': results,
            'user_info': user_info,
            'user_data': restaurant_count()
        }
    return jsonify(response)

@app.route('/user_data', methods=['POST']) 
# This function pulls previous user data to make their custom dashboard
def user_data(data): 
    user_data_type = data.get('user_data_type', 'Unknown')
    user_food_type = data.get('user_food_type', 'Unknown')
    rating_email = data.get('rating_email', 'Unknown')
    store_restaurant = data.get('store_restaurant', 'Unknown')
    store_rating = data.get('store_rating', 0)
    delete_email = data.get('delete_email', 'Unknown')
    delete_password = data.get('delete_password', 'Unknown')
    update_allergen_email = data.get('update_allergen_email', 'Unknown')
    update_allergen_password = data.get('update_allergen_password', 'Unknown')
    update_allergen = data.get('update_allergen', 'Unknown')
    
    results = 'Unknown'
    successMessage = 'Failed'
    with DatabaseConnectionClass() as db:
        if (user_data_type == 'update_user_table'):
        # add additional restaurants to userTable
            user_table_query = f"""
            SELECT DISTINCT r.name, r.address, r.distance_miles, r.restaurant_type, r.average_price_score
            FROM Restaurant r
            LEFT JOIN Menu m ON r.restaurant_id = m.restaurant_id
            WHERE r.restaurant_type = '{user_food_type}';        
            """
            
            db.cursor.execute(user_table_query)
            results = db.cursor.fetchall()
            print('userTable information has been collected')
            successMessage = 'Table has been updated successfully'
        elif (user_data_type == 'store_rating'):
        # store rating for a restaurant in serves 
            restaurant_id_query = f"""
                SELECT restaurant_id AS id FROM Restaurant WHERE name = '{store_restaurant}'
                UNION
                SELECT user_id AS id FROM User WHERE email = '{rating_email}';
            """
            db.cursor.execute(restaurant_id_query)
            results = db.cursor.fetchall()
            print('---------------',results)
            restaurant_id = results[0][0]
            user_id = results[1][0]
            store_rating_query = f"""
                INSERT INTO Serves(restaurant_id, user_id, rating) 
                VALUES ('{restaurant_id}', '{user_id}', {store_rating});        
            """
            db.cursor.execute(store_rating_query)
            db.db.commit()
            print(f'Restaurant: {store_restaurant} has a new rating: {store_rating}')
            successMessage = 'Rating has been stored'
        elif (user_data_type == 'delete_user'):
            # delete user 
            delete_user_query = f"""
            DELETE FROM User 
            WHERE email='{delete_email}' AND password='{delete_password}';
            """
            db.cursor.execute(delete_user_query)
            db.db.commit()
            print(f'User {delete_email} has been deleted')
            successMessage = 'User has been deleted'
        elif (user_data_type == 'update_allergen'):
        # update allergen
            update_allergen_query = f"""
                UPDATE User
                SET allergens = '{update_allergen}'
                WHERE email='{update_allergen_email}' AND password='{update_allergen_password}';
            """
            db.cursor.execute(update_allergen_query)
            db.db.commit()
            print(f'User {update_allergen_email} has an updated allergen')
            successMessage = 'Allergen has been updated for the user'
        else:
            print('Error has occurred: User Data Type = ', user_data_type)
            
        user_data = {
        'restaurant_count': 0,
        'table': results,
        'success': successMessage
        }

        response = {
            'request_type': user_data_type,
            'table': 'Empty',
            'user_info': 'Empty',
            'user_data': user_data
        }
        
    return jsonify(response)
if __name__=='__main__':
    app.run(debug=True)