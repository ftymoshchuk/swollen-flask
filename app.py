from flask import Flask, render_template, request

app = Flask(__name__)

def summ(user_input):
    try:
        return int(user_input) + 2
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def main():
    result = None
    error = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        result = summ(user_input)
        if result is None:
            error = "Please provide only numbers."

    return render_template('main.html', result=result, error=error)

if __name__ == '__main__':
   app.run()
