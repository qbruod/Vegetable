<!-- 
<template>
  <div class="container">
    <div class="shadow-sm p-2 mb-5 bg-body-tertiary rounded">
      <p class="fs-1 fw-bolder" >蔬菜数量查询</p>
    </div>
    <div class="float-end">
      <p class="fs-3 fw-bold" style="color: rgb(11, 94, 215); margin: 0px;">今日售出</p>
    </div>
    <div class="float-end">
        <p class="fs-3 fw-bold" style="color: rgb(11, 94, 215);">库存&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
    </div>
    <br>
    <br>
    <br>
     使用v-for循环渲染多个Product组件，将商品数据作为props传递 
    <Vegetable_Stock 
      v-for="(Vegetable_Stock, index) in Vegetable_Stock"
      :key="index"
      :Sold="Vegetable_Stock.Sold"
      :Inventory="Vegetable_Stock.Inventory"
      :Vegetable_Name="Vegetable_Stock.Vegetable_Name"
    />
    <div class="d-grid gap-2 col-6 mx-auto">
      <a class="btn btn-primary btn-lg" href="#" role="button">刷新</a>
    </div>
  </div>
</template>

<script>
import Vegetable_Stock from './components/Vegetable_Stock.vue'

export default {
  name: 'App',
  components: {
    Vegetable_Stock
  },
  data(){
    return {
      Vegetable_Stock:[
        {
          Sold:'10',Inventory:'10',Vegetable_Name:'西红柿',
        },
        {
          Sold:'10',Inventory:'15',Vegetable_Name:'土豆',
        }
      ]
  }
}
}
</script>
 -->
<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg  bg-primary" data-bs-theme="dark" >
      <div class="container-fluid">

        <router-link to="/">
          <a class="navbar-brand" >&#128526;&#128526;&#128526;</a>
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/">
                <a class="nav-link active" aria-current="page" href="#/" style={text-decoration:none}>&emsp;蔬菜信息管理🥬&emsp;</a>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/vegetableStock">
                <a class="nav-link active" aria-current="page" href="#/">&emsp;库存管理📦&emsp;</a>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/vegetableAgent">
                <a class="nav-link active" aria-current="page" href="#/">&emsp;智能体分析🤔&emsp;</a>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>