from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
model=root/'PowerBI'/'Meridian_Commercial_Performance.SemanticModel'/'definition'/'expressions.tmdl'
data=str((root/'data').resolve()).replace('"','')
model.write_text('expression pDataRoot = "'+data+'" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n',encoding='utf8')
print('Configured Power BI data root:',data)
print('Now open PowerBI/Meridian_Commercial_Performance.pbip in Power BI Desktop (Windows).')
