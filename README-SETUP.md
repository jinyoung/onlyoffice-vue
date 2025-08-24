# OnlyOffice 두 번째 방식 설정 가이드 (host-gateway)

## 🎯 개요
리눅스 Docker 환경에서 `--add-host=host.docker.internal:host-gateway` 옵션을 사용하여 Document Server가 호스트의 백엔드 서버에 접근할 수 있도록 설정합니다.

## 📋 단계별 설정

### 1. Docker 컨테이너 재시작 (중요!)

기존 컨테이너를 중지하고 host-gateway 옵션을 추가하여 다시 실행:

```bash
# 기존 컨테이너 중지 및 제거
docker stop documentserver
docker rm documentserver

# host-gateway 옵션을 추가하여 새로 실행
docker run -d --name documentserver \
  -p 8080:80 \
  --add-host=host.docker.internal:host-gateway \
  onlyoffice/documentserver
```

### 2. 백엔드 서버 설정

파일 업로드 및 서빙을 위한 백엔드 서버를 실행합니다:

```bash
# 의존성 설치
npm install

# 서버 실행
npm start
```

### 3. Vue 앱에서 업로드 기능 활성화

`DocumentEditor.vue`의 `uploadAndOpen` 함수에서 주석 처리된 코드를 활성화:

```typescript
const uploadAndOpen = async () => {
  if (!selectedFile.value) return
  
  isLoading.value = true
  currentDocumentTitle.value = selectedFile.value.name
  
  try {
    // FormData를 생성하여 파일을 서버에 업로드
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await fetch('http://localhost:3000/upload', {
      method: 'POST',
      body: formData
    })
    
    const { publicUrl } = await response.json()
    
    const fileType = getFileType(selectedFile.value.name)
    const documentType = getDocumentType(fileType)
    
    docConfig.value = {
      ...docConfig.value,
      document: {
        fileType: fileType,
        key: "upload-" + Date.now(),
        title: selectedFile.value.name,
        url: publicUrl  // 서버에서 받은 실제 URL 사용
      },
      documentType: documentType
    }
    
    setTimeout(() => {
      isLoading.value = false
      showEditor.value = true
    }, 1000)
    
  } catch (error) {
    console.error('File upload error:', error)
    alert('파일 업로드 중 오류가 발생했습니다.')
    isLoading.value = false
  }
}
```

## 🔍 동작 원리

1. **Document Server**: `http://host.docker.internal:3000/documents/파일명`으로 파일에 접근
2. **백엔드 서버**: 파일을 받아 `uploads/` 폴더에 저장하고 접근 가능한 URL 반환
3. **Vue 앱**: 업로드 후 받은 URL로 OnlyOffice 에디터 실행

## ✅ 확인 사항

- [ ] Docker 컨테이너가 `--add-host` 옵션으로 실행됨
- [ ] 백엔드 서버가 3000포트에서 실행 중
- [ ] `http://localhost:3000/documents/sample.txt` 접근 가능
- [ ] Vue 앱이 5173포트에서 실행 중
- [ ] Sample.txt 버튼 클릭 시 문서가 정상 로드됨

## 🐛 문제 해결

### Sample.txt가 열리지 않는 경우:
```bash
# documents 폴더에 sample.txt 파일이 있는지 확인
ls -la documents/

# 백엔드 서버 로그 확인
# 서버 실행 시 콘솔에 접근 URL이 표시됨
```

### 업로드 기능이 작동하지 않는 경우:
1. 백엔드 서버가 실행 중인지 확인
2. CORS 설정이 올바른지 확인
3. 브라우저 개발자 도구에서 네트워크 탭 확인

## 📁 프로젝트 구조

```
onlyoffice/
├── backend-server-example.js  # 백엔드 서버
├── package.json              # 백엔드 의존성
├── documents/                # 샘플 파일들
│   └── sample.txt
├── uploads/                  # 업로드된 파일들 (자동 생성)
└── onlyoffice-vue-app/       # Vue 프론트엔드
    └── src/components/
        └── DocumentEditor.vue
```

## 🚀 다음 단계

업로드 기능까지 구현하려면:
1. 백엔드 서버 실행
2. Vue 앱에서 주석 처리된 업로드 코드 활성화
3. 편집 완료 시 저장 기능 구현 (콜백 처리)
