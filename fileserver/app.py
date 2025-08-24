import os
import uuid
import aiofiles
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import mimetypes

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# FastAPI 앱 초기화
app = FastAPI(
    title="OnlyOffice File Server",
    description="File upload and serving API for OnlyOffice Document Server integration",
    version="1.0.0"
)

# CORS 미들웨어 설정 (Vue.js 프론트엔드와 OnlyOffice Document Server 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 디렉토리 설정
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 지원되는 파일 형식
SUPPORTED_EXTENSIONS = {
    # Word documents
    '.docx', '.doc', '.odt', '.rtf', '.txt',
    # Excel documents  
    '.xlsx', '.xls', '.ods', '.csv',
    # PowerPoint documents
    '.pptx', '.ppt', '.odp',
    # PDF
    '.pdf'
}

# 파일 메타데이터 저장용 (실제 운영환경에서는 데이터베이스 사용 권장)
file_metadata = {}

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "OnlyOffice File Server",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /upload",
            "files": "GET /files/{file_id}",
            "list": "GET /files",
            "delete": "DELETE /files/{file_id}"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일 업로드 엔드포인트
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일이 선택되지 않았습니다.")
    
    # 파일 확장자 확인
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # 고유한 파일 ID 생성
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    try:
        # 파일 저장
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 메타데이터 저장
        file_metadata[file_id] = {
            "original_filename": file.filename,
            "file_extension": file_extension,
            "content_type": file.content_type,
            "size": len(content),
            "upload_time": datetime.now().isoformat(),
            "file_path": str(file_path)
        }
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "url": f"http://fileserver:8000/files/{file_id}",
            "external_url": f"http://localhost:8081/files/{file_id}",
            "message": "파일이 성공적으로 업로드되었습니다."
        }
        
    except Exception as e:
        # 업로드 실패 시 파일 삭제
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {str(e)}")

@app.get("/files/{file_id}")
async def get_file(file_id: str):
    """
    파일 다운로드/조회 엔드포인트
    """
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    metadata = file_metadata[file_id]
    file_path = Path(metadata["file_path"])
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
    
    # MIME 타입 추정
    content_type = metadata.get("content_type")
    if not content_type:
        content_type, _ = mimetypes.guess_type(metadata["original_filename"])
        if not content_type:
            content_type = "application/octet-stream"
    
    return FileResponse(
        path=file_path,
        filename=metadata["original_filename"],
        media_type=content_type,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.get("/files")
async def list_files():
    """
    업로드된 파일 목록 조회
    """
    files = []
    for file_id, metadata in file_metadata.items():
        files.append({
            "file_id": file_id,
            "filename": metadata["original_filename"],
            "size": metadata["size"],
            "upload_time": metadata["upload_time"],
            "url": f"http://fileserver:8000/files/{file_id}",
            "external_url": f"http://localhost:8081/files/{file_id}"
        })
    
    return {"files": files, "total": len(files)}

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """
    파일 삭제 엔드포인트
    """
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    metadata = file_metadata[file_id]
    file_path = Path(metadata["file_path"])
    
    try:
        # 파일 삭제
        if file_path.exists():
            file_path.unlink()
        
        # 메타데이터 삭제
        del file_metadata[file_id]
        
        return {"message": "파일이 성공적으로 삭제되었습니다.", "file_id": file_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 삭제 중 오류가 발생했습니다: {str(e)}")

@app.get("/files/{file_id}/info")
async def get_file_info(file_id: str):
    """
    파일 정보 조회 엔드포인트 (OnlyOffice Document Server용)
    """
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    metadata = file_metadata[file_id]
    
    return {
        "file_id": file_id,
        "filename": metadata["original_filename"],
        "size": metadata["size"],
        "upload_time": metadata["upload_time"],
        "content_type": metadata["content_type"],
        "file_extension": metadata["file_extension"],
        "url": f"http://fileserver:8000/files/{file_id}",
        "external_url": f"http://localhost:8081/files/{file_id}"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
