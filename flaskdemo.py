from flask import Flask, render_template, request
import scrapetwitter

app = Flask(__name__)

@app.route('/')
@app.route("/index")
def index():
  return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
  output = request.form.to_dict()
  print(output)
  name = output["name"]
  scrapetwitter.get_tweets_from_user(name) 
  
  return render_template('TornadoResults.html', name = name)

if __name__ == '__main__':
  app.run(debug=True)

