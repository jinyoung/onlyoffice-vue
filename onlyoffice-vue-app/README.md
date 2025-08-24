# OnlyOffice Vue.js Integration Sample

OnlyOffice Document Server와 Vue.js를 통합한 실시간 문서 편집 샘플 애플리케이션입니다.

## 기능

- **실시간 문서 편집**: OnlyOffice Document Server를 사용한 웹 기반 문서 편집
- **다양한 문서 형식 지원**: DOCX, XLSX, PPTX 등 다양한 Office 문서 형식
- **Vue.js 통합**: Vue 3 + TypeScript + Composition API 사용
- **반응형 디자인**: 모던한 UI/UX 디자인
- **협업 기능**: 실시간 다중 사용자 편집 지원

## 시스템 요구사항

- Node.js 18+ 
- Docker
- 4GB RAM 이상
- 2GB 여유 디스크 공간

## 설치 및 실행

### 1. OnlyOffice Document Server 실행

```bash
sudo docker run -d -p 8080:80 --restart=always \
    --name onlyoffice-documentserver \
    -e JWT_ENABLED=false \
    onlyoffice/documentserver
```

### 2. Vue.js 애플리케이션 실행

```bash
# 의존성 설치
npm install --legacy-peer-deps

# 개발 서버 실행
npm run dev
```

### 3. 브라우저에서 접속

- Vue.js 애플리케이션: http://localhost:3000
- OnlyOffice Document Server: http://localhost:8080/welcome/

## 사용법

1. 브라우저에서 http://localhost:3000 접속
2. "OnlyOffice 에디터 열기" 버튼 클릭
3. 실시간 문서 편집 시작

## 프로젝트 구조

```
src/
├── components/
│   └── DocumentEditor.vue    # OnlyOffice 에디터 컴포넌트
├── views/
│   ├── HomeView.vue          # 메인 홈페이지
│   └── AboutView.vue         # 정보 페이지
├── router/
│   └── index.ts              # Vue Router 설정
└── main.ts                   # 애플리케이션 진입점
```

## 기술 스택

- **Frontend**: Vue 3, TypeScript, Vue Router, Pinia
- **Build Tool**: Vite
- **Document Server**: OnlyOffice Document Server
- **Containerization**: Docker

## 개발 환경 설정

### IDE 추천

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (Vetur 비활성화 필요)

### 프로젝트 스크립트

```bash
# 개발 서버 실행
npm run dev

# 빌드
npm run build

# 타입 체크
npm run type-check

# 린트
npm run lint
```

## 문제 해결

### OnlyOffice Document Server 접속 문제
- Docker 컨테이너가 실행 중인지 확인: `docker ps`
- 포트 8080이 사용 가능한지 확인

### Vue 개발 서버 실행 문제
- Node.js 버전 확인 (18+ 필요)
- `--legacy-peer-deps` 옵션으로 설치

## 라이선스

이 프로젝트는 학습 및 데모 목적으로 제작되었습니다.

## 참고 자료

- [OnlyOffice Document Server API](https://api.onlyoffice.com/)
- [Vue.js 공식 문서](https://vuejs.org/)
- [OnlyOffice Vue Component](https://www.npmjs.com/package/@onlyoffice/document-editor-vue)
