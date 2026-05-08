# API 文档

## 1. 健康检查

```http
GET /health
```

返回：

```json
{"code": 1, "msg": "ok", "mock_mode": true}
```

## 2. 单件文物处理

```http
POST /api/v1/process_one
Content-Type: application/json
```

请求示例：

```json
{
  "aid": "demo001",
  "collection_name": "妇好鸮尊",
  "original_description": "商代晚期青铜酒器，1976年出土于殷墟妇好墓。",
  "image_url": "https://example.com/image.jpg",
  "position": "河南博物院主展馆",
  "category_name": "镇院之宝"
}
```

## 3. 压缩包批量处理

```http
POST /api/v1/process_zip
Content-Type: multipart/form-data
```

字段：

- `file`: zip 文件

压缩包内支持：

- `*.json`：文物元数据
- `*.jpg/*.png/*.webp`：文物图片

JSON 字段兼容：

- `aid`
- `collection_name`
- `original_description`
- `image_materials`
- `video_materials`
- `position`
- `freeclassificationmanagement_classification_name`

## 4. 返回结果核心字段

- `knowledge`: 结构化文物知识
- `styles`: 多风格讲解词、字数、预计音频时长、音频 URL
- `sync_status`: 回写状态
- `sync_response`: 业务系统响应或本地 mock 记录路径
