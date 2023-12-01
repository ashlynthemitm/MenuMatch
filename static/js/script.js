// Global Variables for sending the request
let form_info = {
    'name': 'Unknown',
    'food_type': 'Unknown',
    'allergens': []
};

let user_info = {
    'name': 'Unknown', 
    'email': 'Unknown',
    'password': 'Unknown', 
    'allergens': 'Unknown'
}

let user_data = {
    'user_data_type': 'restaurantCount',
    'restaurant_count': 0,
    'user_food_type': 'Unknown',
    'rating_email': 'Unknown',
    'store_restaurant': 'Unknown',
    'store_rating': 0,
    'delete_email': 'Unknown',
    'delete_password': 'Unknown',
    'update_allergen_email': 'Unknown',
    'update_allergen_password': 'Unknown',
    'update_allergen': 'Unknown'
}

// function updateRestaurantCount(num_restaurants) {
//     // takes in the number of restaurants in the table
//     document.getElementById("restaurant_count").innerText = num_restaurants + " Restaurants Nearby"; 

// }
// Function to collect the initial form data and output table
function collectFormData() {
    var name = document.getElementById("name").value;
    var foodType = document.getElementById("foodType").value;
    var allergens = [];
    var allergenCheckboxes = document.getElementsByName("allergen");
    for (var i = 0; i < allergenCheckboxes.length; i++) {
        if (allergenCheckboxes[i].checked) {
            allergens.push(allergenCheckboxes[i].value);
        }
    }
    // Process or display the collected data as needed
    console.log("Name: " + name);
    console.log("Food Type: " + foodType);
    console.log("Allergens: " + allergens.join(", "));
    form_info = {
        'name': name,
        'food_type': foodType,
        'allergens': allergens
    };
    
    requestData(form_info, user_info, user_data, 'form');
}
function collectLoginAccountData() {
    var email = document.getElementById("login_email").value;
    var password = document.getElementById("login_password").value;
    
    user_info = {
        'name': 'Unknown', 
        'email': email,
        'password': password, 
        'allergens': 'Unknown'
    }
    requestData(form_info, user_info, user_data,'login');
}
function collectCreateAccountData() {
    var name = document.getElementById("create_name").value;
    var email = document.getElementById("create_email").value;
    var password = document.getElementById("create_password").value;
    var allergens = document.getElementById("create_allergens").value;
    
    console.log("Name: " + name);
    console.log("email:", email);
    console.log("Password: " + password);
    console.log("Allergens: " + allergens);
    user_info = {
        'name': name, 
        'email': email,
        'password': password, 
        'allergens': allergens
    }
    requestData(form_info, user_info, user_data, 'register');
}
// Update User Food Type
function userFoodTypeData() {
    var food_type = document.getElementById("user_food_type").value;
    user_data['user_food_type'] = food_type;
    user_data['user_data_type'] = 'update_user_table';
    requestData(form_info, user_info, user_data, 'update_user_table');
}

// Set Rating in SQL statement
function userRateRestaurant() {
    var store_restaurant = document.getElementById("restaurant_select").value;
    var store_rating = document.getElementById("rating_select").value;
    var store_email = document.getElementById("rating_email").value;
    user_data['user_data_type'] = 'store_rating';
    user_data['store_restaurant'] = store_restaurant;
    user_data['store_rating'] = store_rating;
    user_data['rating_email'] = store_email;
    console.log(store_restaurant, store_rating, );
    requestData(form_info, user_info, user_data, 'store_rating');
}
function deleteAccount() {
    var email = document.getElementById("delete_email").value;
    var password = document.getElementById("delete_password").value;
    user_data['delete_email'] = email;
    user_data['delete_password'] = password;
    user_data['user_data_type'] = 'delete_user';
    console.log(email, password);
    requestData(form_info, user_info, user_data, 'delete_user');
}
function updateAllergen() {
    var update_allergen_email = document.getElementById("update_allergen_email").value;
    var update_allergen_password = document.getElementById("update_allergen_password").value;
    var update_allergen = document.getElementById("update_allergen").value;
    user_data['update_allergen_email'] = update_allergen_email;
    user_data['update_allergen_password'] = update_allergen_password;
    user_data['update_allergen'] = update_allergen;
    user_data['user_data_type'] = 'update_allergen';
    requestData(form_info, user_info, user_data, 'update_allergen');
}

// Attach event listener to the Submit button
document.getElementById("form-submit").addEventListener("click", collectFormData);
document.getElementById("login-submit").addEventListener("click", collectLoginAccountData);
document.getElementById("create-submit").addEventListener("click", collectCreateAccountData);

// User Dashboard event listeners
document.getElementById("user_table-submit").addEventListener("click", userFoodTypeData);
document.getElementById("user_rate-submit").addEventListener("click", userRateRestaurant);
document.getElementById("user_delete-submit").addEventListener("click", deleteAccount);
document.getElementById("user_allergen-submit").addEventListener("click", updateAllergen);


function requestData(form_info=form_info, user_info=user_info, user_data=user_data, request_type=null) {
    // Make an AJAX request to the Flask server
    // AJAX call to Flask server
    $.ajax({
        type: 'POST',
        url: '/process-request',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            request_type: request_type,
            form_name: form_info.name,
            form_food_type: form_info.food_type,
            form_allergens: form_info.allergens,
            user_name: user_info.name,
            user_email: user_info.email,
            user_password: user_info.password,
            user_allergens: user_info.allergens,
            user_data_type: user_data.user_data_type,
            restaurant_count: user_data.restaurant_count,
            user_food_type: user_data.user_food_type,
            rating_email: user_data.rating_email,
            store_restaurant: user_data.store_restaurant,
            store_rating: user_data.store_rating,
            delete_email: user_data.delete_email,
            delete_password: user_data.delete_password,
            update_allergen_email: user_data.update_allergen_email,
            update_allergen_password: user_data.update_allergen_password,
            update_allergen: user_data.update_allergen
        }),
        success: handleResponse,
        error: handleError
    });
}
function handleResponse(response){
    // Handle the response from the server
    if (response.request_type == 'table') { 
        console.log(response.table);
        generateTable(response.table, response.request_type)
    }
    else if (response.request_type == 'register' || response.request_type == 'login') {
        console.log(response.user_info);
        user_info = response.user_info 
        if (user_info.success) {
            console.log('Credentials are valid or have been created');
            console.log('Table Value: ',response.table);
            generateUserPage(response.table, response.request_type, response.user_data.restaurant_count)
        }
        else {
            console.log('Did not successfully login')
        }
    }
    else if (response.request_type == 'update_user_table') {
        console.log(response.user_data.table)
        generateTable(response.user_data.table, response.request_type)
    } else if ((response.request_type == 'store_rating') || (response.request_type == 'update_allergen') || (response.request_type == 'delete_user')) {
        displaySuccessMessage(response.user_data.success);
        console.log(response.user_data.success);
    }
     else {
        console.error('Invalid response:', response);
    }
}
function handleError(error){
        console.error(error);
}
// Generate Table 
function generateTable(data, request_type) {
    // update this table
    console.log('Table is about to be generated', data)
    if (request_type == 'table') {
        var table_name = 'myTable';
    } else {
        var table_name = 'userTable';
    }
    let tableBody = document.getElementById(table_name);

    table_string = ''
    if (tableBody == null) {
        return_data = true
    }else{
        return_data = false
    }
    for (var i = 0; i < data.length; i++) {
        var rating = 'None';
        if ((data.length > 5 )){
            rating = data[i][5]
        }
        var row = `<tr>
                    <td>${data[i][0]}</td>
                    <td>${data[i][1]}</td>
                    <td>${data[i][2]}</td>
                    <td>${data[i][3]}</td>
                    <td>${data[i][4]}</td>
                    <td>${rating}</td>
                </tr>`;
        console.log('Row: ', row)
        table_string += row
        if (!return_data){ // page hasnt loaded yet
            document.getElementById(table_name).innerHTML += row;
        }
    }
    if (return_data){
        return table_string
    }
   
}
function generateUserPage(data, request_type, num_restaurants){
    // Provide the URL of the new page you want to open
    tableData = generateTable(data, request_type);

    // Convert data to JSON and encodeURIComponent to ensure it's properly formatted for the URL
    var requestDataString = `?num_restaurants=${num_restaurants}&data=${encodeURIComponent(JSON.stringify(tableData))}`;

    var newPageUrl = 'http://127.0.0.1:5000/user.html';

    // Open the new page in a new tab or window after it has been updated with userdata
    window.open(newPageUrl + requestDataString, '_blank');
    user_data['user_data_type'] = 'restaurant_count';
    requestData(form_info, user_info, user_data, 'restaurant_count');
}

function displaySuccessMessage(successMessage) {
    // Alert that the SQL function was successful
    alert(successMessage);
  }