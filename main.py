
from utils.LogHandler import LogHandler
from models.user import User
from Config import app, db
from flask import request
from utils.restful_utils import success
from flask_cors import cross_origin

@app.route('/api/user/list', methods=['GET'])
@cross_origin()
def get_user_list():
    page_size=int(request.args.get('pageSize','10'))
    page_number=int(request.args.get('pageNumber','1'))
    users=User.query.paginate(page=page_number,per_page=page_size)
    return success(message='OK',data={
        "total":users.total,
        "pageNumber":page_number,
        "pageSize":page_size,
        "data":users.items
    })


@app.route('/api/user', methods=['PUT'])
@cross_origin()
def add_user():
    data=request.get_json(force=True)
    user=User(name=data['name'],gender=data['gender'])

    db.session.add(user)
    db.session.commit()

    return success()


@app.route('/api/user/<int:id>', methods=['POST'])
@cross_origin()
def edit_user(id):
    data=request.get_json()
    User.query.filter_by(id=id).update({
        "name":data['name'],
        "gender":data['gender']
    })
    db.session.commit()
    return success()


if __name__ == '__main__':
    app.logger.addHandler(LogHandler.getLog())
    app.run(port=9000)


