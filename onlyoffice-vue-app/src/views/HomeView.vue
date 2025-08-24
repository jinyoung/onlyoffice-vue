<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <TheWelcome />
    
    <div class="onlyoffice-section">
      <h2>OnlyOffice Document Editor Integration</h2>
      <p>이 샘플은 OnlyOffice Document Server와 Vue.js의 통합을 보여줍니다.</p>
      
      <div class="features">
        <h3>주요 기능:</h3>
        <ul>
          <li>실시간 문서 편집</li>
          <li>다양한 문서 형식 지원 (DOCX, XLSX, PPTX 등)</li>
          <li>협업 편집 기능</li>
          <li>Vue.js 컴포넌트로 쉬운 통합</li>
        </ul>
      </div>
      
      <div class="action-buttons">
        <router-link to="/upload" class="upload-button">
          📁 파일 업로드
        </router-link>
        <router-link to="/editor" class="editor-button">
          📝 OnlyOffice 에디터 열기
        </router-link>
      </div>
    </div>
  </main>
</template>

<style scoped>
.onlyoffice-section {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.onlyoffice-section h2 {
  color: #2c3e50;
  margin-bottom: 16px;
}

.onlyoffice-section p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.features {
  margin: 20px 0;
}

.features h3 {
  color: #2c3e50;
  margin-bottom: 12px;
}

.features ul {
  list-style-type: none;
  padding: 0;
}

.features li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.features li:before {
  content: "✓";
  color: #4CAF50;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.action-buttons {
  text-align: center;
  margin-top: 30px;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.upload-button, .editor-button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.upload-button {
  background: #2196F3;
}

.upload-button:hover {
  background: #1976D2;
}

.editor-button {
  background: #4CAF50;
}

.editor-button:hover {
  background: #45a049;
}
</style>
