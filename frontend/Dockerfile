FROM node:20-alpine AS builder

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建参数
ARG VITE_API_BASE_URL=http://localhost:8000

# 构建生产版本
RUN npm run build

# 生产镜像
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# 清理默认文件
RUN rm -rf ./*

# 从构建阶段复制文件
COPY --from=builder /app/dist .

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
