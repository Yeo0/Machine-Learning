#웹에서 쉽게 사용할 수 있는 언어판별 애플리케이션
#!/usr/bin/env python3
import cgi, os.path
from sklearn.externals import joblib

#학습 데이터 읽어들이기
pklfile=os.path.dirname(__file__)+"/freq.pkl"
clf=joblib.load(pklfile)

#텍스트 입력 양식 출력하기
def show_form(text, msg=""):
    print("Content-Type : text/html ; charset=utf-8")
    print("")
    print("""
        <html>
        <body><form>
        <textarea name="text" rows="8" cols="40">{0}</textarea>
        <p><input type="submit" value="판정"></p>
        <p>{1}</p>
        </form></body></html>
    """.format(cgi,escape(text), msg))

#판정하기
def detect_lang(text):
    text=text.lower()
    code_a, code_z = (ord("a"), ord("z"))
    cnt=[0 for i in range(26)]
    for char in text:
        n=ord(char)-code_a
        if 0<= n <= 26:
            cnt[n]+=1
    total=sum(cnt)
    if total ==0: return "입력이 없습니다"
    freq=list(map(lambda n: n/ total, cnt))
    
    #언어 예측하기
    res=clf.predict([freq])
    
    #언어코드 한국어로 변환
    lang_dic={"en":"영어", "fr":"프랑스어", "id":"인도네시아어", "tl": "타갈로그어"}
    return lang_dic[res[0]]

#입력 양식의 값 읽어 들이기
form=cgi.FieldStorage()
text=form.getvalue("text", default="")
msg=""
if text!="":
    lang=detect_lang(text)
    msg="판정 결과: "+ lang
    
#입력 양식 출력
show_form(text, msg)