<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height:252px;">
                    <div class="user-info">
                        <img src="../assets/img/img.jpg" class="user-avator" alt />
                        <div class="user-info-cont">
                            <div class="user-info-name">{{ name }}</div>
                        </div>
                    </div>
                </el-card>
                <el-row :gutter="20" class="mgb20" >
                    <el-col >
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-user-solid grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num" >{{blockNumber}}</div>
                                    <div>区块高度</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col >
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-message-solid grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num" >{{TxNumber}}</div>
                                    <div>当前区块交易数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="16">
                <el-card shadow="hover" style="height:475px;">
                    <template #header>
                        <div class="clearfix">
                            <span>待上链交易</span>
                        </div>
                    </template>
                    <el-table :data="txTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                        <el-table-column prop="log_timestamp" label="日志时间" width="155" align="center"></el-table-column>
                        <el-table-column prop="pubkey"  :show-overflow-tooltip="true" label="用户公钥" align="center"></el-table-column>
                        <el-table-column prop="ipfs"  :show-overflow-tooltip="true" label="IPFS文件地址" width="275" align="center"></el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
        <el-card shadow="hover" style="height:475px;">
            <template #header>
                <div class="clearfix">
                    <span>区块信息</span>
                </div>
            </template>
            <el-table :data="BcTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                <el-table-column prop="blockHeight" label="块高" width="55" align="center"></el-table-column>
                <el-table-column prop="blockTimestamp" label="区块生成时间" width="155" align="center"></el-table-column>
                <el-table-column prop="startTimestamp" label="日志开始时间" width="155" align="center"></el-table-column>
                <el-table-column prop="endTimestamp" label="日志结束时间" width="155" align="center"></el-table-column>
                <el-table-column prop="merkleRoot"  :show-overflow-tooltip="true" label="默克尔根" align="center"></el-table-column>
                <el-table-column prop="previousHash"  :show-overflow-tooltip="true" label="前区块哈希" align="center"></el-table-column>
            </el-table>
        </el-card>
    </div>
</template>

<script>
import { getNowTxs, getBlocks} from "../api/index";
export default {
    data:function() {
        return{
            txTableData:[],
            BcTableData:[],
            blockNumber:0,
            TxNumber:0,
            name:"",
            tx_number:{
                number:6
            },
            block_number:{
                number:5
            },
        }
    },
    methods:{
        getTxList() {
            this.$message.success('正在加载...');
            getNowTxs(this.tx_number).then(res => {
                if (res.get_result == 'true') {
                    this.txTableData = res.list;
                    this.TxNumber = res.txNumber;
                } else {
                    this.$message.error('交易数据加载失败');
                }
            });
        },
        getBlocks() {
            getBlocks(this.block_number).then(res => {
                if (res.get_result == 'true') {
                    this.BcTableData = res.list;
                    this.blockNumber = res.list[0].blockHeight;
                } else {
                    this.$message.error('区块数据加载失败');
                }
            });
        }
    },
    created() {
        this.name = localStorage.getItem('ms_username');
        this.getTxList();
        this.getBlocks();
    },
};
</script>

<style scoped>
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}
</style>
