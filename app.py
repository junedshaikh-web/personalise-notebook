from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import io
import csv
from os import name
import openpyxl

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///excelcrud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class College(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    rollno = db.Column(db.Integer,unique=True)
    std=db.Column(db.String(10))
    course = db.Column(db.String(20))


    def __init__(self,name,rollno,std,course):
        self.name = name
        self.rollno = rollno
        self.std = std
        self.course  = course


class PostSchema(ma.Schema):
    class Meta:
        fields = ("name","rollno","std","course")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


with app.app_context():
    db.create_all()
    dbRollno = College.query.with_entities(College.rollno).all()


existing=[]
for x in dbRollno:
    lst = list(x)
    existing+=lst

@app.route('/csvupload',methods=['POST'])
def csvupload():
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            data = uploaded_file.stream.read()
            stream = io.StringIO(data.decode("UTF8"),newline=None)
            reader = csv.reader(stream)
            i = 0
            for row in reader:
                i+=1
                if i == 1:
                    continue
                else:
                    if int(row[1]) in existing:
                        name = row[0]
                        std = row[2]
                        course = row[3]
                        col = College.query.filter_by(rollno=row[1]).first()
                        if col.name != name or col.std != std or col.course != course:
                            col.name = name
                            col.std = std
                            col.course = course
                            db.session.add(col)
                        else:
                            continue
                    else:
                        my_posts=College(*row)
                        db.session.add(my_posts)
                    db.session.commit()

            return jsonify({"message":"csv file uploaded successfully"})

@app.route('/excelupload',methods=['POST'])
def excelupload():
    if request.method=='POST':
        if request.files:
            uploaded_file = request.files['filename']
            wb_obj=openpyxl.load_workbook(uploaded_file)
            sheet = wb_obj.active
            l = 0
            for row in sheet.values:
                l+=1
                if l == 1:
                    continue
                else:
                    if int(row[1]) in existing:
                        name = row[0]
                        std= row[2]
                        course = row[3]
                        col = College.query.filter_by(rollno=row[1]).first()
                        if col.name!=name or col.std!=std or col.course!=course:
                            col.name = name
                            col.std=std
                            col.course=course
                            db.session.add(col)
                    else:
                        my_posts=College(*row)
                        db.session.add(my_posts)
                    db.session.commit()
            return jsonify({"message":"excel file uploaded successfully"})

@app.route('/get',methods=['GET'])
def get_post():
    details=College.query.all()
    result = posts_schema.dump(details)
    return jsonify(result)

@app.route('/get_details/<id>/', methods=['GET'])
def post_details(id):
    post=College.query.get(id)
    return post_schema.jsonify(post)

@app.route('/update_post/<id>/', methods=['PUT'])
def update_post(id):
    post=College.query.get(id)

    name=request.json['name']
    std=request.json['std']
    course=request.json['course']

    post.name=name
    post.std=std
    post.course=course

    db.session.commit()
    return post_schema.jsonify(post)

@app.route('/delete_post/<id>/', methods=['DELETE'])
def delete_post(id):
    post=College.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)

if __name__=="__main__":
    app.run(debug=True)