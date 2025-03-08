from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Ana sayfa
@app.route("/")
def index():
    return render_template("index.html")

# Verileri işleme
@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Kullanıcı tarafından girilen gelir ve giderler
        incomes = request.form.getlist("incomes[]")
        income_names = request.form.getlist("income_names[]")
        income_values = [float(inc) for inc in incomes]

        expenses = request.form.getlist("expenses[]")
        expense_names = request.form.getlist("expense_names[]")
        expense_values = [float(exp) for exp in expenses]

        # Toplam Gelir, Gider ve Tasarruf Hesaplama
        total_income = sum(income_values)
        total_expenses = sum(expense_values)
        savings = total_income - total_expenses

        # Grafik Oluşturma
        labels = income_names + expense_names + ["Kalan"]
        values = income_values + [-val for val in expense_values] + [savings]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=['green' if v > 0 else 'red' for v in values])
        ax.set_title("Gelir ve Gider Dağılımı")
        ax.set_ylabel("TL")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        if not os.path.exists("static"):
            os.mkdir("static")
        plt.savefig("static/budget_chart.png")
        plt.close()

        return render_template("results.html", incomes=zip(income_names, income_values),
                               expenses=zip(expense_names, expense_values),
                               total_income=total_income, total_expenses=total_expenses, savings=savings)
    except Exception as e:
        return f"Bir hata oluştu: {e}"

if __name__ == "__main__":
    app.run(debug=True)
