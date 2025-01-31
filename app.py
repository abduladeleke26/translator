from flask import Flask, render_template, request, redirect, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

urltrans = "https://translate.googleapis.com/v3beta1/projects/929109150783:translateText"
urldetect = "https://translate.googleapis.com/v3beta1/projects/929109150783:detectLanguage"
urllan = "https://translate.googleapis.com/v3beta1/projects/929109150783/supportedLanguages"

headers = {
    "Authorization": f"Bearer {os.environ.get('FLASK_KEY')}",
    "Content-Type": "application/json"
}


def translatee(text,fromm,to):
    if fromm != to:
        payload = {
            "contents": [text],
            "targetLanguageCode": to,
            "sourceLanguageCode": fromm,

        }

        response = requests.post(urltrans, json=payload, headers=headers)
        gett = response.json()
        translated = gett.get("translations")[0].get("translatedText")

        return translated
    else:
        return text


def getCode(text):
    params = {
        "displayLanguageCode": "en"
    }

    response = requests.get(urllan, headers=headers, params=params)

    languagess = response.json().get("languages")
    for language in languagess:
        name = language.get("displayName")
        code = language.get("languageCode")
        if text.lower() == name.lower():
            return code, name
        if text.lower() == code.lower():
            return code, name


def detect(text):
    payload = {

        "content": text

    }

    response = requests.post(urldetect, json=payload, headers=headers)

    gett = response.json()
    language = gett.get("languages")[0].get("languageCode")
    conf = gett.get("languages")[0].get("confidence")
    return language, conf


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/translate', methods=['POST'])
def translate():
    choice1 = request.form.get("choice1")
    choice2 = request.form.get("choice2")
    text = request.form.get("text")

    if choice2 == "Languages" and not text:
        flash('Please fill in all required fields.')
        return redirect('/')
    elif choice2 == "Languages":
        flash('Please pick a language')
        return redirect('/')
    elif not text:
        flash('Please type something to translate')
        return redirect('/')

    if choice1 == "Detect Language":
        language, conf = detect(text)
        fromm, name = getCode(language)
    else:
        fromm, name = getCode(choice1)

    language, conf = detect(text)

    conf *= 100

    if conf> 50:
        fromm, name = getCode(language)

    to, name2 = getCode(choice2)

    translated = translatee(text, fromm, to)

    return render_template("index.html", text=text, translated=translated, choice1=name, choice2=name2)

print(get_access_token())
if __name__ == "__main__":
    app.run(debug=True)
