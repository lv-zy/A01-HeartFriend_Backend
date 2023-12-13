# 第五次会议【线上会议】

与会人员: 王雨田, 范梦瑶, 吕钊阳, 高佳宝

会议时间: 2023年12月3日

会议类型：工作会议

---

## 会议内容

### 协商完成第二次迭代的API设计
大家协商设计第二次迭代的API接口设计如下：

| 功能  | url  |  请求方法 | 具体内容  | 可选  |
|---|---|---|---|---|
|  心情日志 |  /api/v1/diary/upload-image |  POST | 上传一个图片，返回图片的url  |   |
|  药物健康 |  /api/v1/medicine | GET/POST  |  获得所有的用药提醒/增加一条用药提醒 |   |
| 药物健康  |  /api/v1/medicine/4 | GET/PATCH/DELETE  |  获得/修改/删除一条药物提醒 |   |
|  论坛交流 | /api/v1/forum/posts/  |  GET/POST | 获取帖子列表/增加一篇帖子  |   |
| 论坛交流  |  /api/v1/forum/posts/id/ |  GET/DELETE | 查看一个帖子/删除一个帖子 |   |
| 论坛交流  |  /api/v1/forum/posts/id/like |  POST | 喜欢一个帖子 |   |
| 论坛交流  |  /api/v1/forum/posts/comments/ |  GET/POST | 获取所有评论/发布评论 |   |
| 论坛交流  |  /api/v1/forum/posts/comments/id/ |  DELETE | 删除一个评论 |   |
并设计和修改数据表User, Post,  Comment
具体可见后端代码部分