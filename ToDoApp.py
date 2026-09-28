from datatime import datetime
from flash import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flash(__name__)
app.config["SQLACHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQALchemy(app)