from flask import Flask, redirect, render_template, request, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

@app.route('/')
def read_csv():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Phase 1 Wallet list final - True users.csv')
    data = pd.read_csv(filepath)
    return render_template('show_csv_data.html', data_var=data.to_html())

@app.route('/search_wallet', methods=['GET'])
def search_wallet():
    wallet_address = request.args.get('wallet_address')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Phase 1 Wallet list final - True users.csv')
    data = pd.read_csv(filepath)

    # Lakukan pencarian berdasarkan alamat dompet
    filtered_data = data[data['wallet_address'] == wallet_address]

    if filtered_data.empty:
        result_message = "Tidak Eligible"
        nft_type = None
    else:
        result_message = "Eligible"
        nft_type = filtered_data.iloc[0]['NFT type']

    return redirect(url_for('show_result', result=result_message, nft_type=nft_type))

@app.route('/result')
def show_result():
    result = request.args.get('result')
    nft_type = request.args.get('nft_type')
    return render_template('result.html', result=result, nft_type=nft_type)

if __name__ == '__main__':
    app.run(debug=True)