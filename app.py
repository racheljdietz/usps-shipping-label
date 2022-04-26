import config, easypost

from flask import Flask, request, render_template , redirect
app = Flask(__name__, template_folder='.')

easypost.api_key = config.API_KEY

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/shipping-labels/create', methods=['POST'])
def createLabel():
    shipment = easypost.Shipment.create(
        from_address = {
            "name": request.form.get("fromName"),
            "company": request.form.get("fromCompany"),
            "street1": request.form.get("fromAddress"),
            "street2": request.form.get("fromAddress2"),
            "city": request.form.get("fromCity"),
            "state": request.form.get("fromState"),
            "zip": request.form.get("fromZip"),
            "country": request.form.get("fromCountry"),
        },
        to_address = {
            "name": request.form.get("toName"),
            "company": request.form.get("toCompany"),
            "street1": request.form.get("toAddress"),
            "street2": request.form.get("toAddress2"),
            "city": request.form.get("toCity"),
            "state": request.form.get("toState"),
            "zip": request.form.get("toZip"),
            "country": request.form.get("toCountry"),
        },
        parcel = {
            "length": request.form.get("length"),
            "width": request.form.get("width"),
            "height": request.form.get("height"),
            "weight": request.form.get("weight"),
        },
    )

    shipment.buy(rate=shipment.lowest_rate())

    return redirect(shipment.postage_label.label_url)


if __name__=='__main__':
    app.debug = True
    app.run()