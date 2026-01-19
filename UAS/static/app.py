from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
import math

app = Flask(__name__)
app.secret_key = "secret123"

# CART COUNT GLOBAL
@app.context_processor
def inject_cart():
    cart = session.get("cart", {})
    return {
        "cart_count": len(cart)
    }

@app.before_request
def init_cart():
    if "cart" not in session:
        session["cart"] = {}

UPLOAD_FOLDER = "static/img/produk/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================
# DATABASE
# ======================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="harfandi123",
    database="uas_projek"
)
cursor = db.cursor(dictionary=True)

# ======================
# USER
# ======================
@app.route("/")
def index():
    keyword = request.args.get("q")
    pesan = None

    cursor.execute("SELECT * FROM kategori")
    kategori = cursor.fetchall()

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None  

    cursor.execute("""
        SELECT *
        FROM produk
        ORDER BY CAST(kode_barang AS UNSIGNED) DESC
        LIMIT 12
    """)
    produk_rekomendasi = cursor.fetchall()

    return render_template(
        "USER/index.html",
        kategori=kategori,
        produk_rekomendasi=produk_rekomendasi,
        pesan=pesan,
        keyword=keyword
    )

# PROFILE
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None 

    cursor.execute(
        "SELECT id, username, email FROM users WHERE id=%s",
        (session["user_id"],)
    )
    user = cursor.fetchone()

    return render_template(
        "USER/akun.html",
        user=user,
        pesan=pesan,
        keyword=keyword
    )

# ======================
# KATEGORI
# ======================
@app.route("/kategori/<int:kategori_id>")
def produk_per_kategori(kategori_id):
    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None

    cursor.execute("""
        SELECT 
            p.*,
            IFNULL(p.deskripsi,'') AS deskripsi,
            k.nama_kategori
        FROM produk p
        JOIN kategori k ON p.kategori_id = k.id
        WHERE p.kategori_id=%s
    """, (kategori_id,))
    products = cursor.fetchall()

    cursor.execute(
        "SELECT nama_kategori FROM kategori WHERE id=%s",
        (kategori_id,)
    )
    kategori = cursor.fetchone()

    return render_template(
        "USER/produk_kategori.html",
        products=products,
        kategori=kategori,
        pesan=pesan,
        keyword=keyword
    )

# ======================
# DETAIL PRODUK
# ======================
@app.route("/product/<kode>")
def product_detail(kode):
    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None

    cursor.execute("""
        SELECT *
        FROM produk
        WHERE kode_barang=%s
    """, (kode,))
    product = cursor.fetchone()

    if not product:
        return redirect("/")

    return render_template(
        "USER/product_detail.html",
        product=product,
        pesan=pesan,
        keyword=keyword
    )

@app.template_filter("rupiah")
def rupiah(value):
    return "{:,.0f}".format(value).replace(",", ".")


# ======================
# TAMBAH KE CART 
# ======================
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        return redirect("/login")

    kode = request.form["kode"]
    qty = int(request.form.get("qty", 1))  

    cursor.execute("""
        SELECT kode_barang, nama_barang, harga, gambar
        FROM produk
        WHERE kode_barang=%s
    """, (kode,))
    produk = cursor.fetchone()

    if not produk:
        return redirect("/")

    cart = session.get("cart", {})

    if kode in cart:
        cart[kode]["qty"] += qty
    else:
        cart[kode] = {
            "nama": produk["nama_barang"],
            "harga": int(produk["harga"]),
            "qty": qty,
            "gambar": produk["gambar"]
        }

    session["cart"] = cart
    session.modified = True

    return redirect("/")

# HALAMAN CART
@app.route("/cart")
def cart():
    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None  # 

    cart = session.get("cart", {})
    total = sum(int(i["harga"]) * int(i["qty"]) for i in cart.values())

    return render_template(
        "USER/cart.html",
        cart=cart,
        total=total,
        pesan=pesan,
        keyword=keyword
    )

# ======================
# CART UPDATE QTY 
# ======================
@app.route("/cart/update", methods=["POST"])
def cart_update():
    data = request.get_json(silent=True) or {}

    kode = data.get("kode")
    delta = int(data.get("delta", 0))

    cart = session.get("cart", {})

    if not kode or kode not in cart:
        return jsonify({"success": False})

    cart[kode]["qty"] += delta

    if cart[kode]["qty"] < 1:
        cart[kode]["qty"] = 1

    session["cart"] = cart
    session.modified = True

    return jsonify({
        "success": True,
        "qty": cart[kode]["qty"]
    })


# ======================
# CART DELETE ITEM
# ======================
@app.route("/cart/delete/<kode>", methods=["POST"])
def cart_delete(kode):
    cart = session.get("cart", {})

    if kode in cart:
        del cart[kode]
        session["cart"] = cart
        session.modified = True

    return jsonify({"success": True})

# ======================
# LOGIN / REGISTER 
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            error = "Username tidak ditemukan"
        elif user["email"] != email:
            error = "Email tidak sesuai"
        elif user["password"] != password:
            error = "Password salah"
        else:
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            return redirect("/")

    return render_template(
        "USER/login.html",
        error=error,
        pesan=pesan,
        keyword=keyword
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    keyword = request.args.get("q")
    pesan = None

    if keyword:
        cursor.execute("""
            SELECT kode_barang
            FROM produk
            WHERE nama_barang LIKE %s
            LIMIT 1
        """, (f"%{keyword}%",))
        hasil = cursor.fetchone()

        if hasil:
            return redirect(f"/product/{hasil['kode_barang']}")
        else:
            pesan = "Produk tidak ditemukan"
            keyword = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            error = "Username sudah digunakan"
        else:
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s,%s,%s)
            """, (username, email, password))
            db.commit()
            return redirect("/login")

    return render_template(
        "USER/register.html",
        error=error,
        pesan=pesan,
        keyword=keyword
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================
# ADMIN 
# ======================
@app.route("/admin")
def admin_pilih_kategori():
    cursor.execute("SELECT * FROM kategori")
    kategori = cursor.fetchall()
    return render_template("ADMIN/pilih_kategori.html", kategori=kategori)

@app.route("/admin/kategori/<int:kategori_id>")
def admin_produk_kategori(kategori_id):

    keyword = request.args.get("keyword", "")
    sort = request.args.get("sort", "")
    page = request.args.get("page", 1, type=int)

    limit = 10
    offset = (page - 1) * limit

    # AMBIL JUDUL KATEGORI
    cursor.execute(
        "SELECT nama_kategori FROM kategori WHERE id=%s",
        (kategori_id,)
    )
    kategori = cursor.fetchone()

    # =====================
    # BASE QUERY
    # =====================
    base_query = """
        FROM produk p
        JOIN kategori k ON p.kategori_id = k.id
        WHERE p.kategori_id=%s
    """
    params = [kategori_id]

    # =====================
    # SEARCH
    # =====================
    if keyword:
        base_query += " AND (p.nama_barang LIKE %s OR p.kode_barang LIKE %s)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    # =====================
    # SORTING HARGA
    # =====================
    order_by = "ORDER BY CAST(p.kode_barang AS UNSIGNED) ASC"

    if sort == "termurah":
        order_by = "ORDER BY p.harga ASC"
    elif sort == "termahal":
        order_by = "ORDER BY p.harga DESC"

    # =====================
    # HITUNG TOTAL DATA
    # =====================
    cursor.execute(f"SELECT COUNT(*) AS total {base_query}", params)
    total_data = cursor.fetchone()["total"]
    total_page = math.ceil(total_data / limit)

    # =====================
    # AMBIL DATA
    # =====================
    query = f"""
        SELECT p.*, k.nama_kategori
        {base_query}
        {order_by}
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, params + [limit, offset])
    data = cursor.fetchall()

    return render_template(
        "ADMIN/index.html",
        data=data,
        kategori_id=kategori_id,
        kategori_nama=kategori["nama_kategori"],
        page=page,
        total_page=total_page,
        keyword=keyword,
        sort=sort
    )

@app.route("/admin/add", methods=["GET","POST"])
def admin_add():
    kategori_id = request.args.get("kategori")

    if request.method == "POST":
        file = request.files["gambar"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        cursor.execute("""
            INSERT INTO produk
            (kode_barang, nama_barang, deskripsi, stok, harga, kategori_id, gambar)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["kode_barang"],
            request.form["nama_barang"],
            request.form["deskripsi"],
            request.form["stok"],
            request.form["harga"],
            request.form["kategori_id"],
            filename
        ))
        db.commit()
        return redirect(f"/admin/kategori/{kategori_id}")

    return render_template("ADMIN/add.html", kategori_id=kategori_id)

@app.route("/admin/edit/<kode>", methods=["GET","POST"])
def admin_edit(kode):
    kategori_id = request.args.get("kategori")

    cursor.execute("SELECT * FROM produk WHERE kode_barang=%s", (kode,))
    produk = cursor.fetchone()

    if request.method == "POST":
        file = request.files.get("gambar")
        nama_file = produk["gambar"]

        if file and file.filename:
            nama_file = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, nama_file))

        cursor.execute("""
            UPDATE produk SET
            nama_barang=%s,
            deskripsi=%s,
            stok=%s,
            harga=%s,
            gambar=%s
            WHERE kode_barang=%s
        """, (
            request.form["nama_barang"],
            request.form["deskripsi"],
            request.form["stok"],
            request.form["harga"],
            nama_file,
            kode
        ))
        db.commit()
        return redirect(f"/admin/kategori/{kategori_id}")

    return render_template("ADMIN/edit.html", produk=produk, kategori_id=kategori_id)

@app.route("/admin/delete/<kode>")
def admin_delete(kode):
    kategori_id = request.args.get("kategori")
    cursor.execute("DELETE FROM produk WHERE kode_barang=%s", (kode,))
    db.commit()
    return redirect(f"/admin/kategori/{kategori_id}")

if __name__ == "__main__":
    app.run(debug=True)
