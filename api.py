from flask import Flask, jsonify, render_template
import pandas as pd
from collections import defaultdict

app = Flask(_name_)

# Cargar el dataset del Titanic
df = pd.read_csv(r'C:\Users\Acer\Desktop\MiProyectoTitanic\Backend\tested.csv')

@app.route('/chart')
def chart():
    return render_template('front.html')

@app.route('/')
def home():
    return "Bienvenido a la API del Titanic!"

@app.route('/survivors')
def survivors():
    survivors_data = df[df['Survived'] == 1]
    return jsonify(survivors_data.to_dict(orient='records'))

@app.route('/survival-stats')
def survival_stats():
    survival_counts = df['Survived'].value_counts().to_dict()
    data = {
        'Survived': survival_counts.get(1, 0),
        'Did not survive': survival_counts.get(0, 0)
    }
    return jsonify(data)

@app.route('/non-survivors')
def non_survivors():
    non_survivors_data = df[df['Survived'] == 0]
    return jsonify(non_survivors_data.to_dict(orient='records'))

@app.route('/embark-stats')
def embark_stats():
    embark_survived = df.groupby('Embarked')['Survived'].sum().to_dict()
    embark_not_survived = df.groupby('Embarked')['Survived'].apply(lambda x: (x==0).sum()).to_dict()
    data = {
        'embark_survived': embark_survived,
        'embark_not_survived': embark_not_survived
    }
    return jsonify(data)

@app.route('/age-distribution')
def age_distribution():
    # Define los rangos de edades y las etiquetas correspondientes
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, float('inf')]
    labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']

    # Utiliza pd.cut para segmentar las edades en los rangos definidos
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Agrupa por 'AgeGroup' y 'Survived' y cuenta las entradas
    age_dist = df.groupby(['AgeGroup', 'Survived']).size().unstack(fill_value=0)
    
    # Añade el conteo de nulos si es necesario
    null_survived = int(df[df['Age'].isnull() & (df['Survived'] == 1)].shape[0])
    null_not_survived = int(df[df['Age'].isnull() & (df['Survived'] == 0)].shape[0])
    if null_survived or null_not_survived:
        age_dist.loc['Nulos', 1] = null_survived
        age_dist.loc['Nulos', 0] = null_not_survived

    # Prepara los datos para el gráfico
    age_labels = list(age_dist.index)
    survivors = age_dist[1].tolist()
    non_survivors = age_dist[0].tolist()

    return jsonify({
        'age_labels': age_labels,
        'survivors': survivors,
        'non_survivors': non_survivors
    })

@app.route('/fare-stats')
def fare_stats():
    # Aquí se deben crear rangos para los precios de los tickets y calcular los sobrevivientes y no sobrevivientes
    fare_ranges = [0, 25, 50, 100, 200, 300, 400, 500, 600, 'Nulos']
    fare_distribution = {
        str(fare_range): {
            'survivors': 0,
            'non_survivors': 0
        } for fare_range in fare_ranges
    }

    for _, row in df.iterrows():
        fare = row['Fare']
        survived = row['Survived']
        if pd.isna(fare):
            label = 'Nulos'
        else:
            label = str(max([f for f in fare_ranges if f != 'Nulos' and f <= fare], default=0))
        if survived:
            fare_distribution[label]['survivors'] += 1
        else:
            fare_distribution[label]['non_survivors'] += 1
    
    # Prepara los datos para enviar al frontend
    data = {
        'fare_labels': [str(f) for f in fare_ranges],
        'fare_survived': [fare_distribution[str(f)]['survivors'] for f in fare_ranges],
        'fare_not_survived': [fare_distribution[str(f)]['non_survivors'] for f in fare_ranges]
    }
    return jsonify(data)

if _name_ == '_main_':
    app.run(debug=True)
