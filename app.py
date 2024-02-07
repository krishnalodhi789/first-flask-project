from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Create Database , name is todo
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
db = SQLAlchemy(app)


# Create table 'todo_data' in todo database 
class Todo_Data(db.Model):
	s_no = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	description = db.Column(db.String(500),nullable=False)
	date_time = db.Column(db.DateTime,default=datetime.datetime.now)

	def __repr__(self):
		return f'{self.s_no} -> {self.title}'

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		title = request.form.get('title')
		description = request.form.get('description') 
		todo_data =  Todo_Data(title=title, description=description)
		db.session.add(todo_data)
		db.session.commit()
		print(todo_data.s_no)
		return redirect('/')
	todo_list = Todo_Data.query.order_by(Todo_Data.s_no.desc()).all()
	print(todo_list)
	return render_template('index.html', todo_list=todo_list)



@app.route("/todo/delete/<int:id>/")
def todo_delete(id):
	todo = Todo_Data.query.filter_by(s_no=id).first()
	# todo = db.get_or_404(Todo_Data, id)
	db.session.delete(todo)
	db.session.commit()
	return redirect('/')


@app.route("/todo/update/<int:id>/", methods=["get", "post"])
def todo_update(id):
	todo = Todo_Data.query.get(id) 

	if request.method == "POST":
		title = request.form.get('title')
		description = request.form.get('description')
		print(title)
		todo.title =title
		todo.description =description
		todo.date_time = datetime.datetime.now()
		db.session.commit()
		return redirect('/') 
	return render_template('update_todo.html', todo=todo)



with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run(debug=True)
