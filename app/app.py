from flask_jwt_extended import JWTManager
from app.resources.tweets import (
    Tweets,
    TweetSearch,
    AuthorSearch,
    DateSearch,
    LocationSearch,
    SourceSearch,
)
from app.resources.admin import (
    AdminLogin,
    AdminDashboard,
    AdminAnalysis,
    AdminManage,
    AdminRemove,
    AdminSettings,
)
from app.messages import response_errors as Err
from app.setup.settings import TwitterSettings
from app.models.admin import AdminModel
from app.helpers.utils import hash
from app.setup.app_config import create_app

app, api, jwt = create_app()

# Creates default admins and insert in db
for admin in TwitterSettings.get_instance().super_admins:
    admin = AdminModel(admin["email"], admin["username"], hash(admin["password"]))
    admin.insert()

# Error handlers
@app.errorhandler(404)  # Handling HTTP 404 NOT FOUND
def page_not_found(e):
    return Err.ERROR_NOT_FOUND


# API Routes
api.add_resource(Tweets, "/api/tweets")
api.add_resource(TweetSearch, "/api/tweets/tweet")
api.add_resource(SourceSearch, "/api/tweets/source")
api.add_resource(AuthorSearch, "/api/tweets/author")
api.add_resource(DateSearch, "/api/tweets/date")
api.add_resource(LocationSearch, "/api/tweets/location")

api.add_resource(AdminLogin, "/fortauth")
api.add_resource(AdminDashboard, "/admin/dashboard")
api.add_resource(AdminAnalysis, "/admin/analysis")
api.add_resource(AdminManage, "/admin/admins", "/admin/add")
api.add_resource(AdminRemove, "/admin/remove/<int:id>")
api.add_resource(AdminSettings, "/admin/settings")

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
