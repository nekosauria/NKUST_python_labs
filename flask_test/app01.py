from flask import Flask, send_from_directory
from flask import request
from flask import render_template

app = Flask(__name__)


# =========================================================
# index page
# =========================================================

@app.route("/")
def index():
    return send_from_directory("static", "myform.html")


# =========================================================
# process
# =========================================================

@app.route("/process")
def process():
    # =========================================================
    # linear regression model parameter
    # =========================================================

    # y = a1*x1 + a2*x2 + b
    #
    # a1 -> x1 權重(weight)
    # a2 -> x2 權重(weight)
    # b  -> bias / intercept
    #
    # 線性回歸本質：
    # 使用線性方程式預測結果 y
    #
    # x1, x2 -> input feature
    # y      -> predict result

    a1 = 3.2
    a2 = -1.8
    b = 3.3

    # -------------------------
    # get data
    # -------------------------

    x1 = float(request.args.get("x1"))
    x2 = float(request.args.get("x2"))

    # -------------------------
    # predict
    # -------------------------

    y = a1 * x1 + a2 * x2 + b

    # -------------------------
    # render html
    # -------------------------

    return render_template(
        "result.html",
        x1=x1,
        x2=x2,
        y=y
    )


# =========================================================
# run
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)