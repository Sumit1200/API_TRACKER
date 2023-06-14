from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# A list to store the APIs
apis = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        api_link = request.form['api_link']
        status1=''    
        status2 =''
        try:
            if requests.options(api_link):
                response=requests.options(api_link)

            elif requests.post(api_link):
                response=requests.post(api_link)

            elif requests.get(api_link):
                response=requests.get(api_link)

            status_code = response.status_code
            if status_code == 200:
                status1 = 'Online'
            else:
                status2 = f'Offline ({status_code})'
        except requests.exceptions.RequestException:
            status2 = 'Ofline'


        api = {'link': api_link, 'status1': status1,'status2': status2}
        apis.append(api)

    return render_template('index.html', apis=apis)

if __name__ == '__main__':
    app.run(debug=True)


