<template>
    <div class="">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i> 日志上传</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="ms-upload" v-if="this.userinfo == 'user' && userpermit == '0' || userpermit == '2'">
                <el-form ref="jsonformRef" :rules="rules" :inline="true" :model="form" label-width="90px">
                    <el-form-item label="日志类型" prop="resource">
                        <el-radio-group v-model="form.resource">
                            <el-radio label="json"></el-radio>
                            <el-radio label="字符串"></el-radio>
                            <el-radio label="文件"></el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-form>
                    
                <el-form ref="jsonformRef" :rules="rules" :inline="true" :model="form" label-width="90px" v-if="form.resource=='json'">
                    <el-form-item label="日志时间" prop="date1">
                        <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" value-format="YYYY-MM-DD"
                                    style="width: 240px;"></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="date2" >
                        <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 240px;" value-format="HH:mm:ss">
                        </el-time-picker>
                    </el-form-item>
                </el-form>

                <el-form ref="jsonformRef" :rules="rules" :inline="true" :model="form" label-width="90px" >

                    <el-form-item label="客户端IP" prop="clientIP" v-if="form.resource=='json'">
                        <el-input  v-model="form.clientIP"></el-input>
                    </el-form-item>

                    <el-form-item label="邮箱地址" prop="email" v-if="form.resource=='json'">
                        <el-input  v-model="form.email"></el-input>
                    </el-form-item>

                    <el-form-item label="登录名" prop="name" v-if="form.resource=='json'">
                        <el-input  v-model="form.name"></el-input>
                    </el-form-item>

                    <el-form-item label="请求方法" prop="requestmethod"  v-if="form.resource=='json'">
                        <el-input v-model="form.requestmethod"></el-input>
                    </el-form-item>

                    <el-form-item label="状态码" prop="code"  v-if="form.resource=='json'">
                        <el-input v-model="form.code"></el-input>
                    </el-form-item>

                    <el-form-item label="字节数" prop="number"  v-if="form.resource=='json'">
                        <el-input v-model="form.number"></el-input>
                    </el-form-item>

                    <el-form-item label="备注" prop="note"  v-if="form.resource=='json'">
                        <el-input type="textarea" rows="5" style="width:480px" v-model="form.note"></el-input>
                    </el-form-item>
                    
                    <el-form-item  v-if="form.resource=='json'">
                        <el-button type="primary" @click="onSubmit">提交日志</el-button>
                        <el-button type="primary" @click="onReset">重置数据</el-button>
                    </el-form-item>
                </el-form>


                <el-form ref="stringformRef" :rules="rules" :inline="true" :model="form" label-width="90px" v-if="form.resource=='字符串'">
                    <el-form-item label="日志时间" prop="date1">
                        <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" value-format="YYYY-MM-DD"
                                    style="width: 240px;"></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="date2" >
                        <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 240px;" value-format="HH:mm:ss">
                        </el-time-picker>
                    </el-form-item>
                </el-form>

                <el-form ref="stringformRef" :rules="rules" :inline="true" :model="form" label-width="90px" >
                    <el-form-item label="字符串" prop="stringlog"  v-if="form.resource=='字符串'">
                        <el-input type="textarea" rows="5" style="width:480px" v-model="form.stringlog"></el-input>
                    </el-form-item>

                    <el-form-item  v-if="form.resource=='字符串'">
                        <el-button type="primary" @click="onSubmitString">提交日志</el-button>
                        <el-button type="primary" @click="onResetString">重置数据</el-button>
                    </el-form-item>
                </el-form>

                <el-form ref="fileformRef" :rules="rules" :inline="true" :model="form" label-width="90px" v-if="form.resource=='文件'">
                    <el-form-item label="日志时间" prop="date1">
                        <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" value-format="YYYY-MM-DD"
                                    style="width: 240px;"></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="date2" >
                        <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 240px;" value-format="HH:mm:ss">
                        </el-time-picker>
                    </el-form-item>
                </el-form>

                <el-form ref="fileformRef" :rules="rules" :inline="true" :model="form" label-width="90px" >
                    <el-form-item label="字符串" prop="filelog"  v-if="form.resource=='文件'">
                        <el-upload class="upload-demo" 
                        action="http://localhost:5000/uploadLogFile" 
                        ref="upload"
                        :file-list="fileList"
                        :http-request="httpRequest"
                        :auto-upload="false" multiple>
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">
                                将日志文件拖到此处，或
                                <em>点击上传</em>
                            </div>
                            <div class="el-upload__text" >只能上传txt文件</div>
                        </el-upload>
                    </el-form-item>
                </el-form>

                <el-form ref="fileformRef" :rules="rules" :inline="true" :model="form" label-width="90px" >
                    <el-form-item  v-if="form.resource=='文件'">
                        <el-button type="primary" @click="onSubmitFile">提交日志</el-button>
                    </el-form-item>
                </el-form>

            </div>
            <template v-if="this.userinfo == 'user' && userpermit == '1'">
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

            <template v-if="this.userinfo == 'admin'">
                <div class="error-page">
                    <div class="error-desc">管理员使用普通用户登录，才能上传日志</div>
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
import { uploadLogJson,uploadLogFile } from "../api/index";
import { useRouter } from "vue-router";

export default {
    data:function() {
        return{
            form: {
                uploadname:"",
                date1:"",
                date2:"",
                clientIP:"",
                email:"",
                name:"",
                requestmethod:"",
                code:"",
                number:"",
                note:"",
                resource:"json",
                stringlog:"",
            },
            rules: {
                date1:  [{ required: true, message: '请选择日期', trigger: 'blur' }],
                date2:  [{ required: true, message: '请选择时间', trigger: 'blur' }],
                clientIP:  [{ required: true, message: '请输入客户端IP', trigger: 'blur' }],
                requestmethod:  [{ required: true, message: '请输入请求方法', trigger: 'blur' }],
                code:  [{ required: true, message: '请输入状态码', trigger: 'blur' }],
                number:  [{ required: true, message: '请输入字节数', trigger: 'blur' }],
                email:  [{ required: false}],
                name:  [{ required: false }],
                note:  [{ required: false }],
                stringlog: [{ required: true, message: '请输入日志数据', trigger: 'blur' }],
                filelog : [{ required: true, message: '请选择文件', trigger: 'blur' }],
            },
            fileList: [],
        };
    },  
    methods: {
        onSubmit() {
          this.$refs.jsonformRef.validate(async (valid) =>{
                if (valid) {
                    if(this.form.email == ""){
                        this.form.email = "-";
                    }
                    if(this.form.name == ""){
                        this.form.name = "-";
                    }
                    this.form.uploadname = localStorage.getItem('ms_username');
                    uploadLogJson(this.form).then(res => {
                        if (res.upload_result == 'true') {
                            this.onReset();
                            this.$message.success('上传成功');
                        } else {
                            this.$message.error('上传失败');
                        }
                    });
                } else {
                    this.$message.error('请填写必要数据');
                    return false;
                }
          });
        },
        onReset() {
           this.$refs.jsonformRef.resetFields();
        },
        onSubmitString(){
            this.$refs.jsonformRef.validate(async (valid) =>{
             if (valid) {
                    this.form.uploadname = localStorage.getItem('ms_username');
                    uploadLogJson(this.form).then(res => {
                        if (res.upload_result == 'true') {
                            this.onResetString();
                            this.$message.success('上传成功');
                        } else {
                            this.$message.error('上传失败');
                        }
                    });
                } else {
                    this.$message.error('请填写必要数据');
                    return false;
                }
            });
        },
        onResetString() {
            this.$refs.stringformRef.resetFields();
        },
        onSubmitFile() {
            this.$refs.fileformRef.validate(valid => {
                if (valid) {
                    console.log("有效")
                    this.$refs.upload.submit();
                } else {
                    console.log("error submit!!");
                    return false;
                }
            });
        },
        httpRequest(param) {
          let fileObj = param.file; // 相当于input里取得的files
          let data = new FormData(); // FormData 对象
          data.append("file", fileObj); // 文件对象
          data.append("uploadname", localStorage.getItem('ms_username'));
          data.append("date1", this.form.date1);
          data.append("date2", this.form.date2);
          uploadLogFile(data).then(res => {
                if (res.upload_result == 'true') {
                    this.$message.success('上传成功');
                } else {
                    this.$message.error('上传失败');
                }
          }).catch(error => {
                this.$message.error('上传失败');
          })
        },
        goBack() {
           this.$router.go(-1)
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
<style>
.message-title {
    cursor: pointer;
}
.handle-row {
    margin-top: 30px;
}
.ms-upload {
    width: 700px;
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

