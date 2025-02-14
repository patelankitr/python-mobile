
echo "Execute tests..."
pytest -v --alluredir=allure-report/ Test/tutorials/test_launches_tutorial.py --alluredir=allure-report/


echo "Generate Allure report..."
allure generate -c allure-report -o allure-results-html

echo "Combine Allure report..."
allure-combine ./allure-results-html

echo "Report generated at: $(pwd)/allure-results-html/index.html"