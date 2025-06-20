from flask import Flask,render_template
import sqlite3

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

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
    return render_template("all_cameras.html",cameras = cameras)

@app.route("/camera/<int:cam_id>")
def cameras(cam_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT name, manufacturer, release_date, megapixel, ergonomics, cont_shoot, max_iso, min_iso, video_res, vid_frame_rate, flash, bit_depth, mount, sensor_size, slomo_vidres, slomo_vidfps, shots_per_bat, af_points, af_point_type, face_af, eye_af, ibis, price, overall_rating, amount_lens FROM cameras JOIN manufacturer_table ON cameras.manufacturer_id = manufacturer_table.manufacturer_id WHERE cam_id = ?', (cam_id,))
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


    
    }
    conn.close()
    return render_template("camera.html",camera = camera)





if __name__ == "__main__":
    app.run(debug=True)