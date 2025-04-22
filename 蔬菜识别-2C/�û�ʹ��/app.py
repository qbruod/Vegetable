# ***************************************导入的包****************************************
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from test_img_recognition import predict,classify_images,result_classes
app = Flask(__name__)
CORS(app)

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from extension import db
from models import Vegetable,Vegetable_2
import datetime
import random
# **************************************图像识别的结果：***********************************
chinese_predicted_classes = result_classes()
# *********************************数据库连接参数整合为字典**********************************

# 替换为你的MySQL数据库信息
username = 'Userdb'
password = 'rootpop'
host = '39.106.144.42'  # 例如：'localhost' 或 '127.0.0.1'
port = '3306'  # 通常是 3306
database = 'userdb'
# 创建连接引擎
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
# 创建会话

Session = sessionmaker(bind=engine)
session = Session()
# **************************************连接数据库******************************************
result = []  # 初始化结果列表
# 确保predicted_classes_result中的每个元素都是字符串
chinese_predicted_classes = [str(category) for category in chinese_predicted_classes]

# 遍历数据库查询到的Vegetable记录
messages = session.query(Vegetable_2).all()
for i in range(len(chinese_predicted_classes)):
    for message in messages:
        # 检查当前记录的vegetable_name是否在predicted_classes_result中
        if chinese_predicted_classes[i] in message.vegetable_name :
            # 如果匹配，则将该记录的信息作为一个元组添加到result列表中
            # 这里不会去除重复，即使同一个商品信息因匹配多次predicted_classes_result中的类别也会被多次添加
            # print(message.vegetable_name, message.vegetable_sold, message.vegetable_inventory)
            result.append((message.vegetable_name, message.vegetable_sold, message.vegetable_inventory))

result = tuple(result)
# *************************************以上查询数据库操作**********************************
cart_data = []
# 创建一个购物车链表，方便往前端传数据
# 用于追踪每种商品已分配的数量
allocated_quantities = {}
vegetable_prices = {'西红柿': 2.50, '土豆': 3.0}
# # **************************************遍历查询结果*************************************

for vegetable_name,vegetable_sold,vegetable_inventory in result:
    # 获取当前商品的分配值
    vegetable_prices = {'西红柿': 2.50, '土豆': 3.0}
    allocated_quantity_for_item = allocated_quantities.get(vegetable_name, 0)
    remaining_inventory = vegetable_inventory - allocated_quantity_for_item

    if remaining_inventory > 0:
        # 生成一个在1到库存量之间的随机分配数量
        allocated_quantity = random.randint(1, remaining_inventory)
        print(f"随机生成的数量为：{allocated_quantity}")
        allocated_quantities[vegetable_name] = allocated_quantity
        print(f'商品已分配数量：{allocated_quantity}')

        vegetable_price = vegetable_prices.get(vegetable_name, 0)
        subtotal = allocated_quantity * vegetable_price
        print(vegetable_price)
        # 更新数据库中的vegetable_sold和vegetable_inventory（如果需要的话，通常不直接在原数据上加减）
        # 注意：实际操作中，更新库存和销量可能需要更复杂的逻辑来确保数据一致性
        # 下面是示例逻辑，但请注意这只是一个简化示例，并未直接反映到原result中
        
        message2 = Vegetable(vegetable_name=vegetable_name,vegetable_sold=allocated_quantity,
                             vegetable_inventory=remaining_inventory - allocated_quantity,vegetable_price = vegetable_price)
        session.add(message2)
        update_statement = (
            update(Vegetable_2)
            .where(vegetable_name == Vegetable_2.vegetable_name)
            .values(
                vegetable_inventory=Vegetable_2.vegetable_inventory - allocated_quantity,
                vegetable_sold = allocated_quantity,
            )
        )
        session.execute(update_statement)
        # 提交事务
        session.commit()
        print('123')
        cart_data.append({
            # 'img_url': '...',  # 应该是具体的图片URL
            'name': vegetable_name,
            'price': vegetable_price,  # 应该是从元组或数据库获取的实际价格
            'quantity': allocated_quantity,
            'subtotal':subtotal,  # 应该是计算出的子总价
        })
    else:
        print(f"No more {vegetable_name} available for allocation.")

print(cart_data)


# ****************************************方便传输前端***************************************
@app.route('/cart', methods = ['GET'])
def get_cart():

    return jsonify(cart_data)
    
if __name__ == '__main__':
    app.run(port=5555)
