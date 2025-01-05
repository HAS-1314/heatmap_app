import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 密钥配置（用于加密会话等）
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用SQLAlchemy事件系统，节省资源

    # Flask-Login配置
    LOGIN_DISABLED = False  # 是否禁用登录功能（用于测试）

    # 邮件服务器配置（可选，用于发送通知邮件）
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 分页配置
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE') or 10)

    # 文件上传配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)  # 16MB

    # 调试模式配置
    DEBUG = os.environ.get('DEBUG') or False

    # 其他自定义配置
    APP_NAME = os.environ.get('APP_NAME') or 'Heatmap App'

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'dev.db')


class TestingConfig(Config):
    # 测试环境配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'test.db')
    WTF_CSRF_ENABLED = False  # 禁用CSRF保护，方便测试


class ProductionConfig(Config):
    # 生产环境配置
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'prod.db')


# 配置字典，方便根据环境选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}