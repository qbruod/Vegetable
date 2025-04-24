<!-- :header-cell-style="{background:'lightgreen'}" 头行背景颜色 -->
<template>
    <div class="buy" style="margin-top: 12px;left: 0;">
        <el-table :data="tableData"
            
            stripe style="width: 100%"
            height="auto"
            type="index"
            @selection-change="handleSelectionChange"
            ref="multipleTable">
          <el-table-column type="selection" width="55" ></el-table-column>
          <el-table-column label="图片">
            <template v-slot:default="slotProps"> 
              <img :src="`/pic/${slotProps.row.name}.jpg`" alt="产品图片" style="width: 50px; height: 50px;"> 
            </template> 
          </el-table-column>
          <el-table-column prop="name" label="名称"></el-table-column>
          <el-table-column prop="price" label="价格"></el-table-column>
          <el-table-column prop="quantity" label="数量"></el-table-column>
          <el-table-column prop="subtotal" label="小计" :footer-method="getSummaries"></el-table-column>
        </el-table>
        <div class="total-section">
            <p>
              <img  src="../assets/shopping-bag.png" alt="">
              总价为：{{ totalSubtotal }}￥</p>
            <button  class="pay-button" @click="handlePayClick" >确认支付</button>
        </div>
    </div>
</template>
<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 居中对齐，可根据需要调整 */
}
/* 修改表格背景为透明 */
.el-table {
  background-color: transparent;
}

/* 如果需要，也可以移除单元格之间的边框以达到更好的透明效果 */
.el-table td,
.el-table th {
  border: none;
}
/* 为el-table添加样式以设置行间间隙和圆角 */
.el-table .el-table__body tr {
  margin-bottom: 20px;
}

/* 为每一行添加圆角 */
.el-table .el-table__body tr td,
.el-table .el-table__body tr th {
  border-radius: 15px;
}

/* 由于默认情况下单元格之间有边框，我们需要移除这些边框以使圆角效果明显 */
.el-table .el-table__body tr td,
.el-table .el-table__body tr th {
  border-top: none;
  border-left: none;
  border-right: none;
}

/* 为了保持表头和表尾的样式一致性，可能也需要调整表头和表尾的样式 */
.el-table .el-table__header tr th,
.el-table .el-table__footer tr td {
  /* 如果需要也可以为表头和表尾添加圆角 */
  border-radius: 15px;
  margin-bottom: 20px;
}
.total-section {
  display: flex; /* 使用Flex布局 */
  align-items: center; /* 垂直居中对齐 */
}
.total-section img {
  height: 40px; /* 调整图片大小 */
  width: auto; /* 保持图片宽高比 */
  margin-right: 10px; /* 在图片和文本间添加间距 */
}
.total-section p{
  flex: 1; /* 让文本区域占据剩余空间 */
}

.pay-button {
  background-color: #aef6b1; /* 绿色背景 */
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px; /* 圆角 */
  transition: background-color 0.3s; /* 过渡效果 */
}
.pay-button:hover {
  background-color: #27ae30; /* 鼠标悬停时颜色变深 */
}
</style>
<script>
import axios from 'axios';
export default {
    name: 'Buy',
    data() {
    return {
      tableData: [
        // 你的数据列表
      ],
      selectedRows: [], // 用于存储勾选的行
      totalSubtotal: 0, // 存储勾选行的总价
    };
  },
  methods: {
    handleSelectionChange(selection) {
      // 处理勾选变化
      this.selectedRows = selection;
      // 计算总价
      this.totalSubtotal = this.selectedRows.reduce((sum, row) => sum + row.subtotal, 0);
    },
    handlePayClick() {
      alert('确认支付功能即将实现'); // 实际应用中，这里可以替换为调用支付接口、打开支付页面等逻辑
      // 示例：模拟支付过程并关闭对话框
        this.$confirm('确定要支付吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
         this.$message({
           type: 'success',
           message: '支付成功!'
         });
       }).catch(() => {
         this.$message({
           type: 'info',
           message: '已取消支付'
         });          
       });
    },
    getSummaries(param) {
      // 你的汇总方法，如果需要处理总价，也可以在这里加入逻辑，但通常这个方法用于表格底部的汇总行
      // 例如，你可以在此处直接返回总和，但总价通常直接通过上面的handleSelectionChange计算
      const { columns } = param;
      const sums = [];
      columns.forEach((column, index) => {
        if (index === columns.length - 1) { // 假设小计列是最后一列
          sums[index] = '总价: ' + this.totalSubtotal; // 这里展示总价，但通常不推荐这样做，因为它不是纯粹的汇总逻辑
        } else {
          sums[index] = null;
        }
      });
      return sums;
    },
  },
    async mounted() {
        try {
            const response = await axios.get('http://localhost:5555//cart');
            this.tableData = response.data; 
            console.log(this.tableData)
        } catch (error) {
            console.error('Failed to fetch cart data', error);
            // 可以在此处处理错误情况，比如给用户提示
        }
    }
};
</script>


