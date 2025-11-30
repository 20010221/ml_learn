from fastapi import FastAPI, File,UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import uvicorn
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
app2 = FastAPI()

def analyze_data(df):
    company_count = df.groupby("district")["company"].count().reset_index(names="公司数量")
    data = pd.DataFrame(company_count)
    region = data['district']
    company_counts = data['公司数量']
    plt.figure(figsize=(10, 6))
    plt.bar(region,company_counts,color='b')
    plt.title('公司数量柱状图',fontsize=16)
    plt.xlabel('地区',fontsize=12)
    plt.ylabel('公司数量',fontsize=12)

    image = io.BytesIO()
    plt.savefig(
        image,
        format='png',
        dpi=300,
        bbox_inches='tight'
    )
    image.seek(0)
    plt.close()
    return image
@app2.post('/analyze/company_count_chart')
async def company_count_chart(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File type not supported.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        if not all(col in df.columns for col in ['district', 'company']):
            raise HTTPException(status_code=400, detail="文件缺少必要的列")
        excel_stream = analyze_data(df)
        return StreamingResponse(
                excel_stream,
                media_type="image/png",
                headers={"Content-Disposition": "attachment;filename*=UTF-8''各区域公司数量分布.png"}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run("main:app2", host="0.0.0.0", port=8000, reload=True)


