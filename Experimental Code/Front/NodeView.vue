<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 节点查看
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container"  >
            <div v-if="userinfo == 'admin'">
            <el-table :data="NodeData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                <el-table-column prop="nodeid" label="编号" width="65" align="center"></el-table-column>
                <el-table-column prop="nodename" label="节点名" width="160" align="center"></el-table-column>
                <el-table-column prop="nodeip" label="节点IP" width="160" align="center"></el-table-column>
                <el-table-column prop="nodetype" label="节点类型" width="150" align="center"></el-table-column>
                <el-table-column prop="nodestate" label="状态" width="155" align="center"></el-table-column>
                <el-table-column prop="nodenote" label="备注" width="275" align="center"></el-table-column>
            </el-table>
            </div>

            <template v-if="userinfo == 'user'">
                <div class="error-page">
                    <div class="error-code">4<span>0</span>3</div>
                    <div class="error-desc">你没有权限访问该页面</div>
                    <div class="error-handle">
                        <router-link to="/">
                            <el-button type="primary" size="large">返回首页</el-button>
                        </router-link>
                        <el-button class="error-btn" type="primary" size="large" @click="goBack">返回上一页</el-button>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<script>

import { getNodeState} from "../api/index";

export default {
    name: "basetable",
    
    data:function() {
        return {
            NodeData:[],
        }
    },
    methods() {

    },
    created() {
        this.userinfo = localStorage.getItem('ms_userinfo');
        getNodeState().then(res => {
            if (res.get_result == 'true') {
                this.NodeData = res.nodelist;
            } else {
                this.$message.error('加载失败');
            }
        });
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
.error-page {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background: #f3f3f3;
    box-sizing: border-box;
}
.error-code {
    line-height: 1;
    font-size: 250px;
    font-weight: bolder;
    color: #f02d2d;
}
.error-code span {
    color: #f02d2d;
}
.error-desc {
    font-size: 30px;
    color: #777;
}
.error-handle {
    margin-top: 30px;
    padding-bottom: 200px;
}
.error-btn {
    margin-left: 100px;
}
</style>
