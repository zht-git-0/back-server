// 引入 Express 模块
const express = require('express');
const app = express();

// 设置服务器端口号
const port = process.env.PORT || 3000;

// 解析 JSON 数据
app.use(express.json());

// 定义一个简单的 GET 路由
app.get('/', (req, res) => {
  res.send('Hello, Vercel!');
});

// 定义一个 API 路由
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from the API!' });
});

// 启动服务器并监听指定端口
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

