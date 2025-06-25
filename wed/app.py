from flask import Flask,request, jsonify, render_template 

app=flask (__name__)

@app.route("/")
def home ():
    return render_template('index.html')



@app.route('/datos', methods= 'POST')
def datos_json():
    institucion = request.form('institucion')
    identificacion = request.form('identificacion')
    return jsonify({"institucion ": "institucion", "identificacion": "identificacion"})


if __name__ == '__main__':
    app.run(debug=True)