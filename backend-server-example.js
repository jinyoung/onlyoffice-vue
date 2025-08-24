// 백엔드 서버 예시 코드 (Node.js + Express)
// 실행 방법: node backend-server-example.js

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

// CORS 설정 (Vue 앱에서 접근 허용)
app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:3000'], // Vue dev server 포트
  credentials: true
}));

app.use(express.json());

// uploads 디렉토리 생성 (없으면)
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Multer 설정 - 업로드된 파일 저장
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    // 파일명에 타임스탬프 추가하여 중복 방지
    const uniqueName = Date.now() + '-' + file.originalname;
    cb(null, uniqueName);
  }
});

const upload = multer({ 
  storage,
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB 제한
  }
});

// 정적 파일 서빙 - documents 경로로 업로드된 파일 접근
app.use('/documents', express.static(uploadsDir));

// 기존 샘플 파일도 제공 (documents 폴더의 파일들)
const documentsDir = path.join(__dirname, 'documents');
if (fs.existsSync(documentsDir)) {
  app.use('/documents', express.static(documentsDir));
}

// 파일 업로드 API
app.post('/upload', upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: '파일이 업로드되지 않았습니다.' });
    }

    // Document Server가 접근할 수 있는 URL 생성
    const publicUrl = `http://host.docker.internal:${PORT}/documents/${req.file.filename}`;
    
    console.log(`파일 업로드 완료: ${req.file.originalname} -> ${req.file.filename}`);
    console.log(`공개 URL: ${publicUrl}`);

    res.json({
      success: true,
      originalName: req.file.originalname,
      filename: req.file.filename,
      publicUrl: publicUrl,
      size: req.file.size
    });

  } catch (error) {
    console.error('업로드 에러:', error);
    res.status(500).json({ error: '파일 업로드 중 오류가 발생했습니다.' });
  }
});

// OnlyOffice 콜백 처리 (편집 완료 시 저장)
app.post('/onlyoffice/callback', express.raw({ type: 'application/json' }), (req, res) => {
  try {
    const body = JSON.parse(req.body);
    console.log('OnlyOffice 콜백 수신:', body);

    // status: 1 = 편집 중, 2 = 편집 완료, 3 = 에러
    if (body.status === 2) {
      // 편집 완료 - 파일 저장 처리
      console.log('문서 편집 완료, 저장 처리 필요');
      // 실제로는 body.url에서 편집된 파일을 다운로드하여 저장
    }

    res.json({ error: 0 }); // 성공 응답
  } catch (error) {
    console.error('콜백 처리 에러:', error);
    res.status(500).json({ error: 1 });
  }
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`🚀 백엔드 서버가 포트 ${PORT}에서 실행 중입니다.`);
  console.log(`📁 업로드된 파일들: http://localhost:${PORT}/documents/`);
  console.log(`📤 업로드 API: POST http://localhost:${PORT}/upload`);
  console.log(`📝 OnlyOffice 콜백: POST http://localhost:${PORT}/onlyoffice/callback`);
  console.log('');
  console.log('🐳 Docker 명령어:');
  console.log('docker run -d --name documentserver \\');
  console.log('  -p 8080:80 \\');
  console.log('  --add-host=host.docker.internal:host-gateway \\');
  console.log('  onlyoffice/documentserver');
});

// 종료 처리
process.on('SIGINT', () => {
  console.log('\n서버를 종료합니다...');
  process.exit(0);
});
