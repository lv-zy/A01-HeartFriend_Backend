# 第四次会议

与会人员: 王雨田, 范梦瑶, 吕钊阳, 高佳宝

会议时间: 2023年11月19日

会议类型：工作会议

---

## 会议内容

### 协商完成第一次迭代的API设计
大家协商设计第一次迭代的API接口设计如下：

| 功能  | url  |  请求方法 | 具体内容  | 可选  |
|---|---|---|---|---|
|  登陆 |  api/v1/user/login |  POST | 返回token和created  |   |
|  个人主页 |  api/v1/user/info | GET/PATCH  |  返回/修改用户信息 |   |
| 个人主页  |  api/v1/user/upload-avatar/ | POST  |  上传用户头像 |   |
|  日志记录 | api/v1/diary  |  GET/POST | 获取日志列表/增加一篇日志  |   |
| 日志记录  |  api/v1/diary/4 |  DELETE |  删除一篇日记 |   |


并设计数据表Diary和User 
具体可见后端代码部分