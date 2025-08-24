# ONLYOFFICE Vue.js 통합 가이드

## 📋 개요

이 프로젝트는 Vue.js 애플리케이션에 ONLYOFFICE Docs API를 통합하여 파일 업로드 및 문서 편집 기능을 제공합니다.

## 🚀 기능

### ✅ 구현된 기능
- **파일 업로드**: 드래그 앤 드롭 또는 클릭하여 파일 선택
- **Sample.txt 로딩**: 미리 준비된 샘플 텍스트 파일 편집
- **다중 파일 형식 지원**: .txt, .docx, .pdf, .xlsx, .pptx
- **실시간 문서 편집**: ONLYOFFICE Document Editor 통합
- **반응형 UI**: 모바일 친화적인 인터페이스

### 🎯 지원 파일 형식
- **텍스트 문서**: .txt, .docx, .pdf
- **스프레드시트**: .xlsx
- **프레젠테이션**: .pptx

## 🛠️ 사용 방법

### 1. 개발 서버 시작
\`\`\`bash
cd onlyoffice-vue-app
npm run dev
\`\`\`

### 2. 애플리케이션 접근
브라우저에서 `http://localhost:3000`으로 접속한 후, "OnlyOffice Editor" 메뉴를 클릭합니다.

### 3. 파일 편집 방법

#### 샘플 파일 편집
1. **"📄 Sample.txt 불러오기"** 버튼 클릭
2. 문서 편집기가 열리면 텍스트 편집 가능
3. 자동 저장 기능으로 변경사항 자동 보존

#### 새 파일 업로드 및 편집
1. 파일 업로드 영역에 파일 드래그 앤 드롭 또는 클릭하여 선택
2. **"📤 업로드하고 열기"** 버튼 클릭
3. 선택된 파일이 ONLYOFFICE 편집기에서 열림

## 🏗️ 프로젝트 구조

\`\`\`
onlyoffice-vue-app/
├── src/
│   ├── components/
│   │   └── DocumentEditor.vue    # 메인 편집기 컴포넌트
│   ├── views/
│   └── router/
│       └── index.ts              # 라우터 설정 (/editor 경로)
├── public/
│   └── documents/
│       └── sample.txt            # 샘플 텍스트 파일
└── vite.config.ts                # Vite 설정 (CORS, 정적 파일 서빙)
\`\`\`

## 🔧 주요 구현 사항

### DocumentEditor.vue 컴포넌트
- **파일 업로드 UI**: 드래그 앤 드롭 지원
- **동적 문서 설정**: 파일 타입에 따른 편집기 모드 자동 전환
- **에러 핸들링**: 파일 로딩 실패 시 사용자 알림
- **로딩 상태**: 스피너와 함께 사용자 경험 향상

### 기술적 특징
- **Blob URL 활용**: 업로드된 파일을 메모리에서 직접 편집
- **타입 안전성**: TypeScript로 구현
- **반응형 디자인**: 모바일 및 데스크톱 지원
- **CORS 설정**: 크로스 오리진 리소스 공유 지원

## 📁 파일 설명

### `/documents/sample.txt`
프로젝트 루트의 documents 폴더에 위치한 원본 샘플 파일입니다.

### `/public/documents/sample.txt`
Vue 앱에서 웹으로 제공되는 샘플 파일의 복사본입니다.

## 🌐 API 참조

이 구현은 [ONLYOFFICE Docs API](https://api.onlyoffice.com/docs/docs-api/get-started/basic-concepts/)의 기본 개념을 따릅니다:

- **Document Configuration**: 문서 타입, 키, URL 설정
- **Editor Configuration**: 편집 모드, 언어, 사용자 설정
- **Event Handling**: 문서 준비 완료 및 오류 이벤트 처리

## 🎨 UI/UX 특징

- **현대적인 디자인**: 카드 기반 레이아웃
- **직관적인 인터랙션**: 호버 효과 및 애니메이션
- **접근성**: 시각적 피드백 및 명확한 사용자 안내
- **성능 최적화**: 지연 로딩 및 효율적인 상태 관리

## 🔍 문제 해결

### 편집기가 로드되지 않는 경우
1. 개발 서버가 정상 실행 중인지 확인
2. 브라우저 콘솔에서 CORS 오류 확인
3. `http://localhost:3000/documents/sample.txt` 직접 접근하여 파일 접근성 확인

### 파일 업로드가 작동하지 않는 경우
1. 지원되는 파일 형식인지 확인
2. 파일 크기가 적절한지 확인
3. 브라우저의 개발자 도구에서 JavaScript 오류 확인

## 🔗 관련 링크

- [ONLYOFFICE Docs API 공식 문서](https://api.onlyoffice.com/docs/docs-api/)
- [Vue.js 공식 문서](https://vuejs.org/)
- [Vite 공식 문서](https://vitejs.dev/)

---

이 가이드를 통해 ONLYOFFICE Docs API와 Vue.js의 통합 방법을 이해하고, 실제 프로젝트에 적용할 수 있습니다.
