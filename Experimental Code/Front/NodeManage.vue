<template>
    <div class="">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i>节点申请</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-dialog title="节点申请" v-model="AddNodeDialog" width="45%">
                <el-form :model="nodeInfo" :rules="rules" :inline="true" ref="register" label-width="80px" >
                    <el-form-item label="节点名"  prop="nodename">
                        <el-input style="width:100%" v-model="nodeInfo.nodename"></el-input>
                    </el-form-item>
                    <el-form-item label="节点IP"  prop="nodeip">
                        <el-input style="width:100%"  v-model="nodeInfo.nodeip"></el-input>
                    </el-form-item>
                    <el-form-item label="节点类型" prop="nodetype">
                        <el-input style="width:100%" v-model="nodeInfo.nodetype"></el-input>
                    </el-form-item>
                    <el-form-item label="节点备注"  prop="nodenote">
                        <el-input style="width:100%" v-model="nodeInfo.nodenote"></el-input>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="AddNodeDialog = false" >取 消</el-button>
                        <el-button type="primary" @click="registerNode">申 请</el-button>
                    </span>
                </template>
            </el-dialog>

            <el-tabs v-model="message" v-if="userinfo == 'admin'">
                <el-tab-pane :label="`未处理(${unreadData.length})`" name="first">
                    <el-table :data="unreadData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                        <el-table-column prop="nodeid" label="编号" width="65" align="center"></el-table-column>
                        <el-table-column prop="nodename" label="节点名" width="80" align="center"></el-table-column>
                        <el-table-column prop="nodeip" label="节点IP" width="160" align="center"></el-table-column>
                        <el-table-column prop="nodetype" label="节点类型" width="80" align="center"></el-table-column>
                        <el-table-column prop="nodetime" label="申请时间" width="275" align="center"></el-table-column>
                        <el-table-column prop="nodenote" label="备注" width="275" align="center"></el-table-column>
                        <el-table-column label="操作" width="180" align="center">
                            <template #default="scope">
                                <el-button type="text" icon="el-icon-check" @click="passApp(scope.$index,scope.row)">通过
                                </el-button>
                                <el-button type="text" icon="el-icon-close" @click="refuseApp(scope.$index,scope.row)">拒绝
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-button @click="addNodeInfo">添加节点</el-button>
                </el-tab-pane>


                <el-tab-pane :label="`已通过(${readData.length})`" name="second">
                    <el-table :data="readData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                        <el-table-column prop="nodeid" label="编号" width="65" align="center"></el-table-column>
                        <el-table-column prop="nodename" label="节点名" width="80" align="center"></el-table-column>
                        <el-table-column prop="nodeip" label="节点IP" width="160" align="center"></el-table-column>
                        <el-table-column prop="nodetype" label="节点类型" width="80" align="center"></el-table-column>
                        <el-table-column prop="nodetime" label="申请时间" width="275" align="center"></el-table-column>
                        <el-table-column prop="nodenote" label="备注" width="275" align="center"></el-table-column>
                        <el-table-column label="操作" width="180" align="center">
                            <template #default="scope">
                                <el-button type="text" icon="el-icon-close" @click="refuseApplication(scope.$index,scope.row)">拒绝</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>

                <!--<el-tab-pane :label="`未通过申请(${state.recycle.length})`" name="third">-->
                <el-tab-pane :label="`未通过(${recycleData.length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="recycleData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                            <el-table-column prop="nodeid" label="编号" width="65" align="center"></el-table-column>
                            <el-table-column prop="nodename" label="节点名" width="80" align="center"></el-table-column>
                            <el-table-column prop="nodeip" label="节点IP" width="160" align="center"></el-table-column>
                            <el-table-column prop="nodetype" label="节点类型" width="80" align="center"></el-table-column>
                            <el-table-column prop="nodetime" label="申请时间" width="275" align="center"></el-table-column>
                            <el-table-column prop="nodenote" label="备注" width="275" align="center"></el-table-column>
                            <el-table-column label="操作" width="180" align="center">
                            <template #default="scope">
                                <el-button type="text" icon="el-icon-check" @click="passApplication(scope.$index,scope.row)">通过</el-button>
                            </template>
                            </el-table-column>
                        </el-table>
                    </template>
                </el-tab-pane>
            </el-tabs>


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
import { ref, reactive } from "vue";
import { getNode, changeNodeState,addNode } from "../api/index";

export default {
    data:function() {
        return {
            unreadData:[],
            readData: [],
            recycleData:[],
            message:ref("first"),
            changeNode:{
                nodeip:"",
                nodestate:""
            },
            nodeInfo:{
                nodename:"",
                nodeip:"",
                nodetype:"",
                nodenote:"",
            },
            rules:{nodename:  [{ required: true, message: '请输入节点名', trigger: 'blur' }],
                    nodeip:  [{ required: true, message: '请输入节点IP', trigger: 'blur' }],
                    nodetype:  [{ required: true, message: '请输入节点类型', trigger: 'blur' }],
                    nodenote:  [{ required: true, message: '请输入备注', trigger: 'blur' }],
            },
            AddNodeDialog:false,
        }
    },
    methods: {
        getNodeList(){
            getNode().then(res => {
                if (res.get_result == 'true') {
                    this.unreadData = res.unreadData;
                    this.readData = res.readData;
                    this.recycleData = res.recycleData;
                } else {
                    this.$message.error('加载失败');
                }
            });
        },
        changeNodeState(node_ip,node_state){
            this.changeNode.nodeip = node_ip;
            this.changeNode.nodestate = node_state;
            changeNodeState(this.changeNode).then(res =>{
                if (res.change_result == 'true') {
                    this.$message.success('修改成功');
                } else {
                    this.$message.error('修改失败');
                }
            });
            //this.getUserList();
        },  
        passApplication(index,row){
            this.changeNodeState(row.nodeip,"已通过");
            this.readData.push(row);
            this.recycleData.splice(index,1);
        },
        refuseApplication(index,row){
            this.changeNodeState(row.nodeip,"未通过");
            this.recycleData.push(row);
            this.readData.splice(index,1);
        },
        passApp(index,row){
            this.changeNodeState(row.nodeip,"已通过");
            this.readData.push(row);
            this.unreadData.splice(index,1);
        },
        refuseApp(index,row){
            this.changeNodeState(row.nodeip,"未通过");
            this.recycleData.push(row);
            this.unreadData.splice(index,1);
        },

        goBack() {
           this.$router.go(-1)
        },
        addNodeInfo(){
            this.AddNodeDialog = true;
        },
        registerNode(){
            this.$refs.register.validate(async (valid) =>{
                if (valid) { 
                    addNode(this.nodeInfo).then(res =>{
                        if (res.add_result == 'true') {
                            this.$message.success('申请成功');
                            this.AddNodeDialog = false;
                            this.$router.go(0);
                        } else {
                            this.$message.error('申请失败');
                        }
                    });
                }else{
                    this.$message.error('请输入必要信息');
                }
            });
        }
    },
    created() {
        this.userinfo = localStorage.getItem('ms_userinfo');
        this.getNodeList();
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