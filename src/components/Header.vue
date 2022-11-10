<template>
    <nav class="navbar">
        <div class="title" @click="goToIndex">
            钵钵鸡BBS
        </div>
        <div class="search-and-user">
            <a-input-search
            v-model:value="value"
            placeholder="搜索"
            style="width: 200px"
            @search="onSearch"
            />
            <a-button type="primary">发布</a-button>
            <a-button @click="login">登录</a-button>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
const login = function() {
    router.push('/login');
}

const goToIndex = function() {
    router.push('/')
}
</script>

<style scoped>
.navbar {
    background-color: white;
    box-shadow: 0 2px 0 0 #f5f5f5;
    min-height: 3.25rem;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.title {
    font-size: large;
    cursor: pointer;
}

.search-and-user {
    display: flex;
    width: 30%;
    gap: 5%;
    justify-content: center;
}
</style>