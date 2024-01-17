from flask import request, abort, render_template
from manager import Manager

from shell import app
from pick_list import PickList


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/leave', methods=["POST"])
def leave_pick_list():
    passcode = request.form['code']
    uname = request.form['username']

    if passcode and uname:
        Manager.remove_user(passcode, uname)


@app.route("/delete", methods=["GET, POST"])
def delete_pick_list():
    passcode = request.form['code']
    uname = request.form['username']  # Each device's username will be stored on client

    if passcode and uname:
        Manager.delete_entry(passcode, uname)
    else:
        abort(400)


# example uri: https/url.com/join?username=pat-mart
@app.route("/join", methods=["GET", "POST"])
def join_pick_list():
    username = request.form['username']
    passcode = request.form['code']

    if username and passcode:
        Manager.add_user(code=passcode, username=username)

    else:
        abort(400)


# example uri: https://url.com/create?code=hello_world&bins=[{254: {a: num}}, {3950: {b: num}}]&username=pat_mart
@app.route("/create", methods=["GET", "POST"])
def create_pick_list():
    passcode = request.form['code']
    bins = request.form['bins']
    creator_uname = request.form['username']  # Username of creator

    if request.method == "POST" and passcode and bins and creator_uname:
        new_val = PickList(
            code=passcode,
            creator=creator_uname,
            usernames=[],  # Represented as string, parsing will be handled client-side
            bins=bins
        )
        Manager.add_list(new_val)
    else:
        abort(400)
