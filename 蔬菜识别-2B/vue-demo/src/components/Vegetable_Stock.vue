<!-- <template>
    <div class="item">
        <div class="float-end">
            <p class="fs-4 fw-bold"><span v-text="Sold"></span></p>
        </div>
        <div class="float-end">
            <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </p>
        </div>
        <div class="float-end">
            <p class="fs-4 fw-bold"><span v-text="Inventory"></span></p>
        </div>
        <p class="fs-4"><span v-text="Vegetable_Name"></span></p>
            <div class="progress" role="progressbar" aria-label="Animated striped example" :aria-valuenow="percentageValue" aria-valuemin="0" aria-valuemax="100">
                <div class="progress-bar progress-bar-striped progress-bar-animated" :style="{ width: percentage + '%' }">{{ percentage + '%' }}</div>
            </div>
        <br>
        <br>
    </div>
</template>
<script>
export default{
    names:"Vegetable_Stock",
    props:
    {
        Sold:String,
        Inventory:String,
        Vegetable_Name:String,
    },
    computed: {
        // 计算进度百分比，同时处理分母为0的情况
        percentage() {
            const sold = parseFloat(this.Sold);
            const inventory = parseFloat(this.Inventory);

            // 防止除以零错误
            if (inventory === 0||(sold / inventory)>1) {
                return '数据错误'; // 或者返回其他提示信息，表示无法计算
            }

            // 计算百分比
            return ((sold / inventory) * 100).toFixed(0); // toFixed用于保留小数点后两位
        },
        percentageValue() {
            // 用于aria-valuenow，确保返回一个有效的数字或处理特殊情形
            const percent = parseFloat(this.percentage);
            return isNaN(percent) ? 0 : percent;
        },
    },
};
</script> -->