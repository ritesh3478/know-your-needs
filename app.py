from flask import Flask, render_template, request

app = Flask(__name__)

# Nutrient multipliers per kg (estimated average)
NUTRIENT_RATIOS = {
    'protein': {
        'sedentary': 0.8,
        'light': 1.0,
        'moderate': 1.2,
        'active': 1.5,
        'athlete': 1.8
    },
    'vitamin_b12_mcg': 0.002,
    'vitamin_d_iu': 10,
    'vitamin_e_mg': 0.2,
    'iron_mg': 0.3,
    'zinc_mg': 0.25,
    'calcium_mg': 12
}

def calculate_ideal_weight(height_cm):
    return round((height_cm - 100 + (height_cm - 150) / 4), 2)

def get_bmi_status(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal"
    else:
        return "overweight"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            activity = request.form["activity"]

            if height > 250 or weight > 400:
                result = "Your height or weight exceeds standard health ranges. Please consult a healthcare provider for personalized guidance."
                return render_template("index.html", result=result)

            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 2)
            bmi_status = get_bmi_status(bmi)
            ideal_weight = calculate_ideal_weight(height)

            if bmi_status == "overweight":
                base_weight = ideal_weight
                weight_basis = "(based on ideal weight due to overweight)"
            else:
                base_weight = weight
                weight_basis = "(based on actual weight)"
            
            protein_per_kg = NUTRIENT_RATIOS['protein'].get(activity, 0.8)
            protein = round(protein_per_kg * base_weight, 2)

            vitamins = {
                'Vitamin B12 (mcg)': round(NUTRIENT_RATIOS['vitamin_b12_mcg'] * base_weight, 2),
                'Vitamin D (IU)': round(NUTRIENT_RATIOS['vitamin_d_iu'] * base_weight, 2),
                'Vitamin E (mg)': round(NUTRIENT_RATIOS['vitamin_e_mg'] * base_weight, 2),
                'Iron (mg)': round(NUTRIENT_RATIOS['iron_mg'] * base_weight, 2),
                'Zinc (mg)': round(NUTRIENT_RATIOS['zinc_mg'] * base_weight, 2),
                'Calcium (mg)': round(NUTRIENT_RATIOS['calcium_mg'] * base_weight, 2)
            }

            activity_advice = ""
            if activity in ["sedentary", "light"]:
                activity_advice = (
                    "🟡 Consider increasing your physical activity for better health. "
                    "Even 30 minutes a day of light walking can improve wellbeing."
                )

            result = (
                f"🔍 Your BMI is {bmi} ({bmi_status}).<br>"
                f"🎯 Ideal weight: {ideal_weight} kg<br>"
                f"🍗 Protein needed: {protein} g {weight_basis}<br><br>"
            )

            result += "<b>🔬 Suggested Micronutrients:</b><br>"
            for nutrient, value in vitamins.items():
                result += f"• {nutrient}: {value}<br>"

            if bmi_status != "normal":
                result += f"<br>⚠️ Your weight is considered {bmi_status}. Please consult a doctor or certified nutritionist for tailored advice.<br>"

            if activity_advice:
                result += f"<br>{activity_advice}"
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
