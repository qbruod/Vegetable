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