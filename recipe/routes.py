# from urllib import request
import os
import time

from flask import render_template, flash, redirect, url_for, request, session, jsonify
from recipe import app, db
from recipe.forms import LoginForm, SignupForm, ChangeForm, EditInfoForm, UploadRecipeForm, AddClassifyForm, DeleteClassifyForm
from recipe.models import User, steps, Recipe, materials, Classify, Log, Collections
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # main page
    if not session.get("USERNAME") is None: # session exists
        username = session.get("USERNAME")
    else: # session does not exist
        username = None

    # recommend recipes
    recipes = Recipe.query.all()
    recipeloop1 = {}
    recipeloop2 = {}
    i = 0
    for r in recipes:
        if i<4:
            recipeloop1[r.name] = r.image
        elif i<8:
            recipeloop2[r.name] = r.image

        i = i + 1

    # classify
    classify = Classify.query.all()
    classifies = {}
    for c in classify:
        classifies[c.region] = c.image
    return render_template('index.html', title='Home', username=username, recipes=recipes, recipe1= recipeloop1, recipe2= recipeloop2, classify=classifies)

@app.route('/base', methods=['GET', 'POST'])
def base():
    # main page
    style = request.json['style']
    print(style)
    # session["Style"] = style
    #
    # if session.get("USERNAME") is None: # session exists
    #     session["Style"] = "Light"
    #
    # style = session.get("Style")

    return jsonify({'Style': style})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('username or password is incorrect')

            # create error
            e = Log(description="User "+form.username.data+" is not existed!", type="Error")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            if not check_password_hash(u.password_hash, form.password.data):
                # form.password.error = 'Passwords do not match!'
                flash('username or password is incorrect')

                # create warning
                e = Log(description="User " + form.username.data + " input wrong password", type="Warning")
                db.session.add(e)
                db.session.commit()
                return redirect(url_for('login'))

            session["USERNAME"] = u.username

            # create message
            e = Log(description="User " + form.username.data + " login!", type="Message")
            db.session.add(e)
            db.session.commit()
        return redirect(url_for('index'))
    print("2")
    return render_template('login.html', title='Sign up', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))
        # add user to database
        passw_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(user)
        db.session.commit()
        # flash('User registered with username:{}'.format(form.username.data))

        # create message
        e = Log(description="New user " + form.username.data + " sign up!", type="Message")
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register a new user', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():

    # create message
    e = Log(description="User " + session.get("USERNAME") + " logout!", type="Message")
    db.session.add(e)
    db.session.commit()

    session.pop("USERNAME", None)
    return render_template('index.html', title='Home')

@app.route('/recipe/<name>', methods=['GET', 'POST'])
def recipe(name):
    print("get the title: ", name)
    # get steps from database
    step = steps.query.filter_by(name=name).order_by("order").all()

    # get image of this dish
    image = Recipe.query.filter_by(name=name).first().image
    description = Recipe.query.filter_by(name=name).first().description
    author = Recipe.query.filter_by(name=name).first().author

    # get materials of this dish
    material = materials.query.filter_by(name=name).order_by("order").all()

    recipe = {}
    for s in step:
        # put image url and step string into a dictionary
        recipe.update({".."+s.image: s.step})

    mat = {}
    for m in material:
        col = m.order % 2
        mat.update({m.material: col})

    # get whether collection
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        c = Collections.query.filter_by(recipe=name, username=username).first()
        if c:
            collection = "cancel"
        else:
            collection = "collect"
    else:
        username = None
        collection = "collect"
    return render_template('recipebase.html', title=name, recipe=recipe, image=".."+image, description=description, author=author, materials=mat, collection=collection, username=username)

@app.route('/classify/<name>', methods=['GET', 'POST'])
def classify(name):
    if not session.get("USERNAME") is None:  # session exists
        username = session.get("USERNAME")
    else:  # session does not exist
        username = None

    # get dishes of specific region from database
    dishes = Recipe.query.filter_by(region=name).all()
    dish = {}
    for d in dishes:
        print(d.name, d.region)
        dish.update({d.name: d.image})
        # dish.update({d.image:d.image})
    return render_template('classify.html', title=name, dish=dish, username=username)


@app.route('/changePass', methods=['GET', 'POST'])
def changePass():
    # change password
    form = ChangeForm()
    username = session.get("USERNAME")
    oldpassword = User.query.filter_by(username=username).first().password_hash
    print("2222222222222222222222222222222222222222",oldpassword)
    if form.validate_on_submit():
        print("22222222222222222222222222229999999999", form.password.data)
        if not check_password_hash(form.password.data,oldpassword):
            flash('Original password is incorrect')
            print("!!!!!!!!!!!!!!!!!!!!!!!jinru")

            # create warning
            e = Log(description="User " + username + " input wrong original password to change password!", type="Message")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('userinfor'))
        else:
            User.query.filter_by(username=username).first().password_hash = generate_password_hash(form.newPassword.data)
            db.session.commit()
            # flash('Modify successfully!')

            # create message
            e = Log(description="User " + username + " changed password!", type="Message")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('passwordEdit.html', title='User Information', username=username, form=form)



@app.route('/editinfo', methods=['GET', 'POST'])
def editinfo():
    # change password
    form = EditInfoForm()
    username = session.get("USERNAME")
    user = User.query.filter_by(username=username).first()
    age = user.age
    gender = user.gender
    detail = user.detail

    # form.name.value = user.username
    # if user.age:
    #     form.age.value = user.age
    # if user.gender:
    #     form.gender.value = user.gender
    # if user.detail:
    #     form.detail.value = user.detail


    print(user.username)
    if form.validate_on_submit():

        print(form.age.data)
        user.username = form.username.data
        session["USERNAME"] = user.username
        user.age = form.age.data
        user.gender = form.gender.data
        user.detail = form.detail.data
        db.session.commit()


        # create message
        e = Log(description="User " + username + " changed detailed information", type="Message")
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('personal'))

    return render_template('editInformation.html', title='Edit Information', form=form, username=username, age=age, gender=gender, detail=detail)

@app.route('/personal', methods=['GET', 'POST'])
def personal():
    # show personal information
    username = session.get("USERNAME")
    email = User.query.filter_by(username=username).first().email
    age = User.query.filter_by(username=username).first().age
    gender = User.query.filter_by(username=username).first().gender
    detail = User.query.filter_by(username=username).first().detail
    return render_template('personal.html', title='personal', username=username, email=email, gender=gender, age=age, detail=detail)

@app.route('/collection', methods=['GET', 'POST'])
def collection():
    # my collection page
    username = session.get("USERNAME")
    cols = Collections.query.filter_by(username=username).all()
    dic = {}
    for c in cols:
        name = c.recipe
        image = Recipe.query.filter_by(name=name).first().image
        dic.update({name:image})
    return render_template('collection.html', title='User Information', cols=cols,dic=dic)


@app.route('/checkuser', methods=['POST'])
def check_username():
    # check username every time
    chosen_name = request.json['username']
    print(chosen_name)
    user_in_db = User.query.filter_by(username=chosen_name).first()
    if not user_in_db:
        return jsonify({'text': 'Username is available'}, {'returnvalue': 0})
    else:
        return jsonify({'text': 'Username is already taken!'}, {'returnvalue': 1})


@app.route('/showdetails', methods=['POST'])
def show_details():
    # show personal detailed information
    chosen_name = request.json['username']
    print(chosen_name)
    user_in_db = User.query.filter_by(username=chosen_name).first()
    gender = user_in_db.gender
    age = user_in_db.age
    detail = user_in_db.detail
    return jsonify({'gender': gender}, {'age': age}, {'detail': detail})


@app.route('/upload_recipe', methods=['GET', 'POST'])
def upload_recipe():
    form = UploadRecipeForm()

    if session.get("USERNAME") is None:  # session not exists
        return redirect(url_for('login'))

    username = session.get("USERNAME")
    print(username)

    # classify
    classify = Classify.query.all()

    if request.method == 'POST':

        if form.validate_on_submit():

            print(request.form.to_dict())
            # calculate materials numbers
            n = 1
            for d in request.form.to_dict():
                if request.form.to_dict().get("mat"+str(n)):
                    n = n + 1
            n = n - 1

            # calculate step numbers
            print("n: ", n)
            diclen = int( (len(request.form.to_dict())-5-n) )
            dishname = request.form['dishname']
            description = request.form['description']
            # classify = request.form['classify']
            classify = request.form['region']

            pic1 = request.files["pics"]
            # Set the path to which the image will be saved
            path = basedir + "/static/upload/img/"
            # Gets the image name and suffix
            imgName = pic1.filename
            # The image path and name form the image saving path
            file_path = path + imgName
            # Save image
            pic1.save(file_path)
            # url is the path of image
            url = '/static/upload/img/' + imgName

            step1 = request.form['step']
            s = steps(name=dishname, order=1, step=step1, image=url)
            db.session.add(s)

            # add materials to database
            for i in range(1, n + 1):
                mat = request.form['mat' + str(i)]
                m_temp = materials(name=dishname, order=i, material=mat)
                db.session.add(m_temp)

            # add steps to database
            print("d: ", diclen)
            if diclen > 1:
                for i in range(2, diclen+1):
                    pic = request.files['pics'+str(i)]
                    path = basedir + "/static/upload/img/"
                    imgName = pic.filename
                    file_path = path + imgName
                    pic.save(file_path)
                    url = '/static/upload/img/' + imgName
                    step = request.form['step'+str(i)]
                    s_temp = steps(name=dishname, order=i, step=step, image=url)
                    db.session.add(s_temp)
                    if i == diclen:
                        r = Recipe(name=dishname, region=classify, image=url, description=description, author=username)
                        db.session.add(r)
            else:
                r = Recipe(name=dishname, region=classify, image=url, description=description, author=username)
                db.session.add(r)
            db.session.commit()

            # create message
            e = Log(description="User " + username + " upload " + dishname + " recipe", type="Message")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('addRecipe.html', title='Edit Recipe', form=form, username=username, classify=classify)

@app.route('/add_classify', methods=['GET', 'POST'])
def add_classify():
    form = AddClassifyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            region = request.form['region']

            image = request.files["image"]
            # Set the path to which the image will be saved
            path = basedir + "/static/img/"
            # Gets the image name and suffix
            imgName = image.filename
            # The image path and name form the image saving path
            file_path = path + imgName
            # Save image
            image.save(file_path)
            # url is the path of image
            url = '../static/img/' + imgName

            c = Classify(region=region, image=url)
            db.session.add(c)
            db.session.commit()

            # create message
            e = Log(description="Admin add "+ region +" cuisine", type="Message")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('personal'))
    return render_template('addClassify.html', title='Add classify', form=form)

@app.route('/delete_classify', methods=['GET', 'POST'])
def delete_classify():
    form = DeleteClassifyForm()
    classes = Classify.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():
            region = request.form['region']
            print(region)

            c = Classify.query.filter_by(region=region).first()
            db.session.delete(c)
            # delete recipes
            for i in Recipe.query.filter_by(region=region).all():
                dishname = i.name
                # delete steps
                for n in steps.query.filter_by(name=dishname).all():
                    db.session.delete(n)
                # delete materials
                for n in materials.query.filter_by(name=dishname).all():
                    db.session.delete(n)
                db.session.delete(i)
            db.session.commit()

            # create message
            e = Log(description="Admin delete " + region + " cuisine", type="Message")
            db.session.add(e)
            db.session.commit()
            return redirect(url_for('personal'))
    return render_template('deleteClassify.html', title='Delete classify', form=form, classes=classes)

@app.route('/viewlog', methods=['GET', 'POST'])
def viewlog():
    # view log
    errors = Log.query.filter_by(type="Error").all()
    warnings = Log.query.filter_by(type="Warning").all()
    messages = Log.query.filter_by(type="Message").all()
    return render_template('log.html', title='View log', errors=errors, warnings=warnings, messages=messages)

@app.route('/addcollection', methods=['POST', 'GET'])
def add_collection():
    # add collection
    # if request.method == 'POST':
    dishname = request.json['dishname']
    print(dishname)

    # add collection must after log in
    if not session.get("USERNAME") is None:
        # return redirect(url_for('login'))

        username = session.get("USERNAME")

        c = Collections(recipe=dishname, username=username)
        db.session.add(c)
        db.session.commit()
    else:
        username = None
    return jsonify({'cancel': "cancel"}, {'username': username})

@app.route('/deletecollection', methods=['POST'])
def delete_collection():
    # cancel collection
    # if request.method == 'POST':
    dishname = request.json['dishname']
    print(dishname)

    username = session.get("USERNAME")

    c = Collections.query.filter_by(recipe=dishname, username=username).first()
    db.session.delete(c)
    db.session.commit()
    return jsonify({'cancel': "cancel"})