from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
login_message = ""
admin_active = False
app.config["UPLOAD_FOLDER"] = "static/images"
camera_add = {"manufacturer_id": 0,
              "name": "",
              "release_date": "",
              "megapixel": 1,
              "ergonomics": "",
              "cont_shoot": 0,
              "max_iso": 0,
              "min_iso": 0,
              "video_res": "",
              "vid_frame_rate": 0,
              "flash": "",
              "bit_depth": 0,
              "mount": "",
              "sensor_size": "",
              "slomo_vidres": "",
              "solmo_vidfps": 0,
              "shots_per_bat": 0,
              "af_points": 0,
              "af_points_type": "",
              "face_af": "",
              "eye_af": "",
              "ibis": "",
              "price": 0,
              "overall_rating": "",
              "amount_lens": 0}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin")
def admin():
    with sqlite3.connect("database.db") as db:
        
        manufacturer_entries = db.cursor().execute("SELECT manufacturer_id, manufacturer "
                                                    "FROM manufacturer_table;")
    return render_template("admin.html",
                           admin_active=admin_active,
                           login_message=login_message,
                           manufacturers=manufacturer_entries)


@app.route("/admin/2", methods=["GET", "POST"])
def admin2():
    if admin_active:
        name = request.form.get("name")
        manufacturer = request.form.get("manufacturer")
        release_date = request.form.get("release_date")
        megapixels = request.form.get("megapixels")
        mount = request.form.get("mount")
        price = request.form.get("price")
        overall_rating = request.form.get("overall_rating")
        sensor_size = request.form.get("sensor_size")

        release_date = release_date[8:] + "/" + release_date[5:7] + "/" + release_date[:4]

        camera_add["name"] = name
        camera_add["manufacturer_id"] = manufacturer
        camera_add["release_date"] = release_date
        camera_add["megapixel"] = megapixels
        camera_add["mount"] = mount
        camera_add["price"] = price
        camera_add["overall_rating"] = overall_rating
        camera_add["sensor_size"] = sensor_size


        return render_template("admin2.html")
    else:
        return "You do not have permission to be on this page!"
    

@app.route("/admin/3", methods=["GET", "POST"])
def admin3():
    if admin_active:
        max_iso = request.form.get("max_iso")
        min_iso = request.form.get("min_iso")
        flash = request.form.get("flash")
        bit_depth = request.form.get("bit_depth")

        if flash:
            flash = "does"
        else:
            flash = "doesn't"
        
        camera_add["max_iso"] = max_iso
        camera_add["min_iso"] = min_iso
        camera_add["flash"] = flash
        camera_add["bit_depth"] = bit_depth

        return render_template("admin3.html")
    else:
        return "You do not have permission to be on this page!"


@app.route("/admin/addcamera", methods=["GET", "POST"])
def add_camera():
    if admin_active:
        camera_add["cont_shoot"] = request.form.get("cont_shoot")
        camera_add["video_res"] = request.form.get("video_res")
        camera_add["vid_frame_rate"] = request.form.get("vid_frame_rate")
        camera_add["slomo_vidres"] = request.form.get("slomo_vidres")
        camera_add["solmo_vidfps"] = request.form.get("slomo_vidfps")
        camera_add["shots_per_bat"] = request.form.get("shots_per_bat")
        camera_add["af_points"] = request.form.get("af_points")
        camera_add["af_points_type"] = request.form.get("af_point_type")
        face_af = request.form.get("face_af")
        eye_af = request.form.get("eye_af")
        ibis = request.form.get("ibis")
        camera_add["amount_lens"] = request.form.get("amount_lens")
        camera_add["ergonomics"] = request.form.get("ergonomics")
        if "image" not in request.files:
            pass
        
        image = request.files["image"]

        image_name = secure_filename(image.filename)

        if not (image and image_name and image.name):
            pass

        with sqlite3.connect('database.db') as db:
            camera_id = db.cursor().execute("SELECT cam_id FROM cameras;").fetchall()[-1][0] + 1
        
        os.mkdir(f"{app.config["UPLOAD_FOLDER"]}/{camera_id}")
        image.save(os.path.join(f"{app.config["UPLOAD_FOLDER"]}/{camera_id}/", image_name))

        if face_af:
            face_af = "does"
        else:
            face_af = "doesn't"
        
        if eye_af:
            eye_af = "does"
        else:
            eye_af = "doesn't"
        
        if ibis:
            ibis = "does"
        else:
            ibis = "doesn't"

        camera_add["face_af"] = face_af
        camera_add["eye_af"] = eye_af
        camera_add["ibis"] = ibis

        with sqlite3.connect("database.db") as db:
            db.cursor().execute('''
                                INSERT INTO cameras (manufacturer_id, name, release_date, megapixel, ergonomics, cont_shoot, max_iso, min_iso, video_res, 
                                vid_frame_rate, flash, bit_depth, mount, sensor_size, slomo_vidres, slomo_vidfps, shots_per_bat, af_points, af_point_type, 
                                face_af, eye_af, ibis, price, overall_rating, amount_lens, image)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                                (camera_add["manufacturer_id"], camera_add["name"], camera_add["release_date"], camera_add["megapixel"], camera_add["ergonomics"], camera_add["cont_shoot"], 
                                 camera_add["max_iso"], camera_add["min_iso"], camera_add["video_res"], camera_add["vid_frame_rate"], camera_add["flash"], camera_add["bit_depth"], camera_add["mount"], 
                                 camera_add["sensor_size"], camera_add["slomo_vidres"], camera_add["solmo_vidfps"], camera_add["shots_per_bat"], camera_add["af_points"], camera_add["af_points_type"],
                                 camera_add["face_af"], camera_add["eye_af"], camera_add["ibis"], camera_add["price"], camera_add["overall_rating"], camera_add["amount_lens"], image_name))
        return app.redirect("/all_cameras")

    else:
        return "You do not have permission to be on this page!"


@app.route("/registerlogin", methods=['GET', 'POST'])
def registerlogin():
    global login_message, admin_active
    success = False
    userid = 0
    username = request.form.get("username")
    password = request.form.get("password")
    with sqlite3.connect('database.db') as db:
        userdata = db.cursor().execute("SELECT id, username FROM admin_logins;")
        for user in userdata:
            if username == user[1]:
                success = True
                userid = user[0]
                break
        
        if success:
            if check_password_hash(db.cursor().execute("SELECT passwordhash FROM admin_logins WHERE id=?;", (userid,)).fetchall()[0][0], password):
                admin_active = True
            else:
                login_message = "Incorrect Password"
        else:
            login_message = "Incorrect Username"
    return app.redirect("admin")


@app.route("/logout")
def logout():
    global admin_active
    admin_active = False
    return app.redirect("admin")

@app.route("/comparison")
def comparison():
    return render_template("comparison.html")




@app.route("/all_cameras")
def camera():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT cam_id, name, manufacturer FROM cameras JOIN manufacturer_table ON cameras.manufacturer_id = manufacturer_table.manufacturer_id')
    cameras = cur.fetchall()
    conn.close()
    return render_template("all_cameras.html",cameras = cameras, admin=admin_active)

@app.route("/camera/<int:cam_id>")
def cameras(cam_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT name, manufacturer, release_date, megapixel, ergonomics, cont_shoot, max_iso, min_iso, video_res, vid_frame_rate, flash, bit_depth, mount, sensor_size, slomo_vidres, slomo_vidfps, shots_per_bat, af_points, af_point_type, face_af, eye_af, ibis, price, overall_rating, amount_lens, image FROM cameras JOIN manufacturer_table ON cameras.manufacturer_id = manufacturer_table.manufacturer_id WHERE cam_id = ?', (cam_id,))
    cameradata = cur.fetchall()[0]
    camera = {
            "name": cameradata[0],
            "manufacturer": cameradata[1],
            "release_date": cameradata[2],
            "megapixel": cameradata[3],
            "ergonomics": cameradata[4],
            "cont_shoot": cameradata[5],
            "max_iso": cameradata[6],
            "min_iso": cameradata[7],
            "video_res": cameradata[8],
            "vid_frame_rate": cameradata[9],
            "flash": cameradata[10],
            "bit_depth": cameradata[11],
            "mount": cameradata[12],
            "sensor_size": cameradata[13],
            "slomo_vidres": cameradata[14],
            "slomo_vidfps": cameradata[15],
            "shots_per_bat": cameradata[16],
            "af_points": cameradata[17],
            "af_point_type": cameradata[18],
            "face_af": cameradata[19],
            "eye_af": cameradata[20],
            "ibis": cameradata[21],
            "price": cameradata[22],
            "rating": cameradata[23],
            "lens_amount": cameradata[24],
            "image": cameradata[25],
            "cam_id": cam_id
    }
    conn.close()
    return render_template("camera.html", camera=camera, admin=admin_active)


@app.route("/delete/<int:id>")
def delete_camera(id):
    if admin_active:
        directory = f"{app.config["UPLOAD_FOLDER"]}/{id}"
        for file in os.listdir(directory):
            os.remove(f"{directory}/{file}")
        os.rmdir(directory)
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM cameras WHERE cam_id=?", (id,))
        return app.redirect("/all_cameras")
    else:
        return "You do not have permission to be on this page!"


if __name__ == "__main__":
    app.run(debug=True)