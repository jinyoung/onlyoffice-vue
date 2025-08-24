<template>
  <div class="file-upload-container">
    <h3>파일 업로드</h3>
    
    <!-- 파일 업로드 영역 -->
    <div class="upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
      <input 
        ref="fileInput" 
        type="file" 
        @change="handleFileSelect" 
        style="display: none"
        accept=".docx,.doc,.odt,.rtf,.txt,.xlsx,.xls,.ods,.csv,.pptx,.ppt,.odp,.pdf"
      >
      <div v-if="!uploading" class="upload-content">
        <div class="upload-icon">📁</div>
        <p>클릭하거나 파일을 드래그하여 업로드</p>
        <small>지원 형식: DOCX, XLSX, PPTX, PDF, TXT 등</small>
      </div>
      <div v-else class="uploading">
        <div class="spinner"></div>
        <p>업로드 중...</p>
      </div>
    </div>

    <!-- 업로드된 파일 목록 -->
    <div v-if="uploadedFiles.length > 0" class="uploaded-files">
      <h4>업로드된 파일</h4>
      <div class="file-list">
        <div v-for="file in uploadedFiles" :key="file.file_id" class="file-item">
          <div class="file-info">
            <span class="file-name">{{ file.filename }}</span>
            <small class="file-size">{{ formatFileSize(file.size) }}</small>
          </div>
          <div class="file-actions">
            <button @click="openInEditor(file)" class="btn-edit">편집</button>
            <button @click="deleteFile(file.file_id)" class="btn-delete">삭제</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- 성공 메시지 -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref<HTMLInputElement>()
const uploading = ref(false)
const uploadedFiles = ref<any[]>([])
const errorMessage = ref('')
const successMessage = ref('')

const FILE_SERVER_URL = 'http://localhost:8081'

// 파일 업로드 함수
const uploadFile = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  try {
    uploading.value = true
    errorMessage.value = ''
    
    const response = await fetch(`${FILE_SERVER_URL}/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '업로드 실패')
    }

    const result = await response.json()
    successMessage.value = `${file.name} 업로드 완료!`
    
    // 파일 목록 새로고침
    await loadFileList()
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    return result
  } catch (error: any) {
    errorMessage.value = error.message || '파일 업로드 중 오류가 발생했습니다.'
    setTimeout(() => {
      errorMessage.value = ''
    }, 5000)
  } finally {
    uploading.value = false
  }
}

// 파일 선택 처리
const handleFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  
  if (files && files.length > 0) {
    await uploadFile(files[0])
  }
}

// 드래그 앤 드롭 처리
const handleDrop = async (event: DragEvent) => {
  event.preventDefault()
  const files = event.dataTransfer?.files
  
  if (files && files.length > 0) {
    await uploadFile(files[0])
  }
}

// 파일 입력 트리거
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 파일 목록 로드
const loadFileList = async () => {
  try {
    const response = await fetch(`${FILE_SERVER_URL}/files`)
    if (response.ok) {
      const data = await response.json()
      uploadedFiles.value = data.files
    }
  } catch (error) {
    console.error('파일 목록 로드 실패:', error)
  }
}

// 파일 삭제
const deleteFile = async (fileId: string) => {
  if (!confirm('정말로 이 파일을 삭제하시겠습니까?')) {
    return
  }

  try {
    const response = await fetch(`${FILE_SERVER_URL}/files/${fileId}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      successMessage.value = '파일이 삭제되었습니다.'
      await loadFileList()
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    } else {
      throw new Error('파일 삭제 실패')
    }
  } catch (error: any) {
    errorMessage.value = error.message || '파일 삭제 중 오류가 발생했습니다.'
    setTimeout(() => {
      errorMessage.value = ''
    }, 5000)
  }
}

// 에디터에서 파일 열기
const openInEditor = (file: any) => {
  // OnlyOffice Document Server용 내부 네트워크 URL로 변경
  const internalUrl = file.external_url.replace('localhost:8081', 'fileserver:8000')
  
  // DocumentEditor 컴포넌트로 파일 정보 전달
  router.push({
    name: 'editor',
    query: {
      fileId: file.file_id,
      filename: file.filename,
      url: internalUrl
    }
  })
}

// 파일 크기 포맷팅
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 컴포넌트 마운트 시 파일 목록 로드
onMounted(() => {
  loadFileList()
})
</script>

<style scoped>
.file-upload-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;
  margin-bottom: 20px;
}

.upload-area:hover {
  border-color: #4CAF50;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.uploading {
  display: flex;
  flex-direction: column;
  align-items: center;
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

.uploaded-files {
  margin-top: 30px;
}

.file-list {
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.file-size {
  color: #666;
  font-size: 12px;
}

.file-actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s;
}

.btn-edit {
  background: #4CAF50;
  color: white;
}

.btn-edit:hover {
  background: #45a049;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 4px;
  margin-top: 16px;
  border-left: 4px solid #f44336;
}

.success-message {
  background: #e8f5e8;
  color: #2e7d32;
  padding: 12px;
  border-radius: 4px;
  margin-top: 16px;
  border-left: 4px solid #4CAF50;
}

h3, h4 {
  color: #2c3e50;
  margin-bottom: 16px;
}

small {
  color: #666;
}
</style>
