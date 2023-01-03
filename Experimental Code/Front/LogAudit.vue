<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 日志审计
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box" v-if="userpermit == '0' || userpermit == '1'" > 
                <el-form ref="formRef" :rules="rules" :model="search_form" :inline="true" >
                    <el-form-item label="开始时间" prop="date1">
                        <el-date-picker type="date" placeholder="选择日期" v-model="search_form.date1" value-format="YYYY-MM-DD" style="width: 150px;" ></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="date2">
                        <el-time-picker placeholder="选择时间" v-model="search_form.date2" value-format="HH:mm:ss" style="width: 150px;"></el-time-picker>
                    </el-form-item>

                    <el-form-item label="结束时间"  prop="date3">
                        <el-date-picker type="date" placeholder="选择日期" v-model="search_form.date3" value-format="YYYY-MM-DD" style="width: 150px;"></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="date4">
                        <el-time-picker placeholder="选择时间" v-model="search_form.date4" value-format="HH:mm:ss" style="width: 150px;"></el-time-picker>
                    </el-form-item> 
                    <el-form-item >
                        <el-button type="primary" icon="el-icon-search"  @click="onSubmit" >搜索</el-button>
                    </el-form-item>
                </el-form>
            </div>
        <el-table :data="tableData"  v-if="userpermit == '0' || userpermit == '1'" border class="table" ref="multipleTable" header-cell-class-name="table-header">
            <el-table-column prop="num" label="编号" width="55" align="center"></el-table-column>
            <el-table-column prop="height" label="块高" width="55" align="center"></el-table-column>
            <el-table-column prop="log_timestamp" label="日志时间" width="155" align="center"></el-table-column>
            <el-table-column prop="pubkey"  :show-overflow-tooltip="true" label="用户公钥" align="center"></el-table-column>
            <el-table-column prop="ipfs" label="IPFS文件地址" width="275" align="center"></el-table-column>
            <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                    <el-button type="text" icon="el-icon-download" @click="onDownload(scope.$index, scope.row)">下载
                    </el-button>
                    <el-button type="text" icon="el-icon-reading" @click="handleEdit(scope.$index, scope.row)">查看
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <template v-if="userpermit == '2'">
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
        <el-dialog title="数据信息" v-model="editVisible" width="50%">
            <el-form label-width="70px" :model="search_info">
                <el-form-item label="时间戳">
                    <el-input v-model="search_info.logtime"></el-input>
                </el-form-item>
                <el-form-item label="用户公钥">
                    <el-input type="textarea" v-model="search_info.publickey"></el-input>
                </el-form-item>
                <el-form-item label="签名">
                    <el-input type="textarea" v-model="search_info.signature"></el-input>
                </el-form-item>
                <el-form-item label="加密数据">
                    <el-input type="textarea" v-model="search_info.encrypted_data"></el-input>
                </el-form-item>
                <el-form-item label="明文">
                    <el-input type="textarea" v-model="search_info.decrypted_data"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveEdit">确 定</el-button>
                </span>
            </template>
        </el-dialog>
        
    </div>
</template>

<script>

import { ref } from "vue";
import { searchLog , getIPFSLog , download_file,searchLogAdmin} from "../api/index";
import { useRouter } from "vue-router";
export default {
    data:function() {
        return{
            tableData:[],
            editVisible:ref(false),
            search_form: {
                starttime:"",
                endtime:"",
                name:"",
                date1:"",
                date2:"",
                date3:"",
                date4:"",
            },
            rules: {
                date1:  [{ required: true, message: '请选择日期', trigger: 'blur' }],
                date2:  [{ required: true, message: '请选择时间', trigger: 'blur' }],
                date3:  [{ required: true, message: '请选择日期', trigger: 'blur' }],
                date4:  [{ required: true, message: '请选择时间', trigger: 'blur' }],
            },
            search_info:{
                logtime:"",
                publickey:"",
                signature:"",
                encrypted_data:"",
                decrypted_data:""
            }
        };
    },
    methods:{
        onSubmit() {
            this.$message.success('正在搜索...');
            this.$refs.formRef.validate(async (valid) =>{
                if (valid) {
                    this.search_form.name = localStorage.getItem('ms_username');
                    this.search_form.starttime = this.search_form.date1 + " " + this.search_form.date2;
                    this.search_form.endtime = this.search_form.date3 + " " + this.search_form.date4;
                    if(this.userinfo == 'user'){
                        searchLog(this.search_form).then(res => {
                            if (res.search_result == 'true') {
                                this.$message.success('搜索成功');
                                if(res.search_response_bc.search_result == 'true'){
                                    this.tableData = res.search_response_bc.txs;
                                }
                            } else {
                                this.$message.error('搜索失败');
                            }
                        });
                    }else if(this.userinfo == 'admin'){
                        searchLogAdmin(this.search_form).then(res => {
                            if (res.search_result == 'true') {
                                this.$message.success('搜索成功');
                                if(res.search_response_bc.search_result == 'true'){
                                    this.tableData = res.search_response_bc.txs;
                                }
                            } else {
                                this.$message.error('搜索失败');
                            }
                        });
                    }
                    
                } else {
                    this.$message.error('请填写必要数据');
                    return false;
                }
            });
        },
        goBack() {
           this.$router.go(-1)
        },
        handleEdit(index, row){
            this.$message.success('正在加载和解密...');
            const search_payload ={
                ipfs:"",
                pk:"",
            };
            search_payload.ipfs = row.ipfs;
            search_payload.pk = this.tableData[index].pubkey;
            getIPFSLog(search_payload).then(res =>{
                this.search_info = res;
                this.editVisible = true;
            });
        },
        async onDownload(index,row){
            const requ_data = {
                ipfs: "",
                pk:"",
            };
            requ_data.ipfs = row.ipfs
            requ_data.pk = this.tableData[index].pubkey;
            this.$message.success('服务器正在从IPFS下载数据...');
            download_file(requ_data).then(res =>{
                this.$message.success('正在保存到本地...');
                const blob = new Blob([res])
                const link = document.createElement('a')
                link.download = requ_data.ipfs // a标签添加属性
                link.style.display = 'none'
                link.href = URL.createObjectURL(blob)
                document.body.appendChild(link)
                link.click() // 执行下载
                URL.revokeObjectURL(link.href)  // 释放 bolb 对象
                document.body.removeChild(link) // 下载完成移除元素
            });
        },
    },
    created() {
        this.userinfo = localStorage.getItem('ms_userinfo');
        if ( this.userinfo == 'user')
            this.userpermit = localStorage.getItem('ms_userpermit');
        else{
            this.userpermit = '0';
        }
    }
};
</script>

<style scoped>
.handle-box {
    width: 1000px;
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
