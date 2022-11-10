<template>
    <div class="widget">
        <div class="widget-header">登录</div>
        <div class="widget-main">
            <a-form :model="formState" name="normal_login" class="login-form" @finish="onFinish"
                @finishFailed="onFinishFailed">
                <a-form-item label="用户名" name="username"
                    :rules="[{ required: true, message: '请输入您的用户名！' }]">
                    <a-input v-model:value="formState.username">
                        <template #prefix>
                            <UserOutlined class="site-form-item-icon" />
                        </template>
                    </a-input>
                </a-form-item>

                <a-form-item label="密码" name="password"
                    :rules="[{ required: true, message: '请输入您的密码！' }]">
                    <a-input-password v-model:value="formState.password">
                        <template #prefix>
                            <LockOutlined class="site-form-item-icon" />
                        </template>
                    </a-input-password>
                </a-form-item>

                <a-form-item class="widget-remember">
                    <a-form-item name="remember" no-style>
                        <a-checkbox v-model:checked="formState.remember">记住我</a-checkbox>
                    </a-form-item>
                    <a class="login-form-forgot" href="#">忘记密码</a>
                </a-form-item>

                <a-form-item class="widget-button">
                    <a-button :disabled="disabled" type="primary" html-type="submit" class="login-form-button">
                        登录
                    </a-button>
                    <a href="#">立即使用学生邮箱注册</a>
                </a-form-item>
            </a-form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
const formState = reactive({
    username: '',
    password: '',
    remember: true,
});
</script>

<style scoped>
.widget {
    background: #fff;
    margin: 0 auto;
    padding: 0 12px;
    padding-bottom: 1px;
    margin-top: 10px;
    border-radius: calc(.25rem - 1px);
    max-width: 600px;
}

.widget-header {
    padding: 8px 0;
    font-size: 16px;
    font-weight: 700;
    border-bottom: 1px solid #e9e9e9;
    margin-bottom: 16px;
}

.widget-main {
    text-align: center;
}

:deep(.widget-remember  .ant-form-item-control-input-content:last-child) {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

:deep(.widget-button .ant-form-item-control-input-content:last-child) {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px
}

.login-form-button {
    width: 30%;
}
</style>