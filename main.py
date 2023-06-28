from flask import Flask, render_template, request
import psycopg2

app: Flask = Flask(__name__)
connection = psycopg2.connect(
    host="localhost",
    database="sqltest",
    user="postgres",
    password="admin"
)


@app.route('/')
def main() -> str:
    cursor = connection.cursor()
    cursor.execute("SELECT num1, operation, num2, result FROM calculations ORDER BY id DESC")
    history = cursor.fetchall()
    cursor.close()

    return render_template('index.html', history=history)


@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']

        if operation == '+':
            result = float(num1) + float(num2)
        elif operation == '-':
            result = float(num1) - float(num2)
        elif operation == '*':
            result = float(num1) * float(num2)
        elif operation == ':':
            result = float(num1) / float(num2)
        else:
            return render_template('index.html', result="Недопустимая операция")

        cursor = connection.cursor()
        cursor.execute("INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)",
                       (num1, num2, operation, result))
        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("SELECT num1, operation, num2, result FROM calculations ORDER BY id DESC")
        history = cursor.fetchall()
        cursor.close()

        return render_template('index.html', result=result, history=history)

    except ValueError:
        return render_template('index.html', result="Вы некорректно ввели число")


if __name__ == "__main__":
    app.run(
        port=8800,
        debug=True
    )

connection.close()