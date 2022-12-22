from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, Length
import smtplib
import os

app = Flask(__name__)
app.secret_key = "bingchulovesgyugyuandmandu"
bootstrap = Bootstrap(app)

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


class ContactFrom(FlaskForm):
    name = StringField("Name",
                       validators=[DataRequired(), Length(max=255)])
    email = StringField("Email",
                        validators=[DataRequired(), Email(message="Invalid Email Address"), Length(max=255)])
    message = StringField("Message",
                          validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send Message")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactFrom()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        contact_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        with smtplib.SMTP("smtp.gmail.com") as smtp:
            smtp.starttls()
            smtp.login(user=MY_EMAIL, password=MY_PASSWORD)
            smtp.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject: New Message Alert !!\n\n{contact_message}".encode("utf-8")
            )
        return render_template("thankyou.html", is_thankyou_page=True)
    return render_template("contact.html", form=form, is_contact_page=True)


if __name__ == "__main__":
    app.run(debug=True)
