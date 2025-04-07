import datetime
from flask import Flask, request
from flask.views import MethodView
from extension import db
from models import Vegetable,Vegetable_2
from flask_cors import CORS

app = Flask(__name__)
CORS().init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Rguan1976@localhost:3306/vegetable?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# 在应用上下文中创建所有表
def create_tables():
    with app.app_context():
        db.create_all()

# 初始化蔬菜数据
def init_vegetables():
    with app.app_context():
        db.session.query(Vegetable).delete(synchronize_session='fetch')
        db.session.query(Vegetable_2).delete(synchronize_session='fetch')
        vegetable_stock = [
            Vegetable_2(id=1, vegetable_name='西红柿', vegetable_sold=0, vegetable_inventory=100),
            Vegetable_2(id=2, vegetable_name='土豆', vegetable_sold=0, vegetable_inventory=100),
        ]
        db.session.add_all(vegetable_stock)
        vegetable_massage=[]
        db.session.add_all(vegetable_massage)
        db.session.commit()


@app.route('/')
def hello_world():
    return 'Hello World'


class VegetableAPI(MethodView):
    def get(self,vegetable_id):
        if not vegetable_id:
            vegetable_s:[Vegetable] = Vegetable.query.all()
            results=[
                {
                    'id':vegetable.id,
                    'time':vegetable.time,
                    'vegetable_name':vegetable.vegetable_name,
                    'vegetable_sold':vegetable.vegetable_sold,
                    'vegetable_inventory':vegetable.vegetable_inventory,
                    'vegetable_price':vegetable.vegetable_price,

                }for vegetable in vegetable_s
            ]
            return {
                 'status':'success',
                 'message':'数据查询成功',
                 'result':results
            }
        vegetable:Vegetable=Vegetable.query.get(vegetable_id)
        return{
            'status':'success',
            'message':'数据查询成功',
            'result':{
                'id':vegetable.id,
                    'time':vegetable.time,
                    'vegetable_name':vegetable.vegetable_name,
                    'vegetable_sold':vegetable.vegetable_sold,
                    'vegetable_inventory':vegetable.vegetable_inventory,
                    'vegetable_price':vegetable.vegetable_price,
            }
        }
    
    def post(self):
        form = request.json
        vegetable=Vegetable()
        vegetable_2 = Vegetable_2.query.filter_by(vegetable_name=form.get('vegetable_name')).first()
        vegetable_2.vegetable_inventory=vegetable_2.vegetable_inventory-int(form.get('vegetable_sold'))
        vegetable_2.vegetable_sold=vegetable_2.vegetable_sold+int(form.get('vegetable_sold'))
        
        vegetable.time=datetime.datetime.now()
        vegetable.vegetable_name=form.get('vegetable_name')
        vegetable.vegetable_sold=form.get('vegetable_sold')
        vegetable.vegetable_inventory=vegetable_2.vegetable_inventory
        vegetable.vegetable_price=form.get('vegetable_price')
        db.session.add(vegetable)
        db.session.commit()
        return{
            'status':'success',
            'message':'数据添加成功'
        }

    def delete(self,vegetable_id):
        vegetable:Vegetable=Vegetable.query.get(vegetable_id)
        vegetable_2 = Vegetable_2.query.filter_by(vegetable_name=vegetable.vegetable_name).first()
        vegetable_2.vegetable_inventory=vegetable_2.vegetable_inventory+vegetable.vegetable_sold
        vegetable_2.vegetable_sold=vegetable_2.vegetable_sold-vegetable.vegetable_sold
        vegetable=Vegetable.query.get(vegetable_id)
        db.session.delete(vegetable)
        db.session.commit()
        return{
            'status':'success',
            'message':'数据删除成功'
        }


    def put(self, vegetable_id):
        vegetable:Vegetable=Vegetable.query.get(vegetable_id)
     
        vegetable_2 = Vegetable_2.query.filter_by(vegetable_name=vegetable.vegetable_name).first()
        vegetable_2.vegetable_inventory=vegetable_2.vegetable_inventory+int(vegetable.vegetable_sold)
        vegetable_2.vegetable_sold=vegetable_2.vegetable_sold-int(vegetable.vegetable_sold)

        vegetable.time = datetime.datetime.now()
        vegetable.vegetable_name=request.json.get('vegetable_name')
        vegetable.vegetable_sold=request.json.get('vegetable_sold')
        vegetable.vegetable_price=request.json.get('vegetable_price')

        vegetable_2.vegetable_inventory=vegetable_2.vegetable_inventory-int(request.json.get('vegetable_sold'))
        vegetable_2.vegetable_sold=vegetable_2.vegetable_sold+int(request.json.get('vegetable_sold'))

        vegetable.vegetable_inventory=vegetable_2.vegetable_inventory

        db.session.commit()
        
        return{
            'status':'success',
            'message':'数据修改成功'
        }


class VegetableStockAPI(MethodView):
    def get(self,vegetable_id):
        if not vegetable_id:
            vegetable_s:[Vegetable_2] = Vegetable_2.query.all()
            results=[
                {
                    'id':vegetable_2.id,
                    'vegetable_name':vegetable_2.vegetable_name,
                    'vegetable_sold':vegetable_2.vegetable_sold,
                    'vegetable_inventory':vegetable_2.vegetable_inventory,
            }for vegetable_2 in vegetable_s
            ]
            return {
                 'status':'success',
                 'message':'数据查询成功',
                 'result':results
            }
        vegetable_2:Vegetable_2=Vegetable_2.query.get(vegetable_id)
        return{
            'status':'success',
            'message':'数据查询成功',
            'result':{
                'id':vegetable_2.id,
                'vegetable_name':vegetable_2.vegetable_name,
                'vegetable_sold':vegetable_2.vegetable_sold,
                'vegetable_inventory':vegetable_2.vegetable_inventory,
            }
        }
    
    def put(self,vegetable_id):
        vegetable_2:Vegetable_2=Vegetable_2.query.get(vegetable_id)
        vegetable_2.vegetable_inventory=request.json.get('vegetable_inventory')
        db.session.commit()
        
        return{
            'status':'success',
            'message':'数据修改成功'
        }



vegetable_view=VegetableAPI.as_view('vegetable_api')
app.add_url_rule('/vegetable/',defaults={'vegetable_id':None},
                 view_func=vegetable_view,methods=['GET',])
app.add_url_rule('/vegetable_s',view_func=vegetable_view,methods=['POST',])
app.add_url_rule('/vegetable/<int:vegetable_id>',view_func=vegetable_view
                 ,methods=['GET','PUT','DELETE',])


vegetable_stock_view=VegetableStockAPI.as_view('vegetable_stock_api')
app.add_url_rule('/vegetable_stock/',defaults={'vegetable_id':None},
                 view_func=vegetable_stock_view,methods=['GET',])
app.add_url_rule('/vegetable_stock/<int:vegetable_id>',
                 view_func=vegetable_stock_view,methods=['PUT','GET',])


if __name__ == '__main__':
    # create_tables()  # 创建表
    init_vegetables()  # 初始化数据
    app.run()