from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None

    if request.method == 'POST':
        try:
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            activity = request.form['activity']

            if height > 250 or weight > 400:
                results = {
                    'advice': "Your input values are beyond standard health limits. Please consult a doctor for professional guidance.",
                    'suggestion': None
                }
                return render_template('index.html', results=results)

            # Calculate Ideal Weight (Broca’s Index)
            ideal_weight = round((height - 100) - (height - 100) * 0.1, 1)

            # BMI
            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 1)

            # BMI Category
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_status = "Normal"
            elif 25 <= bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            # Protein Requirement (based on actual/ideal weight)
            if bmi >= 25:
                base_weight = ideal_weight  # use ideal weight if overweight
            else:
                base_weight = weight  # use actual weight if underweight/normal

            activity_factors = {
                'sedentary': 0.8,
                'light': 1.0,
                'moderate': 1.3,
                'active': 1.6,
                'athlete': 1.8
            }

            factor = activity_factors.get(activity, 1.0)
            protein = round(base_weight * factor, 1)

            # Other vitamins/minerals (basic adult RDA)
            b12 = 2.4
            vitd = 600
            vite = 15
            iron = 8 if gender_assumed_male() else 18
            zinc = 11
            calcium = 1000

            # Advice
            advice = None
            suggestion = None

            if bmi < 18.5 or bmi > 30:
                advice = "⚠️ Your BMI indicates a health risk. Please consult a healthcare professional."

            if activity in ['sedentary', 'light']:
                suggestion = "💡 Consider at least 30 minutes of moderate physical activity daily and balanced meals."

            results = {
                'ideal_weight': ideal_weight,
                'bmi': bmi,
                'bmi_status': bmi_status,
                'protein': protein,
                'b12': b12,
                'vitd': vitd,
                'vite': vite,
                'iron': iron,
                'zinc': zinc,
                'calcium': calcium,
                'advice': advice,
                'suggestion': suggestion
            }

        except ValueError:
            results = {
                'advice': "Invalid input. Please enter numerical values only.",
                'suggestion': None
            }

    return render_template('index.html', results=results)

# Optional logic — assumes male for iron requirement (can be expanded later)
def gender_assumed_male():
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
