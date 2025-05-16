from flask import Flask, render_template, request, redirect, session, flash
from db_config import get_db_connection
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Set and ensure upload folder exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)





# Admin Orders Route new for orders page
@app.route('/admin/orders')
def admin_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch orders data
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    # Calculate total revenue
    total_revenue = sum(order['total_amount'] for order in orders)

    # Count order statuses
    completed_orders = sum(1 for order in orders if order['status'] == 'Delivered')
    pending_orders = sum(1 for order in orders if order['status'] == 'Pending')

    conn.close()

    return render_template('admin/orders.html', orders=orders, total_revenue=total_revenue,
                           completed_orders=completed_orders, pending_orders=pending_orders,
                           sort_by=request.args.get('sort', ''),
                           sort_reverse='desc' if request.args.get('order') == 'asc' else 'asc')

# v2 with searching



# admin routes all its working
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            session['admin'] = True
            return redirect('/admin/dashboard')
        flash("Invalid admin credentials")
    return render_template('admin/login.html')

# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if not session.get('admin'):
#         return redirect('/admin')
#     con = get_db_connection()
#     cur = con.cursor()
#     cur.execute("SELECT COUNT(*) FROM items")
#     total_items = cur.fetchone()[0]
#     cur.execute("SELECT * FROM items")
#     items = cur.fetchall()
#     con.close()
#     return render_template('admin/dashboard.html', total_items=total_items, items=items)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    con = get_db_connection()
    cur = con.cursor()

    # Total items on menu
    cur.execute("SELECT COUNT(*) FROM items")
    total_items = cur.fetchone()[0]

    # Total orders
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    # Total revenue from order_items table
    cur.execute("SELECT SUM(oi.quantity * i.price) FROM order_items oi JOIN items i ON oi.item_id = i.id")
    total_revenue = cur.fetchone()[0]
    if total_revenue is None:
        total_revenue = 0.0

    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Menu items
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()

    con.close()

    return render_template(
        'admin/dashboard.html',
        total_items=total_items,
        total_orders=total_orders,
        total_users=total_users,
        total_revenue=total_revenue,
        items=items
    )



@app.route('/admin/add_item', methods=['POST'])
def add_item():
    if not session.get('admin'):
        return redirect('/admin')
    
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    image_file = request.files['image']
    image_name = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    image_file.save(image_path)

    con = get_db_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO items (name, price, description, image) VALUES (%s, %s, %s, %s)",
                (name, price, description, image_name))
    con.commit()
    con.close()
    flash("Item added.")
    return redirect('/admin/dashboard')




@app.route('/admin/delete_item/<int:item_id>')
def delete_item(item_id):
    if not session.get('admin'):
        return redirect('/admin')
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
    con.commit()
    con.close()
    flash("Item deleted.")
    return redirect('/admin/dashboard')

@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if not session.get('admin'):
        return redirect('/admin')
    
    con = get_db_connection()
    cur = con.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files.get('image')

        if image_file and image_file.filename != "":
            image_name = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
            image_file.save(image_path)
            cur.execute("UPDATE items SET name=%s, price=%s, description=%s, image=%s WHERE id=%s",
                        (name, price, description, image_name, item_id))
        else:
            cur.execute("UPDATE items SET name=%s, price=%s, description=%s WHERE id=%s",
                        (name, price, description, item_id))
        con.commit()
        con.close()
        flash("Item updated.")
        return redirect('/admin/dashboard')

    cur.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cur.fetchone()
    con.close()
    return render_template('admin/edit_item.html', item=item)



# deepseak foe user
@app.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect('/admin')
    
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'id')  # Default sort by ID
    order = request.args.get('order', 'desc')  # Default order descending
    
    valid_sort_columns = ['id', 'name', 'email']
    if sort_by not in valid_sort_columns:
        sort_by = 'id'
    
    valid_orders = ['asc', 'desc']
    if order not in valid_orders:
        order = 'desc'
    
    con = get_db_connection()
    cur = con.cursor()
    
    # Base query
    query = "SELECT id, name, email FROM users"
    params = []
    
    # Add search filter if provided
    if search_query:
        query += " WHERE name LIKE %s OR email LIKE %s"
        params.extend([f'%{search_query}%', f'%{search_query}%'])
    
    # Add sorting
    query += f" ORDER BY {sort_by} {order}"
    
    cur.execute(query, params if params else None)
    users = cur.fetchall()
    con.close()
    
    return render_template('admin/users.html', 
                         users=users,
                         search_query=search_query,
                         sort_by=sort_by,
                         order=order)

@app.route('/admin/add_user', methods=['POST'])
def admin_add_user():
    if not session.get('admin'):
        return redirect('/admin')
    
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Email format validation
    if not re.match(r'^[\w\.-]+@gmail\.com$', email):
        flash("Please enter a valid Gmail address (must end with @gmail.com).", "error")
        return redirect('/admin/users')

    con = get_db_connection()
    cur = con.cursor()

    # Check if email exists
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        flash("This email is already registered.", "error")
        con.close()
        return redirect('/admin/users')

    # Insert new user
    hashed_password = generate_password_hash(password)
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
               (name, email, hashed_password))
    con.commit()
    con.close()
    
    flash("User added successfully", "success")
    return redirect('/admin/users')

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('admin'):
        return redirect('/admin')
    
    con = get_db_connection()
    cur = con.cursor()
    
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        con.commit()
        flash("User deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "error")
    finally:
        con.close()
    
    return redirect('/admin/users')

@app.route('/admin/add_item', methods=['GET'])
def add_item_form():
    if not session.get('admin'):
        return redirect('/admin')
    return render_template('admin/add_item.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin')



# user side codes
@app.route('/')
def landing():
    if 'user' not in session:
        return redirect('/login')
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    con.close()
    return render_template('landing.html', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # ✅ Validate Gmail format
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            flash("Please enter a valid Gmail address (must end with @gmail.com).")
            return redirect('/login')

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        con.close()

        if user:
            stored_hashed_password = user[3]  # Assuming columns: id=0, name=1, email=2, password=3
            if check_password_hash(stored_hashed_password, password):
                session['user'] = user[0]  # Save user ID in session
                return redirect('/')
            else:
                flash("Incorrect password.")
        else:
            flash("No account found with this email.")

        return redirect('/login')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # ✅ Backend Email Format Check
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            flash("Please enter a valid Gmail address (must end with @gmail.com).")
            return redirect('/register')

        con = get_db_connection()
        cur = con.cursor()

        # ✅ Check if Email Already Exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("This email is already registered. Please login.")
            con.close()
            return redirect('/register')

        # ✅ Insert New User
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        con.commit()
        con.close()
        flash("Registration successful. Please login.")
        return redirect('/login')

    return render_template('register.html')



# menu
@app.route('/menu')
def menu():
    # Check if user is logged in
    if 'user' not in session:
        return redirect('/login')
    
    # Get database connection
    con = get_db_connection()
    cur = con.cursor()
    
    # Explicitly select fields: id, name, price, image, description
    cur.execute("SELECT id, name, price, image, description FROM items")
    items = cur.fetchall()
    con.close()
    
    # Render menu template
    return render_template('menu.html', items=items)



    
# add to cart
@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'user' not in session:
        return redirect('/login')
    
    user_id = session['user']
    quantity = int(request.form.get('quantity', 1))  # default 1 if input missing

    con = get_db_connection()
    cur = con.cursor()

    # Check if the item already exists in the cart
    cur.execute("SELECT quantity FROM cart WHERE user_id = %s AND item_id = %s", (user_id, item_id))
    existing = cur.fetchone()

    if existing:
        # Update quantity
        new_quantity = existing[0] + quantity
        cur.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND item_id = %s", (new_quantity, user_id, item_id))
    else:
        # Insert new row
        cur.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (%s, %s, %s)", (user_id, item_id, quantity))

    con.commit()
    con.close()
    flash("Item added to cart.")
    return redirect('/menu')



# cart
@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']  # or 'user_id' if you're using that

    con = get_db_connection()
    cur = con.cursor()

    # ✅ Use %s for MySQL placeholder
    cur.execute('''
        SELECT items.id, items.name, items.price, items.image, cart.quantity
        FROM cart
        JOIN items ON cart.item_id = items.id
        WHERE cart.user_id = %s
    ''', (user_id,))
    
    cart_items = cur.fetchall()
    con.close()

    # ✅ Calculate total
    total = sum(item[2] * item[4] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total)

# Remove one item from cart
@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']
    con = get_db_connection()
    cur = con.cursor()

    # Remove only one row that matches item and user
    cur.execute("DELETE FROM cart WHERE user_id = %s AND item_id = %s LIMIT 1", (user_id, item_id))
    con.commit()
    con.close()
    return redirect('/cart')

# Clear entire cart
@app.route('/clear_cart')
def clear_cart():
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    con.commit()
    con.close()
    return redirect('/cart')


# Add these routes to your app.py file

# Checkout page
@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']

    con = get_db_connection()
    cur = con.cursor()

    # Get cart items
    cur.execute('''
        SELECT items.id, items.name, items.price, items.image, cart.quantity
        FROM cart
        JOIN items ON cart.item_id = items.id
        WHERE cart.user_id = %s
    ''', (user_id,))
    
    cart_items = cur.fetchall()
    con.close()

    # Calculate totals
    total = sum(item[2] * item[4] for item in cart_items)
    taxes = round(total * 0.05)
    delivery_fee = 40
    grand_total = total + taxes + delivery_fee

    return render_template('checkout.html', 
                          cart_items=cart_items, 
                          total=total,
                          taxes=taxes,
                          delivery_fee=delivery_fee,
                          grand_total=grand_total)

# Process order
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']
    
    # Get form data
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    pincode = request.form.get('pincode')
    delivery_instructions = request.form.get('delivery_instructions')
    payment_method = request.form.get('payment_method')
    
    # Connect to database
    con = get_db_connection()
    cur = con.cursor()
    
    try:
        # Get cart items
        cur.execute('''
            SELECT items.id, items.price, cart.quantity
            FROM cart
            JOIN items ON cart.item_id = items.id
            WHERE cart.user_id = %s
        ''', (user_id,))
        
        cart_items = cur.fetchall()
        
        if not cart_items:
            return redirect('/cart')
        
        # Calculate totals
        subtotal = sum(item[1] * item[2] for item in cart_items)
        taxes = round(subtotal * 0.05)
        delivery_fee = 40
        total_amount = subtotal + taxes + delivery_fee
        
        # Create order in orders table
        cur.execute("""
            INSERT INTO orders (user_id, name, phone, email, address, city, state, pincode, 
                              delivery_instructions, payment_method, subtotal, 
                              taxes, delivery_fee, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, phone, email, address, city, state, pincode, 
              delivery_instructions, payment_method, subtotal, taxes, delivery_fee, total_amount))
        
        # Get the order id
        order_id = cur.lastrowid
        
        # Create order_items table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                item_id INT NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)
        
        # Add order items
        for item in cart_items:
            item_id = item[0]
            price = item[1]
            quantity = item[2]
            
            cur.execute("""
                INSERT INTO order_items (order_id, item_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item_id, quantity, price))
        
        # Clear the cart
        cur.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        # Commit the changes
        con.commit()
        
        # Log successful order creation
        print(f"Order successfully created with ID: {order_id}")
        
        # Direct redirect to order success page to guarantee a response
        return render_template('order_success.html', order_id=order_id)
    
    except Exception as e:
        # Roll back in case of error
        con.rollback()
        print(f"Error placing order: {e}")
        # Return error message to help debugging
        return f"Error placing order: {e}"
    
    finally:
        con.close()

@app.route('/orders')
def orders():
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']
    
    # Connect to database
    con = get_db_connection()
    cur = con.cursor()
    
    # Fetch all orders for the current user
    cur.execute("""
        SELECT id, order_date, status, total_amount 
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
    """, (user_id,))
    
    orders = cur.fetchall()
    con.close()
    
    return render_template('orders.html', orders=orders)



# Order confirmation page
@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']
    
    # Connect to database
    con = get_db_connection()
    cur = con.cursor()
    
    # Fetch order details
    cur.execute("""
        SELECT id, name, phone, email, address, city, state, pincode, 
               payment_method, order_date, status, subtotal, taxes, 
               delivery_fee, total_amount
        FROM orders
        WHERE id = %s
    """, (order_id,))
    
    order = cur.fetchone()
    
    if not order:
        con.close()
        return redirect('/')
    
    # Fetch order items
    cur.execute("""
        SELECT i.name, oi.quantity, oi.price
        FROM order_items oi
        JOIN items i ON oi.item_id = i.id
        WHERE oi.order_id = %s
    """, (order_id,))
    
    order_items = cur.fetchall()
    con.close()
    
    return render_template('order_confirmation.html', 
                           order=order, 
                           order_items=order_items)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



if __name__ == "__main__":
    app.run(debug=True)
