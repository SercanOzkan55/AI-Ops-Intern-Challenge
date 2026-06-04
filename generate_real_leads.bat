@echo off
echo Generating 100 Real HR Leads...
python src/growth_ai_ops_prototype.py --real
echo Building Excel Workbook Dashboard...
node tools/build_google_sheets_workbook.mjs
echo Done! Please check the output/ directory.
pause
