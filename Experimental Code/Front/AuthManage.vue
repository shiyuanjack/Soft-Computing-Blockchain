<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 权限管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container"  >
            <el-table :data="tableData" border class="table"  ref="multipleTable"  v-if="userinfo == 'admin'" header-cell-class-name="table-header">
                <el-table-column prop="uid" label="用户ID" width="100" align="center"></el-table-column>
                <el-table-column prop="name" label="用户名" width="100" align="center"></el-table-column>
                <el-table-column prop="email" label="邮箱" width="180" align="center"></el-table-column>
                <el-table-column prop="phone" label="联系方式" width="110" align="center"></el-table-column>
                <el-table-column prop="publickKey" label="公钥" :show-overflow-tooltip="true" width="520" align="center"></el-table-column>
                <el-table-column prop="permit" label="权限" width="50" align="center"></el-table-column>
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <el-button type="text" icon="el-icon-edit-outline" @click="handleEdit(scope.$index, scope.row)">修改权限
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog title="修改权限" v-model="editVisible" width="50%">
                <el-form label-width="70px">
                    <el-form-item label="选择权限">
                        <el-radio-group v-model="userpermit">
                            <el-radio label="读写"></el-radio>
                            <el-radio label="只读"></el-radio>
                            <el-radio label="只写"></el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="editVisible = false">取 消</el-button>
                        <el-button type="primary" @click="saveEdit">确 定</el-button>
                    </span>
                </template>
            </el-dialog>
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

import { ref } from "vue";
import { getUserInfo , changeUserPermit} from "../api/index";
import { useRouter } from "vue-router";

export default {
    data:function() {
        return {
            tableData:[],
            editVisible:ref(false),
            userinfo:"",
            userpermit:"",
            username:"",
            changeIndex:0,
        }
    },
    methods:{
        getUserList(){
            if(this.userinfo == "admin"){
                getUserInfo().then(res => {
                    if (res.get_result == 'true') {
                        this.$message.success('加载成功');
                        this.tableData = res.list;
                    } else {
                        this.$message.error('加载失败');
                    }
                });
            }else{

            }
        },
        goBack() {
           this.$router.go(-1)
        },
        handleEdit(index, row){
            this.userpermit = row.permit;
            this.editVisible = true;
            this.username = row.name;
            this.changeIndex = index;
        },
        saveEdit(){
            const search_payload ={
                name:"",
                permit:"",
            };
            search_payload.name = this.username;
            search_payload.permit = this.userpermit
            changeUserPermit(search_payload).then(res =>{
                if (res.change_result == 'true') {
                    this.$message.success('修改成功');
                    this.tableData[this.changeIndex].permit = this.userpermit;
                } else {
                    this.$message.error('修改失败');
                }
            });
            this.editVisible = false;
        }
    },
    created() {
        this.userinfo = localStorage.getItem('ms_userinfo');
        this.getUserList();
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
