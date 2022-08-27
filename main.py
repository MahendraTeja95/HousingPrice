import pickle
from flask import Flask,render_template,request
import decimal



app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/result',methods=['GET','POST'])
def result():
    try:
        area=int(request.form.get("area"))
        br=int(request.form.get("bed-room"))
        bt=int(request.form.get("bath-room"))
        stories=int(request.form.get("stories"))
        mr=int(request.form.get("main-road"))
        gr=int(request.form.get("guest-room"))
        bm=int(request.form.get("basement"))
        hw=int(request.form.get("hot-water"))
        ac=int(request.form.get("air-conditioner"))
        pr=int(request.form.get("parking"))
        pfa=int(request.form.get("prefarea"))
        fs=int(request.form.get("furnishing-status"))
        res=model.predict([[area,br,bt,stories,mr,gr,bm,hw,ac,pr,pfa,fs]])
    
        def currencyInIndiaFormat(n):
            d = decimal.Decimal(str(n))
            if d.as_tuple().exponent < -2:
                s = str(n)
            else:
                s = '{0:.2f}'.format(n)
            l = len(s)
            i = l-1
            res = ''
            flag = 0
            k = 0
            while i>=0:
                if flag==0:
                    res = res + s[i]
                    if s[i]=='.':
                        flag = 1
                elif flag==1:
                    k = k + 1
                    res = res + s[i]
                    if k==3 and i-1>=0:
                        res = res + ','
                        flag = 2
                        k = 0
                else:
                    k = k + 1
                    res = res + s[i]
                    if k==2 and i-1>=0:
                        res = res + ','
                        flag = 2
                        k = 0
                i = i - 1
            return res[::-1]
        
        res1=res[0]
        res1=f"{currencyInIndiaFormat(round(res1))}/-"
        return render_template('result.html',result=f"Price is {res1}")
    except:
        return render_template('result.html',result="Something went wrong")


if __name__=='__main__':
    app.run(debug=True)