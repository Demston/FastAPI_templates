from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

app = FastAPI()


@app.post('/files')
async def upload(up_file: UploadFile):
    """Типа записываем файл"""
    file = up_file.file
    filename = up_file.filename
    with open(f'1_{filename}', 'wb') as f:
        f.write(file.read())


@app.post('/multi_files')
async def uploads(up_files: list[UploadFile]):
    """Типа записываем файлЫ"""
    for i in up_files:
        file = i.file
        filename = i.filename
        with open(f'1_{filename}', 'wb') as f:
            f.write(file.read())


@app.get('/files/{filename}')
async def get_file(filename: str):
    """Получение файла"""
    return FileResponse(filename)


def iterfile(filename: str):
    """Побитовое чтение файла"""
    with open(filename, 'rb') as f:
        while chunk := f.read(1024*1024):
            yield chunk


@app.get('/files/streaming/{filename}')
async def get_streaming_file(filename: str):
    """Побитовое получение файла"""
    return StreamingResponse(iterfile(filename), media_type='image/jpg')
