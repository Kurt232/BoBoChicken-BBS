<template>
    <div class="topic-detail">
        <article>
            <div class="topic-header">
                <div class="user">
                    <a-avatar shape="square" :size="45">
                        U
                    </a-avatar>
                </div>
                <div class="user-name-and-time">
                    <div class="user-name">用户</div>
                    <div class="time">发布于 2019-09-09 19:30:19</div>
                </div>
            </div>
            <div class="topic-content">
                <h1 class="topic-title">测试标题</h1>
                <div class="topic-content-detail">
                    测试内容啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦测试内容啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦测试内容啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦测试内容啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦测试内容啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦啦
                </div>
            </div>
            <div class="topic-tags">
                <span class="tag">交流</span>
            </div>
            <div class="topic-actions">
                <div class="action">浏览(123)</div>
                <div class="action">点赞(123)</div>
                <div class="action">收藏(123)</div>
            </div>
        </article>
    </div>
    <div class="comment-detail">
        <div class="comment-top">123条评论</div>
        <div class="comment-not-login">
            请<span class="login">登录</span>后评论
        </div>
        <div class="comments">
            <div class="comment">
                <div class="user">
                    <a-avatar shape="square" :size="32">
                        U
                    </a-avatar>
                </div>
                <div class="comment-main-content">
                    <div class="comment-top">
                        <div class="user-name">用户</div>
                        <div class="time">发布于12天前</div>
                    </div>
                    <div class="comment-content">
                        <div class="description">测试描述啦啦啦啦啦啦啦啦啦啦啦啦啦</div>
                    </div>
                    <div class="comment-bottom">
                        <div class="handlers">
                            <div class="btn">点赞</div>
                            <div class="btn">评论</div>
                        </div>
                    </div>
                    <div class="replies">
                        <div class="comment">
                            <div class="user">
                                <a-avatar shape="square" :size="32">
                                    U
                                </a-avatar>
                            </div>
                            <div class="comment-main-content">
                                <div class="comment-top">
                                    <div class="user-name">用户</div>
                                    <div class="time">发布于12天前</div>
                                </div>
                                <div class="comment-content">
                                    <div class="description">测试回复哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈</div>
                                </div>
                                <div class="comment-bottom">
                                    <div class="handlers">
                                        <div class="btn">点赞</div>
                                        <div class="btn">评论</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="more">
            <span>查看更多</span>
        </div>
    </div>
</template>

<script setup>

</script>

<style scoped>
.topic-detail {
    margin-top: 20px;
    background-color: white;
    padding: 16px;
    padding-bottom: 0;
}

.topic-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.user-name-and-time {
    margin-left: 8px;
}

.user-name {
    font-size: 16px;
    font-weight: 700;
}

.time {
    font-size: 12px;
    color: #70727c;
    margin-top: 5px;
}

.topic-title {
    font-weight: 700;
    font-size: 20px;
    word-wrap: break-word;
    word-break: normal;
    border-bottom: 1px solid #e9e9e9;
    padding-bottom: 10px;
    margin-bottom: .5em;
}

.topic-content-detail {
    font-size: 16px;
    line-height: 24px;
    word-wrap: break-word;
    -webkit-font-smoothing: antialiased;
    margin-bottom: 16px;
}

.topic-tags {
    margin-bottom: 16px;
}

.tag {
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 12.5px;
    margin-right: 10px;
    background: rgba(247, 248, 250, 0.7);
    border: 1px solid #dcdfe6;
    color: #70727c;
    cursor: pointer;
}

.tag:hover {
    color: #1878f3;
}

.topic-actions {
    padding: 10px 0;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    border-top: 1px solid #dcdfe6;
}

.action {
    cursor: pointer;
    font-size: 14px;
    flex: 1;
    text-align: center;
}

.action:first-child {
    cursor: context-menu;
}

.comment-detail {
    margin-top: 16px;
    background-color: white;
    border-radius: 3px;
    padding: 0 10px;
}

.comment-top {
    font-size: 16px;
    font-weight: 500;
}

.comment-not-login {
    margin: 10px;
    border: 1px solid #e9e9e9;
    border-radius: 0;
    overflow: hidden;
    position: relative;
    padding: 10px;
    box-sizing: border-box;
    color: #d8d8d8;
}

.comment-not-login span {
    margin-left: 10px;
    margin-right: 10px;
    color: #485fc7;
    cursor: pointer;
}

.comments {
    padding: 10px;
    font-size: 14px;
}

.comment {
    border-bottom: 1px solid #e9e9e9;
    display: flex;
    padding: 10px 0;
}

.comment-main-content {
    flex: 1;
    margin-left: 12px;
}

.comment-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.description {
    font-size: 15px;
}

.comment-bottom {
    display: flex;
    justify-content: space-between;
    padding-top: 10px;
}

.handlers {
    display: flex;
    justify-content: space-around;
    font-size: 10px;
}

.btn {
    cursor: pointer;
    margin-right: 20px;
}

.btn:hover {
    color: #1878f3;
}

.replies {
    margin-top: 10px;
    padding: 1px 10px;
    font-size: 12px;
    background-color: rgba(247, 248, 250, 0.7);
}
.replies .comment:last-child {
    border: none;
}

.more {
    text-align: center;
    cursor: pointer;
    font-size: 0.75em;
}
</style>