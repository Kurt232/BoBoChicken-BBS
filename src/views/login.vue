<template>
    <div class="widget">
        <div class="widget-header">登录</div>
        <div class="widget-main">
            <a-form :model="formState" name="normal_login" class="login-form" @finish="onFinish"
                @finishFailed="onFinishFailed">
                <a-form-item label="Username" name="username"
                    :rules="[{ required: true, message: 'Please input your username!' }]">
                    <a-input v-model:value="formState.username">
                        <template #prefix>
                            <UserOutlined class="site-form-item-icon" />
                        </template>
                    </a-input>
                </a-form-item>

                <a-form-item label="Password" name="password"
                    :rules="[{ required: true, message: 'Please input your password!' }]">
                    <a-input-password v-model:value="formState.password">
                        <template #prefix>
                            <LockOutlined class="site-form-item-icon" />
                        </template>
                    </a-input-password>
                </a-form-item>

                <a-form-item>
                    <a-form-item name="remember" no-style>
                        <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
                    </a-form-item>
                    <a class="login-form-forgot" href="">Forgot password</a>
                </a-form-item>

                <a-form-item>
                    <a-button :disabled="disabled" type="primary" html-type="submit" class="login-form-button">
                        Log in
                    </a-button>
                    Or
                    <a href="">register now!</a>
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
</style>