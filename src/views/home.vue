<template>
    <div class="card">
        <div class="user">
            <a-avatar shape="square" :size="32">
                U
            </a-avatar>
        </div>
        <div class="topic-main-content">
            <div class="topic-top">
                <div class="user-name">用户</div>
                <div class="time">发布于12天前</div>
            </div>
            <div class="topic-content" @click="goToTopic">
                <div class="title">测试题目</div>
                <div class="description">测试描述啦啦啦啦啦啦啦啦啦啦啦啦啦</div>
            </div>
            <div class="topic-bottom">
                <div class="handlers">
                    <div class="btn">赞</div>
                    <div class="btn">评论</div>
                    <div class="scan">浏览</div>
                </div>
                <div class="tags">
                    <span>交流</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const goToTopic = function() {
    router.push('/topic');
}
</script>

<style scoped>
.card {
    background-color: white;
    width: 100%;
    margin-top: 15px;
    padding: 12px;
    display: flex;
    transition:background-color 0.5s;
}

.card:hover {
    background-color: #e8e8e8;
}

.user {
    cursor: pointer;
}

.topic-main-content {
    flex: 1;
    margin-left: 12px;
}

.topic-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.user-name {
    color: #70727c;
    font-weight: 700;
    font-size: 16px;
    cursor: pointer;
}

.time {
    font-size: 12px;
    color: #70727c;
}

.title {
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    display: inline-block;
    margin-bottom: 6px;
}

.title:hover {
    text-decoration: underline;
}

.description {
    font-size: 15px;
    cursor: pointer;
}

.topic-bottom {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

.handlers {
    display: flex;
    justify-content: space-around;
    font-size: 12px;
}

.btn {
    cursor: pointer;
    margin-right: 20px;
}

.btn:hover {
    color: #1878f3;
}

.tags {
    font-size: 12px;
    padding: 2px 8px;
    justify-content: center;
    align-items: center;
    border-radius: 12.5px;
    margin-right: 10px;
    background: rgba(247,248,250,0.7);
    border: 1px solid #dcdfe6;
    color: #70727c;
    cursor: pointer;
}

.tags span:hover {
    color: #1878f3;
}
</style>