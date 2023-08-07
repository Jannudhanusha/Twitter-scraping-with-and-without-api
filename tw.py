from flask import Flask, render_template, request, Response
import pandas as pd
from snscrape.modules import twitter as sntwitter
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form['word']
        begin_date = request.form['begin_date']
        end_date = request.form['end_date']
        limit = int(request.form['limit'])
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{begin_date} until:{end_date}').get_items()):
            if i >= limit:
                break
            tweets.append([tweet.date, tweet.username, tweet.content])
        df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
        csv_data = df.to_csv(index=False).encode('utf-8')
        csv_io = io.StringIO(csv_data.decode())
        return render_template('index.html', tweets=df.to_html(index=False), csv_data=csv_io.getvalue())
    else:
        return render_template('index.html')

@app.route('/download_csv')
def download_csv():
    word = request.args.get('word')
    begin_date = request.args.get('begin_date')
    end_date = request.args.get('end_date')
    limit = int(request.args.get('limit'))
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{begin_date} until:{end_date}').get_items()):
        if i >= limit:
            break
        tweets.append([tweet.date, tweet.username, tweet.content])
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    csv_data = df.to_csv(index=False).encode('utf-8')
    response = Response(csv_data, mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='tw.csv')
    return response

if __name__ == '__main__':
    app.run(debug=True)
