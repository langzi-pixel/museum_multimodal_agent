# 文博多模态内容生产与语音讲解 Agent 系统

这是一个可运行的工程 Demo，用于展示“AI/Agent 驱动的文博内容生产闭环”：

> 文物图片/资料包上传 → 文物识别与信息抽取 → 多风格讲解词生成 → 内容质检 → TTS 语音合成 → 音频上传/本地托管 → 业务后台回写

该工程默认启用 `MOCK_MODE=true`，无需真实大模型、TTS、OBS 密钥也能完整跑通流程，便于演示和提交项目证明。配置真实环境变量后，可切换为真实 API 调用模式。

## 1. 核心能力

- 多 Agent 协作：识别 Agent、讲解生成 Agent、内容审核 Agent、语音合成 Agent、数据同步 Agent。
- 支持批量资料包：上传 zip 后自动遍历图片和 JSON 元数据。
- 支持多风格生成：专家严谨风、儿童科普风、脱口秀风、古风雅韵风、网感趣味风、导游讲解风、短视频口播风、研学课程风。
- 支持音频产物：默认生成 mock wav 文件；真实模式可接入讯飞 TTS 或其他 TTS。
- 支持业务闭环：默认写入本地 `runtime/sync_records.jsonl`；真实模式可回写业务系统 API。
- 支持证明材料：内置流程说明、API 文档、MIMO 申请说明、样例输入输出。

## 2. 快速启动

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

启动后访问：

```text
http://127.0.0.1:8001/docs
```

## 3. 运行本地 Demo

```bash
python scripts/run_demo.py
```

输出会生成在：

```text
runtime/jobs/<job_id>/
runtime/audio/
runtime/sync_records.jsonl
```

## 4. 上传压缩包接口

```bash
curl -X POST "http://127.0.0.1:8001/api/v1/process_zip" \
  -F "file=@sample_data/henan_museum_demo.zip"
```

返回示例：

```json
{
  "code": 1,
  "msg": "压缩包处理完成",
  "data": {
    "job_id": "20260508_120001_abcd12",
    "total_count": 1,
    "success_count": 1,
    "fail_count": 0,
    "results": []
  }
}
```

## 5. 真实 API 配置

将 `.env` 中 `MOCK_MODE=false`，并配置：

- `ARK_API_KEY`：火山方舟或 OpenAI-compatible LLM Key
- `ARK_BASE_URL`：LLM 接口地址
- `ARK_MODEL`：模型名或 Endpoint ID
- `BUSINESS_SYNC_API_URL`：业务系统回写接口
- `OBS_*`：对象存储配置
- `XFYUN_*`：讯飞 TTS 配置

> 注意：本工程不包含任何真实密钥。提交证明时请勿上传 `.env`。

## 6. 适合提交 MIMO 的项目亮点

1. 不是单次 Prompt，而是可运行的多 Agent 业务链路。
2. 覆盖图像理解、长文本生成、多风格改写、审核、语音合成、数据入库。
3. Token 消耗真实且可扩展：每件文物会产生识别、生成、审核、多风格输出等多轮调用。
4. 可批量处理文物资料，能从分钟级完成以往需要人工数小时完成的内容生产。
5. 后续可迁移到景区导览、铁路巡检报告、工业质检报告等场景。

## 7. 目录结构

```text
museum_multimodal_agent/
├── app/
│   ├── agents/
│   ├── integrations/
│   ├── main.py
│   ├── pipeline.py
│   ├── schemas.py
│   └── settings.py
├── docs/
├── sample_data/
├── scripts/
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
