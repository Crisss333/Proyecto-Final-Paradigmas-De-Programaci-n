from flask import Flask, jsonify, render_template
import pandas as pd

class TitanicDataHandler:
    def _init_(self, file_path):
        self.df = pd.read_csv(file_path)

    def get_survivors(self):
        return self.df[self.df['Survived'] == 1].to_dict(orient='records')

    def get_survival_stats(self):
        survival_counts = self.df['Survived'].value_counts().to_dict()
        return {'Survived': survival_counts.get(1, 0), 'Did not survive': survival_counts.get(0, 0)}

    def get_non_survivors(self):
        return self.df[self.df['Survived'] == 0].to_dict(orient='records')

    def get_embark_stats(self):
        embark_survived = self.df.groupby('Embarked')['Survived'].sum().to_dict()
        embark_not_survived = self.df.groupby('Embarked')['Survived'].apply(lambda x: (x==0).sum()).to_dict()
        return {'embark_survived': embark_survived, 'embark_not_survived': embark_not_survived}

    def get_age_distribution(self):
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, float('inf')]
        labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
        self.df['AgeGroup'] = pd.cut(self.df['Age'], bins=bins, labels=labels, right=False)
        age_dist = self.df.groupby(['AgeGroup', 'Survived']).size().unstack(fill_value=0)

        age_labels = list(age_dist.index)
        survivors = age_dist[1].tolist()
        non_survivors = age_dist[0].tolist()

        return {
            'age_labels': age_labels,
            'survivors': survivors,
            'non_survivors': non_survivors
        }

    def get_fare_stats(self):
        fare_ranges = [0, 25, 50, 100, 200, 300, 400, 500, 600, float('inf')]
        labels = ['0-24', '25-49', '50-99', '100-199', '200-299', '300-399', '400-499', '500-599', '600+']
        self.df['FareGroup'] = pd.cut(self.df['Fare'], bins=fare_ranges, labels=labels, right=False, include_lowest=True)
        fare_dist = self.df.groupby(['FareGroup', 'Survived']).size().unstack(fill_value=0)

        fare_labels = list(fare_dist.index)
        fare_survived = fare_dist[1].tolist()
        fare_not_survived = fare_dist[0].tolist()

        return {
        'fare_labels': fare_labels,
        'fare_survived': fare_survived,
        'fare_not_survived': fare_not_survived
    }

app = Flask(_name_)
data_handler = TitanicDataHandler(r'C:\Users\Acer\Desktop\MiProyectoTitanic\Backend\tested.csv')  # Reemplaza con la ruta correcta de tu archivo CSV

# Rutas para el API
@app.route('/')
def home():
    return "Bienvenido a la API del Titanic!"

@app.route('/chart')
def chart():
    return render_template('front.html')  # Asegúrate de que tu archivo HTML se llame 'index.html' y esté en la carpeta 'templates'

@app.route('/survivors')
def survivors():
    return jsonify(data_handler.get_survivors())

@app.route('/survival-stats')
def survival_stats():
    return jsonify(data_handler.get_survival_stats())

@app.route('/non-survivors')
def non_survivors():
    return jsonify(data_handler.get_non_survivors())

@app.route('/embark-stats')
def embark_stats():
    return jsonify(data_handler.get_embark_stats())

@app.route('/age-distribution')
def age_distribution():
    return jsonify(data_handler.get_age_distribution())

@app.route('/fare-stats')
def fare_stats():
    return jsonify(data_handler.get_fare_stats())

if _name_ == '_main_':
    app.run(debug=True)
