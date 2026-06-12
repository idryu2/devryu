FROM node:20-slim

WORKDIR /app

# 의존성 레이어 캐시
COPY package.json ./
RUN npm install

COPY . .

EXPOSE 5173
# --host 0.0.0.0: 컨테이너 외부(호스트 브라우저)에서 접근 가능하게
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
