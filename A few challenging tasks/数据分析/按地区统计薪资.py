from fastapi import FastAPI, File, UploadFile, HTTPException
import io
import pandas as pd
from fastapi.responses import StreamingResponse
import uvicorn
app1 = FastAPI()


def analyze_data(df: pd.DataFrame):
    avg_salary = df.groupby("district")["salary"].mean().round(2)
    min_salary = df.groupby("district")["salary"].min().round(2)
    max_salary = df.groupby("district")["salary"].max().round(2)

    data = {"avg_salary": avg_salary,"min_salary": min_salary,"max_salary": max_salary}
    df = pd.DataFrame(data)

    output = io.BytesIO()  # 内存文件对象
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, sheet_name="薪资分析")
    output.seek(0)
    return output


@app1.post("/analyze/salary_by_district")
async def analyze_salary(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=404, detail="File type not supported.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        if not all(col in df.columns for col in ['district', 'salary']):
            raise HTTPException(status_code=404, detail="文件缺少必要的列")
        excel_stream = analyze_data(df)
        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=薪资分析.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
if __name__ == "__main__":
    uvicorn.run("main:app1", host="0.0.0.0", port=8080, reload=True)


