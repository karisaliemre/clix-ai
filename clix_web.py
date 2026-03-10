from flask import Flask, request, render_template_string
from openai import OpenAI
import random
import os

app = Flask(__name__)


client = OpenAI(api_key=os.getenv(api_key=("OPENAI_API_KEY"))

kullanici = None
sohbet = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Clix AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
background:linear-gradient(135deg,#0f172a,#1e3a8a);
font-family:Arial;
color:white;
padding:40px;
}

h1{
margin-bottom:20px;
}

input{
padding:12px;
border-radius:10px;
border:none;
margin-right:10px;
}

button{
padding:12px 20px;
border-radius:10px;
border:none;
background:#2563eb;
color:white;
cursor:pointer;
}

.chat{
margin-top:30px;
max-width:700px;
}

.msg{
padding:12px;
margin:10px 0;
border-radius:12px;
max-width:70%;
}

.user{
background:#fb923c;
margin-left:auto;
text-align:right;
color:black;
}

.bot{
background:#020617;
margin-right:auto;
}

</style>
</head>

<body>

<h1>Clix AI</h1>

<form method="post">
<input name="isim" placeholder="Adınız">
<input name="mesaj" placeholder="Mesajınız">
<button>Gönder</button>
</form>

<div class="chat">

{% for m in sohbet %}
<div class="msg {{m.tip}}">
<b>{{m.kim}}</b>: {{m.yazi}}
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    global kullanici
    global sohbet

    if request.method == "POST":

        isim = request.form.get("isim")
        mesaj = request.form.get("mesaj")

        if kullanici is None and isim:
            kullanici = isim

        hitap = kullanici

        if kullanici and kullanici.lower() == "emre":
            hitap = "patron"

        sohbet.append({
            "tip":"user",
            "kim":kullanici,
            "yazi":mesaj
        })

        mesaj_kucuk = mesaj.lower()

        # CLIX.PY'DEKİ KURAL CEVAPLAR

        if mesaj_kucuk == "merhaba":
            cevap = random.choice([
                f"Selam {hitap}",
                f"Merhaba {hitap}",
                f"Naber {hitap}"
            ])

        elif mesaj_kucuk == "nasılsın":
            cevap = f"İyiyim {hitap}, sen nasılsın?"

        elif mesaj_kucuk == "napıyorsun":
            cevap = f"Buradayım {hitap}, seninle konuşuyorum."

        elif mesaj_kucuk == "kendini tanıt":
            cevap = "Ben Clix, Emre Karış tarafından geliştirilen bir yapay zekayım."

        elif "kötü" in mesaj_kucuk:
            cevap = f"Neden kötü hissediyorsun {hitap}?"

        else:

            # OPENAI CEVABI

            try:

                response = client.chat.completions.create(
                    model="gpt-5-nano",
                    messages=[
                        {
                            "role":"system",
                            "content":f"""
Sen Clix adlı bir yapay zekasın.
Türkçe konuş.
Kullanıcıya '{hitap}' diye hitap et.
Seni Emre Karış yaptı ama sorulursa söyle.
Samimi ve hafif esprili konuş.
Senin kurucun Emre karış ama sorulursa söyle.
"""
                        },
                        {
                            "role":"user",
                            "content":mesaj
                        }
                    ]
                )

                cevap = response.choices[0].message.content

            except Exception as e:
                cevap = str(e)
                print(e)

        sohbet.append({
            "tip":"bot",
            "kim":"Clix",
            "yazi":cevap
        })

    return render_template_string(HTML, sohbet=sohbet)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=5000)


