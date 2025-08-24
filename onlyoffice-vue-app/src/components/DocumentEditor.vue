<template>
  <div class="document-editor-container" :class="{ 'fullscreen': showEditor }">
    <!-- Navigation Bar (only show when editor is open) -->
    <div v-if="showEditor" class="top-nav">
      <div class="nav-left">
        <router-link to="/" class="nav-link">🏠 홈</router-link>
        <router-link to="/upload" class="nav-link">📁 파일 업로드</router-link>
        <span class="document-title">{{ currentDocumentTitle }}</span>
      </div>
      <div class="nav-right">
        <button @click="closeEditor" class="close-btn">✕ 닫기</button>
      </div>
    </div>

    <!-- File Upload Component (only show when editor is closed) -->
    <div v-if="!showEditor" class="upload-section">
      <h2>OnlyOffice Document Editor</h2>
      <FileUpload />
    </div>
    
    <!-- Document Editor (fullscreen when open) -->
    <div v-if="showEditor" class="editor-wrapper">
      <DocumentEditor
        id="docEditor"
        :config="docConfig"
        documentServerUrl="http://localhost:8080/"
        @onDocumentReady="handleDocReady"
        @onLoadComponentError="handleError"
        :style="editorStyle"
      />
    </div>
    
    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>문서를 로딩 중입니다...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DocumentEditor } from '@onlyoffice/document-editor-vue'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import FileUpload from './FileUpload.vue'

const route = useRoute()

// Reactive state
const showEditor = ref(false)
const isLoading = ref(false)
const currentDocumentTitle = ref('')

// Computed style for editor
const editorStyle = computed(() => ({
  width: '100%',
  height: showEditor.value ? 'calc(100vh - 60px)' : '600px'
}))

// Document configuration
const docConfig = ref({
  document: {
    fileType: "txt",
    key: "sample-doc-" + Date.now(),
    title: "Sample Document.txt", 
    url: "http://fileserver:8000/files/sample"
  },
  documentType: "word",
  editorConfig: {
    mode: "edit",
    lang: "ko",
    user: {
      id: "user-1",
      name: "사용자"
    },
    customization: {
      autosave: true,
      showReviewChanges: true,
      toolbarHideFileName: false
    }
  },
  width: "100%",
  height: "600px"
})

// 쿼리 파라미터에서 파일 정보 확인
const checkQueryParams = () => {
  const { fileId, filename, url } = route.query
  
  if (fileId && filename && url) {
    // URL이 localhost:8081이면 fileserver:8000으로 변경
    let documentUrl = url as string
    if (documentUrl.includes('localhost:8081')) {
      documentUrl = documentUrl.replace('localhost:8081', 'fileserver:8000')
    }
    
    openDocument({
      file_id: fileId as string,
      filename: filename as string,
      url: documentUrl
    })
  }
}

// 문서 열기
const openDocument = (file: any) => {
  isLoading.value = true
  
  // 파일 확장자에 따른 문서 타입 결정
  const extension = file.filename.split('.').pop()?.toLowerCase()
  let documentType = "word"
  let fileType = extension || "txt"
  
  if (['xlsx', 'xls', 'ods', 'csv'].includes(extension || '')) {
    documentType = "cell"
  } else if (['pptx', 'ppt', 'odp'].includes(extension || '')) {
    documentType = "slide"
  }
  
  // URL이 이미 내부 네트워크 주소인지 확인하고, 아니면 변환
  let documentUrl = file.external_url || file.url
  if (documentUrl && documentUrl.includes('localhost:8081')) {
    documentUrl = documentUrl.replace('localhost:8081', 'fileserver:8000')
  }
  
  // OnlyOffice 설정 업데이트
  docConfig.value = {
    document: {
      fileType: fileType,
      key: `${file.file_id}-${Date.now()}`,
      title: file.filename,
      url: documentUrl
    },
    documentType: documentType,
    editorConfig: {
      mode: "edit",
      lang: "ko",
      user: {
        id: "user-1",
        name: "사용자"
      },
      customization: {
        autosave: true,
        showReviewChanges: true,
        toolbarHideFileName: false
      }
    },
    width: "100%",
    height: "600px"
  }
  
  currentDocumentTitle.value = file.filename
  showEditor.value = true
  
  // body 스크롤 비활성화 (전체 화면 모드)
  document.body.style.overflow = 'hidden'
  
  setTimeout(() => {
    isLoading.value = false
  }, 1000)
}

// 에디터 닫기
const closeEditor = () => {
  showEditor.value = false
  currentDocumentTitle.value = ''
  
  // body 스크롤 복원
  document.body.style.overflow = 'auto'
  
  // URL 쿼리 파라미터 정리
  window.history.replaceState({}, document.title, window.location.pathname)
}

// Event handlers
const handleDocReady = () => {
  console.log("Document editor is ready")
  isLoading.value = false
}

const handleError = (errorCode: any, errorDescription: any) => {
  console.error("Editor error", errorCode, errorDescription)
  alert(`Editor error: ${errorDescription}`)
  isLoading.value = false
}

// 라우트 변경 감지
watch(() => route.query, () => {
  checkQueryParams()
}, { immediate: true })

onMounted(() => {
  console.log("DocumentEditor component mounted")
  checkQueryParams()
})
</script>

<style scoped>
.document-editor-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.document-editor-container.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  max-width: none;
  margin: 0;
  padding: 0;
  z-index: 1000;
  background: white;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #2c3e50;
  color: white;
  border-bottom: 1px solid #34495e;
  height: 60px;
  box-sizing: border-box;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
  font-size: 14px;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.document-title {
  font-weight: 600;
  font-size: 16px;
  color: #ecf0f1;
  margin-left: 20px;
}

.nav-right {
  display: flex;
  align-items: center;
}

.close-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background: #c0392b;
}

.upload-section {
  padding: 20px;
}

.editor-wrapper {
  width: 100%;
  height: calc(100vh - 60px);
  overflow: hidden;
  background: white;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1001;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

/* 전체 화면 모드에서 body 스크롤 숨기기 */
.document-editor-container.fullscreen {
  overflow: hidden;
}
</style>