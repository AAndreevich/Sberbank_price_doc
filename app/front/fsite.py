"https://www.youtube.com/playlist?list=PLA0M1Bcd0w8yrxtwgqBvT6OM4HkOU3xYn"
import os
import pandas as pd
import numpy as np
import dill
import shutil
from sklearn.metrics import mean_squared_error as mse, r2_score as r2
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, request, flash, send_file
from fileinput import filename

app = Flask(__name__)


def Mkdir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)


def load_model_dill(path):
    with open(path, "rb") as mod1:
        model_name = dill.load(mod1)
    return model_name


app.config["SECRET_KEY"] = "g;lsdjfgljhsdfgjhdaskjglkbngl"
menu = [{"name": "Главная", "url": "main_flask"},
        {"name": "Single", "url": "single"},
        {"name": "Multiple", "url": "multiple"}]

feature_list = [{'name': 'full_sq'}, {'name': 'num_room'}, {'name': 'life_sq'}, {'name': 'kitch_sq'},
                {'name': 'sub_area_num'}, {'name': 'ecology'}, {'name': 'big_road1_km'},
                {'name': 'church_synagogue_km'}, {'name': 'oil_chemistry_km'},
                {'name': 'public_transport_station_min_walk'}, {'name': 'public_transport_station_km'},
                {'name': 'railroad_station_avto_km'}, {'name': 'product_type'}, {'name': 'railroad_station_walk_km'},
                {'name': 'railroad_station_walk_min'}, {'name': 'kindergarten_km'},
                {'name': 'railroad_station_avto_min'}, {'name': 'preschool_km'}, {'name': 'school_km'},
                {'name': 'additional_education_km'}, {'name': 'hospice_morgue_km'}, {'name': 'ice_rink_km'},
                {'name': 'bus_terminal_avto_km'}, {'name': 'big_road2_km'}, {'name': 'power_transmission_line_km'},
                {'name': 'ts_km'}, {'name': 'public_healthcare_km'}, {'name': 'market_shop_km'}, {'name': 'mosque_km'},
                {'name': 'shopping_centers_km'}, {'name': 'metro_km_avto'}, {'name': 'metro_km_walk'},
                {'name': 'metro_min_walk'}, {'name': 'park_km'}, {'name': 'fitness_km'}, {'name': 'big_church_km'},
                {'name': 'metro_min_avto'}, {'name': 'radiation_km'}, {'name': 'museum_km'}, {'name': 'euro_type'},
                {'name': 'exhibition_km'}, {'name': 'workplaces_km'}, {'name': 'thermal_power_plant_km'},
                {'name': 'swim_pool_km'}, {'name': 'catering_km'}, {'name': 'theater_km'}, {'name': 'university_km'},
                {'name': 'detention_facility_km'}, {'name': 'office_km'}, {'name': 'basketball_km'},
                {'name': 'stadium_km'}, {'name': 'nuclear_reactor_km'}, {'name': 'ttk_km'}, {'name': 'bulvar_ring_km'},
                {'name': 'kremlin_km'}, {'name': 'zd_vokzaly_avto_km'}, {'name': 'sadovoe_km'}]


@app.route("/main_flask")
@app.route("/")
def main_flask():
    print(url_for("main_flask"))
    return render_template("index.html", title="Info", menu=menu)


@app.route("/single", methods=["POST", "GET"])
def single():
    if request.method == 'POST':
        print(request.form)
        X = []
        columns = []
        for names in request.form:
            X.append(float(request.form[names]))
            columns.append(names)

        X = np.asarray(X)
        X = np.resize(X, (len(X), len(X)))
        df = pd.DataFrame(X, columns=columns)
        path_to_work_dir = "../"
        model_gbr_load = load_model_dill(path_to_work_dir + "models/" + "GBR_model.dill")
        y_test_preds = model_gbr_load.predict(df)
        flash(f"Calculations finished {round(y_test_preds[0], 1)}", category="success")

    print(url_for("single"))
    return render_template("single.html", title="Predict", menu=menu, feature_list=feature_list)


@app.route("/multiple", methods=["POST", "GET"])
def multiple():
    if request.method == "POST":
        file = request.files['file']
        if ".csv" not in file.filename:
            flash("You should choice files", category="error")
        else:
            count = len(os.listdir("./cash/"))
            file.save("./cash/" + f"{str(count + 1)}_" + file.filename)
            flash("File is saving", category="success")

    print(url_for("multiple"))
    return render_template("multiple.html", title="Predict", menu=menu)


@app.route("/success", methods=["POST", "GET"])
def success():
    if request.method == 'POST':
        path_to_doir_with_x_test = "./cash/"
        if len(os.listdir(path_to_doir_with_x_test)) == 0:
            flash("File didn't download", category="error")
        else:
            file = os.listdir(path_to_doir_with_x_test)[-1]
            X_test = pd.read_csv(path_to_doir_with_x_test + file)
            path_to_work_dir = "../"
            model_gbr_load = load_model_dill(path_to_work_dir + "models/" + "GBR_model.dill")

            y_test_preds = model_gbr_load.predict(X_test)
            y = pd.DataFrame(y_test_preds, columns=["result"])
            round(y, 1).to_csv("./result/y.csv", index=None)
            flash("Calculations finished", category="success")
    return render_template("multiple.html", title="Predict", menu=menu)


@app.route('/download')
def download():
    path_to_doir_with_x_test = "./result/"
    if len(os.listdir(path_to_doir_with_x_test)) == 0:
        flash("File didn't download", category="error")
        return render_template("multiple.html", title="Predict", menu=menu)
    else:
        flash("File is saving", category="success")
        return send_file("./result/y.csv", as_attachment=True)


@app.route('/clear_cash')
def clear_cash():
    path_to_cash = "./cash/"
    path_to_result = "./result/"
    Mkdir(path_to_cash)
    Mkdir(path_to_result)
    flash("Cash cleaned", category="success")
    return render_template("multiple.html", title="Predict", menu=menu)


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', debug=True, port=port)