<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">区块链日志存储系统</div>

      <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
        <el-form-item prop="name">
          <el-input v-model="param.name" placeholder="用户名" >
            <template #prepend>
                <el-button icon="el-icon-user"></el-button>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item  prop="password">
          <el-input type="password" placeholder="密码" v-model="param.password" @keyup.enter="submitForm()">
            <template #prepend>
                <el-button icon="el-icon-lock"></el-button>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item >
          <el-button type="primary" @click="submitForm()" >登录</el-button>
          <el-button type="primary" @click="registerUser()">注册</el-button>
          <el-button type="primary" @click="changeUserPassword()" >忘记密码</el-button>
        </el-form-item>
      </el-form>

    </div>

  <el-dialog title="用户注册" v-model="registerDialog" width="45%">

    <el-form :model="registerform" :rules="rules" :inline="true" ref="register" label-width="80px" >
      <el-form-item label="用户名"  prop="registername">
        <el-input style="width:100%" v-model="registerform.registername"></el-input>
      </el-form-item>

      <el-form-item label="密码"  prop="registerpassword">
        <el-input style="width:100%"  type="password"  v-model="registerform.registerpassword"></el-input>
      </el-form-item>

      <el-form-item label="重复密码" prop="repeatpassword">
          <el-input style="width:100%" type="password"  v-model="registerform.repeatpassword"></el-input>
      </el-form-item>

      <el-form-item label="电子邮箱"  prop="useremail">
          <el-input style="width:100%" v-model="registerform.useremail"></el-input>
      </el-form-item>

      <el-form-item label="联系电话" prop="userphone">
          <el-input style="width:100%" v-model="registerform.userphone"></el-input>
      </el-form-item>

      <el-form-item label="AES密钥"  prop="deskey">
          <el-input style="width:100%"  type="password"  v-model="registerform.deskey"></el-input>
      </el-form-item>
    </el-form>

    <el-form :model="registerform" :rules="rules" ref="register" label-width="80px" >
      <el-form-item label="RSA公钥" prop="rsapk">
          <el-input style="width:90%" v-model="registerform.rsapk"></el-input>
      </el-form-item>

      <el-form-item label="RSA私钥" prop="rsask">
          <el-input style="width:90%" v-model="registerform.rsask"></el-input>
      </el-form-item>
      
      <el-form-item label="验证码" prop="verifycode">
        <el-input style="width:200px" v-model="registerform.verifycode"></el-input>
        <el-button type="success" v-if="show == 0" @click="getcode">发送验证码</el-button>
        <el-button type="success" v-if="show == 1" >已发送{{count}}秒</el-button>
        <el-button type="success" v-if="show == 2" @click="getcode">重新获取</el-button>
      </el-form-item>
    </el-form>
    <template #footer>
        <span class="dialog-footer">
            <el-button type="success" @click="onGenerateRSA">生成RSA密钥对</el-button>
            <el-button @click="registerDialog = false" >取 消</el-button>
            <el-button type="primary" @click="onRegister">注 册</el-button>
        </span>
    </template>
  </el-dialog>
  
  <el-dialog title="找回密码" v-model="changePWDDialog" width="30%">
    <el-form :model="changeform" :rules="rules" ref="changePWD" label-width="80px" >

    <el-form-item label="用户名"  prop="cname">
          <el-input style="width:90%"  v-model="changeform.cname"></el-input>
      </el-form-item>

      <el-form-item label="新密码" prop="newpassword">
          <el-input style="width:90%"  type="password"  v-model="changeform.newpassword"></el-input>
      </el-form-item>

      <el-form-item label="邮箱" prop="useremail">
          <el-input style="width:90%" v-model="changeform.useremail"></el-input>
      </el-form-item>

      <el-form-item label="验证码" prop="verifycode">
        <el-input style="width:200px" v-model="changeform.verifycode"></el-input>
        <el-button type="success" v-if="show == 0" @click="getcodePwd">发送验证码</el-button>
        <el-button type="success" v-if="show == 1" >已发送{{count}}秒</el-button>
        <el-button type="success" v-if="show == 2" @click="getcodePwd">重新获取</el-button>
      </el-form-item>
    </el-form>
      <template #footer>
        <span class="dialog-footer">
            <el-button @click="changePWDDialog = false">取 消</el-button>
            <el-button type="primary" @click="onChangePwd">修改</el-button>
        </span>
      </template>
  </el-dialog>
  </div>
</template>

<script>

import { ref } from "vue";
import { requestLogin, requestRegister, generateRSA,changePassword, getCode} from "../api/index";

export default {
    data:function() {
        return {
            param: {
                name:"",
                password:"",
            },
            registerform: {
                registername:"",
                registerpassword:"",
                repeatpassword:"",
                useremail:"",
                userphone:"",
                deskey:"",
                rsapk:"",
                rsask:"",
                verifycode:"",
            },
            changeform: {
                cname:"",
                newpassword:"",
                useremail:"",
                verifycode:"",
            },
            rules:{name:  [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                    password:  [{ required: true, message: '请输入密码', trigger: 'blur' }],
                    registername:  [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                    registerpassword:  [{ required: true, message: '请输入密码', trigger: 'blur' }],
                    repeatpassword:  [{ required: true, message: '请再次输入密码', trigger: 'blur' }],
                    useremail:  [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
                    userphone:  [{ required: true, message: '请输入电话', trigger: 'blur' }],
                    deskey:  [{ required: true, message: '请输入DES密钥', trigger: 'blur' }],
                    rsapk:  [{ required: true, message: '请输入RSA公钥', trigger: 'blur' }],
                    rsask:  [{ required: true, message: '请输入RSA私钥', trigger: 'blur' }],
                    verifycode:  [{ required: true, message: '请输入验证码', trigger: 'blur' }],
                    cname:  [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                    newpassword:  [{ required: true, message: '请输入新密码', trigger: 'blur' }],
                    useremail:  [{ required: true, message: '请输入邮箱', trigger: 'blur' }]
            },
            registerDialog: ref(false),
            changePWDDialog: ref(false),
            show: 0,
			      count: '',
			      timer: null,
        };
    },
    methods: {
        submitForm() {
          this.$refs.login.validate(async (valid) =>{
                if (valid) {
                    requestLogin(this.param).then(res => {
                        if (res.login_result == 'true') {
                            this.$message.success('登录成功');
                            localStorage.setItem('ms_username', this.param.name);
                            localStorage.setItem('ms_userinfo', res.login_info);
                            if(res.login_info == 'user'){
                              localStorage.setItem('ms_userpermit', res.user_permit);
                            }
                            this.$router.push('/');
                        } else {
                            this.$message.error('账号或密码错误');
                        }
                    });
                } else {
                    this.$message.error('请输入账号和密码');
                    return false;
                }
          });
        },
        registerUser() {
          this.registerDialog = true;
        },
        onRegister() {
          this.$refs.register.validate(async (valid) =>{
                if (valid) {
                    requestRegister(this.registerform).then(res => {
                        if (res.register_result == 'true' && this.registerform.registerpassword == this.registerform.repeatpassword) {
                            this.$message.success('注册成功');
                            this.registerDialog = false;
                        } else if (this.registerform.registerpassword != this.registerform.repeatpassword){
                            this.$message.error('注册失败，两次密码不一致');
                        } else{
                            this.$message.error('注册失败，用户已存在或验证码错误');
                        }
                    });
                } else {
                    this.$message.error('请输入注册必要数据');
                    return false;
                }
          });
        },
        onGenerateRSA() {
          generateRSA().then(res => {
            this.registerform.rsapk = res.public_key;
            this.registerform.rsask = res.private_key;
          })
        },
        onChangePwd(){
          this.$refs.changePWD.validate(async (valid) =>{
                if (valid) {
                    changePassword(this.changeform).then(res => {
                        if (res.changeresult == 'true') {
                            this.$message.success('修改成功');
                            this.changePWDDialog = false;
                            //close
                        } else {
                            this.$message.error('用户名,邮箱或验证码错误');
                        }
                    });
                } else {
                    this.$message.error('请填入必要信息');
                    return false;
                }
          });
        },
        changeUserPassword() {
          this.changePWDDialog = true;
        },
        getcode(){
          getCode(this.registerform).then(res => {
              if (res.get_result == 'true') {
                  this.$message.success('发送成功');
              } else {
                  this.$message.error('邮箱错误');
              }
          });
          const times = 60; // 倒计时时间
          if (!this.timer) {
            this.count = times;
            this.show = 1;
            this.timer = setInterval(() => {
              if (this.count > 0 && this.count <= times) {
                this.count--;
              } else {
                this.show = 2;
                clearInterval(this.timer);
                this.timer = null;
              }
            }, 1000)
          }
        },
        getcodePwd(){
          getCode(this.changeform).then(res => {
              if (res.get_result == 'true') {
                  this.$message.success('发送成功');
              } else {
                  this.$message.error('邮箱错误');
              }
          });
          const times = 60; // 倒计时时间
          if (!this.timer) {
            this.count = times;
            this.show = 1;
            this.timer = setInterval(() => {
              if (this.count > 0 && this.count <= times) {
                this.count--;
              } else {
                this.show = 2;
                clearInterval(this.timer);
                this.timer = null;
              }
            }, 1000)
          }
        },
    },
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/login-bg.jpg);
  background-size: 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #000;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
.login-tips {
  font-size: 12px;
  line-height: 30px;
  color: #fff;
}
</style>