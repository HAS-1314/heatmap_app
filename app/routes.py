from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Location, Rating
from app.forms import RegisterForm, LoginForm, RateForm
from werkzeug.utils import secure_filename
import os
from app import db
from app.forms import UploadAvatarForm


# 创建蓝图
main_routes = Blueprint('main_routes', __name__)

# 定义路由
@main_routes.route('/')
def index():
    locations = Location.query.all()
    location_scores = []  # 满足条件的排行榜数据
    location_scores_below = []  # 不满足条件的未上榜数据

    for location in locations:
        ratings = Rating.query.filter_by(location_id=location.id).all()
        if ratings:
            avg_score = round(sum(r.score for r in ratings) / len(ratings))  # 平均分四舍五入取整
            num_ratings = location.num_ratings  # 直接从 Location 模型中获取参与打分的用户数量
            if num_ratings >= 10:  # 满足条件的排行榜数据
                location_scores.append((location, avg_score, num_ratings))
            else:  # 不满足条件的未上榜数据
                location_scores_below.append((location, avg_score, num_ratings))

    # 按平均分从高到低排序
    location_scores.sort(key=lambda x: x[1], reverse=True)
    location_scores_below.sort(key=lambda x: x[1], reverse=True)

    return render_template('index.html', location_scores=location_scores, location_scores_below=location_scores_below)

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('该邮箱已被注册，请使用其他邮箱。', 'error')
            return redirect(url_for('main_routes.register'))

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('该用户名已被注册，请使用其他用户名。', 'error')
            return redirect(url_for('main_routes.register'))

        # 处理头像上传
        avatar_file = form.avatar.data
        if avatar_file:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            avatar_file.save(avatar_path)
        else:
            avatar_path = None

        # 创建用户并设置密码
        user = User(username=form.username.data, email=form.email.data, avatar=avatar_path)
        user.set_password(form.password.data)  # 生成哈希密码并存储
        db.session.add(user)
        db.session.commit()

        flash('注册成功！即将跳转到登录页面...', 'success')  # 显示成功消息
        return render_template('register_success.html')  # 跳转到注册成功页面
    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.index'))  # 如果用户已登录，跳转到主界面

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登录成功！', 'success')  # 显示成功消息
            return redirect(url_for('main_routes.index'))  # 登录成功后跳转到主界面
        flash('用户名或密码错误。', 'error')
    return render_template('login.html', form=form)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_routes.index'))

@main_routes.route('/rate/<int:location_id>', methods=['GET', 'POST'])
@login_required
def rate(location_id):
    location = Location.query.get_or_404(location_id)
    rating = Rating.query.filter_by(user_id=current_user.id, location_id=location.id).first()
    form = RateForm()
    if form.validate_on_submit():
        if rating:
            if not rating.has_modified:  # 如果未修改过评分
                rating.score = form.score.data
                rating.has_modified = True  # 标记为已修改
                db.session.commit()
                flash('评分修改成功！', 'success')
            else:
                flash('您已经修改过评分，无法再次修改。', 'error')
        else:
            new_rating = Rating(user_id=current_user.id, location_id=location.id, score=form.score.data)
            db.session.add(new_rating)
            location.num_ratings += 1  # 更新参与打分的用户数量
            db.session.commit()
            flash('评分提交成功！', 'success')
        return redirect(url_for('main_routes.index'))

    return render_template('rate.html', location=location, form=form)

@main_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        # 处理头像上传
        avatar_file = form.avatar.data
        if avatar_file:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  # 使用 current_app
            avatar_file.save(avatar_path)

            # 更新用户头像路径
            current_user.avatar = filename
            db.session.commit()

            flash('头像上传成功！', 'success')
            return redirect(url_for('main_routes.profile'))

    return render_template('profile.html', user=current_user, form=form)

