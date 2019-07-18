from flask import Flask,redirect,render_template,url_for,request,g
from get_info_vip_list import get_vip_info_list
from get_serch_html import serch_html
from get_movies_src import get_movie_index
from get_movie_new import serch_movies_new_big
import json
class Config():
    #表单 的配置
    WTF_CSRF_ENABLE=True
    SECRET_KEY="www.xueyiyang.top"
app = Flask(__name__)
app.config.from_object(Config)
quan_ju = ""
@app.route('/',methods=["GET","POST"])
def index():
    from forms import form_serch
    c = get_vip_info_list()
    info = c.get_items_info()
    # print(info)
    form = form_serch()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for("serch_movie",name = name))
    return render_template("/index.html",info_list = info,form = form)
@app.route('/serch_movie')
def serch_movie():
    name = request.args.get("name")
    s = serch_html(name)
    data = s.get_html()
    #        data = {"url":url,"url_img":url_img,"url_h2":html.unescape(url_h2),"url_div":html.unescape(url_div)}
    # print("*****",data)
    return render_template("/serch_movie_data.html",data = data,name = name)
@app.route("/play_movie_new",methods=["GET","POST"])
def play_movie_new():

    # if request.method == 'POST':
    #     ck = request.form.get("ckey")
    #     vid = request.form.get("vidd")
    #     url = request.form.get("url")
    #     print(ck,"**************post",type(vid),url,vid)
    #
    #     # serch = serch_movies_new_big(ckey=str(ck),vid=str(json.loads(vid)[0]))
    #     #
    #     # print(serch.get_paly_url(),json.loads(vid)[0])
    #     # src_url = serch.get_paly_url()
    #     # return render_template("/player.html", src_r= src_url)
    #     # return "ok"
    #
    # if request.method == 'GET':
    #     print("get")
    #     ck = request.args.get("ckey")
    #     # ck = request.args.get("ckey")
    #     vid = request.args.get("vidd")
    #
    #     print(ck,"************get",vid,"**********vid")
    #     # return redirect(url_for("serch_movie", name="黑豹"))
    #     # print(request.args,g)
    #     # serch = serch_movies_new_big(ckey=str(ck),vid=vid)
    #     #
    #     # print(serch.get_paly_url(),vid)
    #     # src_url = serch.get_paly_url()
    #
    #     # return render_template("/player.html", src_r= src_url)

    # return render_template("/test_ck8.html")
    # return "ok"
    pass
@app.route("/play_movies_zui_new")
def play_movies_zui_new():
  #  print(request.args)
    ck = request.args.get("ckey")
    # ck = request.args.get("ckey")
    vid = request.args.get("vid")

 #   print(ck, "************get", vid, "**********vid")
    serch = serch_movies_new_big(ckey=str(ck),vid=vid)

    # print(serch.get_paly_url(),vid)
    src_url = serch.get_paly_url()

    return render_template("/player.html", src_r= src_url)

@app.route("/test",methods=["GET","POST"])
def test():

    if request.method == 'POST':
        ck = request.form.get("ckey")
        print(request.args)
        print(ck,"**************")
    if request.method == 'GET':
        print("get")
        ck = request.args.get("ckey")
        print(request.args)
        print(ck,"**************")
    return render_template("/test_ck8.html")
@app.route('/play_movie')
def play_movie():
    url = request.args.get("url")

    #print(url)
    s = get_movie_index(url=url)
    #print("pk")
    try:
        src_url = s.run()
    except :
        src_url = "//jx.api.163ren.com/vod.php?url="+url
        return redirect(src_url)
    # return "ok"
    # 默认 /ppvod/316F2512E37A26725B3B703D2AEDF36E.m3u8
    #print("**********",src_url)
    # html_text = '<source src= "{}" type="application/x-mpegURL">'
    try:
        if src_url == "/hls/index.m3u8":
            src_url = s.if_not_success()
            print(src_url)
            return render_template("/player.html", src_r= src_url)
        # return render_template("/player.html",src_r = "//cn2.zuidadianying.com"+src_url)
        src_url = "//jx.api.163ren.com/vod.php?url=" + url
        return redirect(src_url)

    except :
        print("*****except")
        src_url = "//jx.api.163ren.com/vod.php?url="+url
        return redirect(src_url)

@app.route('/python')
def get_python_doc():
    return render_template("/python_html/index.html")
if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run()
