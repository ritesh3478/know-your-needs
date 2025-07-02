from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 1)
    return bmi

def calculate_ideal_weight(height_cm):
    return round(22 * ((height_cm / 100) ** 2), 1)

def get_bmi_status(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 24.9:
        return "normal"
    elif 25 <= bmi < 29.9:
        return "overweight"
    else:
        return "obese"

def protein_requirement(weight, activity):
    factor = {
        'sedentary': 0.8,
        'light': 1.0,
        'moderate': 1.3,
        'active': 1.6,
        'athlete': 1.8
    }.get(activity, 0.8)
    return round(weight * factor, 1)

def micronutrient_estimates(weight):
    return {
        'Vitamin B12 (mcg)': round(0.0015 * weight, 2),
        'Vitamin D (IU)': round(7.5 * weight),
        'Vitamin E (mg)': round(0.15 * weight, 2),
        'Iron (mg)': round(0.25 * weight, 2),
        'Zinc (mg)': round(0.2 * weight, 2),
        'Calcium (mg)': round(9.5 * weight)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            activity = request.form['activity']

            if height > 250 or weight > 400:
                result = (
                    f"<strong>⚠️ Height or weight entered is beyond the normal range.</strong><br>"
                    f"Please consult a healthcare professional for personalized assessment."
                )
                return render_template('index.html', result=result)

            bmi = calculate_bmi(weight, height)
            bmi_status = get_bmi_status(bmi)
            ideal_weight = calculate_ideal_weight(height)

            # Decide which weight to base protein on
            if bmi_status in ["normal", "underweight"]:
                protein_weight = weight
                weight_basis = "(based on actual weight)"
            else:
                protein_weight = ideal_weight
                weight_basis = "(based on ideal weight due to overweight)"

            protein = protein_requirement(protein_weight, activity)
            vitamins = micronutrient_estimates(protein_weight)

            result = (
                f"<strong>🔍 Your BMI:</strong> {bmi} ({bmi_status})<br>"
                f"<strong>🎯 Ideal Weight:</strong> {ideal_weight} kg<br>"
                f"<strong>🍗 Protein Required:</strong> {protein} g {weight_basis}<br><br>"
                f"<strong>🔬 Micronutrients:</strong><br>"
                f"• Vitamin B12: {vitamins['Vitamin B12 (mcg)']} mcg<br>"
                f"• Vitamin D: {vitamins['Vitamin D (IU)']} IU<br>"
                f"• Vitamin E: {vitamins['Vitamin E (mg)']} mg<br>"
                f"• Iron: {vitamins['Iron (mg)']} mg<br>"
                f"• Zinc: {vitamins['Zinc (mg)']} mg<br>"
                f"• Calcium: {vitamins['Calcium (mg)']} mg<br><br>"
            )

            # Add health suggestion if underweight or overweight
            if bmi_status == "underweight":
                result += "⚠️ You are underweight. Consider consulting a doctor or nutritionist.<br>"
            elif bmi_status in ["overweight", "obese"]:
                result += "⚠️ You are above normal BMI. Please consult a doctor for a proper plan.<br>"

            # Suggest minimum activity for sedentary/light
            if activity in ['sedentary', 'light']:
                result += "<br><strong>💡 Suggestion:</strong> Consider at least moderate physical activity (3–5 days/week) for improved metabolic and nutritional health."

        except ValueError:
            result = "❌ Please enter valid numerical values."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
